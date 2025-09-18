// Sidebar logic cu animatie smooth
document.addEventListener('DOMContentLoaded', function() {
  var sidebar = document.getElementById('filter-sidebar');
  var openBtn = document.getElementById('filter-button');
  var closeBtn = document.getElementById('close-sidebar');
  if (openBtn && sidebar) {
    openBtn.addEventListener('click', function() {
      sidebar.classList.add('open');
    });
  }
  if (closeBtn && sidebar) {
    closeBtn.addEventListener('click', function() {
      sidebar.classList.remove('open');
    });
  }
  document.addEventListener('click', function(e) {
    if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && e.target !== openBtn) {
      sidebar.classList.remove('open');
    }
  });
});
// Slider JS pentru galeria de imagini a fiecărui produs

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.slider-gallery').forEach(function(gallery) {
    const images = gallery.querySelectorAll('.slider-img');
    const prevBtn = gallery.querySelector('.slider-arrow.prev');
    const nextBtn = gallery.querySelector('.slider-arrow.next');
    let current = 0;
    if (images.length === 0) return;

    function showImage(idx) {
      images.forEach((img, i) => {
        img.classList.toggle('active', i === idx);
      });
    }

    prevBtn.addEventListener('click', function(e) {
      e.preventDefault();
      current = (current - 1 + images.length) % images.length;
      showImage(current);
    });
    nextBtn.addEventListener('click', function(e) {
      e.preventDefault();
      current = (current + 1) % images.length;
      showImage(current);
    });
    showImage(current);
  });
});
