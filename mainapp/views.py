from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.conf import settings

from mainapp.models import Product, ProductCategory, Contact
from basketapp.models import Basket


# Create your views here.


def main(request):
    context = {
        'page_title': 'Магазин - Главная',
        'products': Product.objects.all()[:4],
        'media_url': settings.MEDIA_URL,
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request, pk=None):
    page_title = 'Каталог - Продукты'
    links_menu = ProductCategory.objects.all()

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')
        context = {
            'page_title': page_title,
            'links_menu': links_menu,
            'category': category,
            'products': products,
            'media_url': settings.MEDIA_URL,
            'basket': basket,
        }
        return render(request, 'mainapp/products_list.html', context=context)

    context = {
        'page_title': page_title,
        'links_menu': links_menu,
        'same_products': Product.objects.all(),
        'media_url': settings.MEDIA_URL,
        'basket': basket,
    }

    if pk:
        print(f'User select category: {pk} xD')
        print(basket.get_total_quantity())
    return render(request, 'mainapp/products.html', context=context)


def contact(request):
    context = {
        'page_title': 'Контакты - О нас',
        'visit_date': timezone.now(),
        'locations': Contact.objects.all(),
    }
    return render(request, 'mainapp/contact.html', context=context)


def page_not_found(request, exception):
    context = {
        'exception': exception,
        'page_title': 'Страница, на которую Вы пытаетесь попасть не найдена или не существует.',
    }
    return render(request, 'mainapp/page-not-found.html', context=context)
