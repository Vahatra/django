import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Command to initialize the DB (Production).
    """

    def handle(self, *args, **options):
        subprocess.run(args=["python", "manage.py", "migrate"])
        # other script here

        self.stdout.write(self.style.SUCCESS("Initialization completed."))
