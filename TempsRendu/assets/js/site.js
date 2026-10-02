(function () {
  var $ = function (id) { return document.getElementById(id); };

  // Menu mobile
  var toggle = $('nav-toggle'), nav = $('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Bandeau défilant
  var ticks = document.querySelectorAll('.tick');
  var still = function () { return document.documentElement.getAttribute('data-motion') === 'off' || (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches); };
  if (ticks.length > 1) {
    var i = 0, paused = false, bar = ticks[0].parentNode;
    bar.addEventListener('mouseenter', function () { paused = true; });
    bar.addEventListener('mouseleave', function () { paused = false; });
    bar.addEventListener('focusin', function () { paused = true; });
    bar.addEventListener('focusout', function () { paused = false; });
    setInterval(function () {
      if (paused || still()) return;
      ticks[i].classList.remove('on');
      i = (i + 1) % ticks.length;
      ticks[i].classList.add('on');
    }, 5000);
  }

  // Confort de lecture
  var ctoggle = $('comfort-toggle'), cpanel = $('comfort-panel');
  var prefs = {};
  try { prefs = JSON.parse(localStorage.getItem('tr-confort') || '{}'); } catch (e) { prefs = {}; }
  var paint = function () {
    document.querySelectorAll('[data-set]').forEach(function (b) {
      b.setAttribute('aria-pressed', (prefs[b.getAttribute('data-set')] || '') === b.getAttribute('data-val') ? 'true' : 'false');
    });
  };
  if (ctoggle && cpanel) {
    ctoggle.addEventListener('click', function () {
      cpanel.hidden = !cpanel.hidden;
      ctoggle.setAttribute('aria-expanded', cpanel.hidden ? 'false' : 'true');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !cpanel.hidden) { cpanel.hidden = true; ctoggle.setAttribute('aria-expanded', 'false'); ctoggle.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (!cpanel.hidden && !cpanel.contains(e.target) && !ctoggle.contains(e.target)) { cpanel.hidden = true; ctoggle.setAttribute('aria-expanded', 'false'); }
    });
    document.querySelectorAll('[data-set]').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.getAttribute('data-set'), v = b.getAttribute('data-val');
        prefs[k] = v;
        if (v) document.documentElement.setAttribute('data-' + k, v); else document.documentElement.removeAttribute('data-' + k);
        try { localStorage.setItem('tr-confort', JSON.stringify(prefs)); } catch (e) {}
        paint();
      });
    });
    paint();
  }

  // Panneau newsletter du bandeau
  var nlt = $('nl-toggle'), nlp = $('nl-panel');
  if (nlt && nlp) {
    nlt.addEventListener('click', function () {
      nlp.hidden = !nlp.hidden;
      nlt.setAttribute('aria-expanded', nlp.hidden ? 'false' : 'true');
      if (!nlp.hidden) { var inp = nlp.querySelector('input'); if (inp) inp.focus(); }
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !nlp.hidden) { nlp.hidden = true; nlt.setAttribute('aria-expanded', 'false'); nlt.focus(); } });
    document.addEventListener('click', function (e) { if (!nlp.hidden && !nlp.contains(e.target) && !nlt.contains(e.target)) { nlp.hidden = true; nlt.setAttribute('aria-expanded', 'false'); } });
  }

  // Simulateur affiché à la demande
  var openCalc = $('open-calc'), calcSec = $('calcul');
  if (openCalc && calcSec) {
    var show = function (scroll) {
      calcSec.hidden = false;
      openCalc.setAttribute('aria-expanded', 'true');
      if (scroll) { calcSec.scrollIntoView({ behavior: still() ? 'auto' : 'smooth' }); var t = $('calc-title'); if (t) t.focus({ preventScroll: true }); }
    };
    openCalc.addEventListener('click', function () {
      if (calcSec.hidden) { show(true); } else { calcSec.hidden = true; openCalc.setAttribute('aria-expanded', 'false'); }
    });
    if (location.hash === '#calcul') show(true);
  }

  // Calculateur de temps rendu
  if ($('c-people')) {
    var fmt = new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 0 });
    var calc = function () {
      var p = +$('c-people').value, m = +$('c-min').value, part = +$('c-part').value / 100;
      $('v-people').textContent = p;
      $('v-min').textContent = m + ' min';
      $('v-part').textContent = Math.round(part * 100) + ' %';
      var h = p * (m / 60) * 220 * part;
      $('r-hours').textContent = fmt.format(h) + ' h';
      $('r-days').textContent = 'soit ' + fmt.format(h / 7) + ' jours de travail';
      var wk = Math.round(m * part * 5);
      $('r-week').textContent = Math.floor(wk / 60) + ' h ' + String(wk % 60).padStart(2, '0');
    };
    ['c-people', 'c-min', 'c-part'].forEach(function (id) { $(id).addEventListener('input', calc); });
    calc();
  }

  // Onglets des tarifs (et lien direct #entreprises, #formations, #particuliers)
  var tabs = document.querySelectorAll('.tab');
  var select = function (t) {
    tabs.forEach(function (o) {
      o.setAttribute('aria-selected', o === t ? 'true' : 'false');
      $(o.getAttribute('aria-controls')).hidden = (o !== t);
    });
  };
  tabs.forEach(function (t) { t.addEventListener('click', function () { select(t); }); });
  if (tabs.length && location.hash) {
    var match = document.querySelector('.tab[data-hash="' + location.hash.slice(1) + '"]');
    if (match) select(match);
  }

  // Formulaire de contact : profil choisi par l'ancre (#entreprise / #particulier) et blocs conditionnels
  var showIf = function () {
    document.querySelectorAll('[data-show-if]').forEach(function (el) {
      var parts = el.getAttribute('data-show-if').split('=');
      var checked = document.querySelector('input[name="' + parts[0] + '"]:checked');
      var on = checked && parts[1].split('|').indexOf(checked.value) > -1;
      el.hidden = !on;
      el.querySelectorAll('input,select,textarea').forEach(function (i) { i.disabled = !on; });
    });
  };
  if (location.hash) {
    var pre = document.querySelector('input[name="profil"][value="' + location.hash.slice(1) + '"]');
    if (pre) pre.checked = true;
    var obj = document.querySelector('select[name="objet"] option[value="' + location.hash.slice(1) + '"]');
    if (obj) obj.selected = true;
  }
  document.querySelectorAll('input[name="profil"]').forEach(function (r) { r.addEventListener('change', showIf); });
  showIf();

  // Envoi des formulaires vers Make
  var endpoint = (document.querySelector('meta[name="forms-endpoint"]') || {}).content || '';
  document.querySelectorAll('form[data-form]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var m = f.querySelector('[data-msg]');
      var data = new URLSearchParams(new FormData(f));
      data.delete('consentement');
      data.append('formulaire', f.getAttribute('data-form'));
      data.append('page', location.pathname);
      data.append('date', new Date().toISOString());
      var done = function (ok) {
        m.textContent = ok ? (f.getAttribute('data-success') || 'Merci, votre message est bien parti.') :
          "L'envoi n'est pas encore activé. Écrivez-nous en attendant, nous vous répondrons rapidement.";
        m.hidden = false;
        if (ok) { f.reset(); showIf(); }
      };
      if (!endpoint) { done(false); return; }
      fetch(endpoint, { method: 'POST', mode: 'no-cors', body: data }).then(function () { done(true); }).catch(function () { done(false); });
    });
  });
})();
