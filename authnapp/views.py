from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from authnapp.forms import ShopUserLoginForm


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
