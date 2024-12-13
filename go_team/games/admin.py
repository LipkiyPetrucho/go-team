from django.contrib import admin

from games.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['sport', 'max_players', 'location', 'created_at',]
    list_filter = ['created_at']