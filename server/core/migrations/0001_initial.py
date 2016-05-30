# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-30 01:47
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
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
            name='Advertise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('position', models.IntegerField(choices=[(0, 'Home'), (1, 'Splash'), (1, 'Settings')])),
                ('picture', models.ImageField(blank=True, null=True, upload_to='advertises')),
                ('url', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('feedback_type', models.IntegerField(choices=[(0, 'Political'), (1, 'Erotic'), (2, 'Customize')], default=0, verbose_name='feedback_type')),
                ('content', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
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
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('type_kbn', models.IntegerField(choices=[(0, 'Oscar'), (1, 'Ishiyaki')])),
                ('description', models.TextField()),
                ('scene_seq', models.CommaSeparatedIntegerField(blank=True, max_length=100, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_author', to=settings.AUTH_USER_MODEL)),
                ('favourites', models.ManyToManyField(related_name='gallerys_favourites', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='gallerys_likes', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'gallery',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
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
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('exif', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo_author', to=settings.AUTH_USER_MODEL)),
                ('gallery', models.ManyToManyField(related_name='photo_gallery', to='core.Gallery')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('photo_seq', models.CommaSeparatedIntegerField(max_length=100)),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scene_gallery', to='core.Gallery')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SceneTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='scene_covers')),
                ('background', models.ImageField(blank=True, null=True, upload_to='scene_backgrounds')),
                ('capacity', models.IntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five'), (6, 'Six'), (7, 'Seven'), (8, 'Eight'), (9, 'Nine')], validators=[django.core.validators.MaxValueValidator(50)])),
                ('canvas_config', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('unit_price', models.FloatField()),
                ('content', models.TextField()),
                ('period', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_author', to=settings.AUTH_USER_MODEL)),
                ('favourites', models.ManyToManyField(related_name='services_favourites', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='services_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'service',
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('amount', models.FloatField()),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tip_gallery', to='core.Gallery')),
                ('tipper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tip_user', to=settings.AUTH_USER_MODEL)),
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
        migrations.AddField(
            model_name='service',
            name='service_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_service_type', to='core.ServiceType'),
        ),
        migrations.AddField(
            model_name='service',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='scene',
            name='scene_template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scene_scene_template', to='core.SceneTemplate'),
        ),
        migrations.AddField(
            model_name='comment',
            name='gallery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_gallery', to='core.Gallery'),
        ),
    ]
