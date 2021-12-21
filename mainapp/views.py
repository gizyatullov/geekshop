from django.shortcuts import render


# Create your views here.


def main(request):
    context = {
        'page_title': 'Магазин',
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request):
    context = {
        'page_title': 'Каталог',
    }
    return render(request, 'mainapp/products.html', context=context)


def contact(request):
    context = {
        'page_title': 'Контакты',
    }
    return render(request, 'mainapp/contact.html', context=context)
