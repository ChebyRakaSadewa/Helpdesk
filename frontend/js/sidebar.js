// Toggle sidebar untuk mobile
document.getElementById('sidebarCollapseMobile')?.addEventListener('click', function () {
    document.getElementById('sidebar').classList.toggle('active');
});

// Toggle sidebar untuk desktop (kalau dipakai juga)
document.getElementById('sidebarCollapse')?.addEventListener('click', function () {
    document.getElementById('sidebar').classList.toggle('active');
});
