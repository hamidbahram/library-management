# Generated by Django 3.0.8 on 2020-07-19 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_management_app', '0009_auto_20200718_1411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmodel',
            name='cover',
        ),
    ]
