#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from method.publicqrcode import *
from method.verify import *
from controller.mail_string import *
from controller.validate import *
from db.db_method import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from method.callserver import *


if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less

@status_methods.route('/api/v1/register/register_business',methods=['POST'])
def register_business_api_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)})
        try:
            dataForm = request.form
            if 'one_token' in dataForm and 'taxid' in dataForm and 'citizen_id' in dataForm and 'name_th' in dataForm and 'name_eng' in dataForm and 'dataJson' in dataForm and len(dataForm) == 6:
                tmp_one_token = dataForm['one_token']
                tmp_taxid = dataForm['taxid']
                tmp_citizen_id = dataForm['citizen_id']
                tmp_name_th = dataForm['name_th']
                tmp_name_eng = dataForm['name_eng']
                tmp_dataJson = dataForm['dataJson']

                approve_document  = request.files['approve_document']
                result_document   = request.files['result_document']
                porpor20_document = request.files['porpor20_document']                
                path = path_global_1 + '/storage/register/' + tmp_citizen_id + '-' + tmp_taxid
                # path = './storage/register/' + tmp_citizen_id + '-' + tmp_taxid
                if not os.path.exists(path):
                    os.makedirs(path)
                if approve_document and result_document and porpor20_document:
                    approve_document.save(os.path.join(path,approve_document.filename))
                    result_document.save(os.path.join(path,result_document.filename))
                    porpor20_document.save(os.path.join(path,porpor20_document.filename))
                    path_approve   = path+'/'+approve_document.filename
                    path_result    = path+'/'+result_document.filename
                    path_porpor20  = path+'/'+porpor20_document.filename
                dataJson_eval = eval(str(tmp_dataJson))
                if 'account_title_th' in dataJson_eval and 'first_name_th' in dataJson_eval and 'account_title_eng' in dataJson_eval and  'first_name_eng' in dataJson_eval and 'id_card_type' in dataJson_eval and 'id_card_num' in dataJson_eval and 'email' in dataJson_eval and 'mobile_no' in dataJson_eval and 'tel_no' in dataJson_eval and 'name_on_document_th' in dataJson_eval and 'name_on_document_eng' in dataJson_eval and 'owner_detail' in dataJson_eval and  'address' in dataJson_eval and 'branch_name' in dataJson_eval and 'branch_no' in dataJson_eval and len(dataJson_eval) == 15:
                    account_title_th = dataJson_eval['account_title_th']
                    first_name_th = dataJson_eval['first_name_th']
                    account_title_eng = dataJson_eval['account_title_eng']
                    first_name_eng = dataJson_eval['first_name_eng']
                    id_card_type = dataJson_eval['id_card_type']
                    id_card_num = dataJson_eval['id_card_num']
                    email = dataJson_eval['email']
                    mobile_no = dataJson_eval['mobile_no']
                    tel_no = dataJson_eval['tel_no']
                    # approve_document = dataJson_eval['approve_document']
                    # result_meeting = dataJson_eval['result_meeting']
                    name_on_document_th = dataJson_eval['name_on_document_th']
                    name_on_document_eng = dataJson_eval['name_on_document_eng']
                    owner_detail = dataJson_eval['owner_detail']
                    owner_detail_eval = eval(str(owner_detail))
                    address = dataJson_eval['address']
                    address_eval = eval(str(address))
                    branch_name = dataJson_eval['branch_name']
                    branch_no = dataJson_eval['branch_no']
                    json_owner_detail = eval(str(owner_detail_eval[0]))
                    json_address = eval(str(address_eval[0]))
                    result_list_Upload = []
                    if 'department' in json_owner_detail and 'position' in json_owner_detail and 'thai_email' in json_owner_detail and len(json_owner_detail) == 3:
                        department = json_owner_detail['department']
                        position = json_owner_detail['position']
                        thai_email = json_owner_detail['thai_email']
                        if 'house_code' in json_address and 'house_no' in json_address and 'room_no' in json_address and 'moo_ban' in json_address and 'moo_no'in json_address and 'building_name' in json_address and 'floor' in json_address and 'yaek' in json_address and 'street' in json_address and 'fax_number' in json_address and 'soi' in json_address and 'province' in json_address and 'tambon' in json_address and 'amphoe' in json_address and 'zipcode' in json_address and 'country' and len(json_address) == 16:
                            house_code = json_address['house_code']
                            house_no = json_address['house_no']
                            room_no = json_address['room_no']
                            moo_ban = json_address['moo_ban']
                            moo_no = json_address['moo_no']
                            building_name = json_address['building_name']
                            floor = json_address['floor']
                            yaek = json_address['yaek']
                            street = json_address['street']
                            fax_number = json_address['fax_number']
                            soi = json_address['soi']
                            province = json_address['province']
                            tambon = json_address['tambon']
                            amphoe = json_address['amphoe']
                            zipcode = json_address['zipcode']
                            country = json_address['country']
                            result_approveDocument_Upload = callOneid_Upload(one_url+'/api/upload_approve_api',path_approve,'approveDocument',token_header)
                            if result_approveDocument_Upload['result'] == 'OK':
                                tmp_message_appDoc = result_approveDocument_Upload['messageText'].json()
                                if tmp_message_appDoc['result'] == 'Success':
                                    tmp_data_path_appDoc = tmp_message_appDoc['data']
                                    result_list_Upload.append({'message_approveDocument':tmp_message_appDoc})
                                    result_resultDoc_Upload = callOneid_Upload(one_url+'/api/upload_result_api',path_result,'resultDocument',token_header)
                                    if result_resultDoc_Upload['result'] == 'OK':
                                        tmp_message_resultDoc = result_resultDoc_Upload['messageText'].json()
                                        if tmp_message_resultDoc['result'] == 'Success':
                                            result_list_Upload.append({'message_resultDocument':tmp_message_resultDoc})
                                            tmp_data_path_resultDoc = tmp_message_resultDoc['data']
                                            info_json_regis = {
                                                "account_title_th" : account_title_th,
                                                "first_name_th" : first_name_th,
                                                "account_title_eng" : account_title_eng,
                                                "first_name_eng" : first_name_eng,
                                                "id_card_type" : id_card_type,
                                                "id_card_num" : id_card_num,
                                                "email" : email,
                                                "mobile_no" : mobile_no,
                                                "tel_no" : tel_no,
                                                "approve_document" : tmp_data_path_appDoc,
                                                "result_meeting" : tmp_data_path_resultDoc,
                                                "name_on_document_th" : name_on_document_th,
                                                "name_on_document_eng" : name_on_document_eng,
                                                "owner_detail" : [{
                                                    "thai_email" : thai_email,
                                                    "department" : department,
                                                    "position":   position
                                                }],
                                                "address" : [{
                                                    "house_code" : house_code,
                                                    "house_no" : house_no,
                                                    "room_no" : room_no,
                                                    "moo_ban" : moo_ban,
                                                    "moo_no" : moo_no,
                                                    "building_name" : building_name,
                                                    "floor" : floor,
                                                    "yaek" : yaek,
                                                    "street" : street,
                                                    "fax_number" : fax_number,
                                                    "soi" : soi,
                                                    "province" : province,
                                                    "tambon" : tambon,
                                                    "amphoe": amphoe,
                                                    "zipcode": zipcode,
                                                    "country": country
                                                }],
                                                "branch_name" : branch_name,
                                                "branch_no" : branch_no
                                            }
                                            result_regisBusiness = callAuth_post(one_url+'/api/register_business',info_json_regis,token_header)
                                            if result_regisBusiness['result'] == 'OK':
                                                tmp_messageRegis = result_regisBusiness['messageText'].json()
                                                if tmp_messageRegis['result'] == 'Success':
                                                    tmp_all_data = str(info_json_regis)
                                                    result_insert = insert().insert_register_business_v1(tmp_citizen_id,tmp_taxid,tmp_all_data,path_approve,path_result,tmp_name_th,tmp_name_eng,path_porpor20)
                                                    return jsonify({'result':'OK','messageText':[{'data':info_json_regis,'message':'register business success and insert success'}],'status_Code':200,'messageER':None}),200
                                                else:
                                                    tmp_errMessage = tmp_messageRegis['errorMessage']
                                                    return jsonify({'result':'ER','messageText':[],'status_Code':200,'messageER':tmp_errMessage}),200
                                            else:
                                                return jsonify({'result':'ER','messageText':[],'status_Code':200,'messageER':result_regisBusiness['messageER']}),200
                                        else:
                                            result_list_Upload.append({'message_resultDocument':tmp_message_resultDoc})
                                            return jsonify({'result':'ER','messageText':result_list_Upload,'status_Code':200,'messageER':None}),200
                                    else:
                                        result_list_Upload.append({'message_resultDocument':tmp_message_resultDoc})
                                        return jsonify({'result':'ER','messageText':result_list_Upload,'status_Code':200,'messageER':None}),200
                                else:
                                    result_list_Upload.append({'message_approveDocument':tmp_data_path_appDoc})
                                    return jsonify({'result':'ER','messageText':result_list_Upload,'status_Code':200,'messageER':None}),200
                            else:
                                result_list_Upload.append(result_approveDocument_Upload)
                                return jsonify({'result':'ER','messageText':result_list_Upload,'status_Code':200,'messageER':None}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect in address'}),404
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect in owner'}),404

                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect in dataJson'}),404
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'status_Code':500,'messageER':'message : ' + str(e)}),500

@status_methods.route('/api/v1/register/register_citizen',methods=['POST'])
def register_citizen_api_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'account_title_th' in dataJson and 'first_name_th' in dataJson and 'last_name_th' in dataJson and 'account_title_eng' in dataJson and 'first_name_eng' in dataJson and 'last_name_eng' in dataJson and 'id_card_type' in dataJson and 'id_card_num' in dataJson and 'email' in dataJson and 'mobile_no' in dataJson and 'birth_date' in dataJson and 'username' in dataJson and 'password' in dataJson:
            account_title_th  = dataJson['account_title_th']
            first_name_th     = dataJson['first_name_th']
            last_name_th      = dataJson['last_name_th']
            account_title_eng = dataJson['account_title_eng']
            first_name_eng    = dataJson['first_name_eng']
            last_name_eng     = dataJson['last_name_eng']
            id_card_type      = dataJson['id_card_type']
            id_card_num       = dataJson['id_card_num']
            email             = dataJson['email']
            mobile_no         = dataJson['mobile_no']
            birth_date        = dataJson['birth_date']
            username          = dataJson['username']
            password          = dataJson['password']
            info_json = {
                "account_title_th":  account_title_th,
                "first_name_th":     first_name_th,
                "last_name_th":      last_name_th,
                "account_title_eng": account_title_eng,
                "first_name_eng":    first_name_eng,
                "last_name_eng":     last_name_eng ,
                "id_card_type":      id_card_type,
                "id_card_num":       id_card_num,
                "email":             email,
                "mobile_no":         mobile_no,
                "birth_date":        birth_date,
                "username":          username,
                "password":          password,        
                "ref_code":          ref_code,
                "clientId":          clientId,
                "secretKey":         secretKey
            }
            tmp_json_login = {
                "grant_type":  "password",
                "username":     username,
                "password":     password,
                "client_id":    clientId,
                "client_secret":secretKey
            }
            try:                
                one_regis = callPost_v2(one_url+"/api/register_api",info_json)
                if one_regis['result'] == 'OK':
                    json_one = one_regis['messageText'].json()
                    if json_one['result'] == 'Success':
                        tmp_data = json_one['data']
                        tmp_accountID = tmp_data['accountID']
                        tmp_email = tmp_data['email']
                        result_insert = insert().insert_register_citizen_v1(tmp_accountID,account_title_th,first_name_th,last_name_th,account_title_eng,first_name_eng
                        ,last_name_eng,id_card_type,id_card_num,email,mobile_no,birth_date,username,tmp_email)                        
                        result_login = callPost_v2(one_url+"/api/oauth/getpwd",tmp_json_login)
                        if result_login['result'] == 'OK':
                            tmp_message = result_login['messageText'].json()
                            if tmp_message['result'] == 'Success':
                                tmp_access_token = tmp_message['access_token']
                                tmp_username = tmp_message['username']
                                one_access_token = tmp_message['token_type'] + ' ' + tmp_access_token
                                result_getInfo = callGET_v2(one_url+'/api/account_and_biz_detail',one_access_token)
                                if result_getInfo['result'] == 'OK':
                                    tmp_data_info = result_getInfo['messageText'].json()
                                    if result_insert['result'] == 'OK':
                                        result_json = {
                                            "result":'OK',
                                            "username":tmp_username,
                                            "one_access_token":tmp_access_token,
                                            "one_result_data":tmp_data_info,
                                            "message":'register success and insert success'
                                        }
                                        return jsonify(result_json)
                                    else:
                                        result_json = {
                                            "result":'OK',
                                            "username":tmp_username,
                                            "one_access_token":tmp_access_token,
                                            "one_result_data":tmp_data_info,
                                            "message":'register success and insert fail'
                                        }
                                        return jsonify(result_json)
                                else:
                                    result_json = {
                                        "result":'OK',
                                        "username":tmp_username,
                                        "one_access_token":tmp_access_token,
                                        "one_result_data":{},
                                        "message":"register success and cant get account_and_biz_detail"
                                    }
                                    return jsonify(result_json)
                            else:
                                result_json = {
                                    "result":'OK',
                                    "username":username,
                                    "one_access_token":None,
                                    "one_result_data":{},
                                    "message":"register success and login fail"
                                }
                                return jsonify(result_json),401
                        else:
                            if result_login['status_Code'] == 401:
                                result_json = {
                                    "result":'OK',
                                    "username":username,
                                    "one_access_token":None,
                                    "one_result_data":{},
                                    "message":"register success and login fail"
                                }
                                return jsonify(result_json),401
                            else:
                                result_json = {
                                    "result":'OK',
                                    "username":username,
                                    "one_access_token":None,
                                    "one_result_data":{},
                                    "message":"register success and login fail " + result_login['messageText']
                                }
                                return jsonify(result_json),result_login['status_Code']
                    else:
                        tmp_err_msg = json_one['errorMessage']
                        if 'email' in tmp_err_msg:
                            for n in tmp_err_msg['email']:
                                return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':str(n)}),200
                        elif 'id_card_num' in tmp_err_msg:
                            for n in tmp_err_msg['id_card_num']:
                                return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':str(n)}),200
                        elif 'username' in tmp_err_msg:
                            for n in tmp_err_msg['username']:
                                return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':str(n)}),200
                        else:
                            return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':tmp_err_msg}),200
                else:
                    return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':one_regis['messageText']}),200
            except Exception as e:
                return jsonify({'result':'ER','status_Code':400,'messageText':None,'messageER':str(e)}),400

@status_methods.route('/api/v1/register/after_regis',methods=['POST'])
def after_regis_api_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)}),401
        dataJson = request.json
        if 'tax_id' in dataJson and len(dataJson) == 1:
            tmp_taxId = dataJson['tax_id']
            get_details_Buz = callGET_v2(one_url+"/api/getBusinessAccount/" + tmp_taxId,token_header)
            if get_details_Buz['result'] == 'OK':
                tmp_message = get_details_Buz['messageText'].json()
                if tmp_message['result'] == 'Success':
                    return jsonify({'result':'OK','messageText':tmp_message['data'],'messsageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messsageER':tmp_message['errorMessage'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messsageER':str(get_details_Buz['messageText']),'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404

@status_methods.route('/api/v1/register/business_role',methods=['POST','GET'])
def create_role_api_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)}),401
        dataJson = request.json
        if 'tax_id' in dataJson and 'role_name' in dataJson and 'role_level' in dataJson and len(dataJson) == 3:
            tmp_tax_id = dataJson['tax_id']
            tmp_role_name = dataJson['role_name']
            tmp_role_level = dataJson['role_level']
            info_json = {
                "tax_id":tmp_tax_id,
                "role_name":tmp_role_name,
                "role_level":tmp_role_level
            }
            result_CreateRole = callAuth_post(one_url+'/api/v1/service/business/role',info_json,token_header)
            if result_CreateRole['result'] == 'OK':
                tmp_message = result_CreateRole['messageText'].json()
                if tmp_message['result'] == 'Success':
                    tmp_data = tmp_message['data']
                    return jsonify({'result':'OK','messageText':{'message':'create role success','data':tmp_data},'status_Code':200,'messageER':None}),200
                else:
                    if 'errorMessage' in tmp_message:
                        messageER = tmp_message['errorMessage']
                    else:
                        messageER =str(tmp_message)
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':messageER}),200
            else:
                try:
                    tmp_message = result_CreateRole['messageText'].json()
                except Exception as e:
                    tmp_message = str(result_CreateRole['messageText'])
                if 'result' in tmp_message:
                    if 'errorMessage' in tmp_message:
                        messageER = tmp_message['errorMessage']
                    else:
                        messageER =str(tmp_message)
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':messageER}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':tmp_message}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404
    elif request.method == 'GET':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'status_Code':400,'messageER':'token expire unauthorized ' + str(e)}),400
        tmp_tax_id = request.args.get('tax_id')
        result_list = []
        if tmp_tax_id != None:
            result_role = callGET_v2(one_url+'/api/v1/service/business/role?tax_id='+tmp_tax_id,token_header)
            if result_role['result'] == 'OK':
                tmp_message = result_role['messageText'].json()
                if tmp_message['result'] == 'Success':
                    tmp_data = tmp_message['data']
                    if len(tmp_data) != 0:
                        for i in range(len(tmp_data)):
                            json_result = {}
                            tmp_role_details = tmp_data[i]['role'][0]
                            json_result['role_id'] = tmp_role_details['id']
                            json_result['role_level'] = tmp_role_details['role_level']
                            json_result['role_name'] = tmp_role_details['role_name']
                            result_list.append(json_result)
                        return jsonify({'result':'OK','messageText':result_list,'status_Code':200,'messageER':None}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data role not found'}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':tmp_message}),200
            else:
                tmp_message = result_role['messageText'].json()
                if tmp_message['result'] == 'Fail':
                    if 'errorMessage' in tmp_message:
                        messageER = tmp_message['errorMessage']
                    else:
                        messageER = str(tmp_message)
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':messageER}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404

@status_methods.route('/api/v1/register/business_department',methods=['POST','GET'])
def create_department_api_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)})
        dataJson = request.json
        if 'tax_id' in dataJson and 'dept_name' in dataJson and 'parent_dept_id' in dataJson and len(dataJson) == 3:
            tmp_tax_id = dataJson['tax_id']
            tmp_dept_name = dataJson['dept_name']
            tmp_parent_dept_id = dataJson['parent_dept_id']
            info_json = {
                "tax_id":tmp_tax_id,
                "dept_name":tmp_dept_name,
                "parent_dept_id":tmp_parent_dept_id
            }
            result_CreateDept = callAuth_post(one_url+'/api/v1/service/business/department',info_json,token_header)
            if result_CreateDept['result'] == 'OK':
                tmp_message = result_CreateDept['messageText'].json()
                if tmp_message['result'] == 'Success':
                    tmp_data = tmp_message['data']
                    return jsonify({'result':'OK','messageText':{'message':'create dept success','data':tmp_data},'status_Code':200,'messageER':None}),200
                else:
                    if 'errorMessage' in tmp_message:
                        messageER = tmp_message['errorMessage']
                    else:
                        messageER =str(tmp_message)
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':messageER}),200
            else:
                try:
                    tmp_message = result_CreateDept['messageText'].json()
                except Exception as e:
                    tmp_message = str(result_CreateDept['messageText'])
                if 'result' in tmp_message:
                    if 'errorMessage' in tmp_message:
                        messageER = tmp_message['errorMessage']
                    else:
                        messageER =str(tmp_message)
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':messageER}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':tmp_message}),200                
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404
    elif request.method == 'GET':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'status_Code':400,'messageER':'token expire unauthorized ' + str(e)}),400
        tmp_tax_id = request.args.get('tax_id')
        result_list = []
        if tmp_tax_id != None:
            result_role = callGET_v2(one_url+'/api/v1/service/business/department?tax_id='+tmp_tax_id,token_header)
            if result_role['result'] == 'OK':
                tmp_message = result_role['messageText'].json()
                if tmp_message['result'] == 'Success':
                    tmp_data = tmp_message['data']
                    print(tmp_data)
                    if tmp_data != 'no content':
                        if len(tmp_data) != 0:
                            for i in range(len(tmp_data)):
                                json_result = {}
                                tmp_dept_details = tmp_data[i]['department'][0]
                                json_result['dept_id'] = tmp_dept_details['id']
                                json_result['dept_name'] = tmp_dept_details['dept_name']
                                json_result['dept_position'] = tmp_dept_details['dept_position']
                                result_list.append(json_result)
                            return jsonify({'result':'OK','messageText':result_list,'status_Code':200,'messageER':None}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data department not found'}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'data department not found'}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':tmp_message}),200
            else:
                tmp_message = result_role['messageText'].json()
                if tmp_message['result'] == 'Fail':
                    if 'errorMessage' in tmp_message:
                        messageER = tmp_message['errorMessage']
                    else:
                        messageER = str(tmp_message)
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':messageER}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404

@status_methods.route('/api/v1/register/add_simple_business',methods=['POST'])
def add_simple_business_api_v1():
    if request.method == 'POST':
        dataJson = request.json
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)}),401
        if 'tax_id' in dataJson and len(dataJson) == 1:
            tmp_tax_id = dataJson['tax_id']
            info_dept = {
                "tax_id":tmp_tax_id,
                "dept_name":"Simple-Dept",
                "parent_dept_id":"0"
            }
            info_role = [{
                "tax_id":tmp_tax_id,
                "role_name":"Admin",
	            "role_level":"1"
            },{
                "tax_id":tmp_tax_id,
                "role_name":"User",
	            "role_level":"99"
            }]
            list_result = []
            tmp_data_dept_id = ''
            
            try:
                result_createDept = callAuth_post(one_url+'/api/v1/service/business/department',info_dept,token_header)
                if result_createDept['result'] == 'OK':
                    tmp_message = result_createDept['messageText'].json()
                    if tmp_message['result'] == 'Success':
                        tmp_data = tmp_message['data']
                        tmp_data_dept_id = tmp_data['id']
                        list_result.append({'result':'OK','messageText':{'message':'create dept success','data':tmp_data},'status_Code':200,'messageER':None})
                    else:
                        if 'errorMessage' in tmp_message:
                            messageER = tmp_message['errorMessage']
                        else:
                            messageER = str(tmp_message)
                        list_result.append({'result':'ER','messageText':None,'status_Code':200,'messageER':messageER})
                else: 
                    try:
                        tmp_message = result_createDept['messageText'].json()
                    except Exception as e:
                        tmp_message = str(result_createDept['messageText'])
                    if 'result' in tmp_message:
                        if 'errorMessage' in tmp_message:
                            messageER = tmp_message['errorMessage']
                        else:
                            messageER =str(tmp_message)
                        list_result.append({'result':'ER','messageText':None,'status_Code':200,'messageER':messageER})
                    else:
                        list_result.append({'result':'ER','messageText':None,'status_Code':200,'messageER':tmp_message})
                for i in range(len(info_role)):
                    result_CreateRole = callAuth_post(one_url+'/api/v1/service/business/role',info_role[i],token_header)
                    if result_CreateRole['result'] == 'OK':
                        tmp_message = result_CreateRole['messageText'].json()
                        if tmp_message['result'] == 'Success':
                            tmp_data = tmp_message['data']
                            tmp_data_role_id = tmp_data['id']
                            info_json = {
                                "tax_id":tmp_tax_id,
                                "dept_id":tmp_data_dept_id,
                                "role_id":tmp_data_role_id,
                                "parent_dept_role_id":"0",
                                "dept_role_level":1
                            }
                            result_add_roleToDept = callAuth_post(one_url+'/api/v1/service/business/department_role',info_json,token_header)
                            list_result.append({'result':'OK','messageText':{'message':'create role success','data':tmp_data},'status_Code':200,'messageER':None})
                        else:
                            if 'errorMessage' in tmp_message:
                                messageER = tmp_message['errorMessage']
                            else:
                                messageER =str(tmp_message)
                            list_result.append({'result':'ER','messageText':None,'status_Code':200,'messageER':messageER})
                    else:
                        try:
                            tmp_message = result_CreateRole['messageText'].json()
                        except Exception as e:
                            tmp_message = str(result_CreateRole['messageText'])
                        if 'result' in tmp_message:
                            if 'errorMessage' in tmp_message:
                                messageER = tmp_message['errorMessage']
                            else:
                                messageER =str(tmp_message)
                            list_result.append({'result':'ER','messageText':None,'status_Code':200,'messageER':messageER})
                        else:
                            list_result.append({'result':'ER','messageText':None,'status_Code':200,'messageER':tmp_message})
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'message ' + str(e)}),200                       
            return jsonify({'result':'OK','messageText':list_result,'status_Code':200,'messageER':None}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404

@status_methods.route('/api/v1/register/dept_role_business',methods=['POST'])
def dept_role_business_api_v1():
    if request.method == 'POST':
        dataJson = request.json
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)}),401
        if 'tax_id' in dataJson and 'secret_key' in dataJson and len(dataJson) == 2:
            tax_id = dataJson['tax_id']
            secret_key = dataJson['secret_key']
            list_result_role = []
            list_department_role = []
            if secret_key == 'gIiogu2SRj':
                json_info = {
                    "tax_id": tax_id
                }
                result_CallAPI_00 = CallAPI_POST_oneid(one_url + '/api/get_all_role_in_business',token_header,json_info)
                if result_CallAPI_00['result'] == 'OK':
                    if result_CallAPI_00['messageText']['result'] == 'Success':
                        json_info_all_department = {
                            "tax_id": tax_id
                        }
                        result_CallAPI_01 = CallAPI_POST_oneid(one_url + '/api/get_all_department_in_business',token_header,json_info_all_department)
                        if result_CallAPI_01['result'] == 'OK':
                            if result_CallAPI_01['messageText']['result'] == 'Success':
                                data_all_department = result_CallAPI_01['messageText']['data']
                                data_ = result_CallAPI_00['messageText']['data']
                                if data_all_department != None:
                                    for uu in range(len(data_all_department)):
                                        list_role_arr = []
                                        json_role_department = {}
                                        dept_id = data_all_department[uu]['department'][0]['id']
                                        dept_name = data_all_department[uu]['department'][0]['dept_name']
                                        json_role_department['dept_id'] = dept_id
                                        json_role_department['dept_name'] = dept_name
                                        json_info = {
                                            "tax_id": tax_id,
                                            "dept_id": dept_id
                                        }
                                        print(dept_id)
                                        result_CallAPI_02 = CallAPI_POST_oneid(one_url + '/api/get_all_role_in_department',token_header,json_info)
                                        if result_CallAPI_02['result'] == 'OK':
                                            if result_CallAPI_02['messageText']['result'] == 'Success':
                                                data_role_in_department =  result_CallAPI_02['messageText']['data']
                                                print(data_role_in_department)
                                                if data_role_in_department != None:
                                                    for uy in range(len(data_role_in_department)):
                                                        json_role_2 = {}
                                                        role_id_form_in_department = data_role_in_department[uy]['role'][0]['id']
                                                        role_name_form_in_department = data_role_in_department[uy]['role'][0]['role_name']
                                                        json_role_2['role_id'] = role_id_form_in_department
                                                        json_role_2['role_name'] = role_name_form_in_department
                                                        list_role_arr.append(json_role_2)
                                                    list_department_role.append({'department_':json_role_department,'role_':list_role_arr})
                                else:
                                    return jsonify({'result':'OK','messageText':None,'messageER':'not found data in tax id','status_Code':200}),200
                        list_check_role = []                                    
                        list_department = []                                        
                        for ui in range(len(list_department_role)):
                            
                            role_arr_info = list_department_role[ui]['role_']
                            
                            for role_index_name in range(len(role_arr_info)):
                                dept_id_form_list = list_department_role[ui]['department_']['dept_id']
                                dept_name_form_list = list_department_role[ui]['department_']['dept_name'] 
                                role_id_form_list = role_arr_info[role_index_name]['role_id']
                                role_name_form_list = role_arr_info[role_index_name]['role_name']
                                for i in range(len(data_)):                                           
                                    role_id = data_[i]['role'][0]['id']
                                    role_name = data_[i]['role'][0]['role_name']
                                    role_level = data_[i]['role'][0]['role_level']                            
                                    if role_id_form_list == role_id:
                                        list_department.append({'dept_id':dept_id_form_list,'dept_name':dept_name_form_list,'role_name':role_name,'role_id':role_id})
                        for ind in range(len(data_)):
                            my_result_json = {}
                            department_list = []
                            role_id = data_[ind]['role'][0]['id']
                            role_name = data_[ind]['role'][0]['role_name']
                            role_level = data_[ind]['role'][0]['role_level']  
                            for uub in range(len(list_department)):
                                role_id_and_department = list_department[uub]['role_id']
                                if role_id == role_id_and_department:
                                    department_list.append({'dept_id':list_department[uub]['dept_id'],'dept_name':list_department[uub]['dept_name']})
                                    my_result_json['role_id'] = role_id
                                    my_result_json['role_name'] = role_name
                                    my_result_json['role_level'] = role_level
                                    my_result_json['department_info'] = department_list                                        
                                else:
                                    my_result_json['role_id'] = role_id
                                    my_result_json['role_name'] = role_name
                                    my_result_json['role_level'] = role_level
                                    my_result_json['department_info'] = department_list
                            list_result_role.append(my_result_json)   
                        if len(list_result_role) != 0:
                            return jsonify({'result':'OK','messageText':list_result_role,'status_Code':200,'messageER':None}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'messageER':'not found data','status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'messageER':'not found data or Token fail','status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':'not found data or Token fail','status_Code':200}),200                
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':'secret_key incorrect','status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':'parameter incorrect','status_Code':200}),200
    
@status_methods.route('/api/v1/register/append_role_dept',methods=['POST'])
def append_role_dept_api_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)}),401
        dataJson = request.json
        if 'tax_id' in dataJson and 'role_id' in dataJson and 'dept_id' in dataJson and len(dataJson) ==3:
            tmp_tax_id = dataJson['tax_id']
            tmp_role_id = dataJson['role_id']
            tmp_dept_id = dataJson['dept_id']
            info_json = {
                "tax_id":tmp_tax_id,
                "dept_id":tmp_dept_id,
                "role_id":tmp_role_id,
                "parent_dept_role_id":"0",
                "dept_role_level":1
            }
            result_add_roleToDept = callAuth_post(one_url+'/api/v1/service/business/department_role',info_json,token_header)
            if result_add_roleToDept['result'] == 'OK':
                tmp_message = result_add_roleToDept['messageText'].json()
                if tmp_message['result'] == 'Success':
                    tmp_data = tmp_message['data']
                    return jsonify({'result':'OK','messageText':{'message':'append success','data':tmp_data},'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':{'message':'append fail','data':None},'status_Code':200,'messageER':None}),200
            else:
                try:
                    tmp_message = result_add_roleToDept['messageText'].json()
                except Exception as e:
                    tmp_message = result_add_roleToDept['messageText']
                if 'result' in tmp_message:
                    if 'errorMessage' in tmp_message:
                        tmp_errMessage = tmp_message['errorMessage']
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':tmp_errMessage}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':tmp_message}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404

@status_methods.route('/api/v1/register/add_citizen',methods=['POST'])
def append_citizen_api_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except Exception as e:            
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)}),401
        dataJson = request.json
        if 'tax_id' in dataJson and 'dept_id' in dataJson and 'role_id' in dataJson and 'account_id' in dataJson and len(dataJson) == 4:
            tmp_tax_id = dataJson['tax_id']
            tmp_dept_id = dataJson['dept_id']
            tmp_role_id = dataJson['role_id']
            tmp_account_id = dataJson['account_id']
            info_json = {
                "tax_id":tmp_tax_id,
                "dept_id":tmp_dept_id,
                "role_id":tmp_role_id,
                "id_card":tmp_account_id
            }
            result_add_citizen = callAuth_post(one_url+'/api/v1/service/business/department_role/account',info_json,token_header)
            if result_add_citizen['result'] == 'OK':
                tmp_message = result_add_citizen['messageText'].json()
                if tmp_message['result'] == 'Success':
                    tmp_data = tmp_message['data']
                    return jsonify({'result':'OK','messageText':{'message':'add citizen success','data':tmp_data},'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':{'message':'add citizen fail','data':None},'status_Code':200,'messageER':None}),200
            else:
                try:
                    tmp_message = result_add_citizen['messageText'].json()
                except Exception as e:
                    tmp_message = result_add_citizen['messageText']
                if 'result' in tmp_message:
                    if 'errorMessage' in tmp_message:
                        tmp_errMessage = tmp_message['errorMessage']
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':tmp_errMessage}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':tmp_message}),200

@status_methods.route('/api/v1/register/approve_business_ppl',methods=['POST'])
def approve_business_ppl_api_v1():
    if request.method == 'POST':
        dataJson = request.json
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)}),401
        if 'tax_id' in dataJson and len(dataJson) == 1:
            tmp_tax_id = dataJson['tax_id']
            result_insert = insert().insert_register_business_ppl_v1(tmp_tax_id)
            if result_insert['result'] == 'OK':
                return jsonify({'result':'OK','messageText':tmp_tax_id +' insert success','status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':tmp_tax_id +' insert fail ' + result_insert['messageText']}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404

@status_methods.route('/api/v1/register/account_in_business',methods=['POST'])
def account_in_business_api_v1():
    if request.method == 'POST':
        dataJson = request.json
        
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)}),401
        if 'tax_id' in dataJson and len(dataJson) == 1:
            tmp_list_res = []
            tmp_tax_id = dataJson['tax_id']
            result_get_account = callGET_v2(one_url+'/api/v1/service/business/account?tax_id=' + tmp_tax_id,token_header)
            if result_get_account['result'] == 'OK':
                tmp_message = result_get_account['messageText'].json()
                if tmp_message['result'] == 'Success':
                    tmp_data = tmp_message['data']
                    for i in range(len(tmp_data)):
                        json_result = {}
                        tmp_account_id = tmp_data[i]['account_id']
                        tmp_account_detail = tmp_data[i]['account_detail']
                        json_result['account_id'] = tmp_account_id
                        json_result['account_detail']  = tmp_account_detail
                        result_get_account_details = callGET_v2(one_url+'/api/v1/service/business/account/'+tmp_account_id+'/department_role?tax_id='+tmp_tax_id,token_header)
                        if result_get_account_details['result'] == 'OK':
                            tmp_message_2 = result_get_account_details['messageText'].json()
                            if tmp_message_2['result'] == 'Success':
                                tmp_data_2 = tmp_message_2['data']
                                json_result['business_detail'] = tmp_data_2
                            else:
                                json_result['business_detail'] = []
                        else:
                            json_result['business_detail'] = []                                                        
                        tmp_list_res.append(json_result)
                    return jsonify({'result':'OK','messageText':{'message':'success','data':tmp_list_res},'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':{'message':'fail cant get account oneid','data':[]},'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':{'message':'fail cant get account oneid','data':[]},'status_Code':200,'messageER':None}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404

@status_methods.route('/api/v1/register/unassign_account',methods=['POST'])
def unassign_account_api_v1():
    if request.method == 'POST':
        dataJson = request.json
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)}),401
        if 'tax_id' in dataJson and 'dept_id' in dataJson and 'role_id' in dataJson and 'account_id' in dataJson and len(dataJson) == 4:
            tmp_tax_id = dataJson['tax_id']
            tmp_dept_id = dataJson['dept_id']
            tmp_role_id = dataJson['role_id']
            tmp_account_id = dataJson['account_id']
            data_info = {
                "tax_id":tmp_tax_id,
                "dept_id":tmp_dept_id,
                "role_id":tmp_role_id,
                "account_id":tmp_account_id
            }
            result_unassign_account = callAuth_post(one_url+'/api/unassign_role_from_account',data_info,token_header)
            if result_unassign_account['result'] == 'OK':
                tmp_message = result_unassign_account['messageText'].json()
                if tmp_message['result'] == 'Success': 
                    return jsonify({'result':'OK','messageText':{'message':'success','data':[]},'status_Code':200,'messageER':None}),200
                else:
                    if 'errorMessage' in tmp_message:
                        return jsonify({'result':'ER','messageText':None,'status_Code':tmp_message['code'],'messageER':{'message':'fail ' + tmp_message['errorMessage'],'data':[]}}),tmp_message['code']
            else:
                try:
                    tmp_message = result_unassign_account['messageText'].json()
                except Exception as e:
                    tmp_message = result_unassign_account['messageText']
                if 'result' in tmp_message:
                    if 'errorMessage' in tmp_message:
                        tmp_errMessage = tmp_message['errorMessage']
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':tmp_errMessage,'data':[]}}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':tmp_message,'data':[]}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404
    
    