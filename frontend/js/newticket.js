document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('FormTicket');
  const previewGambar = document.getElementById('previewGambar');
  const loader = document.getElementById('loader');

  if (!form) {
    console.error('FormTicket tidak ditemukan!');
    return;
  }

  // Preview gambar saat upload
  document.getElementById('file').addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        previewGambar.src = e.target.result;
        previewGambar.style.display = 'block';
      };
      reader.readAsDataURL(file);
    } else {
      previewGambar.src = '';
      previewGambar.style.display = 'none';
    }
  });

  // Validasi form + submit ke backend + loader jalan
  form.addEventListener('submit', async function (e) {
    e.preventDefault();

    if (!form.checkValidity()) {
      e.stopPropagation();
      form.classList.add('was-validated');
      return;
    }

    showLoader();
    const formData = new FormData(form);

    try {
      const res = await fetch('http://127.0.0.1:8000/api/task/', {
        method: "POST",
        body: formData,
        headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
      });

      let data;
      let errorMsg = "Gagal kirim ticket";

      // Coba parse JSON, jika gagal tampilkan pesan error umum
      try {
        data = await res.json();
      } catch {
        data = null;
      }

      if (!res.ok) {
        errorMsg += data && data.detail ? ": " + data.detail : "";
        throw new Error(errorMsg);
      }

      showNotif(
        `Tiket berhasil dibuat!\n\nJudul: ${formData.get("judul")}\nStatus: ${formData.get("prioritas")}`,
        true
      );

      form.reset();
      form.classList.remove('was-validated');
      previewGambar.src = '';
      previewGambar.style.display = 'none';
    } catch (err) {
      console.error(err);
      showNotif(err.message, false);
    } finally {
      hideLoader();
    }
  });

  function showLoader() {
    loader.classList.remove('d-none');
  }

  function hideLoader() {
    loader.classList.add('d-none');
  }
});
