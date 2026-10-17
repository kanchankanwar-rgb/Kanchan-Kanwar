(function () {
  // Mobile menu
  var menuBtn = document.getElementById('menu-btn');
  var nav = document.getElementById('site-nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', String(open));
    });
  }

  // Services mega menu
  var megaBtn = document.getElementById('mega-btn');
  var mega = document.getElementById('mega');
  function setMega(open) {
    if (!mega) return;
    mega.classList.toggle('open', open);
    megaBtn.setAttribute('aria-expanded', String(open));
  }
  if (megaBtn && mega) {
    megaBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      setMega(!mega.classList.contains('open'));
    });
    document.addEventListener('click', function (e) {
      if (!mega.contains(e.target) && window.innerWidth > 960) setMega(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { setMega(false); megaBtn.focus(); }
    });
  }

  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canObserve = 'IntersectionObserver' in window;

  // What we do: connected hub tabs, auto-advancing until the visitor interacts
  var hub = document.querySelector('[data-hub]');
  if (hub) {
    var tabs = Array.prototype.slice.call(hub.querySelectorAll('.hub-node'));
    var panels = hub.querySelectorAll('.hub-panel');
    var lines = hub.querySelectorAll('.hub-line');
    var current = 0, timer = null, userPicked = false, inView = false;
    function select(i, focus) {
      current = i;
      tabs.forEach(function (t, n) {
        t.setAttribute('aria-selected', String(n === i));
        t.tabIndex = n === i ? 0 : -1;
      });
      Array.prototype.forEach.call(panels, function (p, n) { p.hidden = n !== i; });
      Array.prototype.forEach.call(lines, function (l) { l.classList.toggle('on', +l.getAttribute('data-line') === i); });
      if (focus) tabs[i].focus();
    }
    function stop() { clearInterval(timer); timer = null; }
    function start() {
      if (reduceMotion || userPicked || timer || !inView) return;
      timer = setInterval(function () { select((current + 1) % tabs.length); }, 6000);
    }
    tabs.forEach(function (t, n) {
      t.addEventListener('click', function () { userPicked = true; stop(); select(n); });
      t.addEventListener('keydown', function (e) {
        var k = e.key, next = null;
        if (k === 'ArrowRight' || k === 'ArrowDown') next = (current + 1) % tabs.length;
        if (k === 'ArrowLeft' || k === 'ArrowUp') next = (current - 1 + tabs.length) % tabs.length;
        if (next !== null) { e.preventDefault(); userPicked = true; stop(); select(next, true); }
      });
    });
    select(0);
    hub.addEventListener('mouseenter', stop);
    hub.addEventListener('mouseleave', start);
    if (canObserve) {
      new IntersectionObserver(function (entries) {
        inView = entries[0].isIntersecting;
        if (inView) start(); else stop();
      }, { threshold: 0.35 }).observe(hub);
    }
  }

  // Scroll reveal and count-up numbers
  if (canObserve && !reduceMotion) {
    var sel = '.section-head, .feature, .svc-card, .insight, .ind, .deliv, .stat, .steps li, .outcomes li, ' +
              '.value, .meaning > div, .ind-row, .founder-photo, .founder-copy, .hub-map, .hub-panels, ' +
              '.intro-grid, .two-col > div, .contact-copy, .contact-form, .article, .cta-copy, .channels .eyebrow';
    var items = document.querySelectorAll(sel);
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('in');
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    Array.prototype.forEach.call(items, function (el) {
      if (el.closest('.hero, .page-hero, .mega')) return;
      var sibs = Array.prototype.filter.call(el.parentNode.children, function (c) { return c.matches(sel); });
      el.style.setProperty('--rv-d', Math.min(sibs.indexOf(el), 5) * 0.08 + 's');
      el.classList.add('rv');
      io.observe(el);
    });
    document.querySelectorAll('.steps').forEach(function (el) { io.observe(el); });
    document.documentElement.classList.add('js-rv');

    var counters = document.querySelectorAll('[data-count]');
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        cio.unobserve(en.target);
        var el = en.target, target = +el.getAttribute('data-count'), text = el.textContent;
        var t0 = null;
        (function step(ts) {
          if (!t0) t0 = ts;
          var k = Math.min((ts - t0) / 1400, 1), eased = 1 - Math.pow(1 - k, 3);
          el.textContent = text.replace(String(target), String(Math.round(target * eased)));
          if (k < 1) requestAnimationFrame(step);
        })(performance.now());
      });
    }, { threshold: 0.6 });
    Array.prototype.forEach.call(counters, function (c) { cio.observe(c); });
  }

  // Contact form: posts JSON to the webhook set in data-endpoint
  var form = document.getElementById('contact-form');
  if (!form) return;
  var status = document.getElementById('form-status');
  var submit = document.getElementById('f-submit');
  var email = 'hello@hemavik.com';

  function setStatus(msg, kind) {
    status.textContent = msg;
    status.className = 'form-status' + (kind ? ' ' + kind : '');
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = form.elements.name;
    var mail = form.elements.email;
    var bad = null;
    [name, mail].forEach(function (el) { el.removeAttribute('aria-invalid'); });
    if (!name.value.trim()) bad = name;
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(mail.value.trim())) bad = mail;
    if (bad) {
      bad.setAttribute('aria-invalid', 'true');
      bad.focus();
      setStatus(bad === name ? 'Please add your name.' : 'Please enter a valid email address.', 'err');
      return;
    }

    var endpoint = form.dataset.endpoint;
    if (!endpoint) {
      setStatus('This form is not connected yet. Please email ' + email + ' directly.', 'err');
      return;
    }

    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = v; });
    data.source = 'hemavik.com contact form';
    data.page = location.pathname;
    data.submittedAt = new Date().toISOString();

    submit.disabled = true;
    setStatus('Sending…');
    fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(function (res) {
      if (!res.ok) throw new Error(res.status);
      form.reset();
      setStatus('Thank you. We will reply within one working day.', 'ok');
    }).catch(function () {
      setStatus('Your message could not be sent. Please email ' + email + '.', 'err');
    }).finally(function () {
      submit.disabled = false;
    });
  });
})();
