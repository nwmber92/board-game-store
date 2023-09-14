from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from store.models import Game
from store.serializers import GameSerializer


class GameApiTestCase(APITestCase):

    def setUp(self):
        self.game = Game.objects.create(
            title='Тестовая игра',
            short_description='Краткое описание',
            description='Полное описание',
            rules='Правила игры',
            price=100,
            exist=True
        )

    def test_game_list(self):
        url = reverse('api_game_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_game(self):
        url = reverse('api_game_list')
        data = {
            'title': 'Новая игра',
            'short_description': 'Новое краткое описание',
            'description': 'Новое полное описание',
            'rules': 'Новые правила игры',
            'price': 200,
            'exist': True
        }
        serializer = GameSerializer(data=data)
        serializer.is_valid()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.count(), 2)

    def test_game_detail(self):
        url = reverse('api_game_detail', args=[self.game.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.game.title)

    def test_update_game(self):
        url = reverse('api_game_detail', args=[self.game.pk])
        data = {
            'title': 'Обновленная игра',
            'short_description': 'Обновленное краткое описание',
            'description': 'Обновленное полное описание',
            'rules': 'Обновленные правила игры',
            'price': 300,
            'exist': False
        }
        serializer = GameSerializer(self.game, data=data)
        serializer.is_valid()
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Данные успешно изменены')
        self.game.refresh_from_db()
        self.assertEqual(self.game.title, 'Обновленная игра')

    def test_delete_game(self):
        url = reverse('api_game_detail', args=[self.game.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Game.objects.count(), 0)
