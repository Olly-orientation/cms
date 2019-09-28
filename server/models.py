from django.db import models

# Create your models here.

class article(models.Model):
    articleId=models.AutoField(primary_key=True)
    authorId=models.IntegerField(max_length=11)
    columnId=models.IntegerField(max_length=11)
    sourceId=models.IntegerField(max_length=11)
    browserNum=models.IntegerField(max_length=11)
    articleStatus=models.IntegerField(max_length=1)
    heading=models.CharField()
    modifydate=models.DateTimeField(auto_now=True)

class articlecontent(models.Model):
    contentId=models.AutoField(primary_key=True)
    articleId=models.IntegerField(max_length=11)
    contents=models.TextField()
    imgUrl=models.CharField()

class source(models.Model):
    sourceId=models.AutoField(primary_key=True)
    sourceName=models.CharField()

class topics(models.Model):
    topicId=models.AutoField(primary_key=True)
    topicName=models.CharField()

class menu(models.Model):
    menuId=models.AutoField(primary_key=True)
    menuName=models.CharField()
    imgUrl=models.CharField()
    cos=models.IntegerField(max_length=1)
    status=models.IntegerField(max_length=1)

