// Data awal cabang
let dataCabang = [
  {
    nama: "Kantor Jakarta",
    pic: "item",
    pimpinan: "Dewi Sartika",
    waktu: "08.00 - 16.00",
    status: "On Site",
    petugas: [],
    kapasitas: 5,
    gambar: "https://i.imgur.com/MsRJzQy.jpeg",
    alamat: "Jl. Sudirman No. 10, Jakarta",
    maps: "https://www.google.com/maps/embed?pb=!1m18..."
  }
];

const branchList = document.getElementById("branchList");
const searchInput = document.getElementById("searchInput");
const modal = document.getElementById("modalCabang");
const addBranchBtn = document.getElementById("addBranchBtn");
const closeModal = document.getElementById("closeModal");
const formCabang = document.getElementById("formCabang");
const modalTitle = document.getElementById("modalTitle");

const modalDetail = document.getElementById("modalDetail");
const closeDetail = document.getElementById("closeDetail");
const detailNama = document.getElementById("detailNama");
const detailPimpinan = document.getElementById("detailPimpinan");
const detailGambar = document.getElementById("detailGambar");
const detailAlamat = document.getElementById("detailAlamat");
const detailMaps = document.getElementById("detailMaps");

let editingIndex = null;

function renderCabang(data) {
  branchList.innerHTML = "";
  data.forEach((cabang, index) => {
    const jumlah = cabang.petugas.length;
    const kapasitas = cabang.kapasitas;
    const persen = Math.round((jumlah / kapasitas) * 100);

    const card = document.createElement("div");
    card.className = "card";
    card.onclick = () => showDetail(cabang);
    card.innerHTML = `
      <div class="header-card">
        <div><small>${cabang.waktu}</small></div>
        <div class="status">${cabang.status}</div>
      </div>
      <div class="info">
        <h3>${cabang.nama}</h3>
        <p>PIC: ${cabang.pic}</p>
      </div>
      <div class="footer">
        <div class="progress-bar">
          <div class="progress-fill" style="width:${persen}%"></div>
        </div>
        <div class="capacity">${jumlah}/${kapasitas}</div>
      </div>
      <div class="actions">
        <button onclick="event.stopPropagation(); editCabang(${index})">Edit</button>
        <button onclick="event.stopPropagation(); hapusCabang(${index})">Hapus</button>
      </div>
    `;
    branchList.appendChild(card);
  });
}

searchInput.addEventListener("input", () => {
  const keyword = searchInput.value.toLowerCase();
  const filtered = dataCabang.filter(c => c.nama.toLowerCase().includes(keyword));
  renderCabang(filtered);
});

addBranchBtn.onclick = () => {
  modalTitle.textContent = "Tambah Cabang Baru";
  modal.style.display = "flex";
  editingIndex = null;
  formCabang.reset();
};

closeModal.onclick = () => {
  modal.style.display = "none";
};
closeDetail.onclick = () => {
  modalDetail.style.display = "none";
};

window.onclick = (event) => {
  if (event.target === modal) modal.style.display = "none";
  if (event.target === modalDetail) modalDetail.style.display = "none";
};

formCabang.onsubmit = async function (e) {
  e.preventDefault();

  const nama = document.getElementById("namaCabang").value;
  const pic = document.getElementById("picCabang").value;
  const waktu = document.getElementById("jamCabang").value;
  const kapasitas = parseInt(document.getElementById("kapasitasCabang").value);
  const pimpinan = document.getElementById("pimpinanCabang").value;
  const alamat = document.getElementById("alamatCabang").value;
  const gambar = document.getElementById("gambarCabang").value;
  const maps = document.getElementById("mapsCabang").value;

  const newCabang = {
    nama,
    pic,
    waktu,
    status: "On Site",
    petugas: [],
    kapasitas,
    pimpinan,
    alamat,
    gambar,
    maps
  };

  try {
    const res = await fetch("http://localhost:8000/api/cabang/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // tambahin Authorization token kalau perlu login
      },
      body: JSON.stringify(newCabang)
    });

    if (!res.ok) throw new Error("Gagal menyimpan data");

    const result = await res.json();

    showNotif("Cabang berhasil ditambahkan ✅", true);
    modal.style.display = "none";
    formCabang.reset();

    // Optional: Tambahin cabang langsung ke list lokal juga biar nggak nunggu reload
    dataCabang.push(newCabang);
    renderCabang(dataCabang);
  } catch (err) {
    console.error(err);
    showNotif("Gagal menyimpan cabang ❌", false);
  }
};


function editCabang(index) {
  const cabang = dataCabang[index];
  editingIndex = index;
  modalTitle.textContent = "Edit Cabang";
  document.getElementById("namaCabang").value = cabang.nama;
  document.getElementById("picCabang").value = cabang.pic;
  document.getElementById("jamCabang").value = cabang.waktu;
  document.getElementById("kapasitasCabang").value = cabang.kapasitas;
  document.getElementById("pimpinanCabang").value = cabang.pimpinan;
  document.getElementById("alamatCabang").value = cabang.alamat;
  document.getElementById("gambarCabang").value = cabang.gambar;
  document.getElementById("mapsCabang").value = cabang.maps;
  modal.style.display = "flex";
}

function hapusCabang(index) {
  if (confirm("Yakin ingin menghapus cabang ini?")) {
    dataCabang.splice(index, 1);
    renderCabang(dataCabang);
  }
}

function showDetail(cabang) {
  detailNama.textContent = cabang.nama;
  detailPimpinan.textContent = cabang.pimpinan;
  detailAlamat.textContent = cabang.alamat;
  detailGambar.src = cabang.gambar;
  detailMaps.src = cabang.maps;
  modalDetail.style.display = "flex";
}

renderCabang(dataCabang);