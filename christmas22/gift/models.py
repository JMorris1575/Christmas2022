from django.db import models
from django.conf import settings

from base_classes import AuthorName
from user.models import get_adjusted_name

import os


class Gift(models.Model):
    gift_number = models.SmallIntegerField()
    description = models.TextField()
    wrapped = models.BooleanField(default=True)
    selected = models.BooleanField(default=False)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['gift_number']

    def __str__(self):
        return 'Gift ' + str(self.gift_number)

    def get_image_filename(self):
        if self.wrapped:
            status = 'wrapped'
        else:
            status = 'unwrapped'
        return os.path.join('gift', 'images', status, str(self) + '.png')

    def get_thumbnail_filename(self):
        if self.wrapped:
            status = 'wrapped'
        else:
            status = 'unwrapped'
        return os.path.join('gift', 'images', status, 'thumbnails', str(self) + '.png')

    def get_comments(self):
        comments = Comment.objects.filter(gift=self)
        return comments

    def receiver_name(self):
        return get_adjusted_name(self.receiver)


class Comment(AuthorName):
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        if len(self.comment) > 10:
            return self.comment[0:9] + '...'
        else:
            return self.comment

    def display(self):
        prefix = self.get_name(self.user) + ' says: '
        return prefix + self.comment