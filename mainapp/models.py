from django.db import models


# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=64, verbose_name='название', unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(verbose_name='категория активна?', default=True, db_index=True)

    class Meta:
        verbose_name = 'категория товаров'
        verbose_name_plural = 'категории товаров'
        ordering = ('-pk',)

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
        self.save()


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='категория')
    name = models.CharField(max_length=128, verbose_name='название')
    image = models.ImageField(upload_to='products_images', blank=True, verbose_name='изображение')
    short_desc = models.CharField(max_length=64, verbose_name='краткое описание', blank=True)
    description = models.TextField(verbose_name='описание', blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='цена', default=0)
    quantity = models.PositiveIntegerField(verbose_name='количество на складе', default=0)
    is_active = models.BooleanField(verbose_name="продукт активен", default=True, db_index=True)

    class Meta:
        verbose_name = 'товаров'
        verbose_name_plural = 'товары'
        ordering = ('-price',)

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    def delete(self, using=None, keep_parents=False):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
        self.save()

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')


class Contact(models.Model):
    phone = models.CharField(max_length=50, verbose_name="номер телефона")
    email = models.EmailField(max_length=254, verbose_name="электронная почта")
    city = models.CharField(max_length=128, default="Москва", verbose_name="город")
    address = models.CharField(max_length=254, verbose_name="адрес")

    class Meta:
        verbose_name = 'контактов'
        verbose_name_plural = 'контакты'
        ordering = ('-city',)

    def __str__(self):
        return f"{self.pk} {self.email}"
