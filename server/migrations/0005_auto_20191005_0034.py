# Generated by Django 2.2.4 on 2019-10-04 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_position_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='description',
            field=models.CharField(default='无描述', max_length=100),
        ),
    ]