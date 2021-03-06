# Generated by Django 3.0.7 on 2020-06-27 04:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=100)),
                ('published_date_time', models.DateTimeField(blank=True, null=True)),
                ('created_by',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_posted',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TagWeight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveSmallIntegerField(default=1)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_like.Post')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_like.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='PostImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='', upload_to='photos/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_like.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('reaction', models.CharField(choices=[('Like', 'Like'), ('Dislike', 'Dislike')], max_length=7)),
                ('post',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_liked_dislike',
                                   to='app_like.Post')),
                ('user',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_liked_dislike',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('post', 'user', 'reaction')},
            },
        ),
    ]
