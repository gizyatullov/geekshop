from django.shortcuts import render

from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView

from basketapp.models import Basket
from .forms import OrderItemForm
from .models import Order, OrderItem


# Create your views here.


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset


class OrderItemsCreate(CreateView):
    model = Order
    fields = ()
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.get_items(self.request.user)
            if length_basket := len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=length_basket)
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
            else:
                formset = OrderFormSet()

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            # Delete items in basket after order creating only
            Basket.objects.filter(user=self.request.user).delete()

        # Delete empty order
        if self.object.get_total_cost() == 0:
            self.object.delete()

        switch = super(OrderItemsCreate, self).form_valid(form)
        return switch


class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context['page_title'] = 'заказ/просмотр'
        return context


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = ()
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            context['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            context['orderitems'] = OrderFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # Delete empty order
        if self.object.get_total_cost() == 0:
            self.object.delete()

        switch = super().form_valid(form)
        return switch


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:orders_list'))
