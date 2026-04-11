// ── Character counter ─────────────────────────────────────────
const textarea = document.getElementById('feedback');
const counter  = document.getElementById('charCounter');

if (textarea && counter) {
  textarea.addEventListener('input', () => {
    const len = textarea.value.length;
    counter.textContent = `${len} / 280`;
    counter.style.color = len > 250 ? '#E63946' : len > 200 ? '#F4A261' : '#8896a5';
  });
}

// ── Example tweet buttons ────────────────────────────────────
document.querySelectorAll('.ex-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    if (textarea) {
      textarea.value = btn.dataset.text;
      textarea.dispatchEvent(new Event('input'));
      textarea.focus();
      textarea.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  });
});

// ── Loading state on submit ───────────────────────────────────
const form      = document.getElementById('feedbackForm');
const submitBtn = document.getElementById('submitBtn');

if (form && submitBtn) {
  form.addEventListener('submit', () => {
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    submitBtn.querySelector('.btn-text').textContent = 'Analysing';
    submitBtn.querySelector('.btn-arrow').textContent = '⏳';
  });
}
