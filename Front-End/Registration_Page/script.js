const loginFormContainer = document.getElementById("loginFormContainer");
const registerFormContainer = document.getElementById("registerFormContainer");
const message = document.getElementById("message");

// Show Login Form
function showLogin() {
  loginFormContainer.classList.remove("hidden");
  registerFormContainer.classList.add("hidden");
  message.classList.add("hidden");
}

// Show Register Form
function showRegister() {
  registerFormContainer.classList.remove("hidden");
  loginFormContainer.classList.add("hidden");
  message.classList.add("hidden");
}

// Register Handler
document.getElementById("registerForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const name = e.target[0].value;
  message.textContent = `✅ Welcome, ${name}! You have registered successfully.`;
  message.classList.remove("hidden");
});

// Login Handler
document.getElementById("loginForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const email = e.target[0].value;
  const name = email.split("@")[0];
  message.textContent = `✅ Welcome back, ${name}! Login successful.`;
  message.classList.remove("hidden");
});
