from django.conf import settings
from store.models import Game


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __len__(self):
        return sum(int(item['count_item']) for item in self.cart.values())

    def __iter__(self):
        list_item_pk = self.cart.keys()
        list_item_obj = Game.objects.filter(pk__in=list_item_pk)
        cart = self.cart.copy()

        for item_obj in list_item_obj:
            cart[str(item_obj.pk)]['game'] = item_obj

        for item in cart.values():
            total_price = float(item['price_item']) * int(item['count_item'])
            item['total_price'] = int(total_price)
            yield item

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart

    def add(self, item, count_item=1, update_count=False):
        item_pk = str(item.pk)
        if item_pk not in self.cart:
            self.cart[item_pk] = {
                'count_item': 0,
                'price_item': str(item.price)
            }
        if update_count:
            self.cart[item_pk]['count_item'] = min(count_item, 5)
        else:
            self.cart[item_pk]['count_item'] = count_item
        self.save()

    def remove(self, item):
        item_pk = str(item.pk)
        if item_pk in self.cart:
            del self.cart[item_pk]
            self.save()

    def get_total_price(self):
        total_price = sum(float(item['price_item']) * int(item['count_item']) for item in self.cart.values())
        return int(total_price)

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def update_price(self, item):
        item_pk = str(item.pk)
        if item_pk in self.cart:
            self.cart[item_pk]['price_item'] = str(item.price)
            self.cart[item_pk]['total_price'] = float(self.cart[item_pk]['price_item']) * int(
                self.cart[item_pk]['count_item'])
            self.save()
