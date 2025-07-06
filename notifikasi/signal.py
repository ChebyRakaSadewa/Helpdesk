# notifikasi/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from Tiket.models import Tiket
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

@receiver(post_save, sender=Tiket)
def tiket_post_save(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            notification_type='ticket_created',
            content_object=instance,
            message=f"Tiket '{instance.judul}' berhasil dikirim."
        )
    else:
        if instance.status == 'in_progress':
            Notification.objects.create(
                user=instance.user,
                notification_type='ticket_in_progress',
                content_object=instance,
                message=f"Tiket '{instance.judul}' dalam proses pengerjaan."
            )
        elif instance.status == 'completed':
            Notification.objects.create(
                user=instance.user,
                notification_type='ticket_completed',
                content_object=instance,
                message=f"Tiket '{instance.judul}' telah selesai."
            )
        else:
            Notification.objects.create(
                user=instance.user,
                notification_type='ticket_updated',
                content_object=instance,
                message=f"Tiket '{instance.judul}' berhasil diperbarui."
            )

