#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# 影集类型
GALLERY_TYPE = (
    (0, _("Oscar")),        #奥斯卡
    (1, _("Ishiyaki")),     #研烧
)

# 广告类型
ADVERTISE_POSITION = (
    (0, _("Home")),         #首页
    (1, _("Splash")),       #启动画面
    (1, _("Settings")),     #我的画面
)

# 反馈类型
FEEDBACK_TYPE = (
    (0, _("Political")),    #政治话题
    (1, _("Erotic")),       #色情
    (2, _("Customize")),    #自由填写
)

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

# 默认照片列表
PHOTO_LIST_DEFAULT = {
    'scene_list': []
}

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
        user_cert: 会员认证
        experts_cert: 专家认证
        pg_cert: 摄影师认证
        model_cert: 模特认证
        user_state: 用户状态
    """
    user = models.OneToOneField(User,blank=True, null=True)
    avatar = models.ImageField(upload_to="avatar",blank=True,null=True)
    gender = models.IntegerField(verbose_name=_("Gender"), choices=GENDER_TYPE, default=0)
    intro = models.TextField(blank=True, null=True)
    mobile = models.CharField(max_length=11, unique=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(editable=True, blank=True, null=True)
    nickname = models.CharField(max_length=20,blank=True,null=True)
    oauth_token = models.CharField(max_length=100, blank=True,null=True)
    user_type = models.IntegerField(verbose_name=_("User Type"), choices=USER_TYPE, default=0)
    user_cert = models.BooleanField()
    experts_cert = models.BooleanField()
    pg_cert = models.BooleanField()
    model_cert = models.BooleanField()
    user_state = models.IntegerField(choices=USER_STATE)

class Friend(BaseModel):
    """关注关系
    属性:
        follower: 发起关注者
        followee: 被关注者
        friends: 互为好友关系
    """
    follower = models.ForeignKey(User, related_name="friend_follower")
    followee = models.ForeignKey(User, related_name="friend_followee")
    friends = models.BooleanField() 

class Gallery(BaseModel):
    """影集
    属性:
        author: 影集作者
        type_kbn: 影集属性区分
        description: 描述
        scene_seq: 立面顺序
    """
    author = models.ForeignKey(User, related_name="gallery_author")
    type_kbn = models.IntegerField(choices=GALLERY_TYPE) 
    description = models.TextField(blank=True, null=True)
    scene_seq = models.CommaSeparatedIntegerField()

class Comment(BaseModel):
    """评论
    属性:
        author: 评论作者
        gallery: 评论对应的影集
        content: 评论内容
    """
    author = models.ForeignKey(User, related_name="comment_author")
    gallery = models.ForeignKey(Gallery, related_name="comment_gallery")
    content = models.TextField(blank=True, null=True)
        
class Photo(BaseModel):
    """照片
    属性:
        exif: 照片信息
        image: 照片所属具体图片
        gallery: 照片所属照片集
    """
    exif = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="photography",blank=True,null=True)
    gallery = models.ManyToManyField(related_name='photo_gallery')

class Scene(BaseModel):
    """立面
    属性:
        gallery: 立面所属影集
        scene_template: 立面模板
        photo_seq: 照片顺序
    """
    gallery = models.ForeignKey(Gallery, related_name='scene_gallery')
    scene_template = models.ForeignKey(SceneTemplate, related_name='scene_scene_template')
    photo_seq = models.CommaSeparatedIntegerField()

class SceneTemplate(BaseModel):
    """立面模板

    属性:
        cover: 立面封面
        background: 立面背景
        capacity: 立面容量
    """
    cover = models.ImageField(upload_to="scene_cover",blank=True,null=True)
    background = models.ImageField(upload_to="scene_background",blank=True,null=True)
    capacity = models.IntegerField()

# 服务
# class Service(BaseModel):
#     pass

class Favourite(BaseModel):
    """收藏

    属性:
        user:
        gallery:
    """
    user = models.ForeignKey(User, related_name='favourite_user')
    gallery = models.ForeignKey(Gallery, related_name='favourite_gallery')

class Like(BaseModel):
    """赞

    属性:
        user:
        gallery:
    """
    user = models.ForeignKey(User, related_name='favourite_user')
    gallery = models.ForeignKey(Gallery, related_name='favourite_gallery')

class Advertise(BaseModel):
    """广告

    属性:
        position: 广告显示区域
        picture: 照片
        url: 广告指向链接
    """
    position = models.IntegerField(choices=ADVERTISE_POSITION)
    picture = models.ImageField(upload_to="advertise_picture", blank=True, null=True)
    url = models.URLField() 

class Tip(BaseModel):
    """打赏

    属性:
        tipper: 打赏用户
        gallery: 被打赏相册
        amount: 打赏数额
    """
    tipper = models.ForeignKey(User, related_name='favourite_user')
    gallery = models.ForeignKey(Gallery, related_name='favourite_gallery')
    amount = models.FloatField()

class Message(BaseModel):
    """消息

    属性:
        title: 消息标题
        content: 消息内容
        target: 消息对象(用户ID) ｜ 当用户ID为-1的时候，消息为广播
        expires: 消息失效时间
    """
    title = models.CharField()
    content = models.TextField()
    target = models.IntegerField()
    expires = models.DateTimeField()

class Feedback(BaseModel):
    """反馈

    属性:
        author: 反馈用户
        feedback_type: 反馈类型
        content: 反馈内容
    """
    author = models.ForeignKey(User, related_name="feedback_author")
    feedback_type = models.IntegerField(verbose_name=_("feedback_type"), choices=FEEDBACK_TYPE, default=0)
    content = models.TextField(blank=True, null=True)
