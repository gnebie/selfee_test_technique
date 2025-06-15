import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pathlib import Path

class Command(BaseCommand):
    help = 'Seed predefined users from a JSON file'

    def handle(self, *args, **kwargs):
        print(Path(__file__).resolve().parent.parent.parent.parent.parent)
        json_path = Path(__file__).resolve().parent.parent.parent.parent.parent / 'test_users.json'
        with open(json_path) as f:
            users = json.load(f)

        for u in users:
            if not User.objects.filter(username=u["username"]).exists():
                User.objects.create_user(username=u["username"], password=u["password"])
                self.stdout.write(self.style.SUCCESS(f"User '{u['username']}' created"))
            else:
                self.stdout.write(f"User '{u['username']}' already exists")
