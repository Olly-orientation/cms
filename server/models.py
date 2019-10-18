from django.db import models
from DjangoUeditor.models import UEditorField
from datetime import datetime
# Create your models here.

class article(models.Model):
    '''
    articleId----文章id
    adminId----管理员Id
    menuId----菜单Id
    sourceId----来源Id
    browserNum----浏览量
    articleStatus----文章显示状态
    heading----标题
    headingColor----标题颜色
    thumb----缩略图
    modifydate----修改日期
    '''
    articleId=models.AutoField(primary_key=True)
    adminId=models.IntegerField(default=1)
    menuId=models.IntegerField(default=1)
    sourceId=models.IntegerField(default=1)
    browserNum=models.IntegerField(default=0)
    articleStatus=models.IntegerField(default=0)
    heading=models.CharField(max_length=250)
    headingColor=models.CharField(max_length=7,default="#000000")
    thumb=models.CharField(max_length=250,default='compass.png')
    modifydate=models.DateTimeField(auto_now=True)

class articlecontent(models.Model):
    '''
    contentId----内容Id
    articleId----文章Id
    contents----具体内容
    '''
    contentId=models.AutoField(primary_key=True)
    articleId=models.IntegerField()
    contents=UEditorField()

class source(models.Model):
    '''
    sourceId----来源Id
    sourceName----来源名称
    '''
    sourceId=models.AutoField(primary_key=True)
    sourceName=models.CharField(max_length=200)


class menu(models.Model):
    '''
    menuId---菜单Id
    menuName---菜单名称
    menuStatus---菜单显示状态
    '''
    print("menu")
    menuId=models.AutoField(primary_key=True)
    menuName=models.CharField(max_length=200)
    menuStatus=models.SmallIntegerField(default=0)

class position(models.Model):
    '''
    positionId----推荐位Id
    name----推荐位名称
    description----推荐位描述
    createTime----创建时间
    positionStatus----推荐位显示状态
    '''
    positionId=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100,default="无描述")
    createTime=models.DateTimeField(auto_now_add=True)
    positionStatus=models.IntegerField(default=0)

class position_content(models.Model):
    '''
    positionId----推荐位Id
    articleId----文章Id
    '''
    positionId=models.IntegerField()
    articleId=models.IntegerField()

class admin(models.Model):
    '''
    adminId----管理员id
    adminname----管理员性名
    password----密码
    email----邮箱
    introduction----简介
    loginTime----登录时间
    '''
    adminId = models.AutoField(primary_key=True)
    adminname = models.CharField(max_length=50)
    password = models.CharField(max_length=20, default='')
    email = models.CharField(max_length=100, null=True)
    introduction = UEditorField(null=True)
    loginTime = models.DateTimeField(auto_now=True, null=True)
    headImg = models.CharField(max_length=100, default='')