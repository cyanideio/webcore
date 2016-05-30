#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django Core Modules
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

# Third Party Modules
from taggit.managers import TaggableManager

# Helpers
from core.utils.helpers import gen_temp_token
from tastypie.models import create_api_key

CHARFIELD_MAX_LENGTH = 100
IMAGE_URL_MAX_LENGTH = 100

# 性别类型
GENDER_TYPE = (
    (0, _("Male")),         #男性
    (1, _("Female")),       #女性
)

# 用户类型
USER_TYPE = (
    (0, _("Normal")),       #普通用户
    (1, _("Fan")),          #爱好者
    (2, _("Photographer")), #摄影师
    (3, _("Model")),        #模特
)

# 用户状态
USER_STATE = (
    (0, _("Forbidden")),    #禁用     
    (1, _("Normal")),       #正常
)

class BaseModel(models.Model):
    """基础类 
    属性:
        created: 创建时间
        updated: 更新时间
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Collectable(BaseModel):
    """可以被点赞/收藏的类
    属性:
        likes: 赞
        favourites: 收藏
    """
    likes = models.ManyToManyField(User, related_name="%(class)ss_likes", limit_choices_to={'is_superuser': False})
    favourites = models.ManyToManyField(User, related_name="%(class)ss_favourites", limit_choices_to={'is_superuser': False})

    class Meta:
        abstract = True

class UserProfile(BaseModel):
    """用户资料
    属性:
        user: 外键用户
        avatar: 头像
        gender: 性别
        intro: 介绍
        mobile: 手机号码
        location: 地址
        birthday: 生日
        nickname: 昵称
        oauth_token: 第三个方登录返回的用户凭证
        user_type: 用户类型
        user_cert: 会员认证"
        experts_cert: 专家认证"
        pg_cert: 摄影师认证"
        model_cert: 模特认证
        user_state: 用户状态
        tags: 分类标签
    """
    user = models.OneToOneField(User,blank=True, null=True, related_name='user_profile')
    avatar = models.ImageField(max_length=IMAGE_URL_MAX_LENGTH, blank=True, null=True, upload_to='avatars/')
    gender = models.IntegerField(verbose_name=_("Gender"), choices=GENDER_TYPE, default=0)
    intro = models.TextField(blank=True, null=True)
    mobile = models.CharField(max_length=11, unique=True)
    location = models.CharField(max_length=CHARFIELD_MAX_LENGTH, blank=True, null=True)
    birthday = models.DateField(editable=True, blank=True, null=True)
    nickname = models.CharField(max_length=CHARFIELD_MAX_LENGTH, unique=True)
    oauth_token = models.CharField(max_length=CHARFIELD_MAX_LENGTH, blank=True,null=True)
    user_type = models.IntegerField(verbose_name=_("User Type"), choices=USER_TYPE, default=0)
    user_cert = models.BooleanField(default=False)
    experts_cert = models.BooleanField(default=False)
    pg_cert = models.BooleanField(default=False)
    model_cert = models.BooleanField(default=False)
    user_state = models.IntegerField(choices=USER_STATE, default=1)
    tags = TaggableManager()

def create_user_profile_and_apikey(sender, instance, created, **kwargs):
    if instance.is_superuser:
        return
    if created:
        UserProfile.objects.create(
            user=instance, 
            mobile=gen_temp_token(11),
            nickname=instance.username
        )
        create_api_key(User, instance=instance, created=True)

post_save.connect(create_user_profile_and_apikey, sender=User)

class Friend(BaseModel):
    """关注关系
    属性:
        follower: 发起关注者
        followee: 被关注者
    """
    follower = models.ForeignKey(User, related_name="friend_follower", limit_choices_to={'is_superuser': False})
    followee = models.ForeignKey(User, related_name="friend_followee", limit_choices_to={'is_superuser': False})

class Message(BaseModel):
    """消息
    属性:
        author: 消息发送者
        target: 消息接收者
        title: 消息标题
        content: 消息内容
        expires: 消息失效时间
    """
    author = models.ForeignKey(User, related_name="message_author", limit_choices_to={'is_superuser': False})
    target = models.ForeignKey(User, related_name="message_target", limit_choices_to={'is_superuser': False})
    title = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    content = models.TextField()
    system = models.BooleanField(default=False)
    expires = models.DateTimeField()
