from django.contrib import admin
from django.urls import path
from client import views

urlpatterns = [
    path('index/', views.index),
    path('detail/', views.detail),
    path('type/', views.type),
]