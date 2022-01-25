from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import timedelta
from django.utils.timezone import now


# Create your models here.


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to="users_avatars", blank=True)
    age = models.PositiveSmallIntegerField(verbose_name="возраст")
    activation_key = models.CharField(max_length=128, blank=True, verbose_name='ключ подтверждения')
    activation_key_expires = models.DateTimeField(
        default=(now() + timedelta(hours=48)), verbose_name='актуальность ключа'
    )

    def __str__(self):
        return f'{self.username} {self.last_name}'

    def delete(self, using=None, keep_parents=False):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
        self.save()

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True
