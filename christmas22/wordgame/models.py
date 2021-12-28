from django.db import models
from django.conf import settings
from django.utils import timezone

from user.models import get_adjusted_name


class ChristmasWord(models.Model):
    word = models.CharField(max_length=25)
    sequence_number = models.IntegerField(unique=True)
    date_published = models.DateField(default=timezone.now)
    finalized = models.BooleanField(default=False)

    def __str__(self):
        return self.word

    class Meta():
        ordering = ['sequence_number']

class PlayerWord(models.Model):
    word = models.CharField(max_length=25)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_word = models.ForeignKey(ChristmasWord, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    explanation = models.CharField(max_length=50, default='', blank=True)

    def __str__(self):
        return self.word


class WordComment(models.Model):
    comment = models.CharField(max_length=512)
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    daily_word = models.ForeignKey(ChristmasWord, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment


class GameComment(models.Model):
    comment = models.CharField(max_length=512)
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
