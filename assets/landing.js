// Copy-to-clipboard buttons for code blocks on the landing pages.
// Same behavior as the inline script in installation.html: copies the
// adjacent <pre><code> text and flashes a check icon.
(function () {
  var checkIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
  document.querySelectorAll('.copy-btn').forEach(function (btn) {
    var original = btn.innerHTML;
    btn.addEventListener('click', function () {
      var codeEl = btn.parentElement.querySelector('code');
      var text = codeEl ? codeEl.textContent : '';
      if (!text || !navigator.clipboard) return;
      navigator.clipboard.writeText(text).then(function () {
        btn.innerHTML = checkIcon;
        btn.classList.add('copied');
        btn.setAttribute('aria-label', 'Copied');
        setTimeout(function () {
          btn.innerHTML = original;
          btn.classList.remove('copied');
          btn.setAttribute('aria-label', 'Copy');
        }, 1500);
      });
    });
  });
})();
