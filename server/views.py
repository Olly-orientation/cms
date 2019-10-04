from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from server import models
from django.forms import forms
from extra_app.DjangoUeditor.forms import UEditorField


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
    result=models.admin.objects.filter(adminname=username).values("adminname","password")
    if result:
        if result[0]["password"]==password:
            request.session["admin"]=result[0]["adminname"]
            return HttpResponse(returnData(0,"登录成功"),content_type="application/json; charset=utf-8")
        return HttpResponse(returnData(1,"密码错误"),content_type="application/json; charset=utf-8")
    else:
        return HttpResponse(returnData(1,"管理员不存在"),content_type="application/json; charset=utf-8")
def index(request):
    admin=request.session.get("admin")
    context={}
    if not admin:
        context={
            "logined":False
        }
    else:
        context["logined"]=True
        context["admin"]=showAdmin(request)
        context["adminCount"]=countAdmin()
        context["articleCount"]=countArticle()
        context["positionCount"]=countPosition()

    return render(request,"server/serverIndex.html",context)
def clearAdminInfo(request):
    request.session.flush()
    return HttpResponseRedirect("/server/login")

def countAdmin():
    count=models.admin.objects.count()
    return count
def countArticle():
    count=models.article.objects.count()
    return count
def countPosition():
    count=models.position.objects.count()
    return count

def menu(request):
    '''
    菜单管理页面
    :param request:
    :return:
    '''
    context={
        "menuList":models.menu.objects.values(),
        "admin":showAdmin(request)
    }
    return render(request,"server/menu.html",context)
def addmenu(request):
    '''
    渲染添加菜单页面
    :param request:
    :return:
    '''
    id=request.GET.get("id")
    context={}
    if id:
        context["menuInfo"]=models.menu.objects.filter(menuId=id).get()
        context["edit"]="true"
        context["id"]=id

    return render(request,"server/add_menu.html",context)
def savemenu(request):
    '''
    将修改好的或者新增的菜单放入数据库中
    :param request:
    :return:
    '''
    menuName=request.GET.get("menuName")
    status=request.GET.get("status")
    id=request.GET.get("menuId")
    if id:
        #修改菜单
        models.menu.objects.filter(menuId=id).update(menuName=menuName,menuStatus=status)
        return HttpResponse(returnData(0,"修改成功"),content_type="application/json; charset=utf-8")
    else:
        try:
            models.menu.objects.create(menuName=menuName,menuStatus=status)
            return HttpResponse(returnData(0,"添加成功"),content_type="application/json; charset=utf-8")
        except Exception as e:
            return HttpResponse(returnData(1,"添加失败"),content_type="application/json; charset=utf-8")
def delMenu(request):
    '''
    删除文章的方法
    :param request:
    :return:
    '''
    menuId=request.GET.get("menuId")
    try:
        models.menu.objects.get(menuId=menuId).delete()
    except Exception as e:
        return HttpResponse(returnData(1,"删除失败"),content_type="application/json; charset=utf-8")
    return HttpResponse(returnData(0,"删除成功"),content_type="application/json; charset=utf-8")

def articleList(request):
    articleResult=models.article.objects.values()
    articleContentResult=models.article.objects.values()
    articleResult=[]
    # context={
    #     "articleList":
    # }

    print()
    return render(request,"server/articleList.html")
class EditorForm(forms.Form):
    content = UEditorField('',initial="",width=800, height=300,toolbars="full",imagePath="/static/images/", filePath="/static/files/",upload_settings={"imageMaxSize":1204000},settings={})
def addArticle(request):
    context={
        "editor":EditorForm()
    }
    return render(request,"server/add_article.html",context)
def saveArticle(request):

    return HttpResponse(returnData(0,"success"))



def adminList(request):
    return render(request,"server/adminList.html")
def addAdmin(request):
    return render(request,"server/add_admin.html")

def positionList(request):
    return render(request,"server/positionList.html")
def addPosition(request):
    return render(request,"server/add_position.html")
def positionContentList(request):
    return render(request,"server/positionContentList.html")
def addPositionContent(request):
    return HttpResponse(123)

def showAdmin(_request):
    admin=_request.session.get("admin")
    return admin
def returnData(status_code,str_tips=""):
    info={}
    info["status"]=status_code
    info["tips"]=str_tips
    return json.dumps(info)