from django.db import models
from django.contrib.auth.models import AbstractUser

class Customuser(AbstractUser):
    fullname = models.CharField(max_length=150, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    divisi = models.CharField(max_length=100, blank=True, null=True)
    jabatan = models.CharField(max_length=100, blank=True, null=True)
    foto = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    no_hp = models.CharField(max_length=15, blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    office_branch = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('L', 'Laki-laki'), ('P', 'Perempuan')],
        blank=True,
        null=True
    )
    ttl = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username
