# Generated by Django 2.2.4 on 2019-09-29 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_remove_admin_password'),
    ]

    operations = [
        migrations.DeleteModel(
            name='admin',
        ),
    ]