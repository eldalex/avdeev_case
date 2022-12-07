from django.urls import include, re_path
from . import views

urlpatterns = [
    # post views
    re_path(r'^login/$', views.user_login, name='login'),
    re_path(r'^registration/$', views.user_register, name='registration'),
]