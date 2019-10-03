from django.contrib import admin
from django.urls import path
from server import views

urlpatterns = [
    path('serverIndex/', views.index),
    path("clearAdminInfo/",views.clearAdminInfo),
    path("menu/",views.menu),
    path("addmenu/",views.addmenu),
    path("login/",views.login),
    path("savemenu/",views.savemenu),
    path("loginCheck/",views.loginCheck),
    path("articleList/",views.articleList),
    path("addArticle/",views.addArticle),
    path("adminList/",views.adminList),
    path("addAdmin/",views.addAdmin),
    path("positionList/",views.positionList),
    path("addPosition/",views.addPosition),
    path("positionContentList/",views.positionContentList),
]