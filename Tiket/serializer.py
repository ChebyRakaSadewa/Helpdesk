from rest_framework import serializers
from .models import Tiket, Komentar
from users.serializers import UserListSerializer

class TiketSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = Tiket
        fields = [
            'id', 'judul', 'deskripsi', 'prioritas', 'user',
            'sla', 'waktu_dibuat', 'waktu_diperbarui', 'status', 'file',
            'cabang', 'jabatan'
        ]
        baca_kolom = ['sla', 'waktu_dibuat', 'waktu_diperbarui', 'user']

class KomentarSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.nama_lengkap')
    tiket = serializers.PrimaryKeyRelatedField(queryset=Tiket.objects.all())

    class Meta:
        model = Komentar
        fields = ['id', 'tiket', 'user', 'isi', 'waktu_dibuat']
        baca_kolom = ['user', 'waktu_dibuat']