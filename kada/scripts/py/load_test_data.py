#-*- coding:UTF-8 -*-
import os, sys
import django
current_path = os.getcwd()
sys.path.append(current_path)
os.environ["DJANGO_SETTINGS_MODULE"] = "kada.settings"
django.setup()

from autofixture import AutoFixture, generators
from core.models import Gallery, UserProfile
from django.contrib.auth.models import User

from random import randint

# 创建管理员
print "插入管理员...."
User.objects.create_superuser('admin', 'admin@example.com', 'dealdodo')

# 用户
print "插入用户...."
userFixture = AutoFixture(User)
userEntries = userFixture.create(20)

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

