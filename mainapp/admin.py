from django.contrib import admin

from mainapp.models import ProductCategory, Product, Contact

# Register your models here.

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Contact)
