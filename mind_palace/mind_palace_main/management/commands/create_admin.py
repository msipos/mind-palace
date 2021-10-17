from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create an admin user'

    def handle(self, *args, **options):
        print('Creating admin user with password "change_my_password"...')
        try:
            User.objects.create_superuser('admin', password='change_my_password')
            print('... created.')
        except:
            print('... admin user already exists.')
