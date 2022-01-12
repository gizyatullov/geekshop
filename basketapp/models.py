from django.db import models
from django.conf import settings

from mainapp.models import Product


# Create your models here.


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время добавления')

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины пользователей'
        ordering = ('-pk',)

    def get_total_quantity(self):
        all_baskets = Basket.objects.filter(user=self.user)
        total_quantity = sum(i.quantity for i in all_baskets)
        return total_quantity

    def get_total_price(self):
        all_baskets = Basket.objects.filter(user=self.user)
        total_price = sum(i.quantity * i.product.price for i in all_baskets)
        return total_price
