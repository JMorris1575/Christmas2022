from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .views import PortalView, GameView, ScoreView, EditCommentView, DeleteCommentView

app_name = 'concentration'

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('concentration:game'))),
    path('portal/', login_required(PortalView.as_view()), name='portal'),
    path('game/', login_required(GameView.as_view()), name='game'),
    # path('get_player_info/', login_required(Info_View.as_view()), name='info'),
    path('scores/', login_required(ScoreView.as_view()), name='scores'),
    path('edit_comment/<int:comment_id>/', login_required(EditCommentView.as_view()), name="edit_comment"),
    path('delete_comment/<int:comment_id>/', login_required(DeleteCommentView.as_view()), name="delete_comment")
]