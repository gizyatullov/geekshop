from django.shortcuts import render
import os
import json

# Create your views here.

MODULE_DIR = os.path.dirname(__file__)


def main(request):
    file_path = os.path.join(MODULE_DIR, 'fixtures/goods_index.json')
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
        'page_title': 'Магазин',
        'products': json.load(open(file_path, encoding='utf-8')),
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request):
    file_path = os.path.join(MODULE_DIR, 'fixtures/goods_products.json')
    links_menu = [
        {"href": "mainapp:products_all", "name": "все"},
        {"href": "mainapp:products_home", "name": "дом"},
        {"href": "mainapp:products_office", "name": "офис"},
        {"href": "mainapp:products_modern", "name": "модерн"},
        {"href": "mainapp:products_classic", "name": "классика"},
    ]

    # same_products = [
    #     {"name": "Отличный стул", "desc": "Не оторваться.", "image_src": "product-11.jpg", "alt": "продукт 11"},
    #     {"name": "Стул повышенного качества", "desc": "Комфортно.", "image_src": "product-21.jpg", "alt": "продукт 21"},
    #     {
    #         "name": "Стул премиального качества",
    #         "desc": "Просто попробуйте.",
    #         "image_src": "product-31.jpg",
    #         "alt": "продукт 31",
    #     },
    # ]

    context = {
        'page_title': 'Каталог',
        'links_menu': links_menu,
        'same_products': json.load(open(file_path, encoding='utf-8')),
    }
    return render(request, 'mainapp/products.html', context=context)


def contact(request):
    file_path = os.path.join(MODULE_DIR, 'fixtures/locations_contact.json')
    # locations = [
    #     {"city": "Москва",
    #      "phone": "+7-888-888-8888",
    #      "email": "info@geekshop.ru",
    #      "address": "В пределах МКАД"},
    #
    #     {"city": "Екатеринбург",
    #      "phone": "+7-777-777-7777",
    #      "email": "info_yekaterinburg@geekshop.ru",
    #      "address": "Близко к центру"},
    #
    #     {"city": "Владивосток",
    #      "phone": "+7-999-999-9999",
    #      "email": "info_vladivostok@geekshop.ru",
    #      "address": "Близко к океану"},
    # ]

    context = {
        'page_title': 'Контакты',
        'locations': json.load(open(file_path, encoding='utf-8')),
    }
    return render(request, 'mainapp/contact.html', context=context)
