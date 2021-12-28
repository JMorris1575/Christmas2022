from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .views import (ScoreboardView, NextQuestionView, DisplayQuestionView, DisplayResultView, FinishedView,
                    previous_question_view, next_question_view, save_trivia_view)

app_name = 'trivia'

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('trivia:scoreboard'))),
    path('scoreboard/', login_required(ScoreboardView.as_view()), name='scoreboard'),
    path('question/', login_required(NextQuestionView.as_view()), name='next_question'),
    path('finished/', login_required(FinishedView.as_view()), name='finished'),
    path('question/<int:question_number>/', login_required(DisplayQuestionView.as_view()), name='display_question'),
    path('result/<int:question_number>/<int:choice_id>/', login_required(DisplayResultView.as_view()), name='result'),
    path('previous/<int:question_number>/', login_required(previous_question_view), name='previous'),
    path('next/<int:question_number>/', login_required(next_question_view), name='next'),
    path('save/', login_required(save_trivia_view), name='save_files')
]