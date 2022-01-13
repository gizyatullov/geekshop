from django.contrib import admin

from basketapp.models import Basket


# Register your models here.


class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity',)
    list_display_links = ('id', 'user', 'product', 'quantity',)
    search_fields = ('user', 'product',)
    # list_editable = ('quantity',)
    list_filter = ('quantity', 'product', 'user',)


admin.site.register(Basket, BasketAdmin)
