#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# 影集类型
GALLERY_TYPE = (
    (0, _("Oscar")),    #奥斯卡
    (1, _("Ishiyaki")), #研烧
)

class UserProfile(models.Model):
    """用户资料
    Attributes:
        user: 用户
        avatar: 用户头像
        intro: 介绍
        location: 地址
        money: 钱
        nickname: 昵称
        oauth_token: 第三个方登录返回的用户凭证
    """
    user = models.OneToOneField(User,blank=True, null=True)
    avatar = models.ImageField(upload_to="avatar",blank=True,null=True)
    gender = models.IntegerField(verbose_name=_("Gender"), choices=GENDER_CHOICES, default=2)
    intro = models.TextField(blank=True, null=True)
    mobile = models.CharField(max_length=11, unique=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(editable=True, blank=True, null=True)
    money = models.FloatField(default=0)    
    nickname = models.CharField(max_length=20,blank=True,null=True)
    oauth_token = models.CharField(max_length=100, blank=True,null=True)

class Friend(models.Model):
    """关注关系
    Attributes:
        eggs: An integer count of the eggs we have laid.
    """
    created = models.DateTimeField(auto_now_add=True, editable=False)
    follower = models.ForeignKey(User, related_name="friend_follower")
    followee = models.ForeignKey(User, related_name="friend_followee")

class Gallery(models.Model):
    """影集
    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    author = models.ForeignKey(User, related_name="gallery_author")
    type_kbn = models.IntegerField(choices = GALLERY_TYPE) 
    comment = models.ForeignKey(Comment, related_name="gallery_comment")
    like = models.ForeignKey(Comment, related_name="gallery_comment")
    favourite = models.ForeignKey(Comment, related_name="gallery_comment")
    description = models.TextField(blank=True, null=True)n
    photo = models.ImageField(upload_to="avatar",blank=True,null=True)
    scenes = models.ForeignKey(Scene, related_name="gallery_scene") 

class Comment(models.Model):
    """评论
    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
        

class Photo(models.Model):
    """照片
    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    exif = models.TextField(blank=True, null=True)
    url = models.ImageField(upload_to="photography",blank=True,null=True)

class Scene(models.Model):
    """立面
    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    gallery = models.ForeignKey(Gallery, related_name='scene_gallery')
    scene_template = models.ForeignKey(SceneTemplate, related_name='scene_scene_template')
    photos = models.CommaSeparatedIntegerField() #List of Photo Ids

class SceneTemplate(models.Model):
    """立面模板

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    cover = models.ImageField(upload_to="scene_cover",blank=True,null=True) #立面封面
    background = models.ImageField(upload_to="scene_background",blank=True,null=True) #立面背景
    capacity = models.IntegerField() #立面容量

# 服务
class Service(models.Model):
    pass

# 收藏
class Favourite(models.Model):
    pass

# 赞
class Like(models.Model):
    pass

# 广告
class Advertise(models.Model):
    pass

# 打赏
class Tip(models.Model):
    pass

# 消息
class Message(models.Model):
    pass

# 反馈
class Feedback(models.Model):
    pass

