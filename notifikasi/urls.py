# notifikasi/urls.py
from django.urls import path
from .views import NotificationListView, NotificationReadView, ClearNotificationsView, UpdateProfileView, UpdatePasswordView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/read/', NotificationReadView.as_view(), name='notification-read'),
    path('notifications/clear/', ClearNotificationsView.as_view(), name='clear-notifications'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    path('update-password/', UpdatePasswordView.as_view(), name='update-password'),
]
