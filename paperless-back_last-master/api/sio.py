#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from method.publicqrcode import *
from method.document import *
from controller.mail_string import *
from controller.validate import *
from db.db_method import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from api.file import *

@sio.on('connect')
def connect(sid, environ):
    print('con',sid+'==-----------==')

@sio.on('dashboard')
def dashboard_v1(sid,dataJson):
    
    if 'emailUser' in dataJson and 'secret_key' in dataJson and len(dataJson) == 2:
        print(dataJson)
        if dataJson['secret_key'] == '4DnsTP8Nz2':
            emailUser = str(dataJson['emailUser']).lower()
            result_select = select().select_dashboard_recipient_v2(emailUser)
            print(result_select)
    #         sio.emit('test',result_select)
    #         # if result_select['result'] == 'OK':
    #         #     return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
    #         # else:
    #         #     return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':result_select['messageER']}),200
    #     else:
    #         return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'secret key incorrect'}),200
    # else:
    #     return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'}),200
@sio.on('test')
def test_jj(sid,data):
    print(data)

@sio.on('join_room')
def on_join_room(sid,data):
    room = data['room']
    emil = data['emailUser']
    sio.enter_room(sid,room)
    # session[sid] = emil
    # log_os(data['room']+'-----join')
    return "connected"

@sio.on('get_room')
def get_room(sid,data):
    room = data['room']
    print(sid)
    # sio.enter_room(sid,room)
    # log_os(data['room']+'-----join')
    return "connected"

@sio.on('disconnect')
def disconnect(sid):
    print(sid)