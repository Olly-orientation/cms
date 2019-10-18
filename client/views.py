from django.shortcuts import render
from django.http import HttpResponse
from server import models
from datetime import datetime
import json
# Create your views here.
def rightAd(request):
    getRightAdImglist = models.article.objects.values("thumb","heading").all()[0:3]
    sendRightAdImglist=[]
    for item in  getRightAdImglist:
        print(item["thumb"],item["heading"])
        sendRightAdImglist.append(item)
    return render(request,"clientCommon/rightAd.html",{"rightAdImglist":sendRightAdImglist})

def index(request):
    headerInfo = showHeader(request)

    # 小的右侧图片
    getMinAdImglist = models.article.objects.values("thumb","heading").all()[0:3]
    sendRightAdImglist = []
    for item in getMinAdImglist:
        print(item)
        sendRightAdImglist.append(item)
    # 排名
    articleTopFive=models.article.objects.values().order_by("-browserNum","-modifydate")[0:5]
    # 轮播图片
    context={
        "giantPosition":showPositionContent(1),
        "middlePosition":showPositionContent(2,3),
        "smallPosition":showPositionContent(3),
        "rightAdImglist":sendRightAdImglist,
        "menuList": headerInfo["menuList"],
        "currentType":headerInfo["currentType"],
        "articleTopFive":articleTopFive
    }
    return render(request,"client/clientIndex.html",context)
def showPositionContent(_positionId,_limited=5):
    if _limited==5:
        result= models.position_content.objects.filter(positionId=_positionId).values()[0:_limited]
    else:
        result=models.position_content.objects.filter(positionId=_positionId).values()
    articleList=[]
    try:
        for item in result:
            itemResult=models.article.objects.filter(articleId=item["articleId"]).values()[0]
            articleList.append(itemResult)
    except Exception as e:
        print("失败")
    return articleList
def indexArticleList(request):
    index=request.GET.get("index")
    num=request.GET.get("num")
    firstIndex = (int(index)-1)*int(num)
    endIndex=(int(index)*int(num))
    allNum= models.article.objects.count()
    getArticleList = models.article.objects.values("articleId","heading","modifydate","browserNum","thumb","menuId").order_by('-modifydate')[firstIndex:endIndex]
    articleList=[]
    for item in getArticleList:
        articleDict={
            "id":item["articleId"],
            "t": item["menuId"],
            "heading":item["heading"],
            "date":item["modifydate"].strftime("%Y-%m-%d %H:%M:%S"),
            "num":item["browserNum"],
            "thumb":item["thumb"],
        }
        articleList.append(articleDict)
    returnDic={
        "articleList":articleList,
        "allNum":allNum
    }
    return  HttpResponse(json.dumps(returnDic))
def detail(request):
    # 导航
    headerInfo = showHeader(request)
    # 排名
    articleTopFive = models.article.objects.values().order_by("-browserNum", "-modifydate")[0:5]

    # 右侧图片
    getRightAdImglist = models.article.objects.values("thumb", "heading").all()[0:3]
    sendRightAdImglist = []
    for item in getRightAdImglist:
        sendRightAdImglist.append(item)
    context={
        "menuList": headerInfo["menuList"],
        "currentType": headerInfo["currentType"],
        "articleTopFive": articleTopFive,
        "rightAdImglist": sendRightAdImglist
    }

    return render(request,"client/articleDetail.html",context)

def detailHandle(request):
    id=request.GET.get("id")
    print(id)
    try:
        getaddBrowserNum = models.article.objects.values("browserNum").get(articleId=id)
        changeNum=getaddBrowserNum["browserNum"]+1
        models.article.objects.filter(articleId=id).update(browserNum=changeNum)
    except Exception as e:
        return HttpResponse("添加浏览量失败")
    try:
        getArticleDetail=models.article.objects.values("heading","headingColor","modifydate").get(articleId=id)
        getArticleContentDetail=models.articlecontent.objects.values("contents").get(articleId=id)
        ArticleDetail={
            "heading":getArticleDetail["heading"],
            "headingColor": getArticleDetail["headingColor"],
            "modifydate": getArticleDetail["modifydate"].strftime("%y-%m-%d %H:%M:%S"),
            "contents": getArticleContentDetail["contents"]
        }
    except Exception as e:
        return HttpResponse("添加浏览量失败")
    return HttpResponse(json.dumps(ArticleDetail))
def showRank():
    pass
def showHeader(request):
    # 获取当前点击的分类
    currentType = request.GET.get("type")
    context={}
    context["currentType"] = int(currentType) if currentType else 0
    menuList = models.menu.objects.values()
    typeList = []
    typeList.extend(menuList)
    context["menuList"]=typeList
    return context
def type(request):
    # 获取header列表
    headerInfo=showHeader(request)
    # 排名
    articleTopFive = models.article.objects.values().order_by("-browserNum", "-modifydate")[0:5]
    getRightAdImglist = models.article.objects.values("thumb", "heading").all()[0:3]
    sendRightAdImglist = []
    for item in getRightAdImglist:
        print(item["thumb"], item["heading"])
        sendRightAdImglist.append(item)
    context={
        "menuList": headerInfo["menuList"],
        "articleTopFive": articleTopFive,
        "rightAdImglist": sendRightAdImglist,
        "currentType": headerInfo["currentType"]
    }
    print("afawfwa", headerInfo)
    return render(request,"client/articleType.html",context)


def typeList(request):
    type = request.GET.get("type")
    index=request.GET.get("index")
    num=request.GET.get("num")
    firstIndex = (int(index)-1)*int(num)
    endIndex=(int(index)*int(num))
    allNum= models.article.objects.filter(menuId=type).order_by('-modifydate').count()
    getArticleList = models.article.objects.filter(menuId=type).order_by('-modifydate').all()[firstIndex:endIndex]
    articleList=[]
    for item in getArticleList:
        articleDict={
            "id":item.articleId,
            "heading":item.heading,
            "date":item.modifydate.strftime("%Y-%m-%d %H:%M:%S"),
            "num":item.browserNum,
            "type": item.menuId,
            "thumb":item.thumb,
        }
        articleList.append(articleDict)
    returnDic={
        "articleList":articleList,
        "allNum":allNum
    }
    return  HttpResponse(json.dumps(returnDic))

