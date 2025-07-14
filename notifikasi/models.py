# notifikasi/models.py
from django.db import models
from django.contrib.auth import get_user_model
from Tiket.models import Tiket  # Asumsikan model Tiket ada di app tiket

class Notification(models.Model):
    NOTIFICATION_TYPES_USER = (
        ('ticket_created', 'Tiket berhasil dikirim'),
        ('ticket_failed', 'Tiket tidak berhasil dikirim'),
        ('ticket_updated', 'Tiket berhasil diperbarui'),
        ('ticket_in_progress', 'Tiket dalam in progress'),
        ('ticket_completed', 'Tiket selesai'),
        ('password_updated', 'Password berhasil diperbarui'),
        ('profile_updated', 'Profile berhasil diperbarui'),
    )

    NOTIFICATION_TYPES_ADMIN = (
        ('ticket_created', 'Tiket berhasil dikirim'),
        ('ticket_failed', 'Tiket tidak berhasil dikirim'),
        ('ticket_updated', 'Tiket berhasil diperbarui'),
        ('ticket_in_progress', 'Tiket dalam in progress'),
        ('ticket_completed', 'Tiket selesai'),
        ('password_updated', 'Password berhasil diperbarui'),
        ('profile_updated', 'Profile berhasil diperbarui'),
        ('user_updated', 'Data user berhasil diperbarui'),
        ('user_created', 'User berhasil ditambahkan'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Pengguna yang menerima notifikasi
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES_USER + NOTIFICATION_TYPES_ADMIN)  # Jenis notifikasi
    content_object = models.ForeignKey(Tiket, on_delete=models.CASCADE, null=True, blank=True)  # Jika terkait dengan tiket
    message = models.CharField(max_length=255)  # Pesan notifikasi
    is_read = models.BooleanField(default=False)  # Status apakah notifikasi sudah dibaca
    created_at = models.DateTimeField(auto_now_add=True)  # Waktu notifikasi dibuat

    def __str__(self):
        return f"Notifikasi untuk {self.user.email}: {self.message}"
