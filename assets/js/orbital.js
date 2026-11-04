(() => {
  'use strict';

  const dialog = document.querySelector('.figure-dialog');
  if (!dialog || typeof dialog.showModal !== 'function') return;

  const image = dialog.querySelector('.figure-dialog-image');
  const title = dialog.querySelector('#figure-dialog-title');
  const original = dialog.querySelector('.figure-original');
  let trigger = null;

  document.querySelectorAll('[data-paper-figure]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      trigger = link;
      image.src = link.href;
      image.alt = link.querySelector('img').alt;
      title.textContent = link.dataset.title;
      original.href = link.href;
      dialog.showModal();
      document.body.classList.add('figure-open');
      dialog.querySelector('.figure-dialog-body').scrollTop = 0;
    });
  });

  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) {
      dialog.close();
    }
  });

  dialog.addEventListener('close', () => {
    document.body.classList.remove('figure-open');
    if (trigger) trigger.focus({preventScroll: true});
  });
})();
