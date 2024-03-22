from django.urls import path
from .views import OutfitListView, OutfitCreateView, delete_outfit, OutfitUpdateView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'outfits'

urlpatterns = [
    path('', OutfitListView.as_view(), name='my_outfits'),
    path('create/', OutfitCreateView.as_view(), name='create_outfit'),
    path('<int:pk>/delete/', delete_outfit, name='delete_outfit'),
    path('<int:pk>/edit/', OutfitUpdateView.as_view(), name='update_outfit'),
]
