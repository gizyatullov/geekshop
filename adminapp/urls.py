from django.urls import path

import adminapp.views as adminapp

from .apps import AdminappConfig

app_name = AdminappConfig.name

urlpatterns = [
    path('', adminapp.AdminMainRedirectView.as_view(), name='admin_main'),

    path('users/read/', adminapp.UsersListView.as_view(), name='users'),

    # path('users/create/', adminapp.user_create, name='user_create'),
    path('users/create/', adminapp.UserCreateCreateView.as_view(), name='user_create'),

    # path('users/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('users/update/<int:pk>/', adminapp.UserUpdateView.as_view(), name='user_update'),

    # path('users/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),
    path('users/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),

    # path('categories/read/', adminapp.categories, name='categories'),
    path('categories/read/', adminapp.CategoriesListView.as_view(), name='categories'),

    path('categories/create/', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.ProductCategoryDeleteView.as_view(), name='category_delete'),

    path('products/create/category/<int:pk>/', adminapp.product_create, name='product_create'),

    # List of products in category
    path('products/read/category/<int:pk>/', adminapp.products, name='products'),
    path('products/read/category/<int:pk>/<int:page>/', adminapp.products, name='page_products'),
    # path('products/read/category/<int:pk>/', adminapp.ProductsListView.as_view(), name='products'),

    # Detail page of product
    path('products/read/<int:pk>/', adminapp.ProductDetailView.as_view(), name='product_read'),

    # path('products/update/<int:pk>/', adminapp.product_update, name='product_update'),
    path('products/update/<int:pk>/', adminapp.ProductUpdateView.as_view(), name='product_update'),

    # path('products/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),
    path('products/delete/<int:pk>/', adminapp.ProductDeleteView.as_view(), name='product_delete'),
]
