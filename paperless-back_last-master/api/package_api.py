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
from db.db_method_4 import *
from db.db_method_5 import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from api.file import *
from api.memory import *
from api.ocr_api import *
from method.sftp_fucn import *
from method.callwebHook import *
from method.pdfSign import *
from method.cal_file import *
from api.schedule_log import *
from method.cal_BI import *
from method.cal_taxId import *
from method.cal_tdcpm import *
from method.cal_package import *


if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less


# schedule api
@status_methods.route('/api/v1/package_service/around_package', methods=['POST'])
@token_required_v3
def package_service_around_package():
    datajson = request.json
    datetimeNow = datajson['datetimeNow']
    result_package = select_5().check_around_package_v1(datetimeNow)
    if result_package['result'] == 'OK':
        return jsonify({'result':'OK','messageText':result_package['messageText'],'status_Code':200}),200
    else :
        return jsonify({'result':'ER','messageText':result_package['messageText'],'status_Code':200}),200

@status_methods.route('/api/v1/package_service/manage_package_v1', methods=['GET','POST','PUT'])
@token_required_v3
def package_service_manage_package_v1():
    if request.method == 'GET':
        code_service = request.args.get('code_service')
        result_select = select_5().select_package_v1(code_service)
        if result_select['result'] == 'OK':
            return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
        else :
            return jsonify({'result':'ER','messageText':result_select['messageText'],'status_Code':200}),200
    elif request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            print ('username',username)
            print ('email',email)
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
            print ('list_id_card_num',list_id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        datajson = request.json
        if 'code_service' in datajson and 'name_service' in datajson and 'type_service' in datajson and 'transactions' in datajson and 'eform' in datajson and 'support_user' in datajson and 'support_ca' in datajson\
            and 'storage' in datajson and 'one_box' in datajson and 'back_up' in datajson and 'offer' in datajson and 'implement' in datajson and 'cost_month' in datajson and len(datajson) == 13:
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                if level_admin == None :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found'}}),200
                elif int(level_admin) == 0 :
                    result_insert = insert_5().insert_package_v1(datajson['code_service'],datajson['name_service'],datajson['type_service'],datajson['transactions'],datajson['eform'],datajson['support_user'],datajson['support_ca']\
                        ,datajson['storage'],datajson['one_box'],datajson['back_up'],datajson['offer'],datajson['implement'],datajson['cost_month'])
                    if result_insert['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_insert['messageText'],'status_Code':200}),200
                    else :
                        return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200
                elif int(level_admin) == 1 :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'admin level ineligible'}}),200            
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            print ('username',username)
            print ('email',email)
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
            print ('list_id_card_num',list_id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        datajson = request.json
        if 'code_service' in datajson and 'name_service' in datajson and 'type_service' in datajson and 'transactions' in datajson and 'eform' in datajson and 'support_user' in datajson and 'support_ca' in datajson\
            and 'storage' in datajson and 'one_box' in datajson and 'back_up' in datajson and 'offer' in datajson and 'implement' in datajson and 'cost_month' in datajson and len(datajson) == 13:
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                if level_admin == None :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found'}}),200
                elif int(level_admin) == 0 :
                    result_update = update_5().update_package_v1(datajson['code_service'],datajson['name_service'],datajson['type_service'],datajson['transactions'],datajson['eform'],datajson['support_user'],datajson['support_ca']\
                        ,datajson['storage'],datajson['one_box'],datajson['back_up'],datajson['offer'],datajson['implement'],datajson['cost_month'])
                    if result_update['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_update['messageText'],'status_Code':200}),200
                    else :
                        return jsonify({'result':'ER','messageText':result_update['messageText'],'status_Code':200}),200
                elif int(level_admin) == 1 :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'admin level ineligible'}}),200            
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
   
@status_methods.route('/api/v1/package_service/manage_package_v1_remove', methods=['POST'])
@token_required_v3
def package_service_manage_package_v1_remove():
    if request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            print ('username',username)
            print ('email',email)
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
            print ('list_id_card_num',list_id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        datajson = request.json
        code_service = datajson['code_service']
        if code_service != None :
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                if level_admin == None :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found'}}),200
                elif int(level_admin) == 0 :                    
                    result_delete = delete_5().delete_package_v1(code_service)
                    if result_delete['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_delete['messageText'],'status_Code':200}),200
                    else :
                        return jsonify({'result':'ER','messageText':result_delete['messageText'],'status_Code':200}),200
                elif int(level_admin) == 1 :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'admin level ineligible'}}),200            
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/v1/package_service/get_sum_cost', methods=['GET'])
@token_required_v3
def package_service_get_sum_cost():
    if request.method == 'GET':
        tax_id = request.args.get('tax_id')
        if tax_id != None:
            result_select = select_5().select_sum_cost(tax_id)
            if result_select['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
            else :
                return jsonify({'result':'ER','messageText':result_select['messageText'],'status_Code':200}),200

@status_methods.route('/api/v1/package_service/insert_package_main_enhance', methods=['POST'])
@token_required_v3
def package_service_insert_package_main_enhance():
    if request.method == 'POST':
        datajson = request.json
        tax_id = datajson['tax_id']
        package_Enhance = datajson['package_Enhance']
        if 'package_main' in datajson and 'datetimeStart' in datajson and 'datetimeEnd' in datajson:
            datetimeStart = datajson['datetimeStart']
            datetimeEnd = datajson['datetimeEnd']
            package_main = datajson['package_main']
        else:
            datetimeStart = None
            datetimeEnd = None
            package_main = None      
        print(tax_id)
        result_insert = insert_5().insert_package_main_enhance(tax_id,datetimeStart,datetimeEnd,package_main,package_Enhance)
        if result_insert['result'] == 'OK':
            return jsonify({'result':'OK','messageText':result_insert['messageText'],'status_Code':200}),200
        else :
            return jsonify({'result':'ER','messageText':result_insert['messageText'],'status_Code':200}),200

@status_methods.route('/api/v1/package_service/get_persent_storage', methods=['GET'])
@token_required_v3
def package_service_get_persent_storage():
    if request.method == 'GET':
        tax_id = request.args.get('tax_id')
        result_select = select_5().check_storage_business(tax_id)
        if result_select['result'] == 'OK':
            return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
        else :
            return jsonify({'result':'ER','messageText':result_select['messageText'],'status_Code':200}),200

@status_methods.route('/api/v1/package_service/get_package_business', methods=['GET'])
@token_required_v3
def package_service_get_package_business():
    if request.method == 'GET':
        tax_id = request.args.get('tax_id')
        result_select = select_5().select_package_business(tax_id)
        if result_select['result'] == 'OK':
            return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200}),200
        else :
            return jsonify({'result':'ER','messageText':result_select['messageText'],'status_Code':200}),200
