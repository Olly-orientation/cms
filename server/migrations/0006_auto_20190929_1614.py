# Generated by Django 2.2.4 on 2019-09-29 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_admin_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admin',
            old_name='password',
            new_name='passw',
        ),
    ]