from django.db import models
from django.conf import settings

from user.models import get_adjusted_name

class Minor(models.Model):
    minor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    father = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='father_of_minor', on_delete=models.CASCADE)
    mother = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='mother_of_minor', on_delete=models.CASCADE)

    def __str__(self):
        return get_adjusted_name(self.minor)

