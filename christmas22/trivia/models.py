from django.db import models
from django.conf import settings

from user.models import get_adjusted_name


class TriviaQuestion(models.Model):
    number = models.IntegerField(unique=True)
    text = models.TextField()
    publish = models.BooleanField(default=False)
    attempted_count = models.IntegerField(default=0)
    correct_count = models.IntegerField(default=0)
    explanation = models.CharField(max_length=255, default="", blank=True)
    link = models.URLField(default="", blank=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['number']


class TriviaChoice(models.Model):
    question = models.ForeignKey(TriviaQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


    class Meta:
        ordering = ['pk']


class TriviaResponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(TriviaQuestion, on_delete=models.CASCADE)
    response = models.ForeignKey(TriviaChoice, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    def __str__(self):
        text = get_adjusted_name(self.user) + ' responded ' + \
               str(self.response) + ' to question ' + str(self.question.number)
        return text


    class Meta:
        ordering = ['question']


class TriviaConversation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    entry = models.CharField(max_length = 300)

    def __str__(self):
        return get_adjusted_name(self.user) + ': ' + self.entry
