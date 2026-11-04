(() => {
  'use strict';

  function initializeMotion() {
    if (typeof window.matchMedia !== 'function') return;
    const root = document.documentElement;
    const toggle = document.querySelector('.motion-toggle');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const animations = new Map();
    let userPaused = false;
    let motionEnabled = false;

    try {
      userPaused = localStorage.getItem('kairan-motion') === 'off';
    } catch (error) {
      userPaused = false;
    }

    function cancelAnimations() {
      animations.forEach((element, animation) => animation.cancel());
      animations.clear();
    }

    function syncPreference() {
      motionEnabled = !reducedMotion.matches && !userPaused;
      root.dataset.motion = motionEnabled ? 'on' : 'off';
      if (toggle) {
        toggle.hidden = false;
        toggle.disabled = reducedMotion.matches;
        toggle.setAttribute('aria-pressed', String(motionEnabled));
        toggle.setAttribute('aria-label', reducedMotion.matches ? 'Animations disabled by your system settings' : 'Animations');
        toggle.querySelector('[data-motion-status]').textContent = reducedMotion.matches ? 'reduced' : motionEnabled ? 'on' : 'off';
      }
      if (!motionEnabled) cancelAnimations();
    }

    function enter(element, delay = 0, duration = 560) {
      const destination = document.getElementById(window.location.hash.slice(1));
      if (!motionEnabled || document.hidden || typeof element.animate !== 'function' || element.matches(':focus-within')) return;
      if (destination && (destination === element || destination.contains(element))) return;
      const animation = element.animate([
        {opacity: 0, transform: 'translateY(16px)'},
        {opacity: 1, transform: 'translateY(0)'}
      ], {duration, delay, easing: 'cubic-bezier(.22,1,.36,1)', fill: 'backwards'});
      animations.set(animation, element);
      const forgetAnimation = () => animations.delete(animation);
      animation.finished.then(forgetAnimation, forgetAnimation);
    }

    function syncVisibility() {
      root.dataset.pageVisible = String(!document.hidden);
      if (document.hidden) cancelAnimations();
    }

    syncPreference();
    syncVisibility();
    if (toggle) {
      toggle.addEventListener('click', () => {
        userPaused = !userPaused;
        try {
          localStorage.setItem('kairan-motion', userPaused ? 'off' : 'on');
        } catch (error) {
          // The preference still works for this visit when storage is unavailable.
        }
        syncPreference();
      });
    }
    if (typeof reducedMotion.addEventListener === 'function') {
      reducedMotion.addEventListener('change', syncPreference);
    } else if (typeof reducedMotion.addListener === 'function') {
      reducedMotion.addListener(syncPreference);
    }
    document.addEventListener('visibilitychange', syncVisibility);
    window.addEventListener('hashchange', cancelAnimations);
    window.addEventListener('beforeprint', cancelAnimations);
    document.addEventListener('focusin', event => {
      animations.forEach((element, animation) => {
        if (element.contains(event.target)) {
          animation.cancel();
          animations.delete(animation);
        }
      });
    });

    if (!window.location.hash) {
      document.querySelectorAll('.hero-copy > *').forEach((element, index) => enter(element, index * 65, 650));
      const portrait = document.querySelector('.hero-portrait');
      if (portrait) enter(portrait, 180, 800);
    }

    if ('IntersectionObserver' in window) {
      const reveals = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) return;
          enter(entry.target);
          reveals.unobserve(entry.target);
        });
      }, {threshold: 0, rootMargin: '0px 0px -24px 0px'});
      document.querySelectorAll('.section-label, .biography, .education-entry, .papers-heading, .paper-entry').forEach(element => reveals.observe(element));

      const hero = document.querySelector('.hero');
      const heroVisibility = new IntersectionObserver(entries => {
        root.dataset.heroVisible = String(entries[0].isIntersecting);
      });
      if (hero) heroVisibility.observe(hero);
    }
  }

  initializeMotion();

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
