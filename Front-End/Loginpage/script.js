/* ─────────── Local-storage helpers ─────────── */
const getUsers = () => JSON.parse(localStorage.getItem("users") || "[]");
const saveUser = (user) => {
  const users = getUsers();
  users.push(user);
  localStorage.setItem("users", JSON.stringify(users));
};

/* ─────────── UI helper ─────────── */
function showMessage(id, text, type) {
  const box = document.getElementById(id);
  box.className = `message ${type}`;     // .message + .success | .error
  box.textContent = text;
  box.classList.remove("hidden");
}

/* ─────────── Form toggling ─────────── */
function toggleForms() {
  const login  = document.getElementById("loginCard");
  const reg    = document.getElementById("registerCard");
  const showLogin = login.style.display === "none";

  login.style.display = showLogin ? "block" : "none";
  reg.style.display   = showLogin ? "none"  : "block";

  // clear any previous messages
  ["loginMessage", "registerMessage"].forEach(id =>
    document.getElementById(id).classList.add("hidden")
  );
}

/* ─────────── REGISTER ─────────── */
function handleRegister() {
  const fullName = document.getElementById("regFullName").value.trim();
  const mobile   = document.getElementById("regMobile").value.trim();
  const location = document.getElementById("regLocation").value.trim();
  const email    = document.getElementById("regEmail").value.trim().toLowerCase();
  const password = document.getElementById("regPassword").value;

  const msgId = "registerMessage";

  if (!fullName || !mobile || !location || !email || !password) {
    showMessage(msgId, "All fields are required.", "error");
    return;
  }

  if (getUsers().some(u => u.email === email)) {
    showMessage(msgId, "User already registered. Please login.", "error");
    setTimeout(toggleForms, 1500);   // switch to login after 1.5 s
    return;
  }

  saveUser({ fullName, mobile, location, email, password });
  showMessage(msgId, "✅ Registration successful. Please login.", "success");
  setTimeout(toggleForms, 1500);     // switch to login after 1.5 s
}

/* ─────────── LOGIN ─────────── */
function handleLogin() {
  const email    = document.getElementById("loginEmail").value.trim().toLowerCase();
  const password = document.getElementById("loginPassword").value;
  const msgId    = "loginMessage";

  if (!email || !password) {
    showMessage(msgId, "All fields are required.", "error");
    return;
  }

  const user = getUsers().find(u => u.email === email);
  if (!user) {
    showMessage(msgId, "User not found. Please register first.", "error");
    return;
  }
  if (user.password !== password) {
    showMessage(msgId, "Invalid credentials. Please try again.", "error");
    return;
  }

  localStorage.setItem("loggedInUser", JSON.stringify(user));
  showMessage(msgId, `✅ Welcome back, ${user.fullName}! Login successful.`, "success");
  // No redirect – stays on the same page
}

/* ─────────── Basic auth-guard & logout ─────────── */
document.addEventListener("DOMContentLoaded", () => {
  const onAuthPage = window.location.pathname.includes("login.html");
  const loggedIn   = !!localStorage.getItem("loggedInUser");

  if (!loggedIn && !onAuthPage) {
    window.location.href = "login.html";
  }

  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", e => {
      e.preventDefault();
      localStorage.removeItem("loggedInUser");
      window.location.href = "login.html";
    });
  }
});
