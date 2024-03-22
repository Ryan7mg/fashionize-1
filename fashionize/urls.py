
from django.contrib import admin
from django.template.context_processors import media
from django.urls import path, include
from django.urls.conf import re_path
from django.conf.urls.static import static
from django.conf import settings
from account import views
from closet import views as closet_views
from outfits import views as outfits_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('manage/', views.manage_account, name='manage_account'),
    # path('media/<str:username>/<str:clothing_type>/<str:filename>', closet_views.serve_protected_media, name='serve_protected_media'),
    # path('media/<str:username>/outfit_images/<str:filename>', outfits_views.serve_protected_media, name='serve_protected_media_outfit'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]

urlpatterns += [
    re_path(r'^(?P<username>\w+)/closet/', include('closet.urls')),
    re_path(r'^(?P<username>[^/]+)/myaccount/$', views.manage_account, name='manage_account'),
    re_path(r'^(?P<username>\w+)/dashboard/', include('dashboard.urls')),
    re_path(r'^(?P<username>\w+)/outfits/', include('outfits.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


