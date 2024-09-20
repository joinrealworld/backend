from django.core.management.base import BaseCommand
from faker import Faker
from user.models import User
import random

class Command(BaseCommand):
    help = 'Create 500 dummy users'

    def handle(self, *args, **kwargs):
        faker = Faker()
        dummy_users = []

        for _ in range(500):
            first_name = faker.first_name()
            last_name = faker.last_name()
            email = faker.email()
            username = self.generate_unique_username(first_name, last_name)
            bio = faker.text(max_nb_chars=200)
            is_active = True
            is_admin = False
            is_staff = False
            is_superuser = False
            theme = random.choice(['dark', 'light'])
            fa_type = random.choice(['code', 'email'])
            level = random.randint(1, 50)
            xp = random.randint(0, 1000)

            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                bio=bio,
                is_active=is_active,
                is_admin=is_admin,
                is_staff=is_staff,
                is_superuser=is_superuser,
                theme=theme,
                fa_type=fa_type,
                level=level,
                xp=xp,
                is_dummy = True
                # You can fill more fields if required
            )
            dummy_users.append(user)

        # Bulk create users to improve performance
        User.objects.bulk_create(dummy_users)

        self.stdout.write(self.style.SUCCESS('Successfully created 500 dummy users'))

    def generate_unique_username(self, first_name, last_name):
        """Generate a unique username by combining first_name, last_name, and random numbers"""
        base_username = f"{first_name.lower()}_{last_name.lower()}"
        while True:
            username = f"{base_username}{random.randint(100, 999)}"
            if not User.objects.filter(username=username).exists():
                return username
