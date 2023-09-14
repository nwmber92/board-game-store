from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game

        fields = ['title', 'short_description', 'description', 'rules', 'price', 'image', 'exist']

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Название игры',
                }
            ),
            'short_description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Краткое описание',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Полное описание',
                }
            ),
            'rules': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Правила игры',
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Цена',
                }
            ),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Придумайте уникальное имя',
                   }),
        min_length=4,
        max_length=8,
        help_text='Не менее 4 символов',
    )
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Укажите почту для связи',
                   }),
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Придумайте надежный пароль',
                   }),
        min_length=4,
        max_length=12,
        help_text='Не менее 4 символов',
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Повторите пароль',
                   }),
        min_length=4,
        max_length=12,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Введите логин',
                   }),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Введите пароль',
                   }),
    )


class FeedbackForm(forms.Form):
    subject = forms.CharField(
        label='Тема:',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Укажите тему',
                   }),
    )
    body = forms.CharField(
        label='Сообщение:',
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'placeholder': 'Напишите о своей проблеме или пожелании',
                   'rows': 11,
                   }),
    )


class NewsletterForm(forms.Form):
    email = forms.CharField(
        label='Укажите email, на который хотите получать уведомления:',
        widget=forms.EmailInput(
            attrs={'class': 'form-control',
                   'placeholder': 'example@mail.ru',
                   }),
    )
