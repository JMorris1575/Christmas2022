from django.db import models
from django.conf import settings

from base_classes import AuthorName


class Memory(AuthorName):
    memory = models.TextField(max_length=400)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.memory

    def author(self):
        return 'Memory from ' + self.get_name(self.user) + ':'
