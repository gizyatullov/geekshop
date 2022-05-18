import pytz
from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import timedelta, datetime
from django.utils.timezone import now
from django.conf import settings

from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.


class ShopUser(AbstractUser):
    email = models.EmailField(verbose_name='email', blank=True, db_index=True)
    avatar = models.ImageField(upload_to="users_avatars", blank=True)
    age = models.PositiveSmallIntegerField(verbose_name="возраст", default=99)
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


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(max_length=128, blank=True, verbose_name='теги')
    about_me = models.TextField(max_length=512, blank=True, verbose_name='о себе')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='пол')

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
