from django.contrib import admin
from django.forms import Textarea
from django.db import models

from .models import Object, Description, Contribution


class ObjectAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})}
    }

admin.site.register(Object, ObjectAdmin)
admin.site.register(Description)
admin.site.register(Contribution)
