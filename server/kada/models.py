#!/usr/bin/python
# -*- coding: utf-8 -*-
# Kada Models
from __future__ import unicode_literals
import os, time, datetime
# Django Core Modules
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save

# Third Party Modules
from taggit.managers import TaggableManager

# Core Dependencies
from core.models import BaseModel, Collectable, CHARFIELD_MAX_LENGTH, IMAGE_URL_MAX_LENGTH
from django.utils.deconstruct import deconstructible

# 影集类型
GALLERY_TYPE = (
    (0, _("Oscar")),        #奥斯卡
    (1, _("Ishiyaki")),     #研烧
)

TAG_TYPE = (
    (0, _("Oscar")),        #奥斯卡
    (1, _("Ishiyaki")),     #研烧
    (2, _("2")),     #我的画面
    (3, _("3")),     #我的画面
    (4, _("4")),     #我的画面
    (5, _("5")),     #我的画面
    (6, _("6")),     #我的画面
    (7, _("7")),     #我的画面
    (8, _("8")),     #我的画面
    (9, _("9")),     #我的画面
)

# 广告类型
ADVERTISE_POSITION = (
    (1, _("1")),       #启动画面
    (2, _("2")),     #我的画面
    (3, _("3")),     #我的画面
    (4, _("4")),     #我的画面
    (5, _("5")),     #我的画面
    (6, _("6")),     #我的画面
    (7, _("7")),     #我的画面
    (8, _("8")),     #我的画面
    (9, _("9")),     #我的画面
)

# 反馈类型
FEEDBACK_TYPE = (
    (0, _("Political")),    #政治话题
    (1, _("Erotic")),       #色情
    (2, _("Customize")),    #自由填写
    (3, _("Spam")),         #垃圾营销
    (4, _("Copying")),      #抄袭
    (5, _("Bloody")),       #血腥暴力
)

# 反馈对象类型
TARGET_TYPE = (
    (0, _("Gallery")),    #相册
    (1, _("Service")),    #服务
)

# 默认照片列表
PHOTO_LIST_DEFAULT = {
    'scene_list': []
}

# 立面最大照片数
SCENE_MAX_CAPACITY = 50
GALLERY_MAX_CAPACITY = 50

# 图片URL最大长度

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

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(str(int(time.time())), ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

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
    equipment = models.TextField()
    scene_seq = models.CommaSeparatedIntegerField(max_length=GALLERY_MAX_CAPACITY*2, blank=True, null=True)
    tags = TaggableManager()

    class Meta:
        verbose_name = "gallery"

    def __unicode__(self):
        return u'%s' % self.name

class GalleryTags(BaseModel):
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    type_kbn = models.IntegerField(choices=TAG_TYPE)

class SceneSet(BaseModel):
    """立面集合
    属性:
        name: 名称
        tags: 分类标签
    """
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    tags = TaggableManager()

    def __unicode__(self):
        return u'%s' % self.name


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

def create_comment_message(sender, instance, created, **kwargs):
    if created:
        exp = datetime.datetime.now() + datetime.timedelta(days=365)
        Message.objects.create(author=instance.author, target=instance.gallery.author, jump_target=instance.gallery.id, title="你的作品被评论了！", msg_type=1, content="你的作品被评论了！", system=True, expires=exp)

post_save.connect(create_comment_message, sender=Comment)
        
class Photo(BaseModel):
    """照片
    属性:
        exif: 照片信息
        image: 照片所属具体图片
        gallery: 照片所属照片集
    """
    author = models.ForeignKey(User, related_name="photo_author", limit_choices_to={'is_superuser': False})
    exif = models.TextField(blank=True, null=True)
    image = models.ImageField(max_length=IMAGE_URL_MAX_LENGTH, blank=True, null=True, upload_to='photos/%Y/%m/%d/')
    gallery = models.ManyToManyField(Gallery, related_name='photo_gallery')
    description = models.TextField()

class SceneTemplate(BaseModel):
    """立面模板
    属性:
        cover: 立面封面
        background: 立面背景
        capacity: 立面容量
        canvas_vw_p: 画板宽度占屏幕宽度比例
        canvas_top_p: 画板距离屏幕顶部距离比例
    """
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    cover = models.ImageField(max_length=IMAGE_URL_MAX_LENGTH, blank=True, null=True, upload_to='System/scene/cover')
    flat = models.ImageField(max_length=IMAGE_URL_MAX_LENGTH, blank=True, null=True, upload_to='System/scene/2D')
    three_dimension = models.ImageField(max_length=IMAGE_URL_MAX_LENGTH, blank=True, null=True, upload_to='System/scene/3D')
    capacity = models.IntegerField(validators=[MaxValueValidator(SCENE_MAX_CAPACITY)], choices=SCENE_CHOICES)
    canvas_config = models.TextField()
    scene_set = models.ManyToManyField(SceneSet, related_name='scene_set')

    def __unicode__(self):
        return u'%s' % self.name

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

class PhotoFrame(Collectable):
    """相框
    属性:
        corner: 边角图片
        texture: 纹理图片 
        tag: 标签属性
    """
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    description = models.TextField()
    corner = models.ImageField(max_length=IMAGE_URL_MAX_LENGTH, blank=True, null=True, upload_to='System/scene/frame/corner')
    texture = models.ImageField(max_length=IMAGE_URL_MAX_LENGTH, blank=True, null=True, upload_to='System/scene/frame/texture')
    scene_template = models.ManyToManyField(SceneTemplate, related_name='scene_template')
    tags = TaggableManager()

    def __unicode__(self):
        return u'%s' % self.name

class ServiceType(BaseModel):
    """服务类型
    属性:
        name: 服务标题
    """
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)

    def __unicode__(self):
        return u'%s' % self.name

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
    title = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    position = models.IntegerField(choices=ADVERTISE_POSITION)
    picture = models.ImageField(max_length=IMAGE_URL_MAX_LENGTH, blank=True, null=True, upload_to=PathAndRename('advertises'))
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


class Feedback(BaseModel):
    """反馈
    属性:
        author: 反馈用户
        feedback_type: 反馈类型
        content: 反馈内容
    """
    author = models.ForeignKey(User, related_name="feedback_author", limit_choices_to={'is_superuser': False})
    feedback_type = models.IntegerField(verbose_name=_("feedback_type"), choices=FEEDBACK_TYPE, default=0)
    target_type = models.IntegerField(verbose_name=_("target_type"), choices=TARGET_TYPE, blank=True, null=True)
    target = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
