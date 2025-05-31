function toggleForms() {
  const loginCard = document.getElementById("loginCard");
  const registerCard = document.getElementById("registerCard");

  if (loginCard.style.display === "none") {
    loginCard.style.display = "block";
    registerCard.style.display = "none";
  } else {
    loginCard.style.display = "none";
    registerCard.style.display = "block";
  }
}

function getUsers() {
  return JSON.parse(localStorage.getItem("users") || "[]");
}

function saveUser(user) {
  const users = getUsers();
  users.push(user);
  localStorage.setItem("users", JSON.stringify(users));
}

function getUsers() {
  return JSON.parse(localStorage.getItem("users") || "[]");
}

function saveUser(user) {
  const users = getUsers();
  users.push(user);
  localStorage.setItem("users", JSON.stringify(users));
}

function toggleForms() {
  const loginCard = document.getElementById("loginCard");
  const registerCard = document.getElementById("registerCard");
  if (loginCard.style.display === "none") {
    loginCard.style.display = "block";
    registerCard.style.display = "none";
  } else {
    loginCard.style.display = "none";
    registerCard.style.display = "block";
  }
}

function handleRegister() {
  const fullName = document.getElementById("regFullName").value.trim();
  const mobile = document.getElementById("regMobile").value.trim();
  const location = document.getElementById("regLocation").value.trim();
  const email = document.getElementById("regEmail").value.trim().toLowerCase();
  const password = document.getElementById("regPassword").value;

  if (!fullName || !mobile || !location || !email || !password) {
    alert("All fields are required.");
    return;
  }

  const users = getUsers();
  if (users.find(user => user.email === email)) {
    alert("User already registered. Please login.");
    toggleForms();
    return;
  }

  saveUser({ fullName, mobile, location, email, password });
  alert("Registration successful! Please login.");
  toggleForms();
}


function handleLogin() {
  const email = document.getElementById("loginEmail").value.trim().toLowerCase();
  const password = document.getElementById("loginPassword").value;

  if (!email || !password) {
    alert("All fields are required.");
    return;
  }

  const users = getUsers();
  const user = users.find(u => u.email === email);

  if (!user) {
    alert("User not found. Please register first!");
    return;
  }

  if (user.password !== password) {
    alert("Invalid credentials. Please try again.");
    return;
  }

  alert(`Welcome back, ${user.name}! Login successful.`);
  localStorage.setItem("loggedInUser", JSON.stringify(user));
  window.location.href = "index.html"; // Redirect to your main app page
}

// On your index.html or main page, add this to protect unauthorized access:
// window.onload = () => {
//   if (!localStorage.getItem("loggedInUser")) {
//     window.location.href = "login.html";
//   }
// }

window.onload = () => {
  const currentPage = window.location.pathname;

  if (
    !localStorage.getItem("loggedInUser") &&
    !currentPage.includes("login.html")
  ) {
    window.location.href = "login.html";
  }
};


// Navbar logout button script (on main pages):
document.getElementById("logoutBtn").addEventListener("click", function(e) {
  e.preventDefault();
  localStorage.removeItem("loggedInUser");
  window.location.href = "login.html";
});








// Toggle mobile menu

const menuToggle = document.getElementById('menuToggle');
const navLinks = document.getElementById('navLinks');

menuToggle.addEventListener('click', () => {
  navLinks.classList.toggle('active');
  menuToggle.classList.toggle('open'); // toggle hamburger animation

  // Accessibility: update aria-expanded attribute
  const expanded = menuToggle.getAttribute('aria-expanded') === 'true' || false;
  menuToggle.setAttribute('aria-expanded', !expanded);
});



// Optional: Highlight active link
const links = document.querySelectorAll('.nav-links a');
links.forEach(link => {
  link.addEventListener('click', () => {
    links.forEach(l => l.classList.remove('active'));
    link.classList.add('active');
  });
});

// Logout logic (customizable)
 document.addEventListener('DOMContentLoaded', function () {
  document.body.addEventListener('click', function (e) {
    if (e.target && e.target.id === 'logoutBtn') {
      e.preventDefault();
      alert('You have been logged out.');
      // Clear auth (if needed)
      localStorage.clear();
      sessionStorage.clear();
      // Redirect to login page
      window.location.href = 'index.html'; // or 'login.html'
    }
  });
});
