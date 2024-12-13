import logging

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

logger = logging.getLogger(__name__)

class Game(models.Model):
    SPORT_CHOICES = (
        ("football", "футбол"),
        ("tennis", "теннис"),
        ("bowling", "боулинг"),
        ("beach volleyball", "пляжный волейбол"),
        ("volleyball", "волейбол"),
        ("ice hockey", "хоккей на льду"),
        ("chess", "шахматы"),
    )
    STATUS = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("finished", "Finished"),
        ("canceled", "Canceled"),
    ]

    sport = models.CharField(max_length=20, choices=SPORT_CHOICES)
    max_players = models.PositiveIntegerField(default=2)
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default="open")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="games_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    players = models.ManyToManyField(User, related_name="joined_games", blank=True)
    image = models.ImageField(upload_to="game_images/", null=True, blank=True)

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        indexes = [
            models.Index(fields=["created_at"]),
        ]
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sport} game at {self.location} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    @property
    def end_time(self):
        return self.start_time + self.duration

    @property
    def price_per_player(self):
        if self.players.count() > self.max_players:
            return (self.max_players * self.price) / self.players.count()
        elif 1 < self.players.count() < self.max_players:
            return (self.max_players * self.price) / self.players.count()
        else:
            return self.price

    def update_status(self):
        now = timezone.now()
        logger.debug(f"Checking status at {now}. Current status: {self.status}")
        if self.status in ["finished", "canceled"]:
            return
        if now >= self.end_time:
            self.status = "finished"
        elif now >= self.start_time:
            self.status = "in_progress"
        else:
            self.status = "open"
        logger.debug(f"Updated status to: {self.status}")

    def save(self, *args, **kwargs):
        self.update_status()
        super().save(*args, **kwargs)

    # @staticmethod
    # def get_absolute_url():
    #     return reverse("games:detail")
