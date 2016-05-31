#-*- coding:UTF-8 -*-
import os, sys
import django
import datetime
current_path = os.getcwd()
sys.path.append(current_path)
os.environ["DJANGO_SETTINGS_MODULE"] = "manifest.settings"
django.setup()

from autofixture import AutoFixture, generators
from core.models import UserProfile, Friend, Message
from kada.models import Gallery, Photo, Scene, SceneSet, SceneTemplate, Comment, Service, ServiceType, Advertise
from core.auth.utils import get_real_username
from django.contrib.auth.models import User

import random
random.seed(datetime.datetime.now())

## 通用数据集
SCENE_COVERS = [
    'cover_photo_1',
    'cover_photo_2',
    'cover_photo_3',
    'cover_photo_4',
]

SCENE_BACKGROUNDS = [
    'background_photo_1',
    'background_photo_2',
    'background_photo_3',
    'background_photo_4',
]

CANVAS_CONFIGS = [
    '{canvas:position}',
    '{canvas:position}',
    '{canvas:position}',
    '{canvas:position}',
    '{canvas:position}',
]

def GetRandomImage(data):
    return "%s.jpg" % random.choice(data)

def GenUserName():
    n = [str(i) for i in range(0,10)]
    random.shuffle(n)
    return "".join(n)

# 创建管理员
print "插入管理员...."
User.objects.create_superuser('admin', 'admin@example.com', 'dealdodo')

# 用户
print "插入用户...."
userEntries = []
for x in xrange(1,50):
    username = "test_user_%s" % x
    real_username = get_real_username(username)
    email = '%s@beatles.com' % username
    user = User.objects.create_user(username=real_username, email=email, password=username)
    userEntries.append(user)

# 研烧
ishiyakiFixture = AutoFixture(Gallery, field_values={
    'type_kbn'    : 1,
    'scene_seq'   : "",
    'name' : "这是研烧"
})
print "插入研烧...."
ishiyakiEntries = ishiyakiFixture.create(20)

# 奥斯卡
oskarFixture = AutoFixture(Gallery, field_values={
    'type_kbn'    : 0,
    'scene_seq'   : "",
    'name' : "这是奥斯卡"
})
print "插入奥斯卡...."
oskarEntries = oskarFixture.create(20)

# 立面集合
print "插入立面集合...."
scenesetFixture = AutoFixture(SceneSet)
scenesetEntries = scenesetFixture.create(20)

# 立面模板
print "插入立面模板...."
for i in range(100):
    st = SceneTemplate( 
        cover = GetRandomImage(SCENE_COVERS),
        background = GetRandomImage(SCENE_BACKGROUNDS),
        capacity = random.randint(0,9),
        canvas_config = random.choice(CANVAS_CONFIGS)
    )
    st.save()
    st.scene_set.add(random.choice(scenesetEntries))

# 立面
print "插入立面...."
sceneFixture = AutoFixture(Scene)
sceneEntries = sceneFixture.create(60)


# 照片
print "插入照片...."
photoEntries = []
for i in range(200):
    ip = Photo(
        author = random.choice(userEntries),
        exif = 'exif info',
        image = "random_user_image_%s.jpg" % random.randint(0,100),
    )
    ip.save()
    photoEntries.append(ip)

# 研烧插入照片
print "将照片加入到研烧..."
for entry in ishiyakiEntries:
    random.shuffle(photoEntries)
    for e in photoEntries[4:random.randint(5,12)]:
        e.gallery.add(entry)

# 奥斯卡插入照片
print "将照片加入到奥斯卡..."
for osk in oskarEntries:
    scene_seq = []
    for scene in osk.scene_gallery.all():
        random.shuffle(photoEntries)
        scene_seq.append(str(scene.id))
        photo_seq = []
        for e in photoEntries[0:scene.scene_template.capacity]:
            e.gallery.add(osk)
            photo_seq.append(str(e.id)) 

        scene.photo_seq = ",".join(photo_seq)
        scene.save()
    osk.scene_seq = ",".join(scene_seq)
    osk.save()

# 朋友关系
friendFixture = AutoFixture(Friend)
print "插入关注关系...."
friendEntries = friendFixture.create(200)

# 评论
commentFixture = AutoFixture(Comment)
print "插入评论...."
commentEntries = commentFixture.create(100)

# 服务类型
serviceTypeFixture = AutoFixture(ServiceType)
print "插入服务类型...."
serviceTypeEntries = serviceTypeFixture.create(10)

# 服务
serviceFixture = AutoFixture(Service)
print "插入服务...."
serviceEntries = serviceFixture.create(100)

# 消息
messageFixture = AutoFixture(Message)
print "插入消息...."
messageEntries = messageFixture.create(100)

# 广告
advertiseEntries = []
print "插入广告...."
for i in range(50):
    adv = Advertise( 
        position = random.randint(0,2),
        picture = GetRandomImage(SCENE_BACKGROUNDS),
        url = "http://test.com"
    )
    adv.save()
    advertiseEntries.append(adv)
