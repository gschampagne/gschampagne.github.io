document.addEventListener('DOMContentLoaded', () => {
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const captionText = document.getElementById('caption');
  const closeBtn = document.querySelector('.lightbox .close');

  // Handle ALL galleries on the page (fixes art.html having two)
  document.querySelectorAll('.image-gallery img').forEach(img => {
    const wrapper = document.createElement('a');
    wrapper.href = img.src;
    wrapper.dataset.caption = img.alt || '';
    img.parentNode.insertBefore(wrapper, img);
    wrapper.appendChild(img);

    wrapper.addEventListener('click', e => {
      e.preventDefault();
      lightbox.style.display = 'block';
      lightboxImg.src = wrapper.href;
      captionText.textContent = wrapper.dataset.caption;
    });
  });

  closeBtn.addEventListener('click', () => lightbox.style.display = 'none');
  lightbox.addEventListener('click', e => { if (e.target === lightbox) lightbox.style.display = 'none'; });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') lightbox.style.display = 'none'; });

  // Fade-in images on scroll
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } });
  }, { threshold: 0.1 });
  document.querySelectorAll('.image-gallery img').forEach(img => observer.observe(img));

  // Back to top button
  const btn = document.createElement('button');
  btn.id = 'back-to-top';
  btn.textContent = '↑';
  document.body.appendChild(btn);
  window.addEventListener('scroll', () => btn.style.display = window.scrollY > 400 ? 'block' : 'none');
  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
});