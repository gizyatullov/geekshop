from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to="users_avatars", blank=True)
    age = models.PositiveSmallIntegerField(verbose_name="возраст")

    def __str__(self):
        return f'{self.username} {self.last_name}'

    def delete(self, using=None, keep_parents=False):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
        self.save()
