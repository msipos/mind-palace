from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Export all the data'

    def handle(self, *args, **options):
        try:
            User.objects.create_user('demo', password='demo')
        except:
            print('demo user already exists')
    