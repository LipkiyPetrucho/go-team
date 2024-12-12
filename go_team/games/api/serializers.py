from rest_framework import serializers

from games.models import Game
from user.api.serializers import UserSerializer


class GameSerializer(serializers.ModelSerializer):
    end_time = serializers.ReadOnlyField()
    price_per_player = serializers.ReadOnlyField()
    created_by = UserSerializer(read_only=True)
    players = UserSerializer(many=True, read_only=True)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Game
        fields = [
            "id",
            "sport",
            "max_players",
            "location",
            "start_time",
            "duration",
            "total_price",
            "description",
            "status",
            "end_time",
            "price_per_player",
            "created_by",
            "players",
            "image",
        ]
        read_only_fields = ["created_by", "end_time", "price_per_player", "status"]

    def create(self, validated_data):
        # автоматически связывать созданную игру с пользователем, который ее создал
        request = self.context.get("request")
        game = Game.objects.create(created_by=request.user, **validated_data)
        return game

    def update(self, instance, validated_data):
        # Обновление полей, которые могут изменяться пользователем
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
