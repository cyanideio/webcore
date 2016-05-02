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

# 广告类型
ADVERTISE_TYPE = (
    (0, _("Oscar")),    #奥斯卡
    (1, _("Ishiyaki")), #研烧
)

# 反馈类型
FEEDBACK_CHOICES = (
    (0, _("Oscar")),    #奥斯卡
    (1, _("Ishiyaki")), #研烧
)

class BaseModel(models.Model):
    """基础类 
    Attributes:
        created: 创建时间
        updated: 更新时间
    """
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now_add=True, editable=False)
    class Meta:
        abstract = True

class UserProfile(BaseModel):
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

class Friend(BaseModel):
    """关注关系
    Attributes:
        follower
        followee
    """
    follower = models.ForeignKey(User, related_name="friend_follower")
    followee = models.ForeignKey(User, related_name="friend_followee")

class Gallery(BaseModel):
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

class Comment(BaseModel):
    """评论
    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
        

class Photo(BaseModel):
    """照片
    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    exif = models.TextField(blank=True, null=True)
    url = models.ImageField(upload_to="photography",blank=True,null=True)

class Scene(BaseModel):
    """立面
    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    gallery = models.ForeignKey(Gallery, related_name='scene_gallery')
    scene_template = models.ForeignKey(SceneTemplate, related_name='scene_scene_template')
    photos = models.CommaSeparatedIntegerField() #List of Photo Ids

class SceneTemplate(BaseModel):
    """立面模板

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    cover = models.ImageField(upload_to="scene_cover",blank=True,null=True) #立面封面
    background = models.ImageField(upload_to="scene_background",blank=True,null=True) #立面背景
    capacity = models.IntegerField() #立面容量

# 服务
class Service(BaseModel):
    pass

class Favourite(BaseModel):
    """收藏

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    user = models.ForeignKey(User, related_name='favourite_user')
    gallery = models.ForeignKey(Gallery, related_name='favourite_gallery')

class Like(BaseModel):
    """赞

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    user = models.ForeignKey(User, related_name='favourite_user')
    gallery = models.ForeignKey(Gallery, related_name='favourite_gallery')

class Advertise(BaseModel):
    """广告

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    position = models.IntegerField(choices=ADVERTISE_TYPE)
    picture = models.ImageField(upload_to="advertise_picture", blank=True, null=True)
    url = models.URLField() 

class Tip(BaseModel):
    """打赏

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    user = models.ForeignKey(User, related_name='favourite_user')
    gallery = models.ForeignKey(Gallery, related_name='favourite_gallery')
    amount = models.FloatField()

class Message(BaseModel):
    """消息

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    title = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    target = models.IntegerField()

class Feedback(BaseModel):
    """反馈

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    author = models.ForeignKey(User, related_name="feedback_author")
    feedback_type = models.IntegerField(verbose_name=_("feedback_type"), choices=FEEDBACK_CHOICES, default=0)
    content = models.TextField(blank=True, null=True)

