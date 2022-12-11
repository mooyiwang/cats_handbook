from . import views
# from django.conf.urls import url
from django.urls import path, re_path

urlpatterns = [
    path('', views.home),
    re_path(r'cat$', views.show_cat),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('checkcat/', views.checkcat),
    path('feed/', views.feed),
    path('stat/', views.stat),
]