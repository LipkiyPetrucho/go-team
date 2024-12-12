from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from games.api.serializers import GameSerializer
from games.models import Game


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Позволяет редактировать объекты только их создателю.
    """

    def has_object_permission(self, request, view, obj):
        # Безопасные методы (GET, HEAD, OPTIONS) разрешены
        if request.method in permissions.SAFE_METHODS:
            return True
        # Только создатель может изменять
        return obj.created_by == request.user


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def join(self, request, pk=None):
        game = self.get_object()
        if game.players.count() >= game.max_players:
            return Response(
                {"error": "Maximum number of players reached."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.user in game.players.all():
            return Response(
                {"message": "You are already in the game."}, status=status.HTTP_200_OK
            )
        game.players.add(request.user)
        game.save()
        return Response(
            {"message": "You have joined the game."}, status=status.HTTP_200_OK
        )

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def leave(self, request, pk=None):
        game = self.get_object()
        if request.user not in game.players.all():
            return Response(
                {"error": "You are not in the game."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        game.players.remove(request.user)
        game.save()
        return Response(
            {"message": "You have left the game."}, status=status.HTTP_200_OK
        )
