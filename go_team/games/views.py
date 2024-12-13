from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from games.forms import GameForm
from games.models import Game


@login_required
def game_list(request):
    games = Game.objects.all().order_by('start_time')
    for game in games:
        game.update_status()
    return render(request, "games/game_list.html", {"games": games})


@login_required
def game_detail(request, pk):
    now = timezone.now()
    game = get_object_or_404(Game, pk=pk)
    game.update_status()
    return render(request, "games/game_detail.html", {"game": game, 'now': now})


@login_required
def game_create(request):
    if request.method == "POST":
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            game = form.save(commit=False)
            game.created_by = request.user
            game.save()
            if 'image' in request.FILES:
                game.image = request.FILES['image']
                game.save()
            messages.success(request, "Игра успешно создана.")
            return redirect("games:game_detail", pk=game.pk)
    else:
        form = GameForm()
    return render(request, "games/game_form.html", {"form": form})


@login_required
def game_update(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.user != game.created_by:
        messages.error(request, "У вас нет прав на редактирование этой игры.")
        return redirect("games:game_detail", pk=game.pk)
    if request.method == "POST":
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, "Игра успешно обновлена.")
            return redirect("games:game_detail", pk=game.pk)
    else:
        form = GameForm(instance=game)
    return render(request, "games/game_form.html", {"form": form})


@login_required
def game_delete(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.user != game.created_by:
        messages.error(request, "У вас нет прав на удаление этой игры.")
        return redirect("game_detail", pk=game.pk)
    if request.method == "POST":
        game.delete()
        messages.success(request, "Игра успешно удалена.")
        return redirect("games:game_list")
    return render(request, "games/game_confirm_delete.html", {"game": game})


@login_required
def game_join(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if game.players.count() >= game.max_players:
        messages.error(request, "Максимальное количество игроков достигнуто.")
    elif request.user in game.players.all():
        messages.info(request, "Вы уже присоединились к этой игре.")
    else:
        game.players.add(request.user)
        game.save()
        game.refresh_from_db()
        messages.success(request, "Вы присоединились к игре.")
    return redirect("games:game_detail", pk=game.pk)


@login_required
def game_leave(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.user not in game.players.all():
        messages.error(request, "Вы не присоединились к этой игре.")
    else:
        game.players.remove(request.user)
        game.save()
        game.refresh_from_db()
        messages.success(request, "Вы покинули игру.")
    return redirect("games:game_detail", pk=game.pk)