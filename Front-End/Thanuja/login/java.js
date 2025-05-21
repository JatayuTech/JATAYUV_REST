
const getUsers = () => JSON.parse(localStorage.getItem("users") || "[]");

const saveUser = (user) => {
  const users = getUsers();
  users.push(user);
  localStorage.setItem("users", JSON.stringify(users));
};


function toggleForms() {
  const loginCard    = document.getElementById("loginCard");
  const registerCard = document.getElementById("registerCard");

  const loginVisible = loginCard.style.display !== "none";
  loginCard.style.display    = loginVisible ? "none"  : "block";
  registerCard.style.display = loginVisible ? "block" : "none";
}


function handleRegister() {
  const fullName = document.getElementById("regFullName").value.trim();
  const mobile   = document.getElementById("regMobile").value.trim();
  const location = document.getElementById("regLocation").value.trim();
  const email    = document.getElementById("regEmail").value.trim().toLowerCase();
  const password = document.getElementById("regPassword").value;

  if (!fullName || !mobile || !location || !email || !password) {
    alert("All fields are required.");
    return;
  }

  if (getUsers().some(u => u.email === email)) {
    alert("User already registered. Please login.");
    toggleForms();
    return;
  }

  saveUser({ fullName, mobile, location, email, password });
  alert("Registration successful. Please login.");
  toggleForms();
}

//LOGIN
function handleLogin() {
  const email    = document.getElementById("loginEmail").value.trim().toLowerCase();
  const password = document.getElementById("loginPassword").value;

  if (!email || !password) {
    alert("All fields are required.");
    return;
  }

  const user = getUsers().find(u => u.email === email);

  if (!user) {
    alert("User not found. Please register first.");
    return;
  }
  if (user.password !== password) {
    alert("Invalid credentials. Please try again.");
    return;
  }

  alert(`Welcome back, ${user.fullName}! Login successful.`);
  localStorage.setItem("loggedInUser", JSON.stringify(user));
  window.location.href = "index.html";   
}


document.addEventListener("DOMContentLoaded", () => {

  const isAuthPage      = window.location.pathname.includes("login.html");
  const loggedInAlready = !!localStorage.getItem("loggedInUser");

  if (!loggedInAlready && !isAuthPage) {
    window.location.href = "login.html";
  }

  
  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", (e) => {
      e.preventDefault();
      localStorage.removeItem("loggedInUser");
      window.location.href = "login.html";
    });
  }
});
