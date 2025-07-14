let allUsers = [];
let currentTab = 'members';

function renderUsers(users) {
  document.getElementById('total-admin').textContent = allUsers.filter(u => u.is_admin).length;
  document.getElementById('total-user').textContent = allUsers.filter(u => !u.is_admin).length;

  const tableBody = document.getElementById('user-table-body');
  tableBody.innerHTML = '';

  users.forEach(user => {
    tableBody.innerHTML += `
      <tr>
        <td><img class="profile-img" src="${user.foto_url || ''}" alt=""></td>
        <td>${user.nama_lengkap || '-'}</td>
        <td>${user.no_hp || '-'}</td>
        <td>${user.email || '-'}</td>
        <td>
          <span class="${user.is_admin ? 'status-active' : 'status-inactive'}">
            ${user.is_admin ? 'Admin' : 'User'}
          </span>
        </td>
        <td class="operation-icons">
          <i class="fas fa-eye text-info view-btn" data-id="${user.id}"></i>
          <i class="fas fa-edit text-primary edit-btn" data-id="${user.id}"></i>
          <i class="fas fa-trash text-danger delete-btn" data-id="${user.id}"></i>
        </td>
        <td><button class="btn btn-sm btn-primary">Login</button></td>
      </tr>
    `;
  });

  addEventListeners();
}

function switchTab(tab) {
  currentTab = tab;
  document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
  document.querySelector(`.tab-button[onclick="switchTab('${tab}')"]`).classList.add('active');
  document.getElementById('section-title').textContent = tab.charAt(0).toUpperCase() + tab.slice(1);

  let filtered = [];
  if (tab === 'members') {
    filtered = allUsers.filter(u => !u.is_admin);
  } else if (tab === 'admins') {
    filtered = allUsers.filter(u => u.is_admin);
  }
  renderUsers(filtered);
}

function loadUsers() {
  fetch('http://127.0.0.1:8000/api/users/', {
    headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
  })
    .then(res => res.json())
    .then(data => {
      allUsers = Array.isArray(data) ? data : (data.results || []);
      switchTab(currentTab);
    });
}

document.addEventListener('DOMContentLoaded', function () {
  const params = new URLSearchParams(window.location.search);
  const type = params.get('type') || 'members';
  currentTab = type;
  loadUsers();
});

const accessToken = localStorage.getItem('access_token');

// Submit form add/edit user
document.getElementById('addUserForm').addEventListener('submit', function (e) {
  e.preventDefault();
  const form = e.target;
  const formData = new FormData(form);
  const userId = form.querySelector('[name="id"]')?.value;

  // Ubah is_admin ke boolean string
  if (formData.has('is_admin')) {
    formData.set('is_admin', formData.get('is_admin') === 'true');
  }

  // Jangan kirim password/foto kosong saat edit
  if (userId && !form.password.value) formData.delete('password');
  if (userId && !form.foto.value) formData.delete('foto');

  const url = userId
    ? `http://127.0.0.1:8000/api/users/${userId}/`
    : 'http://127.0.0.1:8000/api/register/';
  const method = userId ? 'PATCH' : 'POST';

  fetch(url, {
    method: method,
    headers: {
      'Authorization': `Bearer ${accessToken}`
    },
    body: formData
  })
    .then(res => res.json().then(data => ({status: res.status, body: data})))
    .then(({status, body}) => {
      if (status === 200 || status === 201) {
        alert('User berhasil disimpan!');
        form.reset();
        form.querySelector('[name="id"]')?.remove();
        const modalEl = document.getElementById('addUserModal');
        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.hide();
        loadUsers();
      } else {
        alert('Gagal menyimpan user!');
        console.error(body);
      }
    })
    .catch(error => {
      alert('Terjadi kesalahan saat menyimpan!');
      console.error(error);
    });
});

// Untuk buka modal Add
document.getElementById('addUserBtn').addEventListener('click', function () {
  const form = document.getElementById('addUserForm');
  form.reset();
  form.querySelector('[name="id"]')?.remove();
  const modalEl = document.getElementById('addUserModal');
  const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
  modal.show();
});

function addEventListeners() {
  // Edit
  document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.onclick = function () {
      const userId = this.dataset.id;
      fetch(`http://127.0.0.1:8000/api/users/${userId}/`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
      })
        .then(res => res.json())
        .then(data => {
          const form = document.getElementById('addUserForm');
          form.nama_lengkap.value = data.nama_lengkap || '';
          form.email.value = data.email || '';
          form.no_hp.value = data.no_hp || '';
          form.kantor_cabang.value = data.kantor_cabang || '';
          form.is_admin.value = data.is_admin ? "true" : "false";
          form.jabatan.value = data.jabatan || '';
          form.password.value = '';
          form.gender.value = data.gender || '';
          let hiddenInput = form.querySelector('[name="id"]');
          if (!hiddenInput) {
            hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = 'id';
            form.appendChild(hiddenInput);
          }
          hiddenInput.value = data.id;
          const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('addUserModal'));
          modal.show();
        });
    };
  });

  // Delete
  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.onclick = function () {
      const userId = this.dataset.id;
      if (confirm("Yakin mau hapus data ini?")) {
        fetch(`http://127.0.0.1:8000/api/users/${userId}/`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        })
          .then(res => {
            if (res.ok) {
              alert('User berhasil dihapus!');
              loadUsers();
            } else {
              alert('Gagal hapus user!');
            }
          });
      }
    };
  });

  // View
  document.querySelectorAll('.view-btn').forEach(btn => {
    btn.onclick = function () {
      const userId = this.dataset.id;
      fetch(`http://127.0.0.1:8000/api/users/${userId}/`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
      })
        .then(res => res.json())
        .then(data => {
          const html = `
            <p><strong>Email:</strong> ${data.email}</p>
            <p><strong>No HP:</strong> ${data.no_hp}</p>
            <p><strong>Jabatan:</strong> ${data.jabatan}</p>
            <p><strong>Status:</strong> ${data.is_admin ? 'Admin' : 'User'}</p>
          `;
          document.getElementById('viewUserContent').innerHTML = html;
          const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('viewUserModal'));
          modal.show();
        });
    };
  });
}

// Tambahkan validasi untuk password
document.getElementById('addUserForm').addEventListener('submit', function (e) {
  e.preventDefault();
  const form = e.target;
  const formData = new FormData(form);
  const userId = form.querySelector('[name="id"]')?.value;

  // Ubah is_admin ke boolean string
  if (formData.has('is_admin')) {
    formData.set('is_admin', formData.get('is_admin') === 'true');
  }

  // Jangan kirim password/foto kosong saat edit
  if (userId && !form.password.value) formData.delete('password');
  if (userId && !form.foto.value) formData.delete('foto');

  // Password wajib diisi saat add user
  if (!userId && !form.password.value) {
    alert('Password wajib diisi untuk user baru!');
    form.password.focus();
    return;
  }

  const url = userId
    ? `http://127.0.0.1:8000/api/users/${userId}/`
    : 'http://127.0.0.1:8000/api/register/';
  const method = userId ? 'PATCH' : 'POST';

  fetch(url, {
    method: method,
    headers: {
      'Authorization': `Bearer ${accessToken}`
    },
    body: formData
  })
    .then(res => res.json().then(data => ({status: res.status, body: data})))
    .then(({status, body}) => {
      if (status === 200 || status === 201) {
        alert('User berhasil disimpan!');
        form.reset();
        form.querySelector('[name="id"]')?.remove();
        const modalEl = document.getElementById('addUserModal');
        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.hide();
        loadUsers();
      } else {
        alert('Gagal menyimpan user!');
        console.error(body);
      }
    })
    .catch(error => {
      alert('Terjadi kesalahan saat menyimpan!');
      console.error(error);
    });
});