from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import SendMail

app_name = 'mail'

urlpatterns = [
    path('', login_required(SendMail.as_view()), name='send-mail'),
]