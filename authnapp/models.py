import pytz
from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import timedelta, datetime
from django.utils.timezone import now
from django.conf import settings


# Create your models here.


class ShopUser(AbstractUser):
    email = models.EmailField(verbose_name='email')
    avatar = models.ImageField(upload_to="users_avatars", blank=True)
    age = models.PositiveSmallIntegerField(verbose_name="возраст")
    activation_key = models.CharField(max_length=128, null=True, blank=True, verbose_name='ключ подтверждения')
    activation_key_expires = models.DateTimeField(null=True, blank=True, verbose_name='актуальность ключа')

    def __str__(self):
        return f'{self.username} {self.last_name}'

    def delete(self, using=None, keep_parents=False):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
        self.save()

    def is_activation_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) >= self.activation_key_expires + timedelta(hours=48):
            return True
        return False

    def activate_user(self):
        self.is_active = True
        self.activation_key = None
        self.activation_key_expires = None
        self.save()
