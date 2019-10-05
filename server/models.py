from django.db import models
from DjangoUeditor.models import UEditorField
from datetime import datetime
# Create your models here.

class article(models.Model):
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
    contentId=models.AutoField(primary_key=True)
    articleId=models.IntegerField()
    contents=UEditorField()

class source(models.Model):
    sourceId=models.AutoField(primary_key=True)
    sourceName=models.CharField(max_length=200)


class menu(models.Model):
    menuId=models.AutoField(primary_key=True)
    menuName=models.CharField(max_length=200)
    menuStatus=models.SmallIntegerField(default=0)

class position(models.Model):
    positionId=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100,default="无描述")
    createTime=models.DateTimeField(auto_now_add=True)
    positionStatus=models.IntegerField(default=0)

class position_content(models.Model):
    positionId=models.IntegerField()
    articleId=models.IntegerField()

class admin(models.Model):
    adminId=models.AutoField(primary_key=True)
    adminname=models.CharField(max_length=50)
    password=models.CharField(max_length=20,default='')
    email=models.CharField(max_length=100,null=True)
    introduction=UEditorField(null=True)
    loginTime=models.DateTimeField(auto_now=True,null=True)