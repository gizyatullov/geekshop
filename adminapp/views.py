from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import render_to_string
from django.urls import reverse

from authnapp.models import ShopUser
from mainapp.models import ProductCategory, Product

from .forms import ShopUserAdminEditForm, ProductCategoryEditForm
from authnapp.forms import ShopUserRegisterForm


# Create your views here.


@user_passes_test(lambda u: u.is_superuser)
def admin_main(request):
    response = redirect('admin:users')
    return response


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'page_title': 'админка/пользователи',
        'objects': users_list,
        'media_url': settings.MEDIA_URL,
    }

    return render(request, 'adminapp/users.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegisterForm()

    context = {
        'page_title': 'пользователи/создание',
        'update_form': user_form,
        'media_url': settings.MEDIA_URL,
    }

    return render(request, 'adminapp/user_update.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    edit_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse("admin:user_update", args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    context = {
        'page_title': 'пользователи/редактирование',
        'update_form': edit_form,
        'media_url': settings.MEDIA_URL,
    }

    return render(request, 'adminapp/user_update.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))

    context = {
        'page_title': 'пользователи/удаление',
        'user_to_delete': user,
        'media_url': settings.MEDIA_URL,
    }

    # return render(request, 'adminapp/user_delete.html', context=context)
    correction = render_to_string('adminapp/includes/include__user_delete.html', request=request, context=context)

    return JsonResponse({'correction': correction})


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    categories_list = ProductCategory.objects.all()

    context = {
        'page_title': 'админка/категории',
        'objects': categories_list,
        'media_url': settings.MEDIA_URL,
    }

    return render(request, 'adminapp/categories.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        category_form = ProductCategoryEditForm()

    context = {
        'page_title': 'категории/создание',
        'update_form': category_form,
        'media_url': settings.MEDIA_URL,
    }
    return render(request, 'adminapp/category_update.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    edit_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:category_update', args=[edit_category.pk]))
    else:
        edit_form = ProductCategoryEditForm(instance=edit_category)

    context = {
        'page_title': 'категории/редактирование',
        'update_form': edit_form,
        'media_url': settings.MEDIA_URL,
    }

    return render(request, 'adminapp/category_update.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        category.is_active = False
        category.save()
        return HttpResponseRedirect(reverse('admin:categories'))

    context = {
        'page_title': 'категории/удаление',
        'category_to_delete': category,
        'media_url': settings.MEDIA_URL,
    }
    # return render(request, 'adminapp/category_delete.html', context=context)

    correction = render_to_string('adminapp/includes/include__category_delete.html', request=request, context=context)

    return JsonResponse({'correction': correction})


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    context = {
        'page_title': 'админка/продукт',
        'category': category,
        'objects': products_list,
        'media_url': settings.MEDIA_URL,
    }

    return render(request, 'adminapp/products.html', context=context)


def product_create(request, pk):
    response = redirect('admin:categories')
    return response


def product_read(request, pk):
    response = redirect('admin:categories')
    return response


def product_update(request, pk):
    response = redirect('admin:categories')
    return response


def product_delete(request, pk):
    response = redirect('admin:categories')
    return response
