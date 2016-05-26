#!/usr/bin/python
# -*- coding: utf-8 -*
import uuid

def gen_temp_token(length):
    """生成临时TOKEN""" 
    return "m%s" % str(uuid.uuid1())[0:length-1]