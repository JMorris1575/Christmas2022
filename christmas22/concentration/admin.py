from django.contrib import admin

from .models import ConcentrationPlayer, ConcentrationComment


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['user', 'level']
    ordering = ['user']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment']
    ordering = ['user']


admin.site.register(ConcentrationPlayer, PlayerAdmin)
admin.site.register(ConcentrationComment, CommentAdmin)
