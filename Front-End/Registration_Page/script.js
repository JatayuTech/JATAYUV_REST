document.getElementById('registerForm').addEventListener('submit', function(event) {
  event.preventDefault();
  alert("Registration successful!");
  window.location.href = "login.html";  // Redirects to login page
});
