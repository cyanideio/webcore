#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django Core Modules
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save

# Third Party Modules
from taggit.managers import TaggableManager

# Helpers
from kada.utils.helpers import gen_temp_token
from tastypie.models import create_api_key

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

# 立面最大照片数
SCENE_MAX_CAPACITY = 50
GALLERY_MAX_CAPACITY = 12

# 图片URL最大长度
IMAGE_URL_MAX_LENGTH = 100
CHARFIELD_MAX_LENGTH = 100

SCENE_CHOICES = (
    # (0, _("Zero")),       #0
    (1, _("One")),        #1
    (2, _("Two")),        #2
    (3, _("Three")),      #3
    (4, _("Four")),       #4
    (5, _("Five")),       #5
    (6, _("Six")),        #6
    (7, _("Seven")),      #7
    (8, _("Eight")),      #8
    (9, _("Nine")),       #9
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
    likes = models.ManyToManyField(User, related_name="%(class)ss_likes")
    favourites = models.ManyToManyField(User, related_name="%(class)ss_favourites")

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
    avatar = models.CharField(max_length=IMAGE_URL_MAX_LENGTH, blank=True, null=True)
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
        friends: 互为好友关系
    """
    follower = models.ForeignKey(User, related_name="friend_follower", limit_choices_to={'is_superuser': False})
    followee = models.ForeignKey(User, related_name="friend_followee", limit_choices_to={'is_superuser': False})
    friends = models.BooleanField() 

class Gallery(Collectable):
    """影集
    属性:
        author: 影集作者
        type_kbn: 影集属性区分
        description: 描述
        scene_seq: 立面顺序
        likes: 影集赞
        favourites: 影集收藏
        tags: 分类标签
    """
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    author = models.ForeignKey(User, related_name="gallery_author", limit_choices_to={'is_superuser': False})
    type_kbn = models.IntegerField(choices=GALLERY_TYPE) 
    description = models.TextField()
    scene_seq = models.CommaSeparatedIntegerField(max_length=GALLERY_MAX_CAPACITY*2, blank=True, null=True)
    tags = TaggableManager()

    class Meta:
        verbose_name = "gallery"

class Comment(BaseModel):
    """评论
    属性:
        author: 评论作者
        gallery: 评论对应的影集
        content: 评论内容
    """
    author = models.ForeignKey(User, related_name="comment_author", limit_choices_to={'is_superuser': False})
    gallery = models.ForeignKey(Gallery, related_name="comment_gallery")
    content = models.TextField(blank=True, null=True)
        
class Photo(BaseModel):
    """照片
    属性:
        exif: 照片信息
        image: 照片所属具体图片
        gallery: 照片所属照片集
    """
    author = models.ForeignKey(User, related_name="photo_author", limit_choices_to={'is_superuser': False})
    exif = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=IMAGE_URL_MAX_LENGTH, blank=True, null=True)
    gallery = models.ManyToManyField(Gallery, related_name='photo_gallery')

class SceneTemplate(BaseModel):
    """立面模板
    属性:
        cover: 立面封面
        background: 立面背景
        capacity: 立面容量
        canvas_vw_p: 画板宽度占屏幕宽度比例
        canvas_top_p: 画板距离屏幕顶部距离比例
    """
    cover = models.CharField(max_length=IMAGE_URL_MAX_LENGTH, blank=True, null=True)
    background = models.CharField(max_length=IMAGE_URL_MAX_LENGTH, blank=True, null=True)
    capacity = models.IntegerField(validators=[MaxValueValidator(SCENE_MAX_CAPACITY)], choices=SCENE_CHOICES)
    canvas_config = models.TextField()

class Scene(BaseModel):
    """立面
    属性:
        gallery: 立面所属影集
        scene_template: 立面模板
        photo_seq: 照片顺序
    """
    gallery = models.ForeignKey(Gallery, related_name='scene_gallery', limit_choices_to={'type_kbn': 0})
    scene_template = models.ForeignKey(SceneTemplate, related_name='scene_scene_template')
    photo_seq = models.CommaSeparatedIntegerField(max_length=CHARFIELD_MAX_LENGTH)

class ServiceType(BaseModel):
    """服务类型
    属性:
        name: 服务标题
    """
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)

class Service(Collectable):
    """服务
    属性:
        author: 服务发布者
        title: 服务标题
        style: 服务风格
        unit_price: 服务单价
        content: 服务内容
        period: 服务档期
        tags: 分类标签
    """
    author = models.ForeignKey(User, related_name="service_author", limit_choices_to={'is_superuser': False})
    title = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    service_type = models.ForeignKey(ServiceType, related_name="service_service_type")
    unit_price = models.FloatField()
    content = models.TextField()
    period = models.TextField()
    tags = TaggableManager()

    class Meta:
        verbose_name = "service"

class Advertise(BaseModel):
    """广告
    属性:
        position: 广告显示区域
        picture: 照片
        url: 广告指向链接
    """
    position = models.IntegerField(choices=ADVERTISE_POSITION)
    picture = models.CharField(max_length=IMAGE_URL_MAX_LENGTH, blank=True, null=True)
    url = models.URLField() 

class Tip(BaseModel):
    """打赏
    属性:
        tipper: 打赏用户
        gallery: 被打赏相册
        amount: 打赏数额
    """
    tipper = models.ForeignKey(User, related_name='tip_user', limit_choices_to={'is_superuser': False})
    gallery = models.ForeignKey(Gallery, related_name='tip_gallery')
    amount = models.FloatField()

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

class Feedback(BaseModel):
    """反馈
    属性:
        author: 反馈用户
        feedback_type: 反馈类型
        content: 反馈内容
    """
    author = models.ForeignKey(User, related_name="feedback_author", limit_choices_to={'is_superuser': False})
    feedback_type = models.IntegerField(verbose_name=_("feedback_type"), choices=FEEDBACK_TYPE, default=0)
    content = models.TextField(blank=True, null=True)
