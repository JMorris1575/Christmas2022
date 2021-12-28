from django.db import models
from django.conf import settings

from user.models import get_adjusted_name

import os


class Object(models.Model):
    ONE = '1'
    TWO = '2'
    THREE = '3'
    STAGE_CHOICES = (
        (ONE, 'one'),
        (TWO, 'two'),
        (THREE, 'three')
    )
    number = models.SmallIntegerField(unique=True)
    publish = models.BooleanField(default=False)
    stage = models.CharField(max_length=1, choices=STAGE_CHOICES, default=ONE)
    correct_description = models.TextField()

    class Meta:
        ordering = ['number']

    def __str__(self):
        return 'Object ' + str(self.number)

    def description_count(self):
        return len(Description.objects.filter(object=self))

    def image_filename(self):
        return os.path.join('whatsit', 'images', str(self) + '.png')

    def vote_count(self):
        """
        returns the combined number of votes cast on descriptions for this object
        :return: integer
        """
        return len(Contribution.objects.filter(object=self, type=Contribution.VOTE))


class Description(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    votes = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.author.username + "'s description of Object " + str(self.object.number)


class Contribution(models.Model):
    DESCRIPTION = 'DE'
    VOTE = 'VO'
    TYPE_CHOICES = (
        (DESCRIPTION, 'Description'),
        (VOTE, 'Vote')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)

    def __str__(self):
        return self.user.username + "'s " + self.get_type_display() + " for " + str(self.object)

