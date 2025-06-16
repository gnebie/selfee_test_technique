import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pathlib import Path


def seed_users_from_data(user_list, logger=None):
    created = []
    skipped = []

    for u in user_list:
        if not User.objects.filter(username=u["username"]).exists():
            User.objects.create_user(username=u["username"], password=u["password"])
            created.append(u["username"])
            if logger:
                logger(f"User '{u['username']}' created")
        else:
            skipped.append(u["username"])
            if logger:
                logger(f"User '{u['username']}' already exists")
    return {"created": created, "skipped": skipped}


class Command(BaseCommand):
    help = "Seed predefined users from a JSON file"

    def handle(self, *args, **kwargs):
        json_path = (
            Path(__file__).resolve().parent.parent.parent.parent.parent
            / "test_users.json"
        )
        with open(json_path) as f:
            users = json.load(f)

        result = seed_users_from_data(users, logger=self.stdout.write)
        self.stdout.write(
            self.style.SUCCESS(f"Seed completed: {len(result['created'])} created")
        )
