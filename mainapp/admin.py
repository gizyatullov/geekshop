from django.contrib import admin

from mainapp.models import ProductCategory, Product, Contact


# Register your models here.

class MainappProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'image', 'price', 'quantity',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    list_editable = ('quantity',)
    list_filter = ('quantity', 'category',)
    # prepopulated_fields = {'slug': ('name',)}


class MainappProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    # prepopulated_fields = {'slug': ('name',)}


class MainappContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'city',)
    list_display_links = ('id', 'phone', 'city',)
    search_fields = ('phone', 'address',)


admin.site.register(ProductCategory, MainappProductCategoryAdmin)
admin.site.register(Product, MainappProductAdmin)
admin.site.register(Contact, MainappContactAdmin)
