from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings

from authnapp.models import ShopUser
from mainapp.models import ProductCategory, Product


# Create your views here.


def admin_main(request):
    response = redirect('admin:users')
    return response


def users(request):
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'page_title': 'админка/пользователи',
        'objects': users_list,
        'media_url': settings.MEDIA_URL,
    }

    return render(request, 'adminapp/users.html', context=context)


def user_create(request):
    response = redirect('admin:users')
    return response


def user_update(request, pk):
    response = redirect('admin:users')
    return response


def user_delete(request, pk):
    response = redirect('admin:users')
    return response


def categories(request):
    categories_list = ProductCategory.objects.all()

    context = {
        'page_title': 'админка/категории',
        'objects': categories_list,
        'media_url': settings.MEDIA_URL,
    }

    return render(request, 'adminapp/categories.html', context=context)


def category_create(request):
    response = redirect('admin:categories')
    return response


def category_update(request):
    response = redirect('admin:categories')
    return response


def category_delete(request, pk):
    response = redirect('admin:categories')
    return response


def products(request, pk):
    category = get_object_or_404(ProductCategory, pk)
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


def product_read(request):
    response = redirect('admin:categories')
    return response


def product_update(request, pk):
    response = redirect('admin:categories')
    return response


def product_delete(request, pk):
    response = redirect('admin:categories')
    return response
