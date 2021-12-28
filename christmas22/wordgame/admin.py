from django.contrib import admin

from .models import ChristmasWord, PlayerWord, WordComment, GameComment

class ChristmasWordAdmin(admin.ModelAdmin):
    list_display = ['sequence_number', 'word', 'date_published']
    ordering = ['sequence_number']

admin.site.register(ChristmasWord, ChristmasWordAdmin)
admin.site.register(PlayerWord)
admin.site.register(WordComment)
admin.site.register(GameComment)


