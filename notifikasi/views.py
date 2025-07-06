from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Notification
from .serializer import NotificationSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from notifikasi.models import Notification as NotifikasiNotification

User = get_user_model()

# Menampilkan semua notifikasi untuk pengguna
class NotificationListView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

# Menandai notifikasi sudah dibaca
class NotificationReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response(status=204)  # HTTP 204 No Content

# Menghapus notifikasi yang sudah dibaca
class ClearNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        Notification.objects.filter(user=request.user, is_read=True).delete()
        return Response(status=204)



class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        # ...kode update profile user...
        # Setelah berhasil update:
        Notification.objects.create(
            user=request.user,
            notification_type='profile_updated',
            message="Profil Anda berhasil diperbarui."
        )
        return Response({"detail": "Profile updated"})

class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # ...kode update password user...
        # Setelah berhasil update:
        Notification.objects.create(
            user=request.user,
            notification_type='password_updated',
            message="Password Anda berhasil diperbarui."
        )
        return Response({"detail": "Password updated"})
