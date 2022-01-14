from django.urls import path

from mainapp.apps import MainappConfig
import mainapp.views as mainapp

app_name = MainappConfig.name

urlpatterns = [
    path('', mainapp.products, name='index'),
    path('category/<int:pk>/', mainapp.products, name='category'),
    path('product/<int:pk>/', mainapp.product, name='product'),
]
