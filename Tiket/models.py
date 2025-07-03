from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import timedelta, localtime
import holidays
from datetime import datetime, time

PRIORITAS_PILIHAN = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]

class Tiket(models.Model):
    judul = models.CharField(max_length=255)
    deskripsi = models.TextField()
    prioritas = models.CharField(max_length=10, choices=PRIORITAS_PILIHAN, default='low')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    sla = models.DateTimeField(null=True, blank=True)
    waktu_dibuat = models.DateTimeField(auto_now_add=True)
    waktu_diperbarui = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=50,
        choices=[('new', 'New'), ('in_progress', 'In Progress'), ('completed', 'Completed')],
        default='new'
    )
    file = models.FileField(upload_to='unggahan/', blank=True, null=True)
    cabang = models.CharField(max_length=100, default='-')
    jabatan = models.CharField(max_length=100, default='-')

    def simpan(self, *args, **kwargs):
        """
        Hitung otomatis SLA saat tiket dibuat, 
        memperhitungkan prioritas, hari libur, dan jam kerja.
        """
        if not self.sla:
            waktu_buat = localtime()
            libur_indonesia = holidays.Indonesia(years=waktu_buat.year)
            weekend = waktu_buat.weekday() >= 5
            libur = waktu_buat.date() in libur_indonesia
            luar_jamkerja = not (time(8, 30) <= waktu_buat.time() <= time(17, 30))

            # Hitung waktu dasar SLA berdasarkan prioritas
            if self.prioritas == 'high':
                hari_sla = 1
            elif self.prioritas == 'medium':
                hari_sla = 3
            else:
                hari_sla = 7

            # Jika di luar jam kerja/libur, mulai dari hari kerja berikutnya
            if weekend or libur or luar_jamkerja:
                waktu_mulai = self.waktu_kerja_berikutnya(waktu_buat)
            else:
                waktu_mulai = waktu_buat

            self.sla = waktu_mulai + timedelta(days=hari_sla)

        super().save(*args, **kwargs)

    def waktu_kerja_berikutnya(self, current):
        """
        Cari waktu kerja terdekat (weekday, bukan tanggal merah, dan jam 08:30)
        """
        libur_indonesia = holidays.Indonesia(years=current.year)
        hari_berikutnya = current
        while True:
            hari_berikutnya += timedelta(days=1)
            if hari_berikutnya.weekday() < 5 and hari_berikutnya.date() not in libur_indonesia:
                return datetime.combine(hari_berikutnya.date(), time(8, 30)).astimezone(current.tzinfo)

    def email_admin(self):
        """
        Ambil daftar email semua user yang is_admin=True.
        """
        User = get_user_model()
        return list(User.objects.filter(is_admin=True).values_list('email', flat=True))

class Komentar(models.Model):
    tiket = models.ForeignKey(Tiket, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    isi = models.TextField()
    waktu_dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Komentar oleh {self.user.nama_lengkap} pada {self.tiket.judul}"
