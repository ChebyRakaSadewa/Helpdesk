from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TiketViewset, KomentarViewSet,
    TiketMasukView, TiketSayaView, TiketSelesaiView, StatistikTiketView
)

router = DefaultRouter()
router.register(r'task', TiketViewset, basename='task')           # GANTI dari 'tiket' ke 'task'
router.register(r'komentar', KomentarViewSet, basename='komentar')

urlpatterns = [
    path('', include(router.urls)),
    path('tiket/masuk/', TiketMasukView.as_view(), name='tiket-masuk'),
    path('tiket/saya/', TiketSayaView.as_view(), name='tiket-saya'),
    path('tiket/selesai/', TiketSelesaiView.as_view(), name='tiket-selesai'),
    path('tiket/statistik/', StatistikTiketView.as_view(), name='tiket-statistik'),
]