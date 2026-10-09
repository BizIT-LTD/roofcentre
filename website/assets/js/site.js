/* Roof Centre — site behaviour. No dependencies. */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var mobileNav = window.matchMedia('(max-width: 1040px)');

  /* Header shadow on scroll */
  var header = document.querySelector('[data-header]');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* Mobile menu */
  var toggle = document.querySelector('[data-menu-toggle]');
  var nav = document.getElementById('site-nav');
  function setMenu(open) {
    if (!toggle || !nav) return;
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
    document.body.classList.toggle('nav-open', open);
  }
  if (toggle && nav) {
    toggle.addEventListener('click', function () { setMenu(toggle.getAttribute('aria-expanded') !== 'true'); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) { setMenu(false); toggle.focus(); }
    });
    mobileNav.addEventListener('change', function () { setMenu(false); });
  }

  /* Services submenu toggle (click / keyboard; hover handled in CSS on desktop) */
  document.querySelectorAll('.nav__sub-toggle').forEach(function (btn) {
    var item = btn.closest('.nav__has-sub');
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', String(open));
      item.classList.toggle('is-open', open);
    });
    item.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && item.classList.contains('is-open')) {
        btn.setAttribute('aria-expanded', 'false'); item.classList.remove('is-open'); btn.focus();
      }
    });
    document.addEventListener('click', function (e) {
      if (!mobileNav.matches && !item.contains(e.target)) { btn.setAttribute('aria-expanded', 'false'); item.classList.remove('is-open'); }
    });
  });

  /* Scroll reveal */
  var reveals = document.querySelectorAll('.reveal');
  if (!reduceMotion && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('is-visible'); io.unobserve(entry.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* Gallery filter */
  var chips = document.querySelectorAll('[data-filter]');
  var status = document.querySelector('[data-filter-status]');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var value = chip.getAttribute('data-filter');
      chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
      var shown = 0;
      document.querySelectorAll('[data-category]').forEach(function (li) {
        var match = value === 'all' || li.getAttribute('data-category') === value;
        li.hidden = !match;
        if (match) shown++;
      });
      if (status) status.textContent = 'Showing ' + shown + ' photos';
    });
  });

  /* Lightbox */
  var box = document.querySelector('[data-lightbox]');
  if (box && typeof box.showModal === 'function') {
    var boxImg = box.querySelector('[data-lightbox-img]');
    var boxCap = box.querySelector('[data-lightbox-caption]');
    var items = [];
    var index = 0;
    var opener = null;

    function visibleItems(from) {
      var list = from.closest('ul');
      return Array.prototype.filter.call(list.querySelectorAll('.gallery__item'), function (b) { return !b.closest('li').hidden; });
    }
    function show(i) {
      index = (i + items.length) % items.length;
      var b = items[index];
      boxImg.src = b.getAttribute('data-full');
      boxImg.alt = b.getAttribute('data-caption') || '';
      boxCap.textContent = b.getAttribute('data-caption') || '';
    }
    document.addEventListener('click', function (e) {
      var b = e.target.closest('.gallery__item');
      if (!b) return;
      opener = b;
      items = visibleItems(b);
      show(items.indexOf(b));
      box.showModal();
      document.body.style.overflow = 'hidden';
    });
    box.querySelector('[data-lightbox-close]').addEventListener('click', function () { box.close(); });
    box.querySelector('[data-lightbox-prev]').addEventListener('click', function () { show(index - 1); });
    box.querySelector('[data-lightbox-next]').addEventListener('click', function () { show(index + 1); });
    box.addEventListener('click', function (e) { if (e.target === box || e.target.tagName === 'FIGURE') box.close(); });
    box.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') show(index + 1);
      if (e.key === 'ArrowLeft') show(index - 1);
    });
    box.addEventListener('close', function () {
      document.body.style.overflow = '';
      boxImg.removeAttribute('src');
      if (opener) opener.focus();
    });
    var touchX = null;
    box.addEventListener('touchstart', function (e) { touchX = e.touches[0].clientX; }, { passive: true });
    box.addEventListener('touchend', function (e) {
      if (touchX === null) return;
      var dx = e.changedTouches[0].clientX - touchX;
      if (Math.abs(dx) > 50) show(index + (dx < 0 ? 1 : -1));
      touchX = null;
    });
  }

  /* Enquiry form */
  var serviceParam = new URLSearchParams(window.location.search).get('service');
  document.querySelectorAll('[data-enquiry-form]').forEach(function (form) {
    var started = form.querySelector('[name="started"]');
    var pageField = form.querySelector('[name="page"]');
    if (started) started.value = String(Date.now());
    if (pageField) pageField.value = window.location.pathname;

    if (serviceParam) {
      var select = form.querySelector('[name="service"]');
      var slugToName = {
        'roof-repair': 'Roof Repair', 'roof-restoration': 'Roof Restoration', 'roof-replacment': 'Roof Replacement',
        'colorbond-roofing': 'Colorbond Roofing', 'gutter-8-downpipe-replacement': 'Gutter & Downpipe Replacement',
        'gutter-protection': 'Gutter Protection', 'emergency-roof-make-safe': 'Emergency Roof Make Safe',
        'custom-valley-flashings': 'Custom Valley Flashings'
      };
      if (select && slugToName[serviceParam]) select.value = slugToName[serviceParam];
    }

    var statusEl = form.querySelector('[data-form-status]');
    var submit = form.querySelector('[type="submit"]');
    var submitHtml = submit.innerHTML;

    function setError(field, message) {
      var wrap = field.closest('.field');
      var existing = wrap.querySelector('.field__error');
      if (existing) existing.remove();
      wrap.classList.toggle('has-error', !!message);
      field.setAttribute('aria-invalid', message ? 'true' : 'false');
      if (message) {
        var p = document.createElement('p');
        p.className = 'field__error';
        p.id = field.id + '-error';
        p.textContent = message;
        wrap.appendChild(p);
        field.setAttribute('aria-describedby', p.id);
      } else {
        field.removeAttribute('aria-describedby');
      }
    }
    function validate() {
      var firstBad = null;
      form.querySelectorAll('input[required], textarea[required]').forEach(function (field) {
        var v = field.value.trim();
        var msg = '';
        if (!v) msg = 'Please fill in this field.';
        else if (field.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) msg = 'Please enter a valid email address.';
        else if (field.type === 'tel' && v.replace(/\D/g, '').length < 8) msg = 'Please enter a valid phone number.';
        setError(field, msg);
        if (msg && !firstBad) firstBad = field;
      });
      if (firstBad) firstBad.focus();
      return !firstBad;
    }
    function showStatus(type, html) {
      statusEl.className = 'form-status is-' + type;
      statusEl.innerHTML = html;
      statusEl.focus();
    }
    form.addEventListener('input', function (e) {
      if (e.target.closest('.has-error')) setError(e.target, '');
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validate()) return;
      submit.disabled = true;
      submit.textContent = 'Sending…';
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (res) {
          return res.json().catch(function () { return { ok: false }; }).then(function (data) { data.status = res.status; return data; });
        })
        .then(function (data) {
          if (data.ok) {
            form.reset();
            if (started) started.value = String(Date.now());
            if (pageField) pageField.value = window.location.pathname;
            showStatus('success', 'Thanks, your enquiry has been sent. We will get back to you as soon as possible.');
          } else {
            throw new Error(data.error || 'failed');
          }
        })
        .catch(function (err) {
          var msg = err && err.message && err.message !== 'failed' && err.message.indexOf('fetch') === -1 ? err.message + ' ' : '';
          showStatus('error', msg + 'Sorry, your enquiry could not be sent. Please call us on <a href="tel:+61431848619">0431 848 619</a> or email <a href="mailto:info@roofcentre.com.au">info@roofcentre.com.au</a>.');
        })
        .then(function () {
          submit.disabled = false;
          submit.innerHTML = submitHtml;
        });
    });
  });
})();
