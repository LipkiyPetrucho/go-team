from django import forms
from django.forms import Select, NumberInput, Textarea, TextInput, ClearableFileInput

from games.models import Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            "sport",
            "location",
            "start_time",
            "duration",
            "max_players",
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
            'location': TextInput(),
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "duration": forms.TimeInput(attrs={"type": "time"}),
            "max_players": NumberInput(attrs={"step": "1"}),
            "price": NumberInput(attrs={"step": "10"}),
            "description": Textarea(
                attrs={
                    "cols": 30,
                    "rows": 3,
                    "placeholder": "Опишите например: есть душевые, есть парковочные места",
                    "aria-label": "default input example",
                }
            ),
            'image': ClearableFileInput()
        }
