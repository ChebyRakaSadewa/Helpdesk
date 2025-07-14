from django.db import models
from django.contrib.auth.models import AbstractUser

class Customuser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    nama_lengkap = models.CharField(max_length=150, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    jabatan = models.CharField(max_length=100, blank=True, null=True)
    foto = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    no_hp = models.CharField(max_length=15, blank=True, null=True)
    kantor_cabang = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('L', 'Laki-laki'), ('P', 'Perempuan')],
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.nama_lengkap or self.email
