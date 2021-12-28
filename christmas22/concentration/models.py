from django.db import models
from django.conf import settings

from user.models import get_adjusted_name


class ConcentrationPlayer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)

    def __str__(self):
        return get_adjusted_name(self.user) + ' Level: ' + str(self.level)


class ConcentrationComment(models.Model):
    comment = models.CharField(max_length=512)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment



