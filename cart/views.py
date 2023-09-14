from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CartAddItemForm
from store.models import Game


@require_POST
def cart_add(request, item_id):
    cart = Cart(request)
    item_obj = get_object_or_404(Game, pk=item_id)
    cart_item_count = cart.cart.get(str(item_id), {}).get('count_item', 0)
    form = CartAddItemForm(cart_item_count=cart_item_count, data=request.POST)

    if form.is_valid():
        cart_info = form.cleaned_data
        cart.add(item=item_obj,
                 count_item=cart_info['count_item'],
                 update_count=cart_info['update'])

    return redirect('cart_detail')


def cart_remove(request, item_id):
    cart = Cart(request)
    item_obj = get_object_or_404(Game, pk=item_id)
    cart.remove(item_obj)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')
