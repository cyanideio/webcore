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

class UserProfile(object):
    """用户资料"""
    user = models.OneToOneField(User,blank=True, null=True)
    avatar = models.ImageField(upload_to="avatar",blank=True,null=True)
    gender = models.IntegerField(verbose_name=_("Gender"), choices=GENDER_CHOICES, default=2)
    intro = models.TextField(blank=True, null=True)
    mobile = models.CharField(max_length=11, unique=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(editable=True, blank=True, null=True)
    money = models.FloatField(default=0)    
    nickname = models.CharField(max_length=20,blank=True,null=True)
    oauth_token = models.CharField(max_length=100, blank=True,null=True)   #  第三个方登录返回的用户凭证

class Friend(models.Model):
    """关注关系"""
    created = models.DateTimeField(auto_now_add=True, editable=False)
    follower = models.ForeignKey(User, related_name="friend_follower")
    followee = models.ForeignKey(User, related_name="friend_followee")

class Gallery(models.Model):
    """影集"""
    author = models.ForeignKey(User, related_name="gallery_author")
    type_kbn = models.IntegerField(choices = GALLERY_TYPE) 
    comment = models.ForeignKey(Comment, related_name="gallery_comment")
    like = models.ForeignKey(Comment, related_name="gallery_comment")
    favourite = models.ForeignKey(Comment, related_name="gallery_comment")
    descriptio = models.TextField(blank=True, null=True)n
    photo = models.ImageField(upload_to="avatar",blank=True,null=True)
    scenes = models.ForeignKey(Scene, related_name="gallery_scene") 

class Comment(models.Model):
    """评论"""
        

# 照片
class Photo(models.Model):
    pass

# 立面
class Scene(models.Model):
    pass

# 立面模板
class SceneTemplate(models.Model):
    pass

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

