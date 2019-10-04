from django.db import models
from extra_app.DjangoUeditor.models import UEditorField
# Create your models here.


class article(models.Model):
    articleId=models.AutoField(primary_key=True)
    adminId=models.ForeignKey(to="admin",to_field="adminId",on_delete=None)
    menuId=models.ForeignKey(to="menu",to_field="menuId",on_delete=None)
    sourceId=models.ForeignKey(to="source",to_field="sourceId",on_delete=None)
    browserNum=models.IntegerField()
    articleStatus=models.IntegerField()
    heading=models.CharField(max_length=250)
    thumb=models.CharField(max_length=250)
    modifydate=models.DateTimeField(auto_now=True)

class articlecontent(models.Model):
    contentId=models.AutoField(primary_key=True)
    articleId=models.ForeignKey(to="article",to_field="articleId",on_delete=models.CASCADE)
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

class position_content(models.Model):
    positionId=models.IntegerField()
    articleId=models.IntegerField()

class admin(models.Model):
    adminId=models.AutoField(primary_key=True)
    adminname=models.CharField(max_length=50)
    password=models.CharField(max_length=20,default='')
    email=models.CharField(max_length=100,null=True)