from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from django.http import JsonResponse
from django.contrib.auth import authenticate
from .models import Customuser
from .serializers import RegisterSerializer, UserListSerializer
from rest_framework import generics, status


class RegisterView(APIView):
    permission_classes = [IsAuthenticated]

    

    def post(self, request):
        if not request.user.is_admin:
            raise PermissionDenied("Hanya admin yang dapat mendaftarkan pengguna baru.")

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Pengguna berhasil didaftarkan",
                "user": RegisterSerializer(user).data
            }, status=201)
        return Response(serializer.errors, status=400)


class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            raise AuthenticationFailed("Kredensial tidak valid")

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = JsonResponse({
            'access': access_token,
            'user': {
                'id': user.id,
                'nama_lengkap': user.nama_lengkap,
                'is_admin': user.is_admin,
            }
        })

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,  # Ganti True di produksi (HTTPS)
            samesite='Lax',
            max_age=1 * 24 * 60 * 60
        )

        return response


class CookieTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            raise AuthenticationFailed("Tidak ada refresh token di cookies")

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except Exception:
            raise AuthenticationFailed("Refresh token tidak valid")

        return Response({"access": access_token})


class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logout berhasil"}, status=200)
        response.delete_cookie('refresh_token')
        return response


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = RegisterSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user = request.user
        serializer = RegisterSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Tambahkan notifikasi di sini
            from notifikasi.models import Notification
            Notification.objects.create(
                user=user,
                notification_type='profile_updated',
                message="Profil Anda berhasil diperbarui."
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = Customuser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customuser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]


class UserListView(APIView):
    def get(self, request):
        queryset = Customuser.objects.all()
        serializer = UserListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)