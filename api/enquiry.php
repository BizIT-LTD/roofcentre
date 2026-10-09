<?php
/**
 * Roof Centre enquiry handler.
 *
 * Receives the quote/contact form and emails it to the business.
 * Settings are read from a config file OUTSIDE the web root so that
 * addresses and any SMTP credentials are never published with the site:
 *
 *   <folder containing public_html>/roofcentre-enquiry-config.php
 *   Hostinger: /home/u123456789/domains/roofcentre.com.au/roofcentre-enquiry-config.php
 *
 * See docs/ENQUIRY-SETUP.md for the expected format. Without that file the
 * defaults below are used and mail is sent with PHP's mail() function.
 */

declare(strict_types=1);

$config = [
    'to'        => 'info@roofcentre.com.au',
    'from'      => 'website@roofcentre.com.au',   // must be a mailbox/domain the server is allowed to send for
    'from_name' => 'Roof Centre Website',
    'subject'   => 'New quote request from the Roof Centre website',
    'bcc'       => '',
    'thank_you' => '/thank-you/',
    'min_seconds' => 3,     // reject forms submitted faster than a human could
    'max_per_hour' => 8,    // per IP address
];
$configFile = dirname(__DIR__, 2) . '/roofcentre-enquiry-config.php';
if (is_file($configFile)) {
    $extra = include $configFile;
    if (is_array($extra)) {
        $config = array_merge($config, $extra);
    }
}

$wantsJson = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;

function respond(bool $ok, string $error = '', int $code = 200): void
{
    global $wantsJson, $config;
    http_response_code($code);
    if ($wantsJson) {
        header('Content-Type: application/json; charset=utf-8');
        header('Cache-Control: no-store');
        echo json_encode($ok ? ['ok' => true] : ['ok' => false, 'error' => $error]);
    } elseif ($ok) {
        header('Location: ' . $config['thank_you'], true, 303);
    } else {
        header('Content-Type: text/html; charset=utf-8');
        echo '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Enquiry not sent</title>'
            . '<p style="font:16px/1.5 system-ui;max-width:40em;margin:3em auto;padding:0 1em">'
            . htmlspecialchars($error) . ' Please <a href="javascript:history.back()">go back</a>, or call 0431 848 619.</p>';
    }
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    respond(false, 'Method not allowed.', 405);
}

// Same-site check: block cross-site form posts when the browser tells us the origin.
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin !== '') {
    $host = parse_url($origin, PHP_URL_HOST);
    if ($host && strcasecmp($host, $_SERVER['HTTP_HOST'] ?? '') !== 0) {
        respond(false, 'Invalid request.', 403);
    }
}

function field(string $name, int $max): string
{
    $v = isset($_POST[$name]) && is_string($_POST[$name]) ? $_POST[$name] : '';
    $v = trim(str_replace(["\r\n", "\r"], "\n", $v));
    $v = preg_replace('/[^\P{C}\n\t]/u', '', $v) ?? '';
    return mb_substr($v, 0, $max);
}

$name    = field('name', 100);
$phone   = field('phone', 30);
$email   = field('email', 150);
$suburb  = field('suburb', 80);
$service = field('service', 80);
$message = field('message', 3000);
$page    = field('page', 200);
$honey   = field('website', 200);
$started = (int) field('started', 20);

// Spam traps: hidden field filled in, or submitted implausibly fast. Pretend success.
if ($honey !== '' || ($started > 0 && (microtime(true) * 1000 - $started) < $config['min_seconds'] * 1000)) {
    respond(true);
}

$errors = [];
if ($name === '') $errors[] = 'name';
if (strlen(preg_replace('/\D/', '', $phone)) < 8) $errors[] = 'phone';
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'email';
if ($message === '') $errors[] = 'message';
if ($errors) {
    respond(false, 'Please check your ' . implode(', ', $errors) . '.', 422);
}
// Header injection guard (single-line fields only).
foreach ([$name, $phone, $email, $suburb, $service] as $single) {
    if (preg_match('/[\n\r]/', $single)) {
        respond(false, 'Invalid request.', 400);
    }
}

// Simple per-IP rate limit stored in the system temp directory.
$ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$bucket = sys_get_temp_dir() . '/rc-enquiry-' . hash('sha256', $ip . date('YmdH'));
$count = is_file($bucket) ? (int) file_get_contents($bucket) : 0;
if ($count >= $config['max_per_hour']) {
    respond(false, 'Too many enquiries have been sent from your connection. Please try again later.', 429);
}
@file_put_contents($bucket, (string) ($count + 1), LOCK_EX);

$lines = [
    'Name'    => $name,
    'Phone'   => $phone,
    'Email'   => $email,
    'Suburb'  => $suburb ?: '-',
    'Service' => $service ?: '-',
    'Page'    => $page ?: '-',
];
$body = "New enquiry from the Roof Centre website\n\n";
foreach ($lines as $label => $value) {
    $body .= str_pad($label . ':', 10) . $value . "\n";
}
$body .= "\nMessage:\n" . $message . "\n\n---\nSent " . date('j M Y, g:i a T') . ' from ' . $ip . "\n";

$subject = $config['subject'] . ($suburb !== '' ? ' (' . $suburb . ')' : '');
$encodedSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
$fromName = '=?UTF-8?B?' . base64_encode($config['from_name']) . '?=';
$replyName = '=?UTF-8?B?' . base64_encode($name) . '?=';

$headers = [
    'From: ' . $fromName . ' <' . $config['from'] . '>',
    'Reply-To: ' . $replyName . ' <' . $email . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'X-Mailer: RoofCentreSite',
];
if (!empty($config['bcc'])) {
    $headers[] = 'Bcc: ' . $config['bcc'];
}

$sent = @mail($config['to'], $encodedSubject, $body, implode("\r\n", $headers), '-f' . $config['from']);

if (!$sent) {
    error_log('[roofcentre-enquiry] mail() failed for enquiry from ' . $email);
    respond(false, 'Sorry, there was a problem sending your enquiry.', 500);
}

respond(true);
