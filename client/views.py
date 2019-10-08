from django.shortcuts import render
from django.http import HttpResponse
from server import models
from datetime import datetime
import json
# Create your views here.
def rightAd(request):
    getRightAdImglist = models.article.objects.values("thumb","heading").all()[0:3]
    # print(getRightAdImglist)
    sendRightAdImglist=[]
    for item in  getRightAdImglist:
        print(item["thumb"],item["heading"])
        sendRightAdImglist.append(item)
    # print(sendRightAdImglist)
    return render(request,"clientCommon/rightAd.html",{"rightAdImglist":sendRightAdImglist})

def index(request):
    type_list = models.menu.objects.all()
    typeList = []
    for item in type_list:
        dic = {
            "id": item.menuId,
            "name": item.menuName
        }
        # print("字典",dic)
        typeList.append(dic)

    # 小的右侧图片
    getMinAdImglist = models.article.objects.values("thumb","heading").all()[0:3]
    # print(item["thumb"], item["heading"])
    # print(getMinAdImglist)
    sendRightAdImglist = []
    for item in getMinAdImglist:
        print(item)
        sendRightAdImglist.append(item)
    # print(sendRightAdImglist)
    # 排名
    oneArticle = models.article.objects.order_by('-browserNum').all()[0:1]
    for item in oneArticle:
        oneArticleId = item.articleId
        oneArticleDic = {
            "heading": item.heading,
            "type":item.menuId,
            "id": item.articleId,
            "rank": 1
        }
    twoArticle = models.article.objects.order_by('-browserNum').all()[1:2]
    for item in twoArticle:
        twoArticleDic = {
            "heading": item.heading,
            "type":item.menuId,
            "id": item.articleId,
            "rank": 2
        }
    threeArticle = models.article.objects.order_by('-browserNum').all()[2:3]
    for item in threeArticle:
        threeArticleDic = {
            "heading": item.heading,
            "type": item.menuId,
            "id":item.articleId,
            "rank":3
        }
    fourArticle = models.article.objects.order_by('-browserNum').all()[3:4]
    for item in fourArticle:
        fourArticleDic = {
            "heading": item.heading,
            "type": item.menuId,
            "id": item.articleId,
            "rank":4
        }
    fiveArticle = models.article.objects.order_by('-browserNum').all()[4:5]
    for item in fiveArticle:
        fiveArticleDic = {
            "heading": item.heading,
            "type": item.menuId,
            "id": item.articleId,
            "rank": 5
        }
    rankDict = {
        "oneArticle": oneArticleDic,
        "twoArticle": twoArticleDic,
        "threeArticle": threeArticleDic,
        "fourArticle": fourArticleDic,
        "fiveArticle": fiveArticleDic,

    }
    print(rankDict)

    # 轮播图片
    getfirstImg=models.article.objects.values("thumb","heading").all()[0:1]
    print(getfirstImg)
    for item in getfirstImg:
        print(getfirstImg)
        firstImg=item
    print(firstImg)
    getSlideImglist = models.article.objects.values("thumb","heading").all()[1:3]
    print(getSlideImglist)
    slideImglist = []
    for item in getSlideImglist:
        print(item)
        slideImglist.append(item)
    print(slideImglist)
    slideImgDic={
        "firstImg":firstImg,
        "otherImg":slideImglist
    }
    print(slideImgDic)

    return render(request,"client/clientIndex.html",{"rightAdImglist":sendRightAdImglist,"rankDict":rankDict,"slideImgDic":slideImgDic,"type_list":typeList})

def indexArticleList(request):
    index=request.GET.get("index")
    # index=2
    print(index)
    num=request.GET.get("num")
    print(num)
    firstIndex = (int(index)-1)*int(num)
    endIndex=(int(index)*int(num))
    allNum= models.article.objects.count()
    print("总数是",allNum)
    getArticleList = models.article.objects.values("articleId","heading","modifydate","browserNum","thumb","menuId").order_by('-modifydate').all()[firstIndex:endIndex]
    print("数据库返回的数据",getArticleList)
    articleList=[]
    for item in getArticleList:
        articleDict={
            "id":item["articleId"],
            "type": item["menuId"],
            "heading":item["heading"],
            "date":item["modifydate"].strftime("%Y-%m-%d %H:%M:%S"),
            "num":item["browserNum"],
            "thumb":item["thumb"],
        }
        articleList.append(articleDict)
    print(articleList)
    returnDic={
        "articleList":articleList,
        "allNum":allNum
    }
    return  HttpResponse(json.dumps(returnDic))
def detail(request):
    # 导航
    type_list = models.menu.objects.all()
    typeList = []
    for item in type_list:
        dic = {
            "id": item.menuId,
            "name": item.menuName
        }
        # print("字典",dic)
        typeList.append(dic)

        # 排名
    oneArticle = models.article.objects.order_by('-browserNum').all()[0:1]
    for item in oneArticle:
        oneArticleId = item.articleId
        oneArticleDic = {
            "heading": item.heading,
            "type": item.menuId,
            "id": item.articleId,
            "rank": 1
        }
    twoArticle = models.article.objects.order_by('-browserNum').all()[1:2]
    for item in twoArticle:
        twoArticleDic = {
            "heading": item.heading,
            "type": item.menuId,
            "id": item.articleId,
            "rank": 2
        }
    threeArticle = models.article.objects.order_by('-browserNum').all()[2:3]
    for item in threeArticle:
        threeArticleDic = {
            "heading": item.heading,
            "type": item.menuId,
            "id": item.articleId,
            "rank": 3
        }
    fourArticle = models.article.objects.order_by('-browserNum').all()[3:4]
    for item in fourArticle:
        fourArticleDic = {
            "heading": item.heading,
            "type": item.menuId,
            "id": item.articleId,
            "rank": 4
        }
    fiveArticle = models.article.objects.order_by('-browserNum').all()[4:5]
    for item in fiveArticle:
        fiveArticleDic = {
            "heading": item.heading,
            "type": item.menuId,
            "id": item.articleId,
            "rank": 5
        }
    rankDict = {
        "oneArticle": oneArticleDic,
        "twoArticle": twoArticleDic,
        "threeArticle": threeArticleDic,
        "fourArticle": fourArticleDic,
        "fiveArticle": fiveArticleDic,

    }
    print(rankDict)

    # 右侧图片
    getRightAdImglist = models.article.objects.values("thumb", "heading").all()[0:3]
    # print(getRightAdImglist)
    sendRightAdImglist = []
    for item in getRightAdImglist:
        print(item["thumb"], item["heading"])
        sendRightAdImglist.append(item)

    return render(request,"client/articleDetail.html",{"type_list":typeList,"rankDict":rankDict,"rightAdImglist":sendRightAdImglist})

def detailHandle(request):
    id=request.GET.get("id")
    print(id)
    try:
        getaddBrowserNum = models.article.objects.values("browserNum").get(articleId=id)
        print("当前浏览量是",getaddBrowserNum)
        changeNum=getaddBrowserNum["browserNum"]+1
        print(changeNum)
        models.article.objects.filter(articleId=id).update(browserNum=changeNum)
    except Exception as e:
        return HttpResponse("添加浏览量失败")
    try:
        getArticleDetail=models.article.objects.values("heading","headingColor","modifydate").get(articleId=id)
        getArticleContentDetail=models.articlecontent.objects.values("contents").get(articleId=id)
        # print(getArticleContentDetail)
        ArticleDetail={
            "heading":getArticleDetail["heading"],
            "headingColor": getArticleDetail["headingColor"],
            "modifydate": getArticleDetail["modifydate"].strftime("%y-%m-%d %H:%M:%S"),
            "contents": getArticleContentDetail["contents"]
        }
        # print(ArticleDetail)
    except Exception as e:
        return HttpResponse("添加浏览量失败")
    return HttpResponse(json.dumps(ArticleDetail))
def type(request):
    currentType=request.GET.get("type")
    print("当前type是",currentType)
    type_list = models.menu.objects.all()
    typeList = []
    for item in type_list:
        dic = {
            "id": item.menuId,
            "name": item.menuName
        }
        # print("字典",dic)
        typeList.append(dic)

        # 排名
        oneArticle = models.article.objects.order_by('-browserNum').all()[0:1]
        for item in oneArticle:
            oneArticleDic = {
                "heading": item.heading,
                "type": item.menuId,
                "id": item.articleId,
                "rank": 1
            }
        twoArticle = models.article.objects.order_by('-browserNum').all()[1:2]
        for item in twoArticle:
            twoArticleDic = {
                "heading": item.heading,
                "type": item.menuId,
                "id": item.articleId,
                "rank": 2
            }
        threeArticle = models.article.objects.order_by('-browserNum').all()[2:3]
        for item in threeArticle:
            threeArticleDic = {
                "heading": item.heading,
                "id": item.articleId,
                "type": item.menuId,
                "rank": 3
            }
        fourArticle = models.article.objects.order_by('-browserNum').all()[3:4]
        for item in fourArticle:
            fourArticleDic = {
                "heading": item.heading,
                "type": item.menuId,
                "id": item.articleId,
                "rank": 4
            }
        fiveArticle = models.article.objects.order_by('-browserNum').all()[4:5]
        for item in fiveArticle:
            fiveArticleDic = {
                "heading": item.heading,
                "type": item.menuId,
                "id": item.articleId,
                "rank": 5
            }
        rankDict = {
            "oneArticle": oneArticleDic,
            "twoArticle": twoArticleDic,
            "threeArticle": threeArticleDic,
            "fourArticle": fourArticleDic,
            "fiveArticle": fiveArticleDic,

        }
        print(rankDict)
# 右侧图片
        getRightAdImglist = models.article.objects.values("thumb", "heading").all()[0:3]
        # print(getRightAdImglist)
        sendRightAdImglist = []
        for item in getRightAdImglist:
            print(item["thumb"], item["heading"])
            sendRightAdImglist.append(item)

    return render(request,"client/articleType.html",{"type_list":typeList,"rankDict":rankDict,"rightAdImglist":sendRightAdImglist,"currentType":currentType})


def typeList(request):
    type = request.GET.get("type")
    index=request.GET.get("index")
    print("前端传过来的类型的id",type)
    print(index)
    num=request.GET.get("num")
    print(num)
    firstIndex = (int(index)-1)*int(num)
    endIndex=(int(index)*int(num))
    allNum= models.article.objects.filter(menuId=type).order_by('-modifydate').count()
    print("总数是",allNum)
    getArticleList = models.article.objects.filter(menuId=type).order_by('-modifydate').all()[firstIndex:endIndex]
    print("数据库返回的数据",getArticleList)
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
    print(articleList)
    returnDic={
        "articleList":articleList,
        "allNum":allNum
    }
    return  HttpResponse(json.dumps(returnDic))

