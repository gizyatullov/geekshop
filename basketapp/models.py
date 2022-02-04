from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404

from mainapp.models import Product


# Create your models here.


class BasketQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)


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
        _all_baskets = Basket.objects.filter(user=self.user)
        _total_quantity = sum(i.quantity for i in _all_baskets)
        return _total_quantity

    @property
    def get_total_price(self):
        """
        return total cost for user
        """
        _all_baskets = Basket.objects.filter(user=self.user)
        _total_price = sum(i.get_product_cost for i in _all_baskets)
        return _total_price

    @staticmethod
    def get_items(user):
        baskets_user = Basket.objects.filter(user=user).order_by('product__category')
        return baskets_user

    @staticmethod
    def get_item(pk):
        return get_object_or_404(Basket, pk=pk)

    # Object's saving method
    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super(self.__class__, self).save(*args, **kwargs)

    # Object's deleting method
    def delete(self):
        self.product.quantity += self.quantity
        self.product.save()
        super(self.__class__, self).delete()
