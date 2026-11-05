(() => {
  'use strict';

  const section = document.querySelector('[data-citation-feed]');
  if (!section || typeof fetch !== 'function') return;

  function normalizedTitle(title) {
    return typeof title === 'string' ? title.normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{N}]/gu, '') : '';
  }

  function snapshotDate(value) {
    if (typeof value !== 'string') return null;
    const day = value.slice(0, 10);
    if (!/^\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})?)?$/.test(value)) return null;
    if (Number.isNaN(Date.parse(value.replace(' ', 'T')))) return null;
    const date = new Date(`${day}T00:00:00Z`);
    if (Number.isNaN(date.getTime()) || date.toISOString().slice(0, 10) !== day) return null;
    return {day, label: date.toLocaleDateString('en-US', {year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC'})};
  }

  function updateCitations(data) {
    const updated = snapshotDate(data.updated);
    if (!updated || !data.publications || Array.isArray(data.publications) || typeof data.publications !== 'object') return;
    const publications = Object.values(data.publications);
    section.querySelectorAll('[data-citation-count]').forEach(count => {
      const row = count.closest('[data-paper-title]');
      if (!row || row.dataset.citationUpdated > updated.day) return;
      let publication = row.dataset.scholarId ? data.publications[row.dataset.scholarId] : null;
      if (!publication && !row.dataset.scholarId) {
        const title = normalizedTitle(row.dataset.paperTitle);
        const matches = publications.filter(item => title && normalizedTitle(item?.bib?.title) === title);
        if (matches.length === 1) publication = matches[0];
      }
      const value = publication?.num_citations;
      if (!Number.isSafeInteger(value) || value < 0) return;
      count.textContent = String(value);
      row.dataset.citationUpdated = updated.day;
      const date = row.querySelector('[data-citation-date]');
      date.dateTime = updated.day;
      date.textContent = `as of ${updated.label}`;
      date.hidden = false;
      const label = row.querySelector('span[title]');
      if (label) label.title = 'Google Scholar citation count';
    });
  }

  async function refreshCitations() {
    const controller = typeof AbortController === 'function' ? new AbortController() : null;
    const timeout = controller ? setTimeout(() => controller.abort(), 8000) : null;
    try {
      const response = await fetch(section.dataset.citationFeed, {credentials: 'omit', cache: 'no-cache', ...(controller ? {signal: controller.signal} : {})});
      if (!response.ok) return;
      const data = await response.json();
      if (data && typeof data === 'object') updateCitations(data);
    } catch (error) {
      // Keep the dated, verified snapshot when Scholar data is unavailable.
    } finally {
      if (timeout !== null) clearTimeout(timeout);
    }
  }

  refreshCitations();
})();
