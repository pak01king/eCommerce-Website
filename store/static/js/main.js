document.addEventListener("DOMContentLoaded", function() {
  const faders = document.querySelectorAll('.fade-in');
  const appearOptions = {
    threshold: 0.2,
    rootMargin: "0px 0px -50px 0px"
  };

  const appearOnScroll = new IntersectionObserver(function(entries, appearOnScroll) {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('appear');
      appearOnScroll.unobserve(entry.target);
    });
  }, appearOptions);

  faders.forEach(fader => {
    appearOnScroll.observe(fader);
  });
});

document.addEventListener('DOMContentLoaded', function() {
  // Selectare imagine slider la click pe culoare
  const colorLabels = document.querySelectorAll('.color-img-label');
  const sliderImages = document.querySelectorAll('.slider-img');
  const colorInputs = document.querySelectorAll('input[name="color"]');
  const addToCartForm = document.querySelector('.add-to-cart-form');

  colorLabels.forEach(label => {
    label.addEventListener('click', function() {
      const input = label.querySelector('input[type="radio"]');
      if (input) input.checked = true;
      const colorName = label.querySelector('.color-img').getAttribute('title').toLowerCase();
      let found = false;
      sliderImages.forEach(img => {
        if (img.dataset.color && img.dataset.color.toLowerCase() === colorName) {
          img.classList.add('active');
          found = true;
        } else {
          img.classList.remove('active');
        }
      });
      // Dacă nu există imagine cu data-color, afișează prima
      if (!found && sliderImages.length > 0) {
        sliderImages.forEach(img => img.classList.remove('active'));
        sliderImages[0].classList.add('active');
      }
    });
  });

  // Adaugă culoarea selectată în formularul de adăugare în coș
  if (addToCartForm) {
    addToCartForm.addEventListener('submit', function(e) {
      const selectedColor = [...colorInputs].find(input => input.checked);
      if (selectedColor) {
        let hidden = addToCartForm.querySelector('input[name="selected_color"]');
        if (!hidden) {
          hidden = document.createElement('input');
          hidden.type = 'hidden';
          hidden.name = 'selected_color';
          addToCartForm.appendChild(hidden);
        }
        hidden.value = selectedColor.value;
      }
    });
  }
});