# Create your models here.

from django.db import models
from django.contrib.postgres.fields import JSONField
from datetime import date, datetime


class Game(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    peak_date = models.DateField(default=date.today)
    max_users = models.IntegerField(default=0)


class Player(models.Model):
    id = models.CharField(primary_key=True, max_length=17)
    nickname = models.CharField(max_length=100, blank=True)
    avatar = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        from app.players_updater import PlayersUpdater
        PlayersUpdater.update_nicknames_and_avatars([self.id])
        super(Player, self).save(*args, **kwargs)


class GlobalStats(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    users = models.IntegerField()
    date = models.DateTimeField(default=datetime.today)


class Achievement(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    achievement = models.CharField(max_length=200)
    global_percent = models.FloatField()


class PlayerAchievement(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    achieved = models.BooleanField()
    unlock_time = models.DurationField()


class PlayerStats(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    time = models.DurationField()
    date = models.DateField(default=date.today)
    stats = JSONField()

