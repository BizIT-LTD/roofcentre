<?php
/**
 * TEMPLATE ONLY. Copy to the server as roofcentre-enquiry-config.php in the
 * folder that CONTAINS public_html (never inside public_html, never in Git).
 *
 * Hostinger: /home/u123456789/domains/roofcentre.com.au/roofcentre-enquiry-config.php
 */
return [
    'to'           => 'info@roofcentre.com.au',
    'bcc'          => '',
    'from'         => 'website@roofcentre.com.au',
    'from_name'    => 'Roof Centre Website',
    'subject'      => 'New quote request from the Roof Centre website',
    'min_seconds'  => 3,
    'max_per_hour' => 8,
];
