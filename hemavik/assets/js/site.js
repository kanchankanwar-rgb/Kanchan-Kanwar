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
