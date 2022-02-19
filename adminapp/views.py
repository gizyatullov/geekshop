from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F

from authnapp.models import ShopUser
from mainapp.models import ProductCategory, Product

from .forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authnapp.forms import ShopUserRegisterForm

from django.views.generic import RedirectView

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.


class AdminMainRedirectView(LoginRequiredMixin, RedirectView):
    url = 'admin:users'


class UsersListView(LoginRequiredMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersListView, self).get_context_data(object_list=None, **kwargs)
        context['page_title'] = 'админка/пользователи'
        context['media_url'] = settings.MEDIA_URL
        return context

    def get_queryset(self):
        queryset = super(UsersListView, self).get_queryset()
        queryset = queryset.order_by('-is_active', '-is_superuser', '-is_staff', 'username')
        return queryset


class UserCreateCreateView(LoginRequiredMixin, CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = 'пользователи/создание'
        context['media_url'] = settings.MEDIA_URL
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = ShopUser
    form_class = ShopUserAdminEditForm
    template_name = 'adminapp/user_update.html'

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = 'пользователи/редактирование'
        context['media_url'] = settings.MEDIA_URL
        return context

    def get_success_url(self):
        user_item = ShopUser.objects.get(pk=self.kwargs.get('pk'))
        return reverse('admin:user_update', args=[user_item.pk])


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'пользователи/удаление'
        context['media_url'] = settings.MEDIA_URL
        return context


class CategoriesListView(LoginRequiredMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'пользователи/категории'
        context['media_url'] = settings.MEDIA_URL
        return context


class ProductCategoryCreateView(LoginRequiredMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'категории/создание'
        context['media_url'] = settings.MEDIA_URL
        return context


class ProductCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = 'категории/редактирование'
        context['media_url'] = settings.MEDIA_URL
        return context

    def get_success_url(self):
        return reverse('admin:category_update', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                # print(f'применяется скидка {discount}% к товарам категории {self.object.name}')
                self.object.product_set.update(price=F('price') * (1 - discount / 100))

        return super().form_valid(form)


class ProductCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'категории/удаление'
        context['media_url'] = settings.MEDIA_URL
        return context


class ProductsListView(LoginRequiredMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'админка/продукт'
        context['media_url'] = settings.MEDIA_URL
        context['object'] = ProductCategory.objects.get(pk=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        product_list = Product.objects.filter(category__pk=self.kwargs.get('pk')).order_by('name')
        paginator = Paginator(product_list, 2)
        page = self.kwargs.get('page') or 1
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        return object_list


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'продукт/подробнее'
        context['media_url'] = settings.MEDIA_URL
        return context


# +-
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_category = ProductCategory.objects.get(pk=self.kwargs.get('pk'))
        context['page_title'] = 'продукт/создание'
        context['media_url'] = settings.MEDIA_URL
        context['object'] = product_category
        context['form'] = ProductEditForm(initial={'category': product_category})
        return context

    def get_success_url(self):
        return reverse('admin:products', args=[self.kwargs.get('pk')])


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'продукт/редактирование'
        context['media_url'] = settings.MEDIA_URL
        return context

    def get_success_url(self):
        return reverse('admin:product_update', args=[self.kwargs.get('pk')])


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'продукт/удаление'
        context['media_url'] = settings.MEDIA_URL
        return context

    def get_success_url(self):
        return reverse('admin:products', args=[self.object.category.pk])
