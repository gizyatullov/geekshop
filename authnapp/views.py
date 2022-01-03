from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.conf import settings

from authnapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm


# Create your views here.


def login(request):
    login_form = ShopUserLoginForm(data=request.POST or None)

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main'))

    context = {
        'page_title': 'вход',
        'login_form': login_form,
    }
    return render(request, 'authnapp/login.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    context = {
        'page_title': 'регистрация',
        'register_form': register_form,
    }
    return render(request, 'authnapp/register.html', context=context)


def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    context = {
        'page_title': 'редактирование',
        'edit_form': edit_form,
        'media_url': settings.MEDIA_URL,
    }

    return render(request, 'authnapp/edit.html', context=context)
