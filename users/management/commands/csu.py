from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.create(email="alina_nemo@mail.ru")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password("123qwe")
        user.save()
