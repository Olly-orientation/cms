from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from server import models
from django.forms import forms
from DjangoUeditor.forms import  UEditorField
from datetime import datetime
import math
import json
# Create your views here.
class TestUEditorForm(forms.Form):
    content = UEditorField('', width=900, height=300, toolbars="full", imagePath="static/images/",
                           filePath="static/files/",

                           upload_settings={"imageMaxSize": 1204000},

                           settings={})
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
    admin = request.session.get("admin")
    context={
        "admin":admin
    }
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
    admin = request.session.get("admin")
    page=request.GET.get("page")
    if not page:
        page=1
    articleInfo=switch(5,page)
    articleResult=articleInfo["articleResult"]
    context={
        "articleList":articleResult,
        "positionList":showPosition(),
        "admin":admin,
        "pages":articleInfo["pageNum"],
        "pageNum":len(articleInfo["pageNum"]),
        "current":articleInfo["currentPage"],
        "previous":articleInfo["previousPage"],
        "next":articleInfo["nextPage"]
    }
    return render(request,"server/articleList.html",context)


def countPage(perPage,items):
    '''
    计算一共多少页的方法
    :param perPage: 每页要显示的个数
    :param items: 一共有多少字段
    :return:
    '''
    # 获取字段的数量
    # 设定好一页显示多少条消息
    pageList=[]
    for i in range(1,math.ceil(items/perPage)+1):
        pageList.append(i)
    dic={
        "pageNum":pageList
    }
    return dic

def switch(perPage,page):
    '''
    为文章打造的分页显示方法
    :param perPage: 每一页要显示的数量
    :param page: 传入的页码数
    :return:
    '''
    # 获取页数
    page = int(page)
    start = perPage * (page - 1)
    endDouble = perPage * page
    articleCount=models.article.objects.count()

    # 按需查找
    articleResult = models.article.objects.values().order_by("-modifydate")[start:endDouble]
    sourceResult = models.source.objects.values()
    menuResult = models.menu.objects.values()
    for item in articleResult:
        for item1 in sourceResult:
            if item["sourceId"] == item1["sourceId"]:
                item["sourceName"] = item1["sourceName"]
        for item2 in menuResult:
            if item["menuId"] == item2["menuId"]:
                item["menuName"] = item2["menuName"]
    dic={
        "articleResult":articleResult,
        "pageNum":countPage(perPage,articleCount)["pageNum"],
        "currentPage":page,
        "previousPage":page-1,
        "nextPage":page+1
    }
    return dic

def showPosition():
    result=models.position.objects.values()
    return result
def postPosition(request):
    '''
    将文章进行广告位推送
    :param request:
    :return:
    '''
    #获取多选框的值
    selectedId=request.GET.getlist("selectedGroup")
    positionId=request.GET.get("positionId")
    if len(positionId)>2:
        return HttpResponse(returnData(1,"请选择推荐位再推送"),content_type="application/json; charset=utf-8")
    elif len(selectedId)==0:
        return HttpResponse(returnData(1,"请选择要推送的文章"),content_type="application/json; charset=utf-8")
    try:
        for item in selectedId:
            positionContentResult=models.position_content.objects.filter(articleId=item)
            if positionContentResult:
                models.position_content.objects.filter(articleId=item).update(positionId=positionId,articleId=item)
            else:
                #创建记录
                models.position_content.objects.create(positionId=positionId,articleId=item)
    except Exception as e:
        return HttpResponse(returnData(1, "推送失败"), content_type="application/json; charset=utf-8")
    return HttpResponse(returnData(0,"推送成功"), content_type="application/json; charset=utf-8")

def addArticle(request):
    '''
    添加文章的方法
    :param request:
    :return:
    '''
    id = request.GET.get("id")
    editor=TestUEditorForm()
    admin=showAdmin(request)
    context={
        "editor":editor,
        "admin": admin,
        "adminId":models.admin.objects.get(adminname=admin).adminId
    }
    sourceResult = models.source.objects.values()
    menuResult = models.menu.objects.values()
    if id:
        articleResult = models.article.objects.filter(articleId=id).values().get()
        articleContent=models.articlecontent.objects.filter(articleId=id).values()[0]["contents"]
        selectedSource=models.source.objects.filter(sourceId=articleResult["sourceId"]).values().get()
        selectedMenu=models.menu.objects.filter(menuId=articleResult["menuId"]).values().get()
        context["selectedSource"]=selectedSource
        context["selectedMenu"]=selectedMenu
        context["articleInfo"]=articleResult
        context["initialContent"]=articleContent
        context["edit"]="true"
        context["id"]=id
    context["sourceResult"]=sourceResult
    context["menuResult"]=menuResult
    return render(request,"server/add_article.html",context)

def delArticle(request):
    '''

    :param request:
    :return:
    '''
    articleId = request.GET.get("articleId")
    try:
        models.article.objects.get(articleId=articleId).delete()
        models.articlecontent.objects.get(articleId=articleId).delete()
        print("articleId",articleId)
        positionResult=models.position_content.objects.filter(articleId=articleId)
        print("----------wfaw--",positionResult)
        if positionResult:
            models.articlecontent.objects.filter(articleId=articleId).delete()
    except Exception as e:
        return HttpResponse(returnData(1, "删除失败"), content_type="application/json; charset=utf-8")
    return HttpResponse(returnData(0, "删除成功"), content_type="application/json; charset=utf-8")

def saveArticle(request):
    #存文章内容及其他相关信息
    heading=request.POST.get("heading")
    articlethumb=request.FILES.get("articlethumb")
    headingColor=request.POST.get("headingColor")
    menuId=request.POST.get("menuId")
    souceId=request.POST.get("souceId")
    articleContent=request.POST.get("content")
    articleId=request.POST.get("id")
    adminId=request.POST.get("adminId")
    if articlethumb:
        # 存图片
        size=getsize(articlethumb.size,format="mb")
        thumbname=articlethumb.name
        # 判断文件是否过大
        if float(size) > 10:
            return HttpResponse(returnData(1,"上传图片文件过大，请换图片"))
        # 判断上传过来的文件类型是否是项目需要的：
        if thumbname.split(".")[-1] not in ["jpg", "jpeg", "png"]:
            return HttpResponse(returnData(1,"图片文件格式不正确，请换图片"))
        #把文件保存到指定的路径中
        # 创建文件名 以及指定到保存文件的路径
        filename = "thumb_" + str(int(datetime.now().timestamp() * 1000000)) + "." + thumbname.split(".")[-1]
        savePath = "static/img/clientImg/"+filename
        # 写入文件中
        with open(savePath, 'wb') as f:
            for file in articlethumb.chunks():
                f.write(file)
                f.flush()
    else:
        filename="compass.png"
    try:
        if articleId:
            models.article.objects.update(heading=heading,thumb=filename,modifydate=datetime.now(),adminId=adminId,menuId=menuId,sourceId=souceId,headingColor=headingColor)
            models.articlecontent.objects.update(contents=articleContent,articleId=articleId)
            return HttpResponse(returnData(0, "编辑成功"), content_type="application/json; charset=utf-8")
        else:
            # 把除文章内容外的信息放入article表当中
            insertLog=models.article.objects.create(heading=heading,thumb=filename,modifydate=datetime.now(),adminId=adminId,menuId=menuId,sourceId=souceId,headingColor=headingColor)
            # 获取插入article表后的id值获取
            insert_id=insertLog.articleId
            # 在articlecontent表中加入这个id值
            models.articlecontent.objects.create(contents=articleContent,articleId=insert_id)
            return HttpResponse(returnData(0, "发布成功"), content_type="application/json; charset=utf-8")
    except Exception as e:
        print(e)
        return HttpResponse(returnData(1, "编辑失败"), content_type="application/json; charset=utf-8")

def getsize(size, format = 'kb'):
    p = 0
    if format == 'kb':
        p = 1
    elif format == 'mb':
        p = 2
    elif format == 'gb':
        p = 3
    size /= math.pow(1024, p)
    return "%0.2f"%size


def adminList(request):
    return render(request,"server/adminList.html")
def addAdmin(request):
    return render(request,"server/add_admin.html")

def positionList(request):
    context = {
        "positionList": models.position.objects.values(),
        "admin": showAdmin(request)
    }
    return render(request,"server/positionList.html",context)
def addPosition(request):
    id=request.GET.get("id")
    context={
        "admin":showAdmin(request)
    }
    if id:
        context["positionInfo"]=models.position.objects.filter(positionId=id).get()
        context["edit"]="true"
        context["id"]=id
    return render(request,"server/add_position.html",context)
def savePosition(request):
    positionName = request.GET.get("positionName")
    description=request.GET.get("description")
    status = request.GET.get("status")
    id = request.GET.get("positionId")
    if id:
        # 修改广告位
        models.position.objects.filter(positionId=id).update(name=positionName, positionStatus=status,description=description)
        return HttpResponse(returnData(0, "修改成功"), content_type="application/json; charset=utf-8")
    else:
        try:
            models.position.objects.create(name=positionName, positionStatus=status,description=description)
            return HttpResponse(returnData(0, "添加成功"), content_type="application/json; charset=utf-8")
        except Exception as e:
            return HttpResponse(returnData(1, "添加失败"), content_type="application/json; charset=utf-8")

def delPosition(request):
    positionId = request.GET.get("positionId")
    try:
        models.position.objects.get(articleId=positionId).delete()
        models.position_content.objects.filter(articleId=positionId).delete()
    except Exception as e:
        return HttpResponse(returnData(1, "删除失败"), content_type="application/json; charset=utf-8")
    return HttpResponse(returnData(0, "删除成功"), content_type="application/json; charset=utf-8")

def showAdmin(_request):
    admin=_request.session.get("admin")
    return admin


# 推荐位内容管理部分方法
def positionContentList(request):
    page = request.GET.get("page")
    if not page:
        page = 1
    positionContentInfo = positionContentSwitch(5, page)
    positionContentResult = positionContentInfo["positionContentResult"]
    context = {
        "positionContentResult": positionContentResult,
        "positionList": showPosition(),
        "admin": showAdmin(request),
        "pages": positionContentInfo["pageNum"],
        "pageNum": len(positionContentInfo["pageNum"]),
        "current": positionContentInfo["currentPage"],
        "previous": positionContentInfo["previousPage"],
        "next": positionContentInfo["nextPage"]
    }
    print("---------------", context["pageNum"])
    return render(request, "server/positionContentList.html",context)
def positionContentSwitch(perPage,page):
    '''
    为文章打造的分页显示方法
    :param perPage: 每一页要显示的数量
    :param page: 传入的页码数
    :return:
    '''
    # 获取页数
    page = int(page)
    start = perPage * (page - 1)
    endDouble = perPage * page
    positionContentCount=models.position_content.objects.count()

    # 按需查找
    positionContentResult = models.position_content.objects.values()[start:endDouble]
    for item in positionContentResult:
        # 获取了positionContent表下的文章Id和其对应的推荐位Id，先对文章Id进行查找，然后再把其对应的推荐位名称也获取到
        try:
            articleResult = models.article.objects.filter(articleId=item["articleId"]).values().get()
            positionResult = models.position.objects.filter(positionId=item["positionId"]).values().get()
            item.update(articleResult)
            item.update(positionResult)
            print(item)
        except Exception as e:
            print(e)
    dic={
        "positionContentResult":positionContentResult,
        "pageNum":countPage(perPage,positionContentCount)["pageNum"],
        "currentPage":page,
        "previousPage":page-1,
        "nextPage":page+1
    }
    return dic
def showPositionContent():
    result=models.position.objects.values()
    return result
def delPositionContent(request):
    articleId = request.GET.get("articleId")
    try:
        models.position_content.objects.filter(articleId=articleId).delete()
    except Exception as e:
        return HttpResponse(returnData(1, "删除失败"), content_type="application/json; charset=utf-8")
    return HttpResponse(returnData(0, "删除成功"), content_type="application/json; charset=utf-8")
def returnData(status_code,str_tips=""):
    info={}
    info["status"]=status_code
    info["tips"]=str_tips
    return json.dumps(info)