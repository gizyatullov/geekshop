from django.shortcuts import render
from django.utils import timezone
from django.conf import settings

from .models import Product, ProductCategory, Contact


# Create your views here.


def main(request):
    context = {
        'page_title': 'Магазин - Главная',
        'products': Product.objects.all()[:4],
        'media_url': settings.MEDIA_URL,
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request, pk=None):
    context = {
        'page_title': 'Каталог - Продукты',
        'links_menu': ProductCategory.objects.all(),
        'same_products': Product.objects.all(),
        'media_url': settings.MEDIA_URL,
    }

    if pk:
        print(f'User select category: {pk} xD')
    return render(request, 'mainapp/products.html', context=context)


def contact(request):
    context = {
        'page_title': 'Контакты - О нас',
        'visit_date': timezone.now(),
        'locations': Contact.objects.all(),
    }
    return render(request, 'mainapp/contact.html', context=context)
