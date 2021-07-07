#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from method.publicqrcode import *
from method.document import *
from method.verify import *
from method.callserver import *
from controller.mail_string import *
from controller.validate import *
from db.db_method import *
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from api.file import *
from api.memory import *
from method.sftp_fucn import *
from method.callwebHook import *



if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less

@status_methods.route('/api/v1/hook_chat', methods=['POST'])
def hook_chat_api_v1():
    dataJson = request.json
    if 'source' in dataJson and 'message' in dataJson and 'event' in dataJson and 'bot_id' in dataJson:
        tmpbot_id = dataJson['bot_id']
        tmp_source = dataJson['source']
        tmpmessage = dataJson['message']
        tmpevent = dataJson['event']
        if tmpevent == 'message':
            token_bot = token_service
            bot_chat_id = tmpbot_id
            if 'email' in tmp_source and 'one_id' in tmp_source:
                send_messageToChat_v4('สวัสดีครับ Paperless ยินดีให้บริการครับ',tmp_source['email'],token_bot,bot_chat_id,"")
                # send_messageToChat_v4('สามารถเลือกบริการของ paperless ได้เลยครับ',tmp_source['email'],token_bot,bot_chat_id,"")
                quickreply_onechat_v1('เลือกรายการที่ต้องการใช้งานได้เลยครับ',tmp_source['one_id'],token_bot,bot_chat_id,"")
            print(dataJson)
