from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.decorators import method_decorator
from django.core import mail
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Game
from .forms import GameForm, RegistrationForm, LoginForm, FeedbackForm, NewsletterForm
from .serializers import GameSerializer
from cart.cart import Cart
from cart.forms import CartAddItemForm


def store_index(request):
    return render(request, 'index.html')


class GameListView(ListView):
    model = Game
    paginate_by = 2
    ordering = ['-date_create']
    template_name = 'game/list.html'
    context_object_name = 'game_list'


class GameDetailView(DetailView):
    model = Game
    template_name = 'game/detail.html'
    context_object_name = 'game'
    pk_url_kwarg = 'game_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        item_obj = self.get_object()

        # Получаем количество копий товара в корзине и передаем его в селектор
        cart_item_count = cart.cart.get(str(item_obj.pk), {}).get('count_item', 0)
        cart_form = CartAddItemForm(cart_item_count=cart_item_count)
        context['cart_form'] = cart_form
        return context


class GameCreateView(CreateView):
    model = Game
    form_class = GameForm
    template_name = 'game/create.html'
    context_object_name = 'form'
    success_url = reverse_lazy('game_list')

    @method_decorator(permission_required('store.change_game'))
    def dispatch(self, request, *args, **kwargs):
        context = super().dispatch(request, *args, **kwargs)
        return context


class GameUpdateView(UpdateView):
    model = Game
    form_class = GameForm
    template_name = 'game/update.html'
    context_object_name = 'form'
    success_url = reverse_lazy('game_list')
    pk_url_kwarg = 'game_id'

    @method_decorator(permission_required('store.change_game'))
    def dispatch(self, request, *args, **kwargs):
        context = super().dispatch(request, *args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем идентификатор игры из URL-параметров и добавляем ее заголовок в контекст
        game_id = self.kwargs['game_id']
        context['title'] = Game.objects.get(pk=game_id)

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        game = self.object
        cart = Cart(self.request)
        cart.update_price(game)
        return response


class GameDeleteView(DeleteView):
    model = Game
    success_url = reverse_lazy('game_list')
    pk_url_kwarg = 'game_id'

    @method_decorator(permission_required('store.change_game'))
    def dispatch(self, request, *args, **kwargs):
        context = super().dispatch(request, *args, **kwargs)
        return context


def auth_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store_index')
    else:
        form = RegistrationForm

    return render(request, 'auth/registration.html', {'form': form})


def auth_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('store_index')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


def auth_logout(request):
    logout(request)
    return redirect('store_index')


# Имитируем отправку писем и выводим содержимое в консоль
def contact_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            with mail.get_connection() as connection:
                mail.EmailMessage(
                    form.cleaned_data['subject'],
                    form.cleaned_data['body'],
                    settings.EMAIL_HOST_USER,
                    ['subject@mail.com'],
                    connection=connection,
                ).send()

                sent_messages = mail.outbox
                for message in sent_messages:
                    print(message.subject)
                    print(message.body)
                    print(message.from_email)
                    print(message.to)

            return redirect('contact_success')
    else:
        form = FeedbackForm()

    return render(request, 'contact/feedback.html', {'form': form})


def contact_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            with mail.get_connection() as connection:
                mail.EmailMessage(
                    'Интернет-магазин настольных игр',
                    'Вы подписались на рассылку!',
                    settings.EMAIL_HOST_USER,
                    [form.cleaned_data['email']],
                    connection=connection,
                ).send()

                sent_messages = mail.outbox
                for message in sent_messages:
                    print(message.subject)
                    print(message.body)
                    print(message.from_email)
                    print(message.to)

            return redirect('contact_success')
    else:

        # Достаем email пользователя и помещаем в форму
        if request.user.is_authenticated:
            user_email = request.user.email
            form = NewsletterForm(initial={'email': user_email})
        else:
            form = NewsletterForm()

    return render(request, 'contact/newsletter.html', {'form': form})


def contact_success(request):
    return render(request, 'contact/success.html')


@api_view(['GET', 'POST'])
def api_game_list(request):
    if request.method == 'GET':
        game_list = Game.objects.all()
        serializer = GameSerializer(game_list, many=True)
        return Response({'game_list': serializer.data})
    elif request.method == 'POST':
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def api_game_detail(request, pk):
    game_obj = get_object_or_404(Game, pk=pk)
    if game_obj.exist:
        if request.method == 'GET':
            serializer = GameSerializer(game_obj)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = GameSerializer(game_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Данные успешно изменены', 'game': serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            game_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
