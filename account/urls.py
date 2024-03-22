
from django.urls import path, re_path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('manage/', views.manage_account, name='manage'),
    re_path(r'^(?P<username>[^/]+)/myaccount/$', views.manage_account, name='manage_account'),
]
