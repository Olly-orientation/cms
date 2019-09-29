from django.contrib import admin
from django.urls import path
from server import views

urlpatterns = [
    path('serverIndex/', views.index),
    path("menu/",views.menu)
]