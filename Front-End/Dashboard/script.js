document.addEventListener("DOMContentLoaded", () => {
  const logoutBtn = document.getElementById('logoutBtn');

  if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => {
      e.preventDefault(); // Prevent the default anchor behavior
      console.log('Logout clicked!');

      alert('You have been logged out!');
      window.location.href = 'index.html'; // or 'login.html' if you have one
    });
  }

  
  const planningBtn = document.querySelector('.button-link');
  if (planningBtn) {
    planningBtn.addEventListener('click', () => {
      console.log('Planning page link clicked!');
    });
  }
});