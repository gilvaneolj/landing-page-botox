import './style.css'
import './mobile_overrides.css'

// Landing page logic initialized.

// Optional: Smooth scroll or other small interactions
// Optional: Smooth scroll or other small interactions
// Buttons are now linked directly in HTML to Checkout
document.querySelectorAll('.cta-button').forEach(button => {
  // Logic removed to allow direct link navigation
});

// FAQ Accordion Luxury Logic
document.querySelectorAll('.accordion-trigger-luxury').forEach(button => {
  button.addEventListener('click', () => {
    const accordionItem = button.parentElement;
    const content = accordionItem.querySelector('.accordion-content-luxury');
    const isActive = accordionItem.classList.contains('active');

    // Close other open items
    document.querySelectorAll('.accordion-item-luxury').forEach(item => {
      if (item !== accordionItem) {
        item.classList.remove('active');
        item.querySelector('.accordion-content-luxury').style.maxHeight = null;
      }
    });

    // Toggle current item
    if (!isActive) {
      accordionItem.classList.add('active');
      content.style.maxHeight = content.scrollHeight + "px";
    } else {
      accordionItem.classList.remove('active');
    }
  });
});

// Midnight Countdown Timer Logic
function updateMidnightTimer() {
  const now = new Date();
  const midnight = new Date();
  midnight.setHours(24, 0, 0, 0); // Next midnight

  const diff = midnight - now;

  if (diff <= 0) {
    // Reset if it passes midnight (for consistency if page stays open)
    document.getElementById('timer-hours').innerText = '00';
    document.getElementById('timer-minutes').innerText = '00';
    document.getElementById('timer-seconds').innerText = '00';
    return;
  }

  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((diff % (1000 * 60)) / 1000);

  document.getElementById('timer-hours').innerText = hours.toString().padStart(2, '0');
  document.getElementById('timer-minutes').innerText = minutes.toString().padStart(2, '0');
  document.getElementById('timer-seconds').innerText = seconds.toString().padStart(2, '0');
}

// Start timer if elements exist
if (document.getElementById('midnight-timer')) {
  updateMidnightTimer();
  setInterval(updateMidnightTimer, 1000);
}

