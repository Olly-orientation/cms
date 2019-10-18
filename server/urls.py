from django.contrib import admin
from django.urls import path
from server import views
urlpatterns = [
    path('serverIndex/', views.index),
    path("clearAdminInfo/",views.clearAdminInfo),
    path("login/",views.login),
    path("menu/",views.menu),
    path("addmenu/",views.addmenu),
    path("delmenu/",views.delMenu),
    path("savemenu/",views.savemenu),
    path("loginCheck/",views.loginCheck),
    path("articleList/",views.articleList),
    path("addArticle/",views.addArticle),
    path("saveArticle/",views.saveArticle),
    path("delArticle/",views.delArticle),
    path('adminList/', views.adminList),
    path('delAdmin/', views.delAdmin),
    path('editAdmin/', views.editAdmin),
    path('editAdminHandle/', views.editAdminHandle),
    path('addAdmin/', views.addAdmin),
    path('addAdminHandle/', views.addAdminHandle),
path("positionList/",views.positionList),
    path("postPosition/",views.postPosition),
    path("addPosition/",views.addPosition),
    path("savePosition/",views.savePosition),
    path("positionContentList/",views.positionContentList),
    path("delPositionContent/",views.delPositionContent),
    path("clearUnusedImages/",views.clearUnusedImages)
]