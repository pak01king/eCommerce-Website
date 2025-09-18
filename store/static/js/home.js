document.addEventListener("DOMContentLoaded", function() {
    const section = document.querySelector('.herohero-watch-container');

    function checkVisibility() {
        const rect = section.getBoundingClientRect();
        const windowHeight = window.innerHeight;

        // dacă secțiunea este vizibilă pe ecran
        if (rect.top < windowHeight - 100 && rect.bottom > 100) {
            section.classList.add('show');
        } else {
            section.classList.remove('show');
        }
    }

    window.addEventListener('scroll', checkVisibility);
    checkVisibility(); // verificare inițială
});
