(function () {
  // Mobile menu
  var btn = document.getElementById('menu-btn');
  var nav = document.getElementById('site-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        nav.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // Contact form: posts JSON to an n8n / GoHighLevel webhook set in data-endpoint
  var form = document.getElementById('contact-form');
  if (!form) return;
  var status = document.getElementById('form-status');
  var submit = document.getElementById('f-submit');

  function setStatus(msg, kind) {
    status.textContent = msg;
    status.className = 'form-status' + (kind ? ' ' + kind : '');
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = form.elements.name;
    var email = form.elements.email;
    var bad = null;
    [name, email].forEach(function (el) { el.removeAttribute('aria-invalid'); });
    if (!name.value.trim()) bad = name;
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) bad = email;
    if (bad) {
      bad.setAttribute('aria-invalid', 'true');
      bad.focus();
      setStatus(bad === name ? 'Please add your name.' : 'Please enter a valid email address.', 'err');
      return;
    }

    var endpoint = form.dataset.endpoint;
    if (!endpoint) {
      setStatus('This form is not connected yet. Please email hello@hemavik.com directly.', 'err');
      return;
    }

    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = v; });
    data.source = 'hemavik.com contact form';
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
      setStatus('Your message could not be sent. Please email hello@hemavik.com.', 'err');
    }).finally(function () {
      submit.disabled = false;
    });
  });
})();
