from django import template

import mainapp.models as main_app

register = template.Library()


@register.simple_tag(name='products')
def get_all_products(filter=None):
    if not filter:
        return main_app.Product.objects.all()
    else:
        return main_app.Product.objects.filter(pk=filter)


@register.simple_tag(name='categories')
def get_all_categories():
    return main_app.ProductCategory.objects.all()


@register.inclusion_tag('mainapp/includes/include__categories_menu.html')
def show_categories_menu(sort=None):
    if not sort:
        categories = main_app.ProductCategory.objects.all()
    else:
        categories = main_app.ProductCategory.objects.order_by(sort)
    return {
        'links_menu': categories,
    }
