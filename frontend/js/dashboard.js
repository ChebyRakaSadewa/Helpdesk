$(document).ready(function () {
  // Inisialisasi dropdown Bootstrap
  var dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'));
  var dropdownList = dropdownElementList.map(function (dropdownToggleEl) {
    return new bootstrap.Dropdown(dropdownToggleEl);
  });
  // Handle resize event untuk responsive behavior
  $(window).resize(function () {
    if ($(window).width() >= 992) {
      $('#sidebar').removeClass('active');
    }
  });
});



// ini buat fitur search 
// Buat nyambungin ke backend Django nanti
document.getElementById('searchForm').addEventListener('submit', function (e) {
  e.preventDefault(); // Biar nggak reload
  const query = document.getElementById('searchInput').value;

  // Ganti URL di sini ke endpoint Django 
  // const apiUrl = `/api/search/?q=${encodeURIComponent(query)}`;

  fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      console.log('Hasil dari Django:', data);
      // Lo bisa lanjut render hasilnya di halaman
    })
    .catch(error => {
      console.error('Error:', error);
    });
});

// ini kalo pake metode POST 
fetch(apiUrl, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: query })
})
//   akhir dari search



// ini buat konekin foto profil
// ini kalo mau udah mau di hubungin ke djanggo 
// fetch('/api/user-profile')
//   .then(res => res.json())
//   .then(userData => {
//     document.getElementById('modalUserName').textContent = userData.nama;
//     document.getElementById('modalJabatan').textContent = userData.jabatan;
//     document.getElementById('modalKantor').textContent = userData.kantor;
//     document.getElementById('modalUmur').textContent = userData.umur;
//     document.getElementById('modalGender').textContent = userData.gender;
//     document.getElementById('modalProfileImg').src = userData.foto;
//   });

// ini akhir dari profil




// ini untuk fungsi email ngambil data 
fetch('/api/email-check/')
  .then(res => res.json())
  .then(data => {
    const badge = document.getElementById('emailNotifBadge');
    if (data.adaEmailBaru) {
      badge.classList.remove('d-none');
    } else {
      badge.classList.add('d-none');
    }
  });
  // akhir



  // buat loadpage


function loadPage(page) {
  const content = document.getElementById('main-content');

  content.classList.add('fade-out');

  setTimeout(() => {
    fetch(`${page}.html`)
      .then(res => res.text())
      .then(html => {
        content.innerHTML = html;
        content.classList.remove('fade-out');
        content.classList.add('fade-in');

        // Kalau ada fungsi JS yang harus di-reinit tiap halaman, taruh di sini
        // contoh:
        // reinitCharts();
        // reinitEventListeners();
      });
  }, 200);
}

// Tambahkan kode ini di bagian yang sesuai setelah data tiket berhasil diambil
(Array.isArray(data) ? data : data.results || []).forEach(ticket => {
  const nama = ticket.user?.nama_lengkap || "User";
  const bagian = ticket.user?.bagian || "-";
  const pesan = ticket.content || "";
  const foto = ticket.user?.foto || "img/user1.jpg";
  // ...
});
