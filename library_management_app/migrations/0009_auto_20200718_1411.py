# Generated by Django 3.0.8 on 2020-07-18 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_management_app', '0008_auto_20200718_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmodel',
            name='cover',
            field=models.ImageField(blank=True, default='book3.jpg', null=True, upload_to=''),
        ),
    ]