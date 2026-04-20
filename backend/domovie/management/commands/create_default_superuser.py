import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create a superuser from env vars if none exists"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("Superuser already exists. Skipping.")
            return

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not all([username, email, password]):
            self.stderr.write("Missing one or more DJANGO_SUPERUSER_* env vars. Skipping.")
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(f"Superuser '{username}' created.")
