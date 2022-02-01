from django.urls import path, re_path

import adminapp.views as adminapp

from .apps import AdminappConfig

app_name = AdminappConfig.name

urlpatterns = [
    re_path(r'^$', adminapp.AdminMainRedirectView.as_view(), name='admin_main'),

    re_path(r'^users/read/$', adminapp.UsersListView.as_view(), name='users'),
    re_path(r'^users/create/$', adminapp.UserCreateCreateView.as_view(), name='user_create'),
    re_path(r'^users/update/(?P<pk>\d+)/$', adminapp.UserUpdateView.as_view(), name='user_update'),
    re_path(r'^users/delete/(?P<pk>\d+)/$', adminapp.UserDeleteView.as_view(), name='user_delete'),

    re_path(r'^categories/read/$', adminapp.CategoriesListView.as_view(), name='categories'),
    re_path(r'^categories/create/$', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    re_path(r'^categories/update/(?P<pk>\d+)/$', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    re_path(r'^categories/delete/(?P<pk>\d+)/$', adminapp.ProductCategoryDeleteView.as_view(), name='category_delete'),

    # List of products in category
    re_path(r'^products/read/category/(?P<pk>\d+)/$', adminapp.ProductsListView.as_view(), name='products'),
    re_path(r'^products/read/category/(?P<pk>\d+)/(?P<page>\d+)/$', adminapp.ProductsListView.as_view(),
            name='page_products'),

    # Detail page of product
    re_path(r'^products/read/(?P<pk>\d+)/$', adminapp.ProductDetailView.as_view(), name='product_read'),
    re_path(r'^products/create/category/(?P<pk>\d+)/$', adminapp.ProductCreateView.as_view(), name='product_create'),
    re_path(r'^products/update/(?P<pk>\d+)/$', adminapp.ProductUpdateView.as_view(), name='product_update'),
    re_path(r'^products/delete/(?P<pk>\d+)/$', adminapp.ProductDeleteView.as_view(), name='product_delete'),
]
