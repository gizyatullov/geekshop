from datetime import datetime

import pytz
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
import hashlib
import random
from django.conf import settings

from .models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ShopUser
        fields = ('username',
                  'password',)

    # self validators!
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 12:
            raise ValidationError('Длина логина превышает 12 символов')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 4:
            raise ValidationError('Длина пароля меньше 4 символов')
        return password


class ShopUserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(ShopUserRegisterForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)

        user.is_active = False

        # salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:6]
        # user.activation_key = hashlib.sha1((user.email + salt).encode('utf-8')).hexdigest()

        user.activation_key = hashlib.sha1(user.email.encode('utf-8')).hexdigest()
        user.activation_key_expires = datetime.now(pytz.timezone(settings.TIME_ZONE))
        user.save()
        return user

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Вы слишком молоды')
        return data

    class Meta:
        model = ShopUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'age',
            'avatar',
            'password1',
            'password2',
        )


class ShopUserEditForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(ShopUserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Вы слишком молоды! xD')

        return data

    class Meta:
        model = ShopUser
        fields = ('username',
                  'first_name',
                  'email',
                  'age',
                  'avatar')
