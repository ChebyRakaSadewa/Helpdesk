// export ke excel dan word
  function exportToExcel() {
    const table = document.querySelector("table");
    const wb = XLSX.utils.table_to_book(table, { sheet: "Tickets" });
    XLSX.writeFile(wb, "tickets.xlsx");
  }

  function exportToWord() {
    const table = document.querySelector("table").outerHTML;
    const html = `
      <html xmlns:o='urn:schemas-microsoft-com:office:office'
            xmlns:w='urn:schemas-microsoft-com:office:word'
            xmlns='http://www.w3.org/TR/REC-html40'>
        <head><meta charset='utf-8'><title>Export HTML To Word</title></head>
        <body>${table}</body>
      </html>`;

    const blob = new Blob(['\ufeff', html], { type: 'application/msword' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'tickets.doc';
    link.click();
  }
// akhir dari export

<!-- Komentar -->
<hr>
<h6>Komentar</h6>
<div id="comments-list" style="max-height:150px;overflow-y:auto;"></div>
<form id="commentForm" class="mt-2">
  <div class="input-group">
    <input type="text" class="form-control" id="commentInput" placeholder="Tulis komentar..." required>
    <button class="btn btn-primary" type="submit">Kirim</button>
  </div>
</form>
