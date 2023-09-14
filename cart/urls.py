from django.urls import path

from .views import *

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:item_id>', cart_add, name='cart_add'),
    path('remove/<int:item_id>', cart_remove, name='cart_remove'),
    path('clear/', cart_clear, name='cart_clear'),
]