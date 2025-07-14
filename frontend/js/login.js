document.getElementById('loginForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();
  const message = document.getElementById('message');

  fetch('http://127.0.0.1:8000/api/login/', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: email,
      password: password
    })
  })
  .then(async (response) => {
    if (!response.ok) {
      // Ambil error message dari response JSON jika ada
      const errorData = await response.json();
      throw new Error(errorData.detail || "Email atau Password salah");
    }
    return response.json();
  })
  .then(data => {
    // Simpan access token dan user info ke localStorage (atau sesuaikan)
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('user', JSON.stringify(data.user));
    localStorage.setItem("isLoggedIn", "true");

    setTimeout(() => {
    if (data.user.is_admin) {
      // Kalau admin, redirect ke halaman admin
      window.location.href = 'dashboard_admin.html';  
    } else {
      // Kalau bukan admin, redirect ke halaman user biasa
      window.location.href = 'dashboard_admin.html';
    }
  }, 1500);
  })
  .catch(error => {
    console.error('Login error:', error);
    message.innerHTML = `<div class="alert alert-danger">${error.message}</div>`;
  });
});
