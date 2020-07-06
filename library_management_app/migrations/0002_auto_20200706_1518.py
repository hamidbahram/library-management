# Generated by Django 3.0.8 on 2020-07-06 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library_management_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmodel',
            name='description',
            field=models.TextField(default=' '),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='library_management_app.BookModel')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]