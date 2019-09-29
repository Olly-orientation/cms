# Generated by Django 2.2.4 on 2019-09-29 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='admin',
            fields=[
                ('adminId', models.AutoField(primary_key=True, serialize=False)),
                ('adminname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='article',
            fields=[
                ('articleId', models.AutoField(primary_key=True, serialize=False)),
                ('authorId', models.IntegerField()),
                ('columnId', models.IntegerField()),
                ('sourceId', models.IntegerField()),
                ('browserNum', models.IntegerField()),
                ('articleStatus', models.IntegerField()),
                ('heading', models.CharField(max_length=250)),
                ('thumb', models.CharField(max_length=250)),
                ('modifydate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='articlecontent',
            fields=[
                ('contentId', models.AutoField(primary_key=True, serialize=False)),
                ('articleId', models.IntegerField()),
                ('contents', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='menu',
            fields=[
                ('menuId', models.AutoField(primary_key=True, serialize=False)),
                ('menuName', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='position',
            fields=[
                ('positionId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='position_content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positionId', models.IntegerField()),
                ('articleId', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='source',
            fields=[
                ('sourceId', models.AutoField(primary_key=True, serialize=False)),
                ('sourceName', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='topics',
            fields=[
                ('topicId', models.AutoField(primary_key=True, serialize=False)),
                ('topicName', models.CharField(max_length=200)),
            ],
        ),
    ]
