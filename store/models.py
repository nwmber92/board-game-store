from django.db import models
from django.urls import reverse


class Game(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    short_description = models.TextField(blank=True, null=True, verbose_name='Краткое описание')
    description = models.TextField(blank=True, null=True, verbose_name='Полное описание')
    rules = models.TextField(blank=True, null=True, verbose_name='Правила игры')
    price = models.IntegerField(verbose_name='Цена')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    image = models.ImageField(upload_to='image/game/', blank=True, null=True, verbose_name='Изображение')
    exist = models.BooleanField(default=True, verbose_name='Наличие')

    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'game_id': self.pk})

    class Meta:
        verbose_name = 'Игру'
        verbose_name_plural = 'Игры'
        ordering = ['title', 'id']
