# Generated by Django 3.0.8 on 2020-07-27 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_management_app', '0012_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmodel',
            name='cover',
            field=models.ImageField(blank=True, default='book.jpg', null=True, upload_to=''),
        ),
    ]
