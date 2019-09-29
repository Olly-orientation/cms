from django.db import models

# Create your models here.

class article(models.Model):
    articleId=models.AutoField(primary_key=True)
    authorId=models.IntegerField()
    columnId=models.IntegerField()
    sourceId=models.IntegerField()
    browserNum=models.IntegerField()
    articleStatus=models.IntegerField()
    heading=models.CharField(max_length=250)
    thumb=models.CharField(max_length=250)
    modifydate=models.DateTimeField(auto_now=True)

class articlecontent(models.Model):
    contentId=models.AutoField(primary_key=True)
    articleId=models.IntegerField()
    contents=models.TextField()

class source(models.Model):
    sourceId=models.AutoField(primary_key=True)
    sourceName=models.CharField(max_length=200)

class topics(models.Model):
    topicId=models.AutoField(primary_key=True)
    topicName=models.CharField(max_length=200)

class menu(models.Model):
    menuId=models.AutoField(primary_key=True)
    menuName=models.CharField(max_length=200)

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
