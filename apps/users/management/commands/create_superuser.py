from django.conf import settings
from apps.users.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Create Superuser CLI Command
    """
    help = "Create superuser if it does not exist"

    def handle(self, *args, **options):
        """
        Handler to catch this CLI command
        """
        if not User.objects.filter(username=settings.SUPERUSER_USERNAME):
            User.objects.create_superuser(
                username=settings.SUPERUSER_USERNAME,
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD
            )
            self.stdout.write("Successfully created.")
        else:
            self.stdout.write("Superuser already exist.")