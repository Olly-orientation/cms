from django.shortcuts import render
from django.http import HttpResponse
from server import models
import json
# Create your views here.
def login(request):
    '''
    登陆页面
    :param request:
    :return:
    '''
    return render(request,"server/login.html")
def loginCheck(request):
    username=request.POST.get("username")
    password=request.POST.get("pwd")
    print(username,password)
    return HttpResponse(123)
# 后台首页
def index(request):
    return render(request,"server/serverIndex.html")

def menu(request):
    '''
    菜单管理页面
    :param request:
    :return:
    '''
    return render(request,"server/menu.html")
def addmenu(request):
    return render(request,"server/add_menu.html")
def savemenu(request):
    menuName=request.GET.get("menuName")
    status=request.GET.get("status")
    try:
        models.menu.objects.create(menuName=menuName)
    except Exception as e:
        return HttpResponse(123)

def returnData(status_code,str_tips=""):
    info={}
    info["status"]=status_code
    info["tips"]=str_tips
    return json.dumps(info)
