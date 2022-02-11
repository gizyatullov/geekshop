import random

from basketapp.models import Basket
from mainapp.models import Product


def get_hot_product():
    all_products = Product.objects.filter(is_active=True, category__is_active=True)
    return random.sample(list(all_products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category, is_active=True).exclude(pk=hot_product.pk)[:3]
    return same_products


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []
