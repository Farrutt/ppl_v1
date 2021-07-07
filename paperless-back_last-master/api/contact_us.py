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
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *
from db.db_method_4 import *
from db.db_method_5 import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from api.file import *
from method.sftp_fucn import *
from method.callwebHook import *
from api.schedule_log import *

if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less

@status_methods.route('/api/v1/contact_us', methods=['POST','GET'])
def contact_us_api():
    if request.method == 'POST':
        dataJson = request.json
        if 'name' in dataJson and 'company_name' in dataJson and 'phone_no' in dataJson and 'email' in dataJson and 'title' in dataJson and 'message' in dataJson:
            name = dataJson['name']
            company_name = dataJson['company_name']
            phone_no = dataJson['phone_no']
            email = dataJson['email']
            title = dataJson['title']
            message = dataJson['message']
            r = insert_5().insert_contactus_v1(name,company_name,phone_no,email,title,message)
            if r['result'] == 'OK':
                return jsonify({'result':'OK','status_Code':200,'messageText':r['messageText'],'messageER':None})
            else:
                return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':r['messageText']})
        abort(404)