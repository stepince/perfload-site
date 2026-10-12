// Light/dark theme toggle. Works with the inline <head> snippet that sets
// <html data-theme> before first paint. Any <button data-theme-toggle> on the
// page is wired up, so the control is reusable anywhere.
(function () {
  var KEY = 'theme';
  var root = document.documentElement;
  var media = window.matchMedia('(prefers-color-scheme: light)');

  function saved() {
    try {
      var v = localStorage.getItem(KEY);
      return v === 'light' || v === 'dark' ? v : null;
    } catch (e) { return null; }
  }
  function systemTheme() { return media.matches ? 'light' : 'dark'; }

  function apply(theme) {
    root.setAttribute('data-theme', theme);
    document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
      btn.setAttribute('aria-checked', theme === 'dark' ? 'true' : 'false');
    });
  }

  function animate() {
    root.classList.add('theme-transition');
    setTimeout(function () { root.classList.remove('theme-transition'); }, 350);
  }

  apply(root.getAttribute('data-theme') || saved() || systemTheme());

  // A <button> already activates on Enter and Space, so click covers keyboard.
  document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      animate();
      apply(next);
      try { localStorage.setItem(KEY, next); } catch (e) {}
    });
  });

  // Follow the OS while the user has not made an explicit choice.
  var onSystem = function () { if (!saved()) { animate(); apply(systemTheme()); } };
  if (media.addEventListener) media.addEventListener('change', onSystem);

  // Keep other open tabs in sync.
  window.addEventListener('storage', function (e) {
    if (e.key === KEY) apply(saved() || systemTheme());
  });
})();
