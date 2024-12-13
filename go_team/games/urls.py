from django.urls import path

from games.views import game_list, game_create, game_detail, game_update, game_delete, \
    game_join, game_leave

app_name = 'games'

urlpatterns = [
    path("", game_list, name="game_list"),
    path("create/", game_create, name="game_create"),
    path("<int:pk>/", game_detail, name="game_detail"),
    path("<int:pk>/edit/", game_update, name="game_edit"),
    path("<int:pk>/delete/", game_delete, name="game_delete"),
    path("<int:pk>/join/", game_join, name="game_join"),
    path("<int:pk>/leave/", game_leave, name="game_leave"),
]
