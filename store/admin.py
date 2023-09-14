from django.contrib import admin
from .models import Game


class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'exist')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'price')
    list_editable = ('price', 'exist')
    list_filter = ('price',)
    ordering = ['pk']


admin.site.register(Game, GameAdmin)
