from django.contrib import admin
from django.forms import Textarea
from django.db import models

from .models import Gift, Comment

@admin.action(description='Mark selected gifts as unwrapped')
def unwrap(modeladmin, request, queryset):
    queryset.update(wrapped=False)

@admin.action(description='Mark selected gifts as wrapped')
def wrap(modeladmin, request, queryset):
    queryset.update(wrapped=True)

class GiftAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})}
    }
    list_display = ['gift_number', 'wrapped', 'selected', 'receiver']
    ordering = ['gift_number']
    actions = [unwrap, wrap]

admin.site.register(Gift, GiftAdmin)
admin.site.register(Comment)

admin.site.site_header = "Christmas 2021 Admin"