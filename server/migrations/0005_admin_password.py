# Generated by Django 2.2.4 on 2019-09-29 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='password',
            field=models.CharField(default='', max_length=20),
        ),
    ]