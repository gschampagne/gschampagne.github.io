document.addEventListener('DOMContentLoaded', () => {
  const gallery = document.querySelector('.image-gallery');
  const images = gallery.querySelectorAll('img');

  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const captionText = document.getElementById('caption');
  const closeBtn = document.querySelector('.lightbox .close');

  // Wrap each image in a <a> tag dynamically
  images.forEach(img => {
    const wrapper = document.createElement('a');
    wrapper.href = img.src;
    wrapper.dataset.caption = img.alt || '';
    img.parentNode.insertBefore(wrapper, img);
    wrapper.appendChild(img);

    // Click opens lightbox
    wrapper.addEventListener('click', e => {
      e.preventDefault();
      lightbox.style.display = 'block';
      lightboxImg.src = wrapper.href;
      captionText.textContent = wrapper.dataset.caption;
    });
  });

  // Close lightbox
  closeBtn.addEventListener('click', () => {
    lightbox.style.display = 'none';
  });

  // Close on clicking outside image
  lightbox.addEventListener('click', e => {
    if (e.target === lightbox) lightbox.style.display = 'none';
  });

  // Close on ESC key
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') lightbox.style.display = 'none';
  });
});
