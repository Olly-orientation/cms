from django.contrib import admin
from django.urls import path
from server import views

urlpatterns = [
    path('serverIndex/', views.index),
    path("menu/",views.menu),
    path("addmenu/",views.addmenu),
    path("login/",views.login),
    path("savemenu/",views.savemenu),
    path("loginCheck/",views.loginCheck)
]