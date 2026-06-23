'use strict';

// ── NAV TOGGLE ─────────────────────────────────────────
const navToggle = document.getElementById('navToggle');
const navLinks  = document.getElementById('navLinks');

if (navToggle) {
  navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
}

// ── TABS ───────────────────────────────────────────────
function initTabs() {
  document.querySelectorAll('[data-tab-group]').forEach(group => {
    const groupId = group.dataset.tabGroup;
    const buttons = group.querySelectorAll('.tab-btn');
    const panes   = document.querySelectorAll(`[data-tab-pane="${groupId}"]`);

    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        buttons.forEach(b => b.classList.remove('active'));
        panes.forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        const target = document.getElementById(btn.dataset.tab);
        if (target) target.classList.add('active');
        // Update URL hash without scroll
        history.replaceState(null, '', `#${btn.dataset.tab}`);
      });
    });

    // Activate from URL hash
    const hash = location.hash.replace('#', '');
    if (hash) {
      const matchBtn = group.querySelector(`[data-tab="${hash}"]`);
      if (matchBtn) matchBtn.click();
    }
  });
}

// ── TRANSPARENCY METERS ────────────────────────────────
function animateMeters() {
  const meters = document.querySelectorAll('.t-meter-fill[data-width]');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        el.style.width = el.dataset.width + '%';
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.3 });

  meters.forEach(m => {
    m.style.width = '0%';
    observer.observe(m);
  });
}

// Also animate rating breakdown bars
function animateBars() {
  const bars = document.querySelectorAll('.rb-fill[data-width], .sub-rating-fill[data-width]');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.width = entry.target.dataset.width + '%';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  bars.forEach(b => {
    b.style.width = '0%';
    observer.observe(b);
  });
}

// ── STAR RATINGS (review form) ─────────────────────────
function initStarRatings() {
  document.querySelectorAll('.star-field').forEach(field => {
    const hiddenInput = document.getElementById(field.dataset.target);
    const labels = field.querySelectorAll('label');
    const radios  = field.querySelectorAll('input[type=radio]');

    radios.forEach(radio => {
      radio.addEventListener('change', () => {
        if (hiddenInput) hiddenInput.value = radio.value;
      });
    });
  });
}

// ── SEARCH AUTOCOMPLETE ────────────────────────────────
function initSearch() {
  const input    = document.getElementById('heroSearch');
  const dropdown = document.getElementById('searchDropdown');
  if (!input || !dropdown) return;

  let debounceTimer;

  input.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    const q = input.value.trim();
    if (q.length < 2) { dropdown.classList.remove('open'); return; }

    debounceTimer = setTimeout(async () => {
      try {
        const res  = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
        const data = await res.json();
        renderDropdown(data);
      } catch (e) {
        console.error('Search error:', e);
      }
    }, 280);
  });

  function renderDropdown(items) {
    if (!items.length) { dropdown.classList.remove('open'); return; }
    dropdown.innerHTML = items.map(c => `
      <a class="search-result-item" href="/companies/${c.slug}">
        <div class="search-result-logo"
             style="background:var(--navy);">${c.logo_initials}</div>
        <div>
          <div class="search-result-name">${c.name}</div>
          <div class="search-result-meta">${c.industry} · ${c.avg_rating}★ · ${c.review_count} reviews</div>
        </div>
      </a>
    `).join('');
    dropdown.classList.add('open');
  }

  document.addEventListener('click', e => {
    if (!input.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.classList.remove('open');
    }
  });

  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') {
      const q = input.value.trim();
      if (q) window.location.href = `/search?q=${encodeURIComponent(q)}`;
    }
  });

  // Hero search button
  const searchBtn = document.getElementById('heroSearchBtn');
  if (searchBtn) {
    searchBtn.addEventListener('click', () => {
      const q = input.value.trim();
      if (q) window.location.href = `/search?q=${encodeURIComponent(q)}`;
    });
  }
}

// ── HELPFUL VOTES ──────────────────────────────────────
function initVotes() {
  document.querySelectorAll('.helpful-btn[data-review]').forEach(btn => {
    btn.addEventListener('click', async () => {
      const reviewId = btn.dataset.review;
      const helpful  = btn.dataset.helpful === 'true';

      try {
        const res  = await fetch(`/reviews/vote/${reviewId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json',
                     'X-CSRFToken': getCSRF() },
          body: JSON.stringify({ helpful })
        });
        const data = await res.json();
        const row  = btn.closest('.helpful-btns');
        if (row) {
          row.querySelector('[data-helpful=true] .vote-count').textContent  = data.helpful;
          row.querySelector('[data-helpful=false] .vote-count').textContent = data.not_helpful;
        }
        btn.classList.add('voted');
      } catch (e) {
        console.error('Vote error:', e);
      }
    });
  });
}

// ── SALARY BAR WIDTHS ──────────────────────────────────
function initSalaryBars() {
  document.querySelectorAll('.salary-bar-fill[data-pct]').forEach(bar => {
    setTimeout(() => { bar.style.width = bar.dataset.pct + '%'; }, 300);
  });
}

// ── FORM VALIDATION HELPERS ────────────────────────────
function initReviewForm() {
  const form = document.getElementById('reviewForm');
  if (!form) return;

  form.addEventListener('submit', e => {
    const overall = document.getElementById('overall_rating');
    if (!overall || !overall.value) {
      e.preventDefault();
      showToast('Please select an overall rating.', 'error');
      overall.closest('.form-group').scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  });
}

// ── TOAST UTILITY ──────────────────────────────────────
function showToast(msg, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `flash flash-${type}`;
  toast.style.cssText = 'position:fixed;bottom:2rem;right:1rem;z-index:9999;max-width:340px;';
  toast.innerHTML = `<span>${msg}</span><button class="flash-close" onclick="this.parentElement.remove()">✕</button>`;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

// ── CSRF TOKEN ─────────────────────────────────────────
function getCSRF() {
  const meta = document.querySelector('meta[name=csrf-token]');
  return meta ? meta.content : '';
}

// ── INIT ───────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  animateMeters();
  animateBars();
  initStarRatings();
  initSearch();
  initVotes();
  initSalaryBars();
  initReviewForm();
});
