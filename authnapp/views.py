from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib import auth
from django.urls import reverse
from django.conf import settings
from django.contrib import messages

from authnapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from .models import ShopUser
from .services import send_verify_mail


# Create your views here.


def login(request):
    login_form = ShopUserLoginForm(data=request.POST or None)
    next_page = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user and user.is_active:
            auth.login(request, user)
            if 'next_page' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next_page'])
            return HttpResponseRedirect(reverse('main'))

    context = {
        'page_title': 'вход',
        'login_form': login_form,
        'next_page': next_page,
    }
    return render(request, 'authnapp/login.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    message = 'Сообщение для подтверждения регистрации отправлено Вам на электронную почту указанную при регистрации!'
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                messages.success(request=request, message=message)
                print('сообщение для подтверждения регистрации отправлено')
                # return HttpResponseRedirect(reverse('auth:login'))
                return HttpResponseRedirect(reverse('auth:register'))
            print('ошибка отправки сообщения для подтверждения регистрации')
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


def verify(request, email, activation_key):
    # user = get_object_or_404(ShopUser, email=email)
    user = ShopUser.objects.filter(email=email).first()
    # user = ShopUser.objects.get(email=email)
    try:
        if user and user.activation_key == activation_key and not user.is_activation_key_expired():
            print(f'user {user} is activated')
            # user.is_active = True
            # user.activation_key = None
            # user.activation_key_expires = None
            # user.save()
            user.activate_user()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return render(request, 'authnapp/verification.html')

        print(f'error activation user: {user}')
        return render(request, 'authnapp/verification.html')

    except Exception as e:
        print(f'error activation user: {e.args}')

    return HttpResponseRedirect(reverse('main'))
