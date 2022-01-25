from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from authnapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from .models import ShopUser


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
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('сообщение для подтверждения регистрации отправлено')
                return HttpResponseRedirect(reverse('auth:login'))
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


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME} перейдите по ссылке: \
              \n{settings.DOMAIN_NAME}{verify_link}'

    print(f'from: {settings.EMAIL_HOST_USER}, to: {user.email}')

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            print(f'user {user} is activated')
            user.is_active = True
            user.save()
            auth.login(request, user)

        print(f'error activation user: {user}')

        return render(request, 'authnapp/verification.html')

    except Exception as e:
        print(f'error activation user: {e.args}')

    return HttpResponseRedirect(reverse('main'))
