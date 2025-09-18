// Slider galerie imagini produs

document.addEventListener('DOMContentLoaded', function() {

  // Slider logic + color filter
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

    // Color select logic
    const colorDots = document.querySelectorAll('.color-dot[data-color]');
    colorDots.forEach(dot => {
      dot.addEventListener('click', function() {
        colorDots.forEach(d => d.classList.remove('selected'));
        dot.classList.add('selected');
        const color = dot.getAttribute('data-color');
        let found = false;
        images.forEach((img, i) => {
          if (img.dataset.color === color) {
            showImage(i);
            current = i;
            found = true;
          }
        });
        if (!found) {
          // fallback: show main image (data-color="")
          images.forEach((img, i) => {
            if (img.dataset.color === '') {
              showImage(i);
              current = i;
            }
          });
        }
      });
    });

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

  // Tab logic
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(tc => tc.style.display = 'none');
      btn.classList.add('active');
      const tabId = 'tab-' + btn.getAttribute('data-tab');
      document.getElementById(tabId).style.display = 'block';
    });
  });
});
