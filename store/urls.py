from django.urls import path
from .views import *

urlpatterns = [
    path('', store_index, name='store_index'),
    path('list/', GameListView.as_view(), name='game_list'),
    path('game/<int:game_id>', GameDetailView.as_view(), name='game_detail'),
    path('game/create', GameCreateView.as_view(), name='game_create'),
    path('game/update/<int:game_id>', GameUpdateView.as_view(), name='game_update'),
    path('game/delete/<int:game_id>', GameDeleteView.as_view(), name='game_delete'),
    path('auth/registration', auth_registration, name='auth_registration'),
    path('auth/login', auth_login, name='auth_login'),
    path('auth/logout', auth_logout, name='auth_logout'),
    path('contact/feedback/', contact_feedback, name='contact_feedback'),
    path('contact/newsletter/', contact_newsletter, name='contact_newsletter'),
    path('contact/success/', contact_success, name='contact_success'),
    path('api/game/list/', api_game_list, name='api_game_list'),
    path('api/game/detail/<int:pk>', api_game_detail, name='api_game_detail'),

]

