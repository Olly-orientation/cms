# Generated by Django 2.2.4 on 2019-09-29 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0006_auto_20190929_1614'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admin',
            old_name='passw',
            new_name='password',
        ),
    ]
