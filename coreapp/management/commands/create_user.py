# python manage.py create_user <username> <password> --role <role>

from django.core.management.base import BaseCommand
from coreapp.models import User

class Command(BaseCommand):
    help = 'Create a new user using the create_user function'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username for the new user')
        parser.add_argument('password', type=str, help='The password for the new user')
        parser.add_argument('--role', type=str, help='The role for the new user', default='user')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        password = kwargs['password']
        role = kwargs['role']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR('User with this username already exists'))
        else:
            user = User.objects.create_user(username=username, password=password, role=role)
            self.stdout.write(self.style.SUCCESS(f'Successfully created user: {user.username}'))

