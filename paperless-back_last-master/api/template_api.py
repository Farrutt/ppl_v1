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
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from api.file import *



if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less

@status_methods.route('/api/v2/template/template_document', methods=['POST','PUT','GET'])
@token_required_v3
def template_document_v2():
    if request.method == 'POST':
        dataJson = request.json
        logger.info(len(dataJson))
        if 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Name' in dataJson and 'step_Upload' in dataJson\
        and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and 'documentDetails' in dataJson and 'urgent_type' in dataJson\
        and 'biz_info' in dataJson and 'condition_string' in dataJson and 'template_webhook' in dataJson\
        and 'email_center' in dataJson and 'digit_sign' in dataJson and 'formula_temp' in dataJson and 'page_sign_options' in dataJson and 'options_page' in dataJson and 'use_status' in dataJson\
        and 'time_expire' in dataJson and 'importance' in dataJson and 'last_digitsign' in dataJson and 'status_ref' in dataJson and len(dataJson) == 24:
            step_Code = str(uuid.uuid4())
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            try:
                eval(dataJson['step_Upload'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_Upload ให้เป็น Json ได้'}),200
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            # if dataJson['time_expire'] != None:
            res_insert_template = insert_1().insert_paper_template_sql(step_Code,dataJson['step_Data'],dataJson['step_Max'],dataJson['username'],dataJson['email'],st,dataJson['step_Name'],dataJson['step_Upload'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'],None,dataJson['documentDetails'],dataJson['urgent_type'],dataJson['biz_info'],condition_temp=dataJson['condition_string'],webhook=dataJson['template_webhook'],email_center=dataJson['email_center'],formula_temp=dataJson['formula_temp'],digit_sign=dataJson['digit_sign'],page_sign_options=dataJson['page_sign_options'],options_page=dataJson['options_page'],use_status=dataJson['use_status'],time_expire=dataJson['time_expire'],importance=dataJson['importance'],last_digitsign=dataJson['last_digitsign'],status_ref=dataJson['status_ref'])
            # print(res_insert_template)
            if res_insert_template['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':res_insert_template['messageText'],'data':None},'status_Code':200}),200
        elif 'username' in dataJson and 'template_code' in dataJson and 'use_status' in dataJson and len(dataJson) == 3:
            res_delete = update().update_template_use_status_v3(dataJson['username'],dataJson['template_code'],dataJson['use_status'])
            if res_delete['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':res_delete['messageText'],'data':None},'status_Code':200}),200
        elif 'username' in dataJson and 'template_code' in dataJson and len(dataJson) == 2:
            res_delete = update().update_template_v3(dataJson['username'],dataJson['template_code'])
            if res_delete['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':res_delete['messageText'],'data':None},'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
        dataJson = request.json
        if 'step_Name' in dataJson and 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and 'documentDetails' in dataJson and 'urgent_type' in dataJson and 'condition_string' in dataJson\
        and 'template_webhook' in dataJson and 'email_center' in dataJson and 'biz_info' in dataJson and 'digit_sign' in dataJson and 'formula_temp' in dataJson and 'page_sign_options' in dataJson and 'options_page' in dataJson and 'use_status' in dataJson and 'time_expire' in dataJson and 'importance' in dataJson and 'last_digitsign' in dataJson \
        and 'status_ref' in dataJson and len(dataJson) == 24:
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            res_step_update = update_1().update_step_table_template_sql(dataJson['step_Code'], dataJson['step_Data'], dataJson['step_Max'], dataJson['username'], dataJson['email'], dataJson['step_Name'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'],dataJson['documentDetails'],dataJson['urgent_type'],dataJson['condition_string'],webhook=dataJson['template_webhook'],email_center=dataJson['email_center'],template_biz=dataJson['biz_info'],formula_temp=dataJson['formula_temp'],digit_sign=dataJson['digit_sign'],page_sign_options=dataJson['page_sign_options'],options_page=dataJson['options_page'],use_status=dataJson['use_status'],time_expire=dataJson['time_expire'],importance=dataJson['importance'],last_digit_sign=dataJson['last_digitsign'],status_ref=dataJson['status_ref'])
            if res_step_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':res_step_update['messageText'],'data':None}}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':            
        username = None
        taxid = None
        if (request.args.get('username')) != None and (request.args.get('taxid')) == None and (request.args.get('template')) == None and (request.args.get('status')) == None and (request.args.get('offset')) != None and (request.args.get('limit')) != None:
            # limit offset finish username
            username = str(request.args.get('username')).replace(' ','')
            select_get = select_1().select_get_template_tax_new_v13(username,taxid,str(request.args.get('offset')).replace(' ',''),str(request.args.get('limit')).replace(' ',''))
        elif (request.args.get('username')) == None and (request.args.get('taxid')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None and (request.args.get('offset')) != None and (request.args.get('limit')) != None :
            # limit offset finish taxid
            taxid = str(request.args.get('taxid')).replace(' ','')
            select_get = select_1().select_get_template_tax_new_v13(username,taxid,str(request.args.get('offset')).replace(' ',''),str(request.args.get('limit')).replace(' ',''))
        elif (request.args.get('username')) != None and (request.args.get('status')) != None and (request.args.get('taxid')) == None and (request.args.get('offset')) != None and (request.args.get('limit')) != None:
            # limit offset finish Reject username
            select_get = select_1().select_get_template_Reject_v12(str(request.args.get('username')).replace(' ',''),str(request.args.get('offset')).replace(' ',''),str(request.args.get('limit')).replace(' ',''))
        elif (request.args.get('username')) != None and (request.args.get('template')) != None and (request.args.get('string') == None):
            # Response add key finish
            select_get = select_1().select_get_templateandusername_new_biz_v3(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
        elif (request.args.get('string')) != None and (request.args.get('username')) != None and (request.args.get('template')) != None:
            '''get template string'''
            if str(request.args.get('string')).replace(' ','') == 'true':
                select_get = select().select_get_string_templateAndusername_v2(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
            else:
                return jsonify({'result':'ER','messageText':'string to bool (true)','status_Code':200}),200
        else:
            abort(404)

        if select_get['result'] == 'OK':
            return jsonify(select_get),200
        else:
            return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200            

@status_methods.route('/api/template/v2', methods=['POST','PUT','GET'])
@token_required
def template_v2():
    if request.method == 'POST':
        dataJson = request.json
        if 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Name' in dataJson and 'step_Upload' in dataJson and len(dataJson) == 7:
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            try:
                eval(dataJson['step_Upload'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_Upload ให้เป็น Json ได้'}),200
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            res_insert_template = insert().insert_paper_template_v2(dataJson['step_Code'],dataJson['step_Data'],dataJson['step_Max'],dataJson['username'],dataJson['email'],st,dataJson['step_Name'],dataJson['step_Upload'])
            if res_insert_template['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'Insert OK!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_template['messageText'],'status_Code':200}),200
        elif 'username' in dataJson and 'template_code' in dataJson and len(dataJson) == 2:
            res_delete = delete().delete_template(dataJson['username'],dataJson['template_code'])
            if res_delete['result'] == 'OK':
                return jsonify(res_delete),200
            else:
                return jsonify({'result':'ER','messageText':res_delete['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
        dataJson = request.json
        if 'step_Name' in dataJson and 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and len(dataJson) == 6:
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            res_step_update = update().update_step_table(
                dataJson['step_Code'], dataJson['step_Data'], dataJson['step_Max'], dataJson['username'], dataJson['email'], dataJson['step_Name'])
            if res_step_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'Update OK!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'Can,t to Update!','status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('username')) != None and (request.args.get('template')) == None:
            select_get = select().select_get_template(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('template')) != None and not (request.args.get('string')):
            select_get = select().select_get_templateandusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('string')) != None and (request.args.get('username')) != None and (request.args.get('template')) != None:
            '''get template string'''
            if str(request.args.get('string')).replace(' ','') == 'true':
                pass
            else:
                return jsonify({'result':'ER','messageText':'string to bool (true or false)','status_Code':200}),200
            if str(request.args.get('string')).replace(' ','') == 'true':
                select_get = select().select_get_string_templateAndusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
            else:
                select_get = select().select_get_templateandusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/template/v3', methods=['POST','PUT','GET'])
@token_required
def template_v3():
    if request.method == 'POST':
        dataJson = request.json
        if 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Name' in dataJson and 'step_Upload' in dataJson and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and len(dataJson) == 10:
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            try:
                eval(dataJson['step_Upload'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_Upload ให้เป็น Json ได้'}),200
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            res_insert_template = insert().insert_paper_template_v3(dataJson['step_Code'],dataJson['step_Data'],dataJson['step_Max'],dataJson['username'],dataJson['email'],st,dataJson['step_Name'],dataJson['step_Upload'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'])
            if res_insert_template['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'Insert OK!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_template['messageText'],'status_Code':200}),200
        elif 'username' in dataJson and 'template_code' in dataJson and len(dataJson) == 2:
            res_delete = update().update_template_v3(dataJson['username'],dataJson['template_code'])
            if res_delete['result'] == 'OK':
                return jsonify(res_delete),200
            else:
                return jsonify({'result':'ER','messageText':res_delete['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
        dataJson = request.json
        if 'step_Name' in dataJson and 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and len(dataJson) == 9:
            print()
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            res_step_update = update().update_step_table_v3(dataJson['step_Code'], dataJson['step_Data'], dataJson['step_Max'], dataJson['username'], dataJson['email'], dataJson['step_Name'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'])
            if res_step_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'Update OK!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'Can,t to Update!','status_Code':200,'messageER':res_step_update['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('username')) != None and (request.args.get('template')) == None:
            select_get = select().select_get_template(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('template')) != None and not (request.args.get('string')):
            select_get = select().select_get_templateandusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('string')) != None and (request.args.get('username')) != None and (request.args.get('template')) != None:
            '''get template string'''
            if str(request.args.get('string')).replace(' ','') == 'true':
                pass
            else:
                return jsonify({'result':'ER','messageText':'string to bool (true or false)','status_Code':200}),200
            if str(request.args.get('string')).replace(' ','') == 'true':
                select_get = select().select_get_string_templateAndusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
            else:
                select_get = select().select_get_templateandusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/template/v4', methods=['POST','PUT','GET'])
@token_required
def template_v4():
    if request.method == 'POST':
        dataJson = request.json
        if 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Name' in dataJson and 'step_Upload' in dataJson and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and len(dataJson) == 10:
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            try:
                eval(dataJson['step_Upload'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_Upload ให้เป็น Json ได้'}),200
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            res_insert_template = insert().insert_paper_template_v4(dataJson['step_Code'],dataJson['step_Data'],dataJson['step_Max'],dataJson['username'],dataJson['email'],st,dataJson['step_Name'],dataJson['step_Upload'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'])
            if res_insert_template['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'Insert OK!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_template['messageText'],'status_Code':200}),200
        elif 'username' in dataJson and 'template_code' in dataJson and len(dataJson) == 2:
            res_delete = update().update_template_v3(dataJson['username'],dataJson['template_code'])
            if res_delete['result'] == 'OK':
                return jsonify(res_delete),200
            else:
                return jsonify({'result':'ER','messageText':res_delete['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
        dataJson = request.json
        if 'step_Name' in dataJson and 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and len(dataJson) == 9:
            print()
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            res_step_update = update().update_step_table_v3(dataJson['step_Code'], dataJson['step_Data'], dataJson['step_Max'], dataJson['username'], dataJson['email'], dataJson['step_Name'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'])
            if res_step_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'Update OK!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'Can,t to Update!','status_Code':200,'messageER':res_step_update['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('username')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None:
            select_get = select().select_get_template(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('status')) != None:
            select_get = select().select_get_template_Reject(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('template')) != None and not (request.args.get('string')):
            select_get = select().select_get_templateandusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('string')) != None and (request.args.get('username')) != None and (request.args.get('template')) != None:
            '''get template string'''
            if str(request.args.get('string')).replace(' ','') == 'true':
                pass
            else:
                return jsonify({'result':'ER','messageText':'string to bool (true or false)','status_Code':200}),200
            if str(request.args.get('string')).replace(' ','') == 'true':
                select_get = select().select_get_string_templateAndusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
            else:
                select_get = select().select_get_templateandusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/template/v5', methods=['POST','PUT','GET'])
@token_required
def template_v5():
    if request.method == 'POST':
        dataJson = request.json
        if 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Name' in dataJson and 'step_Upload' in dataJson and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and 'documentDetails' in dataJson and 'urgent_type' in dataJson and 'biz_info' in dataJson and len(dataJson) == 13:
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            try:
                eval(dataJson['step_Upload'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_Upload ให้เป็น Json ได้'}),200
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            res_insert_template = insert().insert_paper_template_v4(dataJson['step_Code'],dataJson['step_Data'],dataJson['step_Max'],dataJson['username'],dataJson['email'],st,dataJson['step_Name'],dataJson['step_Upload'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'],None,dataJson['documentDetails'],dataJson['urgent_type'],dataJson['biz_info'])
            if res_insert_template['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'insert success!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_template['messageText'],'status_Code':200}),200
        elif 'username' in dataJson and 'template_code' in dataJson and len(dataJson) == 2:
            res_delete = update().update_template_v3(dataJson['username'],dataJson['template_code'])
            if res_delete['result'] == 'OK':
                return jsonify(res_delete),200
            else:
                return jsonify({'result':'ER','messageText':res_delete['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
        dataJson = request.json
        if 'step_Name' in dataJson and 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and 'documentDetails' in dataJson and 'urgent_type' in dataJson and len(dataJson) == 11:
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            res_step_update = update().update_step_table_v3(dataJson['step_Code'], dataJson['step_Data'], dataJson['step_Max'], dataJson['username'], dataJson['email'], dataJson['step_Name'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'],dataJson['documentDetails'],dataJson['urgent_type'])
            if res_step_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'Update OK!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'Can,t to Update!','status_Code':200,'messageER':res_step_update['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('username')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None and (request.args.get('taxid')) == None:
            select_get = select().select_get_template(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('taxid')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None:
            select_get = select().select_get_template_tax_new(str(request.args.get('username')).replace(' ',''),str(request.args.get('taxid')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('status')) != None and (request.args.get('taxid')) == None:
            select_get = select().select_get_template_Reject(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('template')) != None and not (request.args.get('string')):
            select_get = select().select_get_templateandusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('string')) != None and (request.args.get('username')) != None and (request.args.get('template')) != None:
            '''get template string'''
            if str(request.args.get('string')).replace(' ','') == 'true':
                pass
            else:
                return jsonify({'result':'ER','messageText':'string to bool (true)','status_Code':200}),200
            if str(request.args.get('string')).replace(' ','') == 'true':
                select_get = select().select_get_string_templateAndusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
            else:
                select_get = select().select_get_templateandusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/template/v6', methods=['POST','PUT','GET'])
@token_required
def template_v6():
    if request.method == 'POST':
        dataJson = request.json
        if 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Name' in dataJson and 'step_Upload' in dataJson and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and 'documentDetails' in dataJson and 'urgent_type' in dataJson and 'biz_info' in dataJson and 'condition_string' in dataJson and len(dataJson) == 13:
            step_Code = str(uuid.uuid4())
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            try:
                eval(dataJson['step_Upload'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_Upload ให้เป็น Json ได้'}),200
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            res_insert_template = insert().insert_paper_template_v4(step_Code,dataJson['step_Data'],dataJson['step_Max'],dataJson['username'],dataJson['email'],st,dataJson['step_Name'],dataJson['step_Upload'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'],None,dataJson['documentDetails'],dataJson['urgent_type'],dataJson['biz_info'],condition_temp=dataJson['condition_string'])
            if res_insert_template['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'insert success!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_template['messageText'],'status_Code':200}),200
        elif 'username' in dataJson and 'template_code' in dataJson and len(dataJson) == 2:
            res_delete = update().update_template_v3(dataJson['username'],dataJson['template_code'])
            if res_delete['result'] == 'OK':
                return jsonify(res_delete),200
            else:
                return jsonify({'result':'ER','messageText':res_delete['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
        dataJson = request.json
        if 'step_Name' in dataJson and 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and 'documentDetails' in dataJson and 'urgent_type' in dataJson and 'condition_string' in dataJson and len(dataJson) == 12:
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            res_step_update = update().update_step_table_biz_v_new(dataJson['step_Code'], dataJson['step_Data'], dataJson['step_Max'], dataJson['username'], dataJson['email'], dataJson['step_Name'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'],dataJson['documentDetails'],dataJson['urgent_type'],dataJson['condition_string'])
            if res_step_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'Update OK!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'Can,t to Update!','status_Code':200,'messageER':res_step_update['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('username')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None and (request.args.get('taxid')) == None:
            select_get = select().select_get_template(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('taxid')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None:
            select_get = select().select_get_template_tax_new(str(request.args.get('taxid')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) == None and (request.args.get('taxid')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None:
            select_get = select().select_get_template_tax_new(str(request.args.get('taxid')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('status')) != None and (request.args.get('taxid')) == None:
            select_get = select().select_get_template_Reject(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('template')) != None and not (request.args.get('string')):
            select_get = select().select_get_templateandusername_new_biz(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('string')) != None and (request.args.get('username')) != None and (request.args.get('template')) != None:
            '''get template string'''
            if str(request.args.get('string')).replace(' ','') == 'true':
                pass
            else:
                return jsonify({'result':'ER','messageText':'string to bool (true)','status_Code':200}),200
            if str(request.args.get('string')).replace(' ','') == 'true':
                select_get = select().select_get_string_templateAndusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
            else:
                select_get = select().select_get_templateandusername_new_biz(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/v7/template', methods=['POST','PUT','GET'])
@token_required
def template_v7():
    if request.method == 'POST':
        dataJson = request.json
        if 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Name' in dataJson and 'step_Upload' in dataJson and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and 'documentDetails' in dataJson and 'urgent_type' in dataJson and 'biz_info' in dataJson and 'condition_string' in dataJson and 'template_webhook' in dataJson and 'email_center' in dataJson and len(dataJson) == 15:
            step_Code = str(uuid.uuid4())
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            try:
                eval(dataJson['step_Upload'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_Upload ให้เป็น Json ได้'}),200
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            res_insert_template = insert().insert_paper_template_v5(step_Code,dataJson['step_Data'],dataJson['step_Max'],dataJson['username'],dataJson['email'],st,dataJson['step_Name'],dataJson['step_Upload'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'],None,dataJson['documentDetails'],dataJson['urgent_type'],dataJson['biz_info'],condition_temp=dataJson['condition_string'],webhook=dataJson['template_webhook'],email_center=dataJson['email_center'])
            if res_insert_template['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'insert success!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_template['messageText'],'status_Code':200}),200
        elif 'username' in dataJson and 'template_code' in dataJson and len(dataJson) == 2:
            res_delete = update().update_template_v3(dataJson['username'],dataJson['template_code'])
            if res_delete['result'] == 'OK':
                return jsonify(res_delete),200
            else:
                return jsonify({'result':'ER','messageText':res_delete['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
        dataJson = request.json
        if 'step_Name' in dataJson and 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and 'documentDetails' in dataJson and 'urgent_type' in dataJson and 'condition_string' in dataJson and 'template_webhook' in dataJson and 'email_center' in dataJson and 'biz_info' in dataJson and len(dataJson) == 15:
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            res_step_update = update().update_step_table_biz_v_2(dataJson['step_Code'], dataJson['step_Data'], dataJson['step_Max'], dataJson['username'], dataJson['email'], dataJson['step_Name'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'],dataJson['documentDetails'],dataJson['urgent_type'],dataJson['condition_string'],webhook=dataJson['template_webhook'],email_center=dataJson['email_center'],template_biz=dataJson['biz_info'])
            if res_step_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'Update OK!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'Can,t to Update!','status_Code':200,'messageER':res_step_update['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('username')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None and (request.args.get('taxid')) == None:
            select_get = select().select_get_template(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('taxid')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None:
            select_get = select().select_get_template_tax_new(str(request.args.get('taxid')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) == None and (request.args.get('taxid')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None:
            select_get = select().select_get_template_tax_new(str(request.args.get('taxid')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('status')) != None and (request.args.get('taxid')) == None:
            select_get = select().select_get_template_Reject(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('template')) != None and not (request.args.get('string')):
            select_get = select().select_get_templateandusername_new_biz(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('string')) != None and (request.args.get('username')) != None and (request.args.get('template')) != None:
            '''get template string'''
            if str(request.args.get('string')).replace(' ','') == 'true':
                pass
            else:
                return jsonify({'result':'ER','messageText':'string to bool (true)','status_Code':200}),200
            if str(request.args.get('string')).replace(' ','') == 'true':
                select_get = select().select_get_string_templateAndusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
            else:
                select_get = select().select_get_templateandusername_new_biz(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/v8/template', methods=['POST','PUT','GET'])
# @token_required
def template_v8():
    if request.method == 'POST':
        dataJson = request.json
        if 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Name' in dataJson and 'step_Upload' in dataJson\
        and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and 'documentDetails' in dataJson and 'urgent_type' in dataJson\
        and 'biz_info' in dataJson and 'condition_string' in dataJson and 'template_webhook' in dataJson\
        and 'email_center' in dataJson and 'digit_sign' in dataJson and 'formula_temp' in dataJson  and len(dataJson) == 17:
            step_Code = str(uuid.uuid4())
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            try:
                eval(dataJson['step_Upload'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_Upload ให้เป็น Json ได้'}),200
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            res_insert_template = insert().insert_paper_template_v8(step_Code,dataJson['step_Data'],dataJson['step_Max'],dataJson['username'],dataJson['email'],st,dataJson['step_Name'],dataJson['step_Upload'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'],None,dataJson['documentDetails'],dataJson['urgent_type'],dataJson['biz_info'],condition_temp=dataJson['condition_string'],webhook=dataJson['template_webhook'],email_center=dataJson['email_center'],formula_temp=dataJson['formula_temp'],digit_sign=dataJson['digit_sign'])
            if res_insert_template['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'insert success!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_template['messageText'],'status_Code':200}),200
        elif 'username' in dataJson and 'template_code' in dataJson and len(dataJson) == 2:
            res_delete = update().update_template_v3(dataJson['username'],dataJson['template_code'])
            if res_delete['result'] == 'OK':
                return jsonify(res_delete),200
            else:
                return jsonify({'result':'ER','messageText':res_delete['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
        dataJson = request.json
        if 'step_Name' in dataJson and 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and 'documentDetails' in dataJson and 'urgent_type' in dataJson and 'condition_string' in dataJson\
        and 'template_webhook' in dataJson and 'email_center' in dataJson and 'biz_info' in dataJson and 'digit_sign' in dataJson and 'formula_temp' in dataJson and len(dataJson) == 17:
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            res_step_update = update().update_step_table_template_v8(dataJson['step_Code'], dataJson['step_Data'], dataJson['step_Max'], dataJson['username'], dataJson['email'], dataJson['step_Name'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'],dataJson['documentDetails'],dataJson['urgent_type'],dataJson['condition_string'],webhook=dataJson['template_webhook'],email_center=dataJson['email_center'],template_biz=dataJson['biz_info'],formula_temp=dataJson['formula_temp'],digit_sign=dataJson['digit_sign'])
            if res_step_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'Update OK!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'Can,t to Update!','status_Code':200,'messageER':res_step_update['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('username')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None and (request.args.get('taxid')) == None:
            select_get = select().select_get_template(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('taxid')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None:
            select_get = select().select_get_template_tax_new(str(request.args.get('taxid')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) == None and (request.args.get('taxid')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None:
            select_get = select().select_get_template_tax_new(str(request.args.get('taxid')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('status')) != None and (request.args.get('taxid')) == None:
            select_get = select().select_get_template_Reject(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('template')) != None and not (request.args.get('string')):
            select_get = select().select_get_templateandusername_new_biz(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('string')) != None and (request.args.get('username')) != None and (request.args.get('template')) != None:
            '''get template string'''
            if str(request.args.get('string')).replace(' ','') == 'true':
                pass
            else:
                return jsonify({'result':'ER','messageText':'string to bool (true)','status_Code':200}),200
            if str(request.args.get('string')).replace(' ','') == 'true':
                select_get = select().select_get_string_templateAndusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
            else:
                select_get = select().select_get_templateandusername_new_biz(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/v9/template', methods=['POST','PUT','GET'])
@token_required
def template_v9():
    if request.method == 'POST':
        dataJson = request.json
        if 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Name' in dataJson and 'step_Upload' in dataJson\
        and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and 'documentDetails' in dataJson and 'urgent_type' in dataJson\
        and 'biz_info' in dataJson and 'condition_string' in dataJson and 'template_webhook' in dataJson\
        and 'email_center' in dataJson and 'digit_sign' in dataJson and 'formula_temp' in dataJson and 'page_sign_options' in dataJson and len(dataJson) == 18:
            step_Code = str(uuid.uuid4())
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            try:
                eval(dataJson['step_Upload'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_Upload ให้เป็น Json ได้'}),200
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            res_insert_template = insert().insert_paper_template_v9(step_Code,dataJson['step_Data'],dataJson['step_Max'],dataJson['username'],dataJson['email'],st,dataJson['step_Name'],dataJson['step_Upload'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'],None,dataJson['documentDetails'],dataJson['urgent_type'],dataJson['biz_info'],condition_temp=dataJson['condition_string'],webhook=dataJson['template_webhook'],email_center=dataJson['email_center'],formula_temp=dataJson['formula_temp'],digit_sign=dataJson['digit_sign'],page_sign_options=dataJson['page_sign_options'])
            if res_insert_template['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'insert success!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_template['messageText'],'status_Code':200}),200
        elif 'username' in dataJson and 'template_code' in dataJson and len(dataJson) == 2:
            res_delete = update().update_template_v3(dataJson['username'],dataJson['template_code'])
            if res_delete['result'] == 'OK':
                return jsonify(res_delete),200
            else:
                return jsonify({'result':'ER','messageText':res_delete['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
        dataJson = request.json
        if 'step_Name' in dataJson and 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and 'documentDetails' in dataJson and 'urgent_type' in dataJson and 'condition_string' in dataJson\
        and 'template_webhook' in dataJson and 'email_center' in dataJson and 'biz_info' in dataJson and 'digit_sign' in dataJson and 'formula_temp' in dataJson and 'page_sign_options' in dataJson and len(dataJson) == 18:
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            res_step_update = update().update_step_table_template_v9(dataJson['step_Code'], dataJson['step_Data'], dataJson['step_Max'], dataJson['username'], dataJson['email'], dataJson['step_Name'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'],dataJson['documentDetails'],dataJson['urgent_type'],dataJson['condition_string'],webhook=dataJson['template_webhook'],email_center=dataJson['email_center'],template_biz=dataJson['biz_info'],formula_temp=dataJson['formula_temp'],digit_sign=dataJson['digit_sign'],page_sign_options=dataJson['page_sign_options'])
            if res_step_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'Update OK!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'Can,t to Update!','status_Code':200,'messageER':res_step_update['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('username')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None and (request.args.get('taxid')) == None:
            select_get = select().select_get_template(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('taxid')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None:
            select_get = select().select_get_template_tax_new(str(request.args.get('taxid')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) == None and (request.args.get('taxid')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None:
            select_get = select().select_get_template_tax_new(str(request.args.get('taxid')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('status')) != None and (request.args.get('taxid')) == None:
            select_get = select().select_get_template_Reject(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('template')) != None and not (request.args.get('string')):
            select_get = select().select_get_templateandusername_new_biz(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('string')) != None and (request.args.get('username')) != None and (request.args.get('template')) != None:
            '''get template string'''
            if str(request.args.get('string')).replace(' ','') == 'true':
                pass
            else:
                return jsonify({'result':'ER','messageText':'string to bool (true)','status_Code':200}),200
            if str(request.args.get('string')).replace(' ','') == 'true':
                select_get = select().select_get_string_templateAndusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
            else:
                select_get = select().select_get_templateandusername_new_biz(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/v10/template', methods=['POST','PUT','GET'])
@token_required
def template_v10():
    if request.method == 'POST':
        dataJson = request.json
        if 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Name' in dataJson and 'step_Upload' in dataJson\
        and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and 'documentDetails' in dataJson and 'urgent_type' in dataJson\
        and 'biz_info' in dataJson and 'condition_string' in dataJson and 'template_webhook' in dataJson\
        and 'email_center' in dataJson and 'digit_sign' in dataJson and 'formula_temp' in dataJson and 'page_sign_options' in dataJson and 'options_page' in dataJson and len(dataJson) == 19:
            step_Code = str(uuid.uuid4())
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            try:
                eval(dataJson['step_Upload'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_Upload ให้เป็น Json ได้'}),200
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            res_insert_template = insert().insert_paper_template_v9(step_Code,dataJson['step_Data'],dataJson['step_Max'],dataJson['username'],dataJson['email'],st,dataJson['step_Name'],dataJson['step_Upload'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'],None,dataJson['documentDetails'],dataJson['urgent_type'],dataJson['biz_info'],condition_temp=dataJson['condition_string'],webhook=dataJson['template_webhook'],email_center=dataJson['email_center'],formula_temp=dataJson['formula_temp'],digit_sign=dataJson['digit_sign'],page_sign_options=dataJson['page_sign_options'],options_page=dataJson['options_page'])
            if res_insert_template['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'insert success!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':res_insert_template['messageText'],'status_Code':200}),200
        elif 'username' in dataJson and 'template_code' in dataJson and len(dataJson) == 2:
            res_delete = update().update_template_v3(dataJson['username'],dataJson['template_code'])
            if res_delete['result'] == 'OK':
                return jsonify(res_delete),200
            else:
                return jsonify({'result':'ER','messageText':res_delete['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
        dataJson = request.json
        if 'step_Name' in dataJson and 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and 'documentDetails' in dataJson and 'urgent_type' in dataJson and 'condition_string' in dataJson\
        and 'template_webhook' in dataJson and 'email_center' in dataJson and 'biz_info' in dataJson and 'digit_sign' in dataJson and 'formula_temp' in dataJson and 'page_sign_options' in dataJson and 'options_page' in dataJson and len(dataJson) == 19:
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            res_step_update = update().update_step_table_template_v9(dataJson['step_Code'], dataJson['step_Data'], dataJson['step_Max'], dataJson['username'], dataJson['email'], dataJson['step_Name'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'],dataJson['documentDetails'],dataJson['urgent_type'],dataJson['condition_string'],webhook=dataJson['template_webhook'],email_center=dataJson['email_center'],template_biz=dataJson['biz_info'],formula_temp=dataJson['formula_temp'],digit_sign=dataJson['digit_sign'],page_sign_options=dataJson['page_sign_options'],options_page=dataJson['options_page'])
            if res_step_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'Update OK!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'Can,t to Update!','status_Code':200,'messageER':res_step_update['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('username')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None and (request.args.get('taxid')) == None:
            select_get = select().select_get_template(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('taxid')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None:
            select_get = select().select_get_template_tax_new(str(request.args.get('taxid')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) == None and (request.args.get('taxid')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None:
            select_get = select().select_get_template_tax_new_v10(str(request.args.get('taxid')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('status')) != None and (request.args.get('taxid')) == None:
            select_get = select().select_get_template_Reject(str(request.args.get('username')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('template')) != None and not (request.args.get('string')):
            select_get = select().select_get_templateandusername_new_biz(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('string')) != None and (request.args.get('username')) != None and (request.args.get('template')) != None:
            '''get template string'''
            if str(request.args.get('string')).replace(' ','') == 'true':
                pass
            else:
                return jsonify({'result':'ER','messageText':'string to bool (true)','status_Code':200}),200
            if str(request.args.get('string')).replace(' ','') == 'true':
                select_get = select().select_get_string_templateAndusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
            else:
                select_get = select().select_get_templateandusername_new_biz(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/v1/template/template_document', methods=['POST','PUT','GET'])
@token_required_v3
def template_document_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Name' in dataJson and 'step_Upload' in dataJson\
        and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and 'documentDetails' in dataJson and 'urgent_type' in dataJson\
        and 'biz_info' in dataJson and 'condition_string' in dataJson and 'template_webhook' in dataJson\
        and 'email_center' in dataJson and 'digit_sign' in dataJson and 'formula_temp' in dataJson and 'page_sign_options' in dataJson and 'options_page' in dataJson and 'use_status' in dataJson\
        and 'time_expire' in dataJson and 'importance' in dataJson and 'last_digitsign' in dataJson and len(dataJson) == 23:
            step_Code = str(uuid.uuid4())
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            try:
                eval(dataJson['step_Upload'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_Upload ให้เป็น Json ได้'}),200
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            # if dataJson['time_expire'] != None:

            res_insert_template = insert().insert_paper_template_v10(step_Code,dataJson['step_Data'],dataJson['step_Max'],dataJson['username'],dataJson['email'],st,dataJson['step_Name'],dataJson['step_Upload'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'],None,dataJson['documentDetails'],dataJson['urgent_type'],dataJson['biz_info'],condition_temp=dataJson['condition_string'],webhook=dataJson['template_webhook'],email_center=dataJson['email_center'],formula_temp=dataJson['formula_temp'],digit_sign=dataJson['digit_sign'],page_sign_options=dataJson['page_sign_options'],options_page=dataJson['options_page'],use_status=dataJson['use_status'],time_expire=dataJson['time_expire'],importance=dataJson['importance'],last_digitsign=dataJson['last_digitsign'])
            # print(res_insert_template)
            if res_insert_template['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':res_insert_template['messageText'],'data':None},'status_Code':200}),200
        elif 'username' in dataJson and 'template_code' in dataJson and 'use_status' in dataJson and len(dataJson) == 3:
            res_delete = update().update_template_use_status_v3(dataJson['username'],dataJson['template_code'],dataJson['use_status'])
            if res_delete['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':res_delete['messageText'],'data':None},'status_Code':200}),200
        elif 'username' in dataJson and 'template_code' in dataJson and len(dataJson) == 2:
            res_delete = update().update_template_v3(dataJson['username'],dataJson['template_code'])
            if res_delete['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':res_delete['messageText'],'data':None},'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
        dataJson = request.json
        if 'step_Name' in dataJson and 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and 'documentDetails' in dataJson and 'urgent_type' in dataJson and 'condition_string' in dataJson\
        and 'template_webhook' in dataJson and 'email_center' in dataJson and 'biz_info' in dataJson and 'digit_sign' in dataJson and 'formula_temp' in dataJson and 'page_sign_options' in dataJson and 'options_page' in dataJson and 'use_status' in dataJson and 'time_expire' in dataJson and 'importance' in dataJson and 'last_digitsign' in dataJson and len(dataJson) == 23:
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            res_step_update = update_3().update_step_table_template_v10(dataJson['step_Code'], dataJson['step_Data'], dataJson['step_Max'], dataJson['username'], dataJson['email'], dataJson['step_Name'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'],dataJson['documentDetails'],dataJson['urgent_type'],dataJson['condition_string'],webhook=dataJson['template_webhook'],email_center=dataJson['email_center'],template_biz=dataJson['biz_info'],formula_temp=dataJson['formula_temp'],digit_sign=dataJson['digit_sign'],page_sign_options=dataJson['page_sign_options'],options_page=dataJson['options_page'],use_status=dataJson['use_status'],time_expire=dataJson['time_expire'],importance=dataJson['importance'],last_digit_sign=dataJson['last_digitsign'])
            if res_step_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':res_step_update['messageText'],'data':None}}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        username = None
        taxid = None

        if (request.args.get('username')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None and (request.args.get('taxid')) == None and (request.args.get('off')) != None and (request.args.get('lim')) != None:
            # limit offset finish username
            username = str(request.args.get('username')).replace(' ','')
            select_get = select_1().select_get_template_tax_new_v12(username,taxid,str(request.args.get('off')).replace(' ',''),str(request.args.get('lim')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) == None and (request.args.get('taxid')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None and (request.args.get('off')) != None and (request.args.get('lim')) != None :
            # limit offset finish taxid
            taxid = str(request.args.get('taxid')).replace(' ','')
            select_get = select_1().select_get_template_tax_new_v12(username,taxid,str(request.args.get('off')).replace(' ',''),str(request.args.get('lim')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) == None and (request.args.get('taxid')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None and (request.args.get('off')) != None and (request.args.get('lim')) != None :
            # limit offset finish taxid
            taxid = str(request.args.get('taxid')).replace(' ','')
            select_get = select_1().select_get_template_tax_new_v12(username,taxid,str(request.args.get('off')).replace(' ',''),str(request.args.get('lim')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('status')) != None and (request.args.get('taxid')) == None and (request.args.get('off')) != None and (request.args.get('lim')) != None:
            # limit offset finish Reject username
            select_get = select_1().select_get_template_Reject_v11(str(request.args.get('username')).replace(' ',''),str(request.args.get('off')).replace(' ',''),str(request.args.get('lim')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) != None and (request.args.get('template')) != None and not (request.args.get('string')):
            # Response add key finish
            select_get = select_1().select_get_templateandusername_new_biz_v2(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('string')) != None and (request.args.get('username')) != None and (request.args.get('template')) != None:
            '''get template string'''
            if str(request.args.get('string')).replace(' ','') == 'true':
                pass
            else:
                return jsonify({'result':'ER','messageText':'string to bool (true)','status_Code':200}),200
            if str(request.args.get('string')).replace(' ','') == 'true':
                select_get = select().select_get_string_templateAndusername(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
            else:
                select_get = select().select_get_templateandusername_new_biz(str(request.args.get('username')).replace(' ',''),str(request.args.get('template')).replace(' ',''))
                if select_get['result'] == 'OK':
                    return jsonify(select_get),200
                else:
                    return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        else:
            abort(404)


@status_methods.route('/api/v1/template/search_template', methods=['POST'])
@token_required_v3
def search_template():
    if request.method == 'POST':
        dataJson = request.json
        username = None
        taxid = None
        if 'taxid' in dataJson and 'offset' in dataJson and 'limit' in dataJson and 'keyword' in dataJson and len(dataJson) == 4:
            taxid = dataJson['taxid']
            offset = dataJson['offset']
            limit = dataJson['limit']
            input_ = dataJson['keyword']
            select_get = select_1().select_template_paper(taxid,username,offset,limit,input_)
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'data not found'}}),200
        elif 'username' in dataJson and 'offset' in dataJson and 'limit' in dataJson and 'keyword' in dataJson and len(dataJson) == 4:
            username = dataJson['username']
            offset = dataJson['offset']
            limit = dataJson['limit']
            input_ = dataJson['keyword']
            select_get = select_1().select_template_paper(taxid,username,offset,limit,input_)
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'data not found'}}),200
        else:
            abort(404)


@status_methods.route('/api/v1/template/search_template/template_sum', methods=['POST'])
@token_required_v3
def check_template():
    if request.method == 'POST':
        dataJson = request.json
        username = None
        taxid = None
        if 'taxid' in dataJson and 'keyword' in dataJson and len(dataJson) == 2 :
            taxid = dataJson['taxid']
            input_ = dataJson['keyword']
            select_get = select_1().select_sum_template(taxid,username,input_)
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
        elif 'username' in dataJson and 'keyword' in dataJson and len(dataJson) == 2 :
            username = dataJson['username']
            input_ = dataJson['keyword']
            select_get = select_1().select_sum_template(taxid,username,input_)
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'data not found'}}),200
        else:
            abort(404)


@status_methods.route('/api/v1/template/template_sum', methods=['GET'])
@token_required_v3
def sum_template():
    if request.method == 'GET':
        username = None
        taxid = None
        if (request.args.get('username')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None and (request.args.get('taxid')) == None :
            username = str(request.args.get('username')).replace(' ','')
            select_get = select_1().select_check_templateTaxV12(username,taxid)
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        elif (request.args.get('username')) == None and (request.args.get('taxid')) != None and (request.args.get('template')) == None and (request.args.get('status')) == None :
            # limit offset finish taxid
            taxid = str(request.args.get('taxid')).replace(' ','')
            select_get = select_1().select_check_templateTaxV12(username,taxid)
            if select_get['result'] == 'OK':
                return jsonify(select_get),200
            else:
                return jsonify({'result':'ER','messageText':select_get['messageText'],'status_Code':200}),200
        else:
            abort(404)
