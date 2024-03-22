from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'closet'

urlpatterns = [
    path('', views.ClosetListView.as_view(), name='closet_list'),  # 显示衣橱列表
    path('add/', views.ClothingCreateView.as_view(), name='clothing_add'),  # 添加衣物
    path('<int:pk>/edit/', views.ClothingUpdateView.as_view(), name='clothing_edit'),  # 编辑衣物
    path('<int:pk>/delete_ajax/', views.ajax_clothing_delete, name='clothing_delete_ajax'),  # 删除衣物
    path('ajax/get_clothing_items/', views.get_clothing_items, name='get_clothing_items'),
    path('get_item_details/', views.get_item_details, name='get_item_details'),

 ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
