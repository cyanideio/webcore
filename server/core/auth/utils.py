#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import redis
import base64
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from random import randint
from django.utils.translation import ugettext_lazy as _

VERIFICATION_SENT = _('Verification Sent')
INVALID_INTERVAL = _('Invalid Interval')
SALT = ''
INTERVAL = 30

r = redis.StrictRedis(host='localhost', port=6379, db=0)


# Mail Conf
sender = 'no-reply@cyanide.io'
username = sender
smtpserver = 'smtp.qiye.163.com'
password = 'Yoren2016'

TITLE = "Mail From Cyanide.io"
CONTENT = """
<html>
<p> 
    Hello, your verification code is: <b>%s</b>
</p> 
<b>
    Cyanide.io
</b>
</html>
"""

def send_mail(vcode, receiver):
    try:
        msg = MIMEText(CONTENT % vcode,'html','utf-8')
        if not isinstance(TITLE,unicode):
            TITLE = unicode(TITLE, 'utf-8')
        msg['Subject'] = TITLE
        msg['From'] = sender
        msg['To'] = receiver
        msg["Accept-Language"]="zh-CN"
        msg["Accept-Charset"]="ISO-8859-1,utf-8"

        smtp = smtplib.SMTP_SSL(smtpserver, 994)
    # print username, password
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        return True
    except Exception, e:
        print str(e)
        return False

def send_email(vcode, number):
    req=top.api.AlibabaAliqinFcSmsNumSendRequest("gw.api.taobao.com", 80)
    req.set_app_info(top.appinfo('23314809','d18426e753bd43d702e990fe1235e55a'))
    req.sms_template_code="SMS_10661343"
    req.sms_type="normal"
    req.sms_free_sign_name=""
    req.sms_param='{"code":"%s"}' % vcode
    req.extend="123456"
    req.rec_num=str(number)
    try:
        resp= req.getResponse()
        return True
    except Exception, e:
        print e
        return False

def get_real_username(mobile_num):
    return base64.b64encode("".join([str(c)+SALT for c in mobile_num]))

def get_mobile_num(real_username):
    return "".join(base64.b64decode(real_username).split(SALT))

def gen_verification_code(num):
    vcode = str(randint(1000, 9999))
    if send_email(vcode, num):
        return vcode
    else:
        return False

def send_vcode(real_username, mobile_num):
    vcode_key = real_username
    vcode_ts_key = "%s_ts" % real_username
    ts = r.get(vcode_ts_key)
    if ts == None:
        vcode = gen_verification_code(mobile_num)
        if vcode:
            r.set(vcode_key, vcode)
            r.set(vcode_ts_key, datetime.datetime.now().strftime("%s")) 
            return unicode(VERIFICATION_SENT), 1
        else:
            return unicode(INVALID_INTERVAL), 0
    else:
        if (int(datetime.datetime.now().strftime("%s")) - int(ts)) >= INTERVAL:
            vcode = gen_verification_code(mobile_num)
            if vcode:
                r.set(vcode_key, vcode)
                r.set(vcode_ts_key, datetime.datetime.now().strftime("%s")) 
                return unicode(VERIFICATION_SENT), 1
            else:
                return unicode(INVALID_INTERVAL), 0
        else:
            return unicode(INVALID_INTERVAL), 0

def vcode_varified(mobile_num, vcode):
    varified = vcode == r.get(get_real_username(mobile_num))
    if varified:
        # When varified, delete keys
        r.delete(get_real_username(mobile_num))
        r.delete("%s_ts" % get_real_username(mobile_num))
    return varified
