from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from django.urls import reverse_lazy

from .views import MemoryListView, MemoryEditView, MemoryDeleteView

app_name = 'memory'

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('memory:memory_list'))),
    path('collection/', login_required(MemoryListView.as_view()), name='memory_list'),
    path('create/', login_required(MemoryEditView.as_view()), name='create'),
    path('edit/<int:memory_id>', login_required(MemoryEditView.as_view()), name='edit'),
    path('delete/<int:memory_id>', login_required(MemoryDeleteView.as_view()), name='delete'),
]