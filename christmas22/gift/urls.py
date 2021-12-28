from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from django.urls import reverse_lazy

from .views import GiftListView, ActivityListView, GiftDetailView, GiftSelectView, GiftChangeMindView, \
                    AddCommentView, EditCommentView, DeleteCommentView

app_name = 'gift'

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('gift:home'))),
    path('gift-list/', login_required(GiftListView.as_view()), name="home"),
    path('activities/', login_required(ActivityListView.as_view()), name="activity_index"),
    path('<int:gift_number>/detail/', login_required(GiftDetailView.as_view()), name="gift_detail"),
    path('<int:gift_number>/select/', login_required(GiftSelectView.as_view()), name="select"),
    path('<int:gift_number>/change_mind/', login_required(GiftChangeMindView.as_view()), name="change_mind"),
    path('<int:gift_number>/comment/', login_required(AddCommentView.as_view()), name="add_comment"),
    path('<int:gift_number>/edit_comment/<int:comment_id>/',
         login_required(EditCommentView.as_view()), name="edit_comment"),
    path('<int:gift_number>/delete_comment/<int:comment_id>/',
         login_required(DeleteCommentView.as_view()), name="delete_comment"),
]