# filepath: d:\Project\HelpDesk Aplikasi\helpdesk\users\management\commands\clean_blacklist.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

class Command(BaseCommand):
    help = 'Hapus token blacklist yang sudah expired'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired = OutstandingToken.objects.filter(expires_at__lt=now)
        count = expired.count()
        for token in expired:
            BlacklistedToken.objects.filter(token=token).delete()
            token.delete()
        self.stdout.write(self.style.SUCCESS(f'Berhasil menghapus {count} token blacklist yang expired.'))