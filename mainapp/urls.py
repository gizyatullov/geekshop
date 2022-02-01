from django.urls import path, re_path

from mainapp.apps import MainappConfig

import mainapp.views as mainapp

app_name = MainappConfig.name

urlpatterns = [
    re_path(r'^$', mainapp.products, name='index'),
    # re_path(r'^$', mainapp.ProductsListView.as_view(), name='index'),

    re_path(r'^category/(?P<pk>\d+)/$', mainapp.products, name='category'),
    # re_path(r'^category/(?P<pk>\d+)/$', mainapp.ProductsListView.as_view(), name='category'),

    re_path(r'^category/(?P<pk>\d+)/page/(?P<page>\d+)/$', mainapp.products, name='page'),
    # re_path(r'^category/(?P<pk>\d+)/page/', mainapp.ProductsListView.as_view(), name='page'),

    re_path(r'^product/(?P<pk>\d+)/$', mainapp.product, name='product'),
]
