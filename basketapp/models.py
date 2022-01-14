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

    @property
    def get_product_cost(self):
        """
        return cost of all products this type
        """
        product_cost = self.quantity * self.product.price
        return product_cost

    @property
    def get_total_quantity(self):
        """
        return total quantity for user
        """
        all_baskets = Basket.objects.filter(user=self.user)
        total_quantity = sum(i.quantity for i in all_baskets)
        return total_quantity

    @property
    def get_total_price(self):
        """
        return total cost for user
        """
        all_baskets = Basket.objects.filter(user=self.user)
        total_price = sum(i.get_product_cost for i in all_baskets)
        return total_price
