from django.db import models
from user.models import get_adjusted_name

class AuthorName(models.Model):

    def get_name(caller=None, user=None):
        return get_adjusted_name(user)

    class Meta:
        abstract = True

