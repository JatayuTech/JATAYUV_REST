document.querySelector('.button-link').addEventListener('click', (event) => {
  // Optional: Prevent default navigation if you want to do something else first
  // event.preventDefault();

  console.log('Planning page link clicked!');
});

document.addEventListener("DOMContentLoaded", () => {
  const planningBtn = document.querySelector('.button-link');
  if (planningBtn) {
    planningBtn.addEventListener('click', () => {
      console.log('Planning page link clicked!');
    });
  }
});
