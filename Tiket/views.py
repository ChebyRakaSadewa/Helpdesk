from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from .models import Tiket, Komentar
from .serializer import TiketSerializer, KomentarSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractDay
from django.db.models import Count
from calendar import month_abbr

# --- Permission Classes ---
class Admin(permissions.BasePermission):
    def izin_akses(self, request, view):
        # Hanya admin yang diizinkan
        return request.user.is_authenticated and request.user.is_admin

class User(permissions.BasePermission):
    def izin_akses(self, request, view):
        # Hanya user biasa yang diizinkan
        return request.user.is_authenticated and not request.user.is_admin

class Perizinan_admin(permissions.BasePermission):
    def izin_akses(self, request, view):
        # Admin hanya boleh akses SAFE_METHODS
        if request.user.is_authenticated and request.user.is_admin:
            return request.method in permissions.SAFE_METHODS
        return True

# --- Tiket ViewSet ---
class TiketViewset(viewsets.ModelViewSet):
    queryset = Tiket.objects.all().order_by('-waktu_dibuat')
    serializer_class = TiketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        tiket = serializer.save(user=self.request.user)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        admin_emails = User.objects.filter(is_admin=True).values_list('email', flat=True)
        from django.core.mail import send_mail
        from django.conf import settings
        send_mail(
            subject='[Helpdesk] Task Baru Diajukan',
            message=f"Tiket '{tiket.judul}' telah dibuat oleh {self.request.user.username}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=list(admin_emails),
            fail_silently=False
        )

    


    def destroy(self, request, *args, **kwargs):
        # (isi sama persis dengan hapus_data)
        tiket = self.get_object()
        if request.user.is_admin:
            if tiket.status or (tiket.sla and tiket.sla < now()):
                user_email = tiket.user.email if tiket.user and tiket.user.email else None
                tiket_judul = tiket.judul
                response = super().destroy(request, *args, **kwargs)
                if user_email:
                    send_mail(
                        subject='[Helpdesk] Tiket Anda Telah Dihapus',
                        message=f"Tiket '{tiket_judul}' telah dihapus oleh {request.user.username}.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user_email],
                        fail_silently=False
                    )
                return response
            return Response(
                {"detail": "Admin hanya bisa hapus task yang sudah selesai atau sudah expired."},
                status=status.HTTP_403_FORBIDDEN
            )
        # User biasa bisa hapus tiket sendiri
        user_email = tiket.user.email if tiket.user and tiket.user.email else None
        tiket_judul = tiket.judul
        response = super().destroy(request, *args, **kwargs)
        if user_email:
            send_mail(
                subject='[Helpdesk] Tiket Anda Telah Dihapus',
                message=f"Tiket '{tiket_judul}' telah dihapus oleh {request.user.username}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False
            )
        admin_emails = tiket.email_admin()
        send_mail(
            subject='[Helpdesk] Tiket Telah Dihapus',
            message=f"Tiket '{tiket.judul}' telah dihapus oleh {request.user.username}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=admin_emails,
            fail_silently=False
        )
        return response

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def confirm_complete(self, request, pk=None):
        # Admin menandai tiket sebagai selesai
        tiket = self.get_object()
        if tiket.status:
            return Response({"detail": "Task sudah selesai sebelumnya"}, status=status.HTTP_400_BAD_REQUEST)
        tiket.status = True
        tiket.save()
        # Notifikasi ke user
        if tiket.user and tiket.user.email:
            send_mail(
                subject='[Helpdesk] Task Anda Telah Selesai',
                message=f"Tiket '{tiket.judul}' telah dikonfirmasi selesai oleh admin.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[tiket.user.email],
                fail_silently=False
            )
        return Response({"status": "Task dikonfirmasi selesai oleh admin"})

    def update(self, request, *args, **kwargs):
        # (isi sama persis dengan ubah_data)
        response = super().update(request, *args, **kwargs)
        tiket = self.get_object()
        if tiket.user and tiket.user.email:
            send_mail(
                subject='[Helpdesk] Tiket Anda Telah Diedit',
                message=f"Tiket '{tiket.judul}' telah diperbarui oleh {request.user.username}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[tiket.user.email],
                fail_silently=False
            )
        admin_emails = tiket.email_admin()
        send_mail(
            subject='[Helpdesk] Tiket Telah Diperbarui',
            message=f"Tiket '{tiket.judul}' telah diperbarui. Silakan periksa untuk detail lebih lanjut.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=admin_emails,
            fail_silently=False
        )
        return response

# --- Komentar ViewSet ---
class KomentarViewSet(viewsets.ModelViewSet):
    queryset = Komentar.objects.all().order_by('-waktu_dibuat')
    serializer_class = KomentarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Simpan komentar dan kirim notifikasi email ke lawan diskusi
        komentar = serializer.save(user=self.request.user)
        tiket = komentar.tiket
        if self.request.user.is_admin:
            recipient_email = tiket.user.email
            subject = "[Helpdesk] Admin Membalas Komentar Anda"
            message = f"Admin membalas tiket '{tiket.judul}':\n\n{komentar.isi}"
        else:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            admin_emails = User.objects.filter(is_admin=True).values_list('email', flat=True)
            recipient_email = list(admin_emails)
            subject = f"[Helpdesk] Komentar Baru untuk tiket '{tiket.judul}'"
            message = f"User {self.request.user.username} mengomentari tiket '{tiket.judul}':\n\n{komentar.isi}"
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email] if isinstance(recipient_email, str) else recipient_email,
            fail_silently=False
        )

# --- Tiket Masuk View ---
class TiketMasukView(APIView):
    def get(self, request):
        # Ambil semua tiket yang belum selesai (status=False)
        tiket = Tiket.objects.filter(status=False)
        serializer = TiketSerializer(tiket, many=True)
        return Response(serializer.data)

# --- Tiket Saya View ---
class TiketSayaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Ambil tiket milik user yang login, bisa difilter dan diurutkan
        tiket = Tiket.objects.filter(user=request.user)
        prioritas = request.GET.getlist('priority')
        if prioritas:
            tiket = tiket.filter(prioritas__in=prioritas)
        status_list = request.GET.getlist('status')
        if status_list:
            status_map = {'New': False, 'Closed': True, 'In Progress': None}
            status_values = [status_map.get(s) for s in status_list if s in status_map]
            tiket = tiket.filter(status__in=status_values)
        kantor = request.GET.getlist('kantor')
        if kantor:
            tiket = tiket.filter(cabang__in=kantor)
        urutan = request.GET.get('sort_by')
        if urutan in ['prioritas', 'status', 'cabang']:
            tiket = tiket.order_by(urutan)
        serializer = TiketSerializer(tiket, many=True)
        return Response(serializer.data)

# --- Tiket Selesai View ---
class TiketSelesaiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Ambil semua tiket yang sudah selesai (status=True)
        tiket = Tiket.objects.filter(status=True)
        serializer = TiketSerializer(tiket, many=True)
        return Response(serializer.data)

# --- Statistik Tiket View ---
class StatistikTiketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Statistik tiket berdasarkan filter tahun, bulan, hari
        queryset = Tiket.objects.all()
        tahun = request.GET.get('tahun')
        bulan = request.GET.get('bulan')
        hari = request.GET.get('hari')
        group_by = request.GET.get('group_by', 'bulan')

        if tahun:
            queryset = queryset.filter(waktu_dibuat__year=tahun)
        if bulan:
            queryset = queryset.filter(waktu_dibuat__month=bulan)
        if hari:
            queryset = queryset.filter(waktu_dibuat__day=hari)

        # Jika filter sampai hari, kembalikan total tiket hari itu saja
        if hari:
            count = queryset.count()
            return Response({str(int(hari)): count})
        # Jika filter sampai bulan, group by hari
        elif bulan:
            stats = queryset.annotate(hari=ExtractDay('waktu_dibuat')).values('hari').annotate(count=Count('id')).order_by('hari')
            result = {str(item['hari']): item['count'] for item in stats if item['hari']}
            return Response(result)
        # Jika filter sampai tahun, group by bulan
        elif tahun:
            stats = queryset.annotate(bulan=ExtractMonth('waktu_dibuat')).values('bulan').annotate(count=Count('id')).order_by('bulan')
            result = {month_abbr[item['bulan']]: item['count'] for item in stats if item['bulan']}
            return Response(result)
        # Default: group by tahun
        else:
            stats = queryset.annotate(tahun=ExtractYear('waktu_dibuat')).values('tahun').annotate(count=Count('id')).order_by('tahun')
            result = {str(item['tahun']): item['count'] for item in stats if item['tahun']}
            return Response(result)
