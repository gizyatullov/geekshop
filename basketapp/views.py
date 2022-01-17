from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string

from basketapp.models import Basket
from mainapp.models import Product


# Create your views here.


@login_required
def basket(request):
    context = {
        'page_title': 'корзина',
        'basket_items': Basket.objects.filter(user=request.user).order_by('product__category'),
        'media_url': settings.MEDIA_URL,
    }

    return render(request, 'basketapp/basket.html', context=context)


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        print(f'{pk} - {quantity}')
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        context = {
            'basket_items': basket_items,
            'media_url': settings.MEDIA_URL,
        }

        # result = render_to_string('basketapp/includes/include__basket_list.html', context=context)
        basket_summary = render_to_string('basketapp/includes/include__basket_summary.html', context=context)

        return JsonResponse({'basket_summary': basket_summary,
                             'basket_pk': pk,
                             'value': basket_items.get(pk=pk).get_product_cost})
