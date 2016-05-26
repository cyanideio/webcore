import redis
import base64
import datetime
from random import randint
from django.utils.translation import ugettext_lazy as _

VERIFICATION_SENT = _('Verification Sent')
INVALID_INTERVAL = _('Invalid Interval')
SALT = '$^45'
INTERVAL = 30

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def get_real_username(mobile_num):
    return base64.b64encode("".join([str(c)+SALT for c in mob]))

def get_mobile_num(real_username):
    return "".join(base64.b64decode(real_username).split(SALT))

def gen_verification_code():
    # return str(randint(1000, 9999))
    return '8888'

def send_vcode(real_username, mobile_num):
    vcode_key = real_username
    vcode_ts_key = "%s_ts" % real_username
    ts = r.get(vcode_ts_key)
    if ts == None:
        vcode = gen_verification_code()
        r.set(vcode_key, vcode)
        r.set(vcode_ts_key, datetime.datetime.now().strftime("%s")) 
        return unicode(VERIFICATION_SENT), 1
    else:
        if (int(datetime.datetime.now().strftime("%s")) - int(ts)) >= INTERVAL:
            vcode = gen_verification_code()
            r.set(vcode_key, vcode)
            r.set(vcode_ts_key, datetime.datetime.now().strftime("%s")) 
            return unicode(VERIFICATION_SENT), 1
        else:
            return unicode(INVALID_INTERVAL), 0

def vcode_varified(mobile_num, vcode):
    varified = vcode == r.get(get_real_username(mobile_num))
    if varified:
        # When varified, delete keys
        r.delete(get_real_username(mobile_num))
        r.delete("%s_ts" % get_real_username(mobile_num))
    return varified