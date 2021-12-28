from django.shortcuts import render
from django.utils import timezone
from django.conf import settings

from .models import Product, ProductCategory


# Create your views here.


def main(request):
    # products = [
    #     {
    #         'name': 'Отличный стул',
    #         'description': 'Расположитесь комфортно.',
    #         'img_src': "product-1.jpg",
    #         'img_href': '/product/1/',
    #         'alt': 'продукт 1',
    #     },
    #     {
    #         'name': 'Стул повышенного качества',
    #         'description': 'Не оторваться.',
    #         'img_src': "product-2.jpg",
    #         'img_href': '/product/2/',
    #         'alt': 'продукт 2',
    #     },
    # ]

    context = {
        'page_title': 'Магазин - Главная',
        'products': Product.objects.all(),
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
    locations = [
        {"city": "Москва",
         "phone": "+7-888-888-8888",
         "email": "info@geekshop.ru",
         "address": "В пределах МКАД"},

        {"city": "Екатеринбург",
         "phone": "+7-777-777-7777",
         "email": "info_yekaterinburg@geekshop.ru",
         "address": "Близко к центру"},

        {"city": "Владивосток",
         "phone": "+7-999-999-9999",
         "email": "info_vladivostok@geekshop.ru",
         "address": "Близко к океану"},
    ]

    context = {
        'page_title': 'Контакты - О нас',
        'visit_date': timezone.now(),
        'locations': locations,
    }
    return render(request, 'mainapp/contact.html', context=context)
