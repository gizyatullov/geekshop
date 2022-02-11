from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.conf import settings

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView

from mainapp.models import Product, ProductCategory, Contact
from .services import get_hot_product, get_same_products, get_hot_product_list


# Create your views here.


def main(request):
    context = {
        'page_title': 'Магазин - Главная',
        'products': Product.objects.filter(is_active=True, category__is_active=True)[:3],
        'media_url': settings.MEDIA_URL,
    }

    return render(request, 'mainapp/index.html', context=context)


class ProductsListView(ListView):
    model = Product
    template_name = 'mainapp/products_list.html'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        category_pk = self.kwargs.get('pk')
        if not category_pk == 0:
            queryset = queryset.filter(category__pk=category_pk)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category_pk = self.kwargs.get('pk')
        # hot_product = get_hot_product()

        context['page_title'] = 'Каталог - Продукты'
        context['links_menu'] = ProductCategory.objects.filter(is_active=True)
        context['category'] = get_object_or_404(ProductCategory, pk=category_pk)
        context['media_url'] = settings.MEDIA_URL
        # context['same_products'] = get_same_products(hot_product)
        # context['hot_product'] = hot_product

        return context


def products(request, pk=None, page=1):
    page_title = 'Каталог - Продукты'
    links_menu = ProductCategory.objects.filter(is_active=True)

    if pk is not None:
        if pk == '0':
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            category = {'name': 'все', 'pk': 0}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')

        paginator = Paginator(products, 2)

        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'page_title': page_title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
            'media_url': settings.MEDIA_URL,
        }

        return render(request, 'mainapp/products_list.html', context=context)

    # hot_product = get_hot_product()
    # same_products = get_same_products(hot_product)
    hot_product, same_products = get_hot_product_list()

    context = {
        'page_title': page_title,
        'links_menu': links_menu,
        'same_products': same_products,
        'media_url': settings.MEDIA_URL,
        'hot_product': hot_product,
    }

    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    prod = get_object_or_404(Product, pk=pk)
    context = {
        'page_title': prod.name,
        'link_menu': ProductCategory.objects.all(),
        'product': prod,
        'media_url': settings.MEDIA_URL,
    }

    return render(request, 'mainapp/product.html', context=context)


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
