// JS pentru cart UX: editare cantitate, actualizare total (frontend only)

document.addEventListener('DOMContentLoaded', function() {
  // Actualizare total linie și total general (frontend, nu salvează în backend)
  function recalcCartTotals() {
    let total = 0;
    document.querySelectorAll('.cart-item-card').forEach(function(card) {
      const qtyInput = card.querySelector('.cart-qty-input');
      const price = parseFloat(card.querySelector('.cart-item-price').textContent.replace(/[^\d.]/g, ''));
      const lineTotal = qtyInput.value * price;
      card.querySelector('.cart-line-total').textContent = lineTotal.toFixed(2);
      total += lineTotal;
    });
    const totalElem = document.querySelector('.cart-total-value');
    if (totalElem) totalElem.textContent = total.toFixed(2) + ' RON';
  }

  document.querySelectorAll('.cart-qty-input').forEach(function(input) {
    input.addEventListener('change', function() {
      if (parseInt(input.value) < 1) input.value = 1;
      recalcCartTotals();
      // Aici poți adăuga un request AJAX pentru a salva cantitatea în backend
    });
  });

  // Poți adăuga confirmare la ștergere produs
  document.querySelectorAll('.cart-remove-btn').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      if (!confirm('Sigur vrei să elimini acest produs din coș?')) {
        e.preventDefault();
      }
    });
  });
});
