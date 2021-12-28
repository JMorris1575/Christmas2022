from django.contrib import admin
from django.forms import Textarea
from django.db import models

from .models import TriviaQuestion, TriviaChoice, TriviaResponse, TriviaConversation


class ChoiceInline(admin.StackedInline):
    model = TriviaChoice
    extra = 4

@admin.action(description='Mark selected questions as published')
def make_published(modeladmin, request, queryset):
    queryset.update(publish=True)

@admin.action(description='Mark selected questions as unpublished')
def make_unpublished(modeladmin, request, queryset):
    queryset.update(publish=False)

class TriviaQuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})}
    }
    list_display = ['number', 'text', 'publish']
    ordering = ['number']
    actions = [make_published, make_unpublished]


admin.site.register(TriviaQuestion, TriviaQuestionAdmin)
admin.site.register(TriviaChoice)
admin.site.register(TriviaResponse)                         # for use during development only
admin.site.register(TriviaConversation)