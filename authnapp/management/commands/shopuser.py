from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create ShopUser'

    @staticmethod
    def accept_name():
        while True:
            username = input('Enter username ')
            if username:
                break
            else:
                print('No enter username!')

        return username

    @staticmethod
    def accept_password():
        while True:
            password_1 = input('Enter password ')
            password_2 = input('Repeat enter password ')

            if password_1 == password_2:
                break
            else:
                print('Passwords don\'t match')

        return password_1

    @staticmethod
    def accept_age():
        while True:
            age = input('Enter age ')
            try:
                age = int(age)
            except ValueError as e:
                print('This is not age!')
            except Exception as e:
                print(f'Unknown error {e} This is not age!')
            else:
                return age

    def handle(self, *args, **kwargs):

        user = get_user_model()

        username = self.accept_name()

        email = input('Enter email ')

        password = self.accept_password()

        age = self.accept_age()

        user.objects.create_user(username=username,
                                 password=password,
                                 age=age,
                                 email=email)
