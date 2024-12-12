from django import forms
from django.forms import Select, NumberInput, Textarea

from games.models import Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            "sport",
            "max_players",
            "location",
            "start_time",
            "duration",
            "price",
            "description",
            "image",
        ]
        labels = {
            "sport": "Вид спорта",
            "location": "Место игры",
            "start_time": "Время начала игры",
            "duration": "Продолжительность",
            "max_players": "Количество игроков",
            "price": "Цена игры",
            "description": "Описание",
            "image": "Обложка",
        }

        widgets = {
            "sport": Select(),
            "max_players": NumberInput(attrs={"step": "1"}),
            "description": Textarea(
                attrs={
                    "cols": 30,
                    "rows": 3,
                    "placeholder": "Опишите например: есть душевые, есть парковочные места",
                    "aria-label": "default input example",
                }
            ),
            "price": NumberInput(attrs={"step": "10"}),
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "duration": forms.TimeInput(attrs={"type": "time"}),
        }
