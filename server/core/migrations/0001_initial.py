# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-30 03:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('followee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_followee', to=settings.AUTH_USER_MODEL)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_follower', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('msg_type', models.IntegerField(choices=[(0, 'Comment'), (1, 'Like'), (2, 'Feedback'), (3, 'Private')], default=0, verbose_name='Message Type')),
                ('content', models.TextField()),
                ('system', models.BooleanField(default=False)),
                ('expires', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_author', to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_target', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('gender', models.IntegerField(choices=[(0, 'Male'), (1, 'Female')], default=0, verbose_name='Gender')),
                ('intro', models.TextField(blank=True, null=True)),
                ('mobile', models.CharField(max_length=11, unique=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('nickname', models.CharField(max_length=100, unique=True)),
                ('oauth_token', models.CharField(blank=True, max_length=100, null=True)),
                ('user_type', models.IntegerField(choices=[(0, 'Normal'), (1, 'Fan'), (2, 'Photographer'), (3, 'Model')], default=0, verbose_name='User Type')),
                ('user_cert', models.BooleanField(default=False)),
                ('experts_cert', models.BooleanField(default=False)),
                ('pg_cert', models.BooleanField(default=False)),
                ('model_cert', models.BooleanField(default=False)),
                ('user_state', models.IntegerField(choices=[(0, 'Forbidden'), (1, 'Normal')], default=1)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
