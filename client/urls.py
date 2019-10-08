from django.contrib import admin
from django.urls import path
from client import views

urlpatterns = [
    path('index/', views.index),
    path('indexArticleList/', views.indexArticleList),
    path('detail/', views.detail),
    path('detailHandle/', views.detailHandle),
    path('type/', views.type),
    path('typeList/', views.typeList),
    path('rightAd/', views.rightAd),
]