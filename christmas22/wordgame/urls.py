from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .views import (ScoreboardView, DailyScoreView, EntryView, CheckView,
                    VerifyView, EditCommentView, DeleteCommentView,)

app_name = 'wordgame'

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('wordgame:scoreboard'))),
    path('scoreboard/', login_required(ScoreboardView.as_view()), name='scoreboard'),
    path('daily_scores/', login_required(DailyScoreView.as_view()), name='daily_scores'),
    path('entry', login_required(EntryView.as_view()), name='entry'),
    path('check', login_required(CheckView.as_view()), name='check'),
    path('verify', login_required(VerifyView.as_view()), name='verify'),
    path('edit_comment/<int:comment_id>/', login_required(EditCommentView.as_view()), name="edit_comment"),
    path('delete_comment/<int:comment_id>/', login_required(DeleteCommentView.as_view()), name="delete_comment")
]