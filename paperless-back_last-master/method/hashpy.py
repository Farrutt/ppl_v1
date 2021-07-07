#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config.lib import *

def encode(data):
    randoms = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    encodes = jwt.encode(data,'bill',algorithm='HS256')
    encodes = encodes.decode('utf8').split('.')
    encodes[1] = encodes[1]+randoms
    encodes = encodes[2] +'.'+encodes[0]+'.'+encodes[1]
    return encodes

def decode(data):
    decodes = data
    decodes = decodes.split('.')
    decodes[2] = decodes[2][:-32] ##[:-32] ลบข้อมูลนับจากหลังไป 32 ตัวอักษร
    decodes = decodes[1]+'.'+decodes[2]+'.'+decodes[0]
    decodes = jwt.decode(decodes,'bill',algorithms='HS256')
    return decodes

def hash_512(data):
    str_data = str(data)
    hash_object = hashlib.sha512(str_data)
    hex_dig = hash_object.hexdigest()
    return hex_dig

    
def hash_512_v2(data):
    str_data = data.encode('utf-8')
    hash_object = hashlib.sha512(str_data)
    hex_dig = hash_object.hexdigest()
    return hex_dig