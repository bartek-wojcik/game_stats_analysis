# Create your models here.

from django.db import models
from django.contrib.postgres.fields import JSONField
from datetime import date, datetime


class Game(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    peak_date = models.DateField(default=date.today)
    max_users = models.IntegerField(default=0)
    average_playtime = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    id = models.CharField(primary_key=True, max_length=17)
    nickname = models.CharField(max_length=100, blank=True)
    avatar = models.URLField(blank=True)

    def __str__(self):
        return self.nickname


class GlobalStats(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    users = models.IntegerField()
    date = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return self.game.__str__() + ' ' + self.date.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        verbose_name_plural = 'Global stats'


class Achievement(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    global_percent = models.FloatField(default=0)
    icon = models.URLField(null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    display_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.game.__str__() + ' ' + self.name

    class Meta:
        index_together = (
            ('game', 'name')
        )


class PlayerAchievement(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    achieved = models.BooleanField()

    def __str__(self):
        return self.player.__str__() + ' ' + self.achievement.__str__()


class PlayerStats(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    time = models.DurationField()
    date = models.DateField(default=date.today)
    stats = JSONField()

    def __str__(self):
        return self.game.__str__() + ' ' + self.player.__str__()

    class Meta:
        verbose_name_plural = 'Player stats'


class AchievementsOverTime(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    time = models.DurationField()
    achievements = models.IntegerField()

    def __str__(self):
        return self.game.__str__() + ' ' + self.player.__str__()

    class Meta:
        verbose_name_plural = 'Achievements over time'
