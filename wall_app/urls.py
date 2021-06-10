from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('wall', views.wall),
    path('message', views.post_message),
    path('comment/<msg_id>', views.post_comment),
    path('destroy', views.destroy),
]