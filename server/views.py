from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from server import models
from django.forms import forms
from DjangoUeditor.forms import  UEditorField
from datetime import datetime
from django.db.models import Max
from cms import settings
import os
import math
import json
import re
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
    return render(request, "server/serverIndex/login.html")

def loginCheck(request):
    '''
    登录检查函数
    :param request:
    :return:
    '''
    #获取表单提交的用户名和密码
    username=request.POST.get("username")
    password=request.POST.get("pwd")
    #数据库查询相应的用户名和密码
    result=models.admin.objects.filter(adminname=username).values("adminname","password")
    if result:
        if result[0]["password"]==password:
            request.session["admin"]=result[0]["adminname"]
            return HttpResponse(returnData(0,"登录成功"),content_type="application/json; charset=utf-8")
        return HttpResponse(returnData(1,"密码错误"),content_type="application/json; charset=utf-8")
    else:
        #用户不存在
        return HttpResponse(returnData(1,"管理员不存在"),content_type="application/json; charset=utf-8")
def index(request):
    '''
    后台首页渲染页面
    在负责渲染页面的同时，负责检查管理员是否登录过后台，因而该方法对此做了一些验证，只有当管理员登录时
    才能看到页面的信息
    :param request:
    :return:
    '''
    admin=request.session.get("admin")
    context={
        "navIndex":0
    }
    if not admin:
        context={
            "logined":False
        }
    else:
        context["logined"]=True
        context["admin"]=showAdmin(request)
        context["adminCount"]=countAdmin()
        context["articleCount"]=countArticle()
        context["mostArticle"]=searchMaxArticle()
        context["positionCount"]=countPosition()


    return render(request, "server/serverIndex/serverIndex.html", context)


def clearAdminInfo(request):
    '''
    清除session的方法，主要对应前端的退出按钮
    :param request:
    :return:
    '''
    request.session.flush()
    return HttpResponseRedirect("/server/login")

def countAdmin():
    '''
    计算有多少管理员
    :return:
    '''
    count=models.admin.objects.count()
    return count
def searchMaxArticle():
    '''
    找最大浏览量的文章
    :return:
    '''
    result=models.article.objects.aggregate(maxRead = Max("browserNum"))
    articleInfo=models.article.objects.filter(browserNum=result["maxRead"]).values("articleId","menuId").get()
    result.update(articleInfo)
    return result

def countArticle():
    '''
    计算平台一共又多少条文章
    :return:
    '''
    count=models.article.objects.count()
    return count
def countPosition():
    '''
    计算一共又多少推荐位
    :return:
    '''
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
        "admin":showAdmin(request),
        "navIndex":1
    }
    return render(request, "server/menu/menu.html", context)
def addmenu(request):
    '''
    渲染添加菜单页面
    :param request:
    :return:
    '''
    id=request.GET.get("id")
    admin = request.session.get("admin")
    context={
        "admin":admin,
        "navIndex": 1
    }
    if id:
        context["menuInfo"]=models.menu.objects.filter(menuId=id).get()
        context["edit"]="true"
        context["id"]=id

    return render(request, "server/menu/add_menu.html", context)


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
    删除菜单的方法
    :param request:
    :return:
    '''
    menuId=request.GET.get("menuId")
    try:
        models.menu.objects.get(menuId=menuId).delete()
        models.article.objects.filter(menuId=menuId).delete()
    except Exception as e:
        return HttpResponse(returnData(1,"删除失败"),content_type="application/json; charset=utf-8")
    return HttpResponse(returnData(0,"删除成功"),content_type="application/json; charset=utf-8")


def articleList(request):
    '''
    文章列表页面渲染
    :param request:
    :return:
    '''
    admin = request.session.get("admin")
    page=request.GET.get("page")
    if not page:
        page=1
    articleInfo=switch(request,5,int(page))
    articleResult=articleInfo["articleResult"]
    context={
        "articleList":articleResult,
        "positionList":showPosition(),
        "admin":admin,
        "pageList":articleInfo["pageList"],
        "current":articleInfo["currentPage"],
        "menuList":articleInfo["menuList"],
        "heading":articleInfo["heading"],
        "menuId":int(articleInfo["menuId"]),
        "navIndex": 2
    }
    return render(request, "server/article/articleList.html", context)


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

def switch(request,perPage,page,panelItem=3):
    '''
    为文章打造的分页显示方法
    :param perPage: 每一页要显示的数量
    :param page: 传入的页码数
    :return:
    '''

    menuId=-1
    heading=''
    if request.GET.get("heading"):
        heading=request.GET.get("heading")
    if request.GET.get("menuId"):
        menuId=int(request.GET.get("menuId"))
    # 按需查找
    search=searchForDemand(page,perPage,heading,menuId)
    articleResult=search["articleResult"]
    articleCount=search["articleCount"]
    sourceResult=search["sourceResult"]
    menuResult=search["menuResult"]
    for item in articleResult:
        itemSourceId=item["sourceId"]
        itemMenuId=item["menuId"]
        def filterSource(items):
            return itemSourceId==items["sourceId"]
        def filterMenu(items):
            return itemMenuId==items["menuId"]
        filterSourceList = list(filter(filterSource, sourceResult))
        filterMenuList=list(filter(filterMenu, menuResult))
        item["sourceName"]=filterSourceList[0]["sourceName"]
        item["menuName"]=filterMenuList[0]["menuName"]
    dic={
        "articleResult":articleResult,
        "pageList":arrangePagination(page,articleCount,perPage,panelItem),
        "currentPage":page,
        "menuList":menuResult,
        "heading":heading,
        "menuId":menuId,
        "panelItem":panelItem
    }
    return dic
def searchForDemand(page,perPage,heading,menuId):
    # 获取页数
    start = perPage * (page - 1)
    endDouble = perPage * page
    # 按需查找
    if menuId == -1:
        articleResult = models.article.objects.filter(heading__contains=heading).values().order_by("-modifydate")[
                        start:endDouble]
        articleCount = models.article.objects.filter(heading__contains=heading).count()
    else:
        articleResult = models.article.objects.filter(menuId=menuId, heading__contains=heading).values().order_by(
            "-modifydate")[start:endDouble]
        articleCount = models.article.objects.filter(menuId=menuId, heading__contains=heading).count()
    sourceResult = models.source.objects.values()
    menuResult = models.menu.objects.values()
    dic={
        "articleResult":articleResult,
        "articleCount":articleCount,
        "sourceResult":sourceResult,
        "menuResult":menuResult
    }

    return dic
def arrangePagination(page,articleCount,perPage,panelItem):
    '''
    渲染前端需要使用的列表
    :param page:
    :param articleCount:
    :param perPage:
    :param panelItem:
    :return:
    '''
    # 需要获取三个变量
    # 1.当前页数page
    # 2.分页器要求在前端显示的个数panelItem
    # 3.总页数 allPages
    # 需要什么变量进行接收？
    # pageList
    pageList = []
    allPages = math.ceil(articleCount / perPage)
    if page == 1:
        for i in range(1, panelItem + 1):
            pageList.append(i)
        pageList = filter(lambda x: x <= allPages, pageList)
    else:
        leftover = (panelItem) % 2
        average = (panelItem - 1) / 2
        if leftover == 0:
            # 均分
            left, right = ((page - 1) - math.floor(average), page + math.ceil(average))
        else:
            average = int(average)
            left, right = ((page) - average, page + average)
        # 左右进行加减
        for i in range(left, page):
            pageList.append(i)
        for i in range(page, right + 1):
            pageList.append(i)
        pageList = list(filter(lambda x: x <= allPages and x >= 1, pageList))
    return pageList

def showPosition():
    '''
    查询所有的推荐位
    :return:
    '''
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
    #渲染富文本编辑器
    editor=TestUEditorForm()
    admin=showAdmin(request)
    context={
        "editor":editor,
        "admin": admin,
        "adminId":models.admin.objects.get(adminname=admin).adminId,
        "navIndex": 2
    }
    #搜索所有的source和menu记录
    sourceResult = models.source.objects.values()
    menuResult = models.menu.objects.values()
    if id:
        #若存在id，则表示文章是要进行编辑修改的，那么将和该文章相关的信息全部搜索到
        articleResult = models.article.objects.filter(articleId=id).values().get()
        articleContents=models.articlecontent.objects.filter(articleId=id).values().get()
        articleResult.update(articleContents)
        selectedSource=models.source.objects.filter(sourceId=articleResult["sourceId"]).values().get()
        selectedMenu=models.menu.objects.filter(menuId=articleResult["menuId"]).values().get()
        context["selectedSource"]=selectedSource
        context["selectedMenu"]=selectedMenu
        context["articleInfo"]=articleResult
        context["edit"]="true"
        context["id"]=id

    context["sourceResult"]=sourceResult
    context["menuResult"]=menuResult
    context["color"]=settings.COLOR_LIST
    return render(request, "server/article/add_article.html", context)

def sendInitialContent(request):
    '''
    设置富文本编辑器的初始值（仅限于编辑状态下使用）
    :param request:
    :return:
    '''
    articleId=request.GET.get("articleId")
    articleContent = models.articlecontent.objects.filter(articleId=articleId).values()[0]["contents"]
    return HttpResponse(json.dumps(articleContent), content_type="application/json; charset=utf-8")
def delArticle(request):
    '''
    删除文章
    :param request:
    :return:
    '''
    articleId = request.GET.get("articleId")
    try:
        #文章删除时，删除关联的articlecontent表，如果该文章添加了推荐位，那么该推荐位内容记录
        #也被删除
        models.article.objects.filter(articleId=articleId).delete()
        models.articlecontent.objects.filter(articleId=articleId).delete()
        models.articlecontent.objects.filter(articleId=articleId).delete()
        models.position_content.objects.filter(articleId=articleId).delete()
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
    articleId=request.POST.get("articleId")
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
            if articlethumb:
                models.article.objects.filter(articleId=articleId).update(heading=heading,thumb=filename,modifydate=datetime.now(),
                                                                          adminId=adminId,menuId=menuId,sourceId=souceId,
                                                                          headingColor=headingColor)
                models.articlecontent.objects.filter(articleId=articleId).update(contents=articleContent)
                return HttpResponse(returnData(0, "编辑成功"), content_type="application/json; charset=utf-8")
            else:
                #如果用户修改时不传图片，则不更新thumb字段
                #这一部分相当于给管理员一个障眼法，实际上前端页面是可以看到自己之前上传的图片的，但实际并没有上传
                models.article.objects.filter(articleId=articleId).update(heading=heading, modifydate=datetime.now(),
                                                                          adminId=adminId, menuId=menuId, sourceId=souceId,
                                                                          headingColor=headingColor)
                models.articlecontent.objects.filter(articleId=articleId).update(contents=articleContent, articleId=articleId)
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
    '''
    文件转换大小
    :param size: 文件大小
    :param format: 转换成何种格式
    :return:
    '''
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
    adminList=models.admin.objects.all()
    admin = showAdmin(request)
    return render(request, "server/admin/adminList.html",{"adminList":adminList,"admin":admin,"navIndex":3})
def delAdmin(request):
    id=request.GET.get("id")
    try:
        models.admin.objects.filter(adminId=id).delete()
        return HttpResponse(returnData(0, "删除管理员成功"))
    except Exception as e:
        return HttpResponse(returnData(1, "删除管理员失败"))
def editAdmin(request):
    adminId =request.GET.get("id")
    adminInfoList=models.admin.objects.values("adminId","adminname","password","email","headImg","introduction").get(adminId=adminId)
    context = {
        "intro": TestUEditorForm(),
        "adminInfoList":adminInfoList,
        "navIndex":3,
        "admin":showAdmin(request)
    }
    return render(request,"server/admin/editAdmin.html",context)
def editAdminHandle(request):
    adminId=request.POST.get("adminId")
    adminname=request.POST.get("username")
    content=request.POST.get("content")
    pwd=request.POST.get("pwd")
    email=request.POST.get("email")
    headImg = request.FILES.get("headImg")
    beforeheadImg=request.POST.get("beforeheadImg")
    if headImg:
        # 此时重新上传缩略图了
        # 先判断文件类型
        if headImg.name.split(".")[1] not in settings.UPLOAD_FILES["types"]:
            print("此时文件类型不正确")
            return HttpResponse(returnData(1, "文件类型不正确"))
        fileName = "headImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + headImg.name.split(".")[-1]
        print("新生成的文件名", fileName)
        print(headImg.size)
        size = HttpResponse(headImg.size, settings.UPLOAD_FILES["unit"])
        print(size)
        if float(size) > settings.UPLOAD_FILES["maxSize"]:
            return HttpResponse(returnData(1, "此时文件过大"))
        # 判断文件夹是否存在
        dir = "static/img/clientImg/"
        jugeDir(dir)
        savePath = dir + fileName
        with open(savePath, 'wb') as f:
            for file in headImg.chunks():
                f.write(file)
                f.flush()
        if beforeheadImg:
            path = 'static/img/clientImg/' + beforeheadImg
            newPath = os.path.join(settings.BASE_DIR, path)
            print("删除图片的路径", newPath)
            os.remove(newPath)
        try:
            models.admin.objects.filter(adminId=adminId).update(adminname=adminname,password=pwd,headImg=fileName,introduction=content,email=email,loginTime=datetime.now())
            return HttpResponse(returnData(0, "编辑用户信息成功"))
        except Exception as e:
            return HttpResponse(returnData(1, "编辑用户信息失败"))
    else:
        # 此时没有重新上传缩略图
        try:
            models.admin.objects.filter(adminId=adminId).update(adminname=adminname, password=pwd, introduction=content,email=email, loginTime=datetime.now())
            return HttpResponse(returnData(0, "编辑用户信息成功"))
        except Exception as e:
            return HttpResponse(returnData(1, "编辑用户信息失败"))
def addAdmin(request):
    context = {
        "intro": TestUEditorForm(),
        "admin":showAdmin(request),
        "navIndex":3
    }
    return render(request, "server/admin/addAdmin.html",context)
def addAdminHandle(request):
    headImg = request.FILES.get("headImg")
    username = request.POST.get("username")
    pwd = request.POST.get("pwd")
    email=request.POST.get("email")
    content = request.POST.get("content")
    # 先判断文件类型
    fileName=""
    if headImg:
        if headImg.name.split(".")[1] not in settings.UPLOAD_FILES["types"]:
            print("此时文件类型不正确")
            return HttpResponse(returnData(1, "文件类型不正确"))
        fileName = "headImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + headImg.name.split(".")[-1]
        size = getsize(headImg.size, settings.UPLOAD_FILES["unit"])
        if float(size) > settings.UPLOAD_FILES["maxSize"]:
            return HttpResponse(returnData(1, "此时文件过大"))
        # 判断文件夹是否存在
        dir = "static/img/clientImg/"
        HttpResponse(dir)
        savePath = dir + fileName
        with open(savePath, 'wb') as f:
            for file in headImg.chunks():
                f.write(file)
                f.flush()
    getServerData = models.admin.objects.filter(adminname=username).all()
    if len(getServerData) == 0:
        newAdmin= models.admin(adminname=username, headImg=fileName, loginTime=datetime.now(), password=pwd,email=email,introduction=content)
        newAdmin.save()
        return HttpResponse(returnData(0, "添加管理员成功"))
    else:
        return HttpResponse(returnData(1, "添加管理员失败"))




def positionList(request):
    '''
    推荐位管理渲染
    :param request:
    :return:
    '''
    context = {
        "positionList": models.position.objects.values(),
        "admin": showAdmin(request),
        "navIndex": 4
    }
    return render(request, "server/position/positionList.html", context)
def addPosition(request):
    '''
    添加推荐位
    :param request:
    :return:
    '''
    id=request.GET.get("id")
    context={
        "admin":showAdmin(request),
        "navIndex": 4
    }
    if id:
        context["positionInfo"]=models.position.objects.filter(positionId=id).get()
        context["edit"]="true"
        context["id"]=id
    return render(request, "server/position/add_position.html", context)
def savePosition(request):
    '''
    修改/添加推荐位
    :param request:
    :return:
    '''
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
    '''
    删除推荐位
    :param request:
    :return:
    '''
    positionId = request.GET.get("positionId")
    try:
        models.position.objects.get(articleId=positionId).delete()
        models.position_content.objects.filter(articleId=positionId).delete()
    except Exception as e:
        return HttpResponse(returnData(1, "删除失败"), content_type="application/json; charset=utf-8")
    return HttpResponse(returnData(0, "删除成功"), content_type="application/json; charset=utf-8")

def showAdmin(_request):
    '''
    用于展示页面最顶层右边的greetings
    :param _request: 从别处views方法传过来的request
    :return:
    '''
    admin=_request.session.get("admin")
    return admin
def jugeDir(dir):
    list=dir.split("/")
    print(list)
    for index,name in enumerate(list,0):
        imgPath=os.path.join(os.getcwd(),name)
        print(imgPath)
        if not os.path.exists(imgPath):
            print("此时文件夹不存在就新建")
            os.mkdir(imgPath)
        if index <len(list)-1:
            print("此时文件夹存在")
            list[index+1]=name+"/"+list[index+1]


# 推荐位内容管理部分方法
def positionContentList(request):
    '''
    推荐位内容管理页面渲染
    :param request:
    :return:
    '''
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
        "next": positionContentInfo["nextPage"],
        "navIndex": 5
    }
    return render(request, "server/position/positionContentList.html", context)

def positionContentSwitch(perPage,page):
    '''
    为推荐位内容打造的分页显示方法
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
    '''
    获取推荐位内容的所有记录
    :return:
    '''
    result=models.position.objects.values()
    return result
def delPositionContent(request):
    '''
    删除推荐位内容
    :param request:
    :return:
    '''
    articleId = request.GET.get("articleId")
    try:
        models.position_content.objects.filter(articleId=articleId).delete()
    except Exception as e:
        return HttpResponse(returnData(1, "删除失败"), content_type="application/json; charset=utf-8")
    return HttpResponse(returnData(0, "删除成功"), content_type="application/json; charset=utf-8")
def clearUnusedImages(request):
    '''
    先获取所有数据库中和图片相关的文件
    :param request:
    :return:
    '''
    dbList=[]
    # 获取文章的缩略图文件名
    imagesarticle=models.article.objects.values("thumb")
    # 获取文章内容中文章编辑的图片地址
    imagesarticleContents=models.articlecontent.objects.values("contents")
    staticImagesList=os.listdir("static/images")
    contentsImagesList=[]
    imagesadmin = models.admin.objects.values("headImg")
    reg = '<img.*?src="(.*?\.(jpg|png|jpeg|bmp))".*?/>'
    try:
        for item in imagesarticleContents:
            # 判断文章中有没有图片
            if re.search(reg, item["contents"]):
                articleImg=re.findall(reg,item["contents"])
                for item in articleImg:
                    # 获取图片文件名称
                    contentImg=item[0].split("/")[-1]
                    contentsImagesList.append(contentImg)
        # 清除文章中多余的图片
        for item in staticImagesList:
            if item not in contentsImagesList:
                path1=os.path.join("static\\images",item)
                os.remove(path1)
    except Exception as e:
        return HttpResponse(returnData(1,"失败"))
    return HttpResponse(returnData(0,"删除成功"))
def findDir(dir):
    li=dir.split("/")
    path=settings.BASE_DIR
    for item in li:
        os.path.join(path,item)
        path=path+"\\"+item
    return path
def returnData(status_code,str_tips=""):
    info={}
    info["status"]=status_code
    info["tips"]=str_tips
    return json.dumps(info)