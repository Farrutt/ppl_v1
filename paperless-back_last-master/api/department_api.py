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



if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less

def CallAPI_POST_oneid(url,header_token,datajson):
    try:
        tmp_header_token = 'Bearer ' + header_token
        response = requests.request("POST",headers={'Authorization': tmp_header_token}, url=url, json=datajson, verify=False, stream=True)
        response = response.json()
        insert().insert_tran_log_v1(str(response),'OK',str(datajson),url,header_token)
        return {'result': 'OK','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(datajson),url,header_token)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(datajson),url,header_token)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(datajson),url,header_token)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,header_token)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(ex)}

def CallAPI_GET_oneid(url,header_token):
    try:
        tmp_header_token = 'Bearer ' + header_token
        response = requests.request("GET",headers={'Authorization': tmp_header_token}, url=url, verify=False, stream=True)
        response = response.json()
        insert().insert_tran_log_v1(str(response),'OK',None,url,header_token)
        return {'result': 'OK','messageText': response}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',None,url,header_token)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',None,url,header_token)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',None,url,header_token)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',None,url,header_token)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(ex)}

@status_methods.route('/api/v1/department_getupper_role', methods=['POST'])
def department_upper_role_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'dept_id' in dataJson and 'maxstep' in dataJson and 'role_id' in dataJson and 'tax_id' in dataJson and len(dataJson) == 4:
            dept_id = dataJson['dept_id']
            maxstep = dataJson['maxstep']
            role_id = dataJson['role_id']
            tax_id = dataJson['tax_id']
            try:
                token_header = request.headers['Authorization']
                try:
                    token_header = str(token_header).split(' ')[1]
                except Exception as ex:
                    return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
            except KeyError as ex:
                return redirect(url_paperless)
            try:
                list_result = []
                json_info = {
                    "tax_id": tax_id,
                    "dept_id" : dept_id,
                	"role_id" : role_id
                }
                result_CallAPI = CallAPI_POST_oneid(one_url + '/api/get_upper_line_role_in_department',token_header,json_info)
                print(result_CallAPI['messageText']['data'])
                if result_CallAPI['result'] =='OK':
                    if result_CallAPI['messageText']['result'] == 'Success':

                        data = result_CallAPI['messageText']['data']
                        for i in range(len(data)):
                            upper_line_role = data[i]['upper_line_role']
                            for yu in range(len(upper_line_role)):
                                list_account = []
                                role_id_get_oneid = upper_line_role[yu]['id']
                                role_name_get_oneid = upper_line_role[yu]['role_name']
                                json_info = {
                                    "tax_id": tax_id,
                                    "dept_id" : "",
                                	"role_id" : role_id_get_oneid
                                }
                                result_CallAPI_01 = CallAPI_GET_oneid(one_url + '/api/v1/service/business/role/' +role_id_get_oneid +'/account?tax_id=' + tax_id,token_header)
                                # print(result_CallAPI_01, ' result_CallAPI_01')
                                if yu == maxstep:
                                    pass
                                else:
                                    if result_CallAPI_01['result'] == 'OK':
                                        if result_CallAPI_01['messageText']['result'] == 'Success':
                                            data_account = result_CallAPI_01['messageText']['data']
                                            if data_account != None:
                                                for ui in range(len(data_account)):
                                                    list_account.append({
                                                        'account_id':data_account[ui]['account_id'],
                                                        'first_name_th':data_account[ui]['account_detail'][0]['first_name_th'],
                                                        'last_name_th':data_account[ui]['account_detail'][0]['last_name_th'],
                                                        'first_name_eng':data_account[ui]['account_detail'][0]['first_name_eng'],
                                                        'last_name_eng':data_account[ui]['account_detail'][0]['last_name_eng'],
                                                        'account_title_th':data_account[ui]['account_detail'][0]['account_title_th'],
                                                        'account_title_eng':data_account[ui]['account_detail'][0]['account_title_eng'],
                                                        'thai_email':data_account[ui]['account_detail'][0]['thai_email']
                                                    })
                                            else:
                                                list_account = []
                                list_result.append({
                                    "role_name":role_name_get_oneid,
                                    "account_details":list_account
                                })
                        if len(list_result) != 0:
                            return jsonify({'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'messageER':'not found data','status_Code':200}),200
                    else:
                        data = result_CallAPI['messageText']['data']
                        if data != None:
                            return jsonify({'result':'ER','messageText':None,'messageER':'ไม่พบข้อมูล','status_Code':200}),200
                        return jsonify({'result':'ER','messageText':None,'messageER':'Authorization Fail!','status_Code':401}),401
            except Exception as e:
                return jsonify({'result':'OK','messageText':None,'messageER':str(e),'status_Code':200}),200

@status_methods.route('/api/v1/department_getdetails_account', methods=['POST'])
def department_get_account_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'account_id' in dataJson and 'tax_id' and dataJson and len(dataJson) == 2:
            account_id = dataJson['account_id']
            tax_id = dataJson['tax_id']
            list_json_result_repo = []
            try:
                token_header = request.headers['Authorization']
                try:
                    token_header = str(token_header).split(' ')[1]
                except Exception as ex:
                    return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
            except KeyError as ex:
                return redirect(url_paperless)
            try:
                json_info = {
                	"tax_id":tax_id,
                	"account_id":account_id
                }
                result_CallAPI = CallAPI_POST_oneid(one_url + '/api/get_detail_employee_in_business',token_header,json_info)
                print(result_CallAPI)
                check_biz_info = []
                dept_id = []
                dept_name = []
                if result_CallAPI['result'] == 'OK':
                    if result_CallAPI['messageText']['result'] == 'Success':
                        data_result = result_CallAPI['messageText']['data']
                        for i in range(len(data_result)):
                            department_details = data_result[i]['department']
                            for iii in range(len(department_details)):
                                dept_id.append(department_details[iii]['id'])
                                dept_name.append(department_details[iii]['dept_name'])
                            if data_result[i]['biz_id'] not in check_biz_info:
                                check_biz_info.append(data_result[i]['biz_id'])
                                account_id = data_result[i]['account_id']
                                role_id = data_result[i]['role_id']
                                get_role = data_result[i]['role']
                                account_detail = data_result[i]['account_detail']

                                for iu in range(len(account_detail)):
                                    first_name_th = account_detail[iu]['first_name_th']
                                    last_name_th = account_detail[iu]['last_name_th']
                                    account_title_th = account_detail[iu]['account_title_th']
                                    thai_email = account_detail[iu]['thai_email']
                                for uu in range(len(get_role)):
                                    role_name = get_role[uu]['role_name']
                                list_json_result_repo.append({
                                    'account_id':account_id,
                                    'dept_id':dept_id,
                                    'role_id':role_id,
                                    'dept_name':dept_name,
                                    'role_name':role_name,
                                    'first_name_th':first_name_th,
                                    'last_name_th':last_name_th,
                                    'account_title_th':account_title_th,
                                    'thai_email':thai_email
                                })
                        return jsonify({'result':'OK','messageText':list_json_result_repo,'status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':None,'messageER':'Authorization Fail!','status_Code':401}),401
            except Exception as e:
                return jsonify({'result':'OK','messageText':None,'messageER':str(e),'status_Code':200}),200

def department_get_lineupper_v1_methods(maxstep,minstep,tax_id,dept_id,token_header,index_count_sum,result_get_department):
    
    if result_get_department == '':
        list_check_role_position = []
        list_account = []
        list_result = []

    total_step = maxstep
    new_upper_position = ''
    # print(minstep, maxstep)
    if minstep < maxstep:
        
        json_info = {
        	"tax_id" : tax_id,
        	"dept_id" : dept_id
        }
        result_CallAPI_02 = CallAPI_POST_oneid(one_url + '/api/get_upper_line_department',token_header,json_info)
        # print(result_CallAPI_02)
        if result_CallAPI_02['result'] == 'OK':
            if result_CallAPI_02['messageText']['result'] == 'Success':
                data_form_oneid = result_CallAPI_02['messageText']['data']
                for ii in range(len(data_form_oneid)):
                    my_department_info = data_form_oneid[ii]['department']
                    upper_line_department = data_form_oneid[ii]['upper_line_department']
                    
                    for u in range(len(my_department_info)):
                        # print(my_department_info[u])
                        my_department_position = my_department_info[u]['dept_position']
                        # print(my_department_position, 'my_department_position')
                        string_position_spilt = str(my_department_position).split('.')
                        count = 1
                        for index_spilt in range(len(string_position_spilt)):
                            if count != len(string_position_spilt):
                                new_upper_position += string_position_spilt[index_spilt] + '.'
                                count = count + 1
                        if new_upper_position not in list_check_role_position:
                            new_upper_position = new_upper_position.replace('.','')
                            list_check_role_position.append(new_upper_position)
                    for uu in range(len(upper_line_department)):
                        upper_position = str(upper_line_department[uu]['dept_position']).replace('.','')
                        if new_upper_position == upper_position:
                            dept_id_new_upper_line = upper_line_department[uu]['id']
                            dept_name_new_upper_line = upper_line_department[uu]['dept_name']
                    json_info = {
                        "tax_id": tax_id,
                        "dept_id": dept_id_new_upper_line
                    }
                    result_CallAPI_03 = CallAPI_POST_oneid(one_url + '/api/get_all_role_in_department',token_header,json_info)
                    if result_CallAPI_03['result'] == 'OK':
                        if result_CallAPI_03['messageText']['result'] == 'Success':
                            count_dept_up = 0
                            data_form_oneid_2 = result_CallAPI_03['messageText']['data']
                            # print(data_form_oneid_2 , ' data_form_oneid_2')
                            if len(data_form_oneid_2) != 0:
                                if len(data_form_oneid_2) > 1:
                                    
                                    getlast_elem = data_form_oneid_2[-1]
                                    role_id_last_elm = getlast_elem['role'][0]['id']
                                    dept_id_last_elm = getlast_elem['dept_id']
                                    json_info = {
                                        "tax_id": tax_id,
                                        "dept_id" : dept_id_last_elm,
                                        "role_id" : role_id_last_elm
                                    }
                                    result_CallAPI_10 = CallAPI_POST_oneid(one_url + '/api/get_upper_line_role_in_department',token_header,json_info)
                                    # print(result_CallAPI_10 , ' result_CallAPI_04')
                                    if result_CallAPI_10['result'] == 'OK':
                                        if result_CallAPI_10['messageText']['result'] == 'Success':
                                            data_list_role_upper = result_CallAPI_10['messageText']['data'][0]['upper_line_role']
                                            for io in range(len(data_list_role_upper)):
                                                minstep = minstep + 1
                                                index_count_sum = index_count_sum + 1
                                                list_account = []
                                                list_role_upper = []
                                                # print(data_list_role_upper[io])
                                                # # list_result = []
                                                role_id_upper_role = data_list_role_upper[io]['id']
                                                role_name_upper_ = data_list_role_upper[io]['role_name']
                                                json_info = {
                                                    "tax_id": tax_id,
                                                    "dept_id" : dept_id_last_elm,
                                                    "role_id" : role_id_upper_role
                                                }
                                                result_CallAPI_04 = CallAPI_GET_oneid(one_url + '/api/v1/service/business/role/' +role_id_upper_role +'/account?tax_id=' + tax_id,token_header)
                                                if result_CallAPI_04['result'] == 'OK':
                                                    if result_CallAPI_04['messageText']['result'] == 'Success':
                                                        data_form_oneid_3 = result_CallAPI_04['messageText']['data']
                                                        if data_form_oneid_3 != None:
                                                            for yyu in range(len(data_form_oneid_3)):
                                                                list_account.append({
                                                                    'index_count':index_count_sum,
                                                                    'account_id':data_form_oneid_3[yyu]['account_id'],
                                                                    'first_name_th':data_form_oneid_3[yyu]['account_detail'][0]['first_name_th'],
                                                                    'last_name_th':data_form_oneid_3[yyu]['account_detail'][0]['last_name_th'],
                                                                    'first_name_eng':data_form_oneid_3[yyu]['account_detail'][0]['first_name_eng'],
                                                                    'last_name_eng':data_form_oneid_3[yyu]['account_detail'][0]['last_name_eng'],
                                                                    'account_title_th':data_form_oneid_3[yyu]['account_detail'][0]['account_title_th'],
                                                                    'account_title_eng':data_form_oneid_3[yyu]['account_detail'][0]['account_title_eng'],
                                                                    'thai_email':data_form_oneid_3[yyu]['account_detail'][0]['thai_email']
                                                                })
                                                        else:
                                                            list_account = []
                                                list_role_upper.append({
                                                    'index_detp_role':index_count_sum,
                                                    "role_name":role_name_upper_,
                                                    "role_id":role_id_upper_role,
                                                    "account_details":list_account,
                                                    "dept_id" : dept_id_last_elm,
                                                    "dept_name":''
                                                })
                                                list_result.append(list_role_upper[0])
                                                print(list_role_upper[0])
                                else:
                                    index_count_sum = index_count_sum + 1
                                    minstep = minstep + 1
                                    for oo in range(len(data_form_oneid_2)):
                                        if count_dept_up != total_step:
                                            role_upper_new_oneid = data_form_oneid_2[oo]['role_id']
                                            role_details = data_form_oneid_2[oo]['role']
                                            for zzz in range(len(role_details)):
                                                role_name_new_upper = role_details[zzz]['role_name']
                                            json_info = {
                                                "tax_id": tax_id,
                                                "dept_id" : dept_id_new_upper_line,
                                                "role_id" : role_upper_new_oneid
                                            }
                                            result_CallAPI_04 = CallAPI_GET_oneid(one_url + '/api/v1/service/business/department/' + dept_id_new_upper_line + '/role/' + role_upper_new_oneid +'/account?tax_id=' +tax_id,token_header)
                                            if result_CallAPI_04['result'] == 'OK':
                                                if result_CallAPI_04['messageText']['result'] == 'Success':
                                                    data_form_oneid_3 = result_CallAPI_04['messageText']['data']
                                                    if data_form_oneid_3 != None:
                                                        for yyu in range(len(data_form_oneid_3)):
                                                            list_account.append({
                                                                'index_count':index_count_sum,
                                                                'account_id':data_form_oneid_3[yyu]['account_id'],
                                                                'first_name_th':data_form_oneid_3[yyu]['account_detail'][0]['first_name_th'],
                                                                'last_name_th':data_form_oneid_3[yyu]['account_detail'][0]['last_name_th'],
                                                                'first_name_eng':data_form_oneid_3[yyu]['account_detail'][0]['first_name_eng'],
                                                                'last_name_eng':data_form_oneid_3[yyu]['account_detail'][0]['last_name_eng'],
                                                                'account_title_th':data_form_oneid_3[yyu]['account_detail'][0]['account_title_th'],
                                                                'account_title_eng':data_form_oneid_3[yyu]['account_detail'][0]['account_title_eng'],
                                                                'thai_email':data_form_oneid_3[yyu]['account_detail'][0]['thai_email']
                                                            })
                                                    else:
                                                        list_account = []
                                                list_result.append({
                                                    'index_detp_role':index_count_sum,
                                                    "role_name":role_name_new_upper,
                                                    "role_id":role_upper_new_oneid,
                                                    "account_details":list_account,
                                                    "dept_id" : dept_id_new_upper_line,
                                                    "dept_name":dept_name_new_upper_line
                                                })
                # print(list_result)
        return list_result,maxstep,minstep,dept_id_new_upper_line,index_count_sum

@status_methods.route('/api/v1/department_get_lineupper', methods=['POST'])
def department_get_lineupper_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'dept_id' in dataJson and 'maxstep' in dataJson and 'role_id' in dataJson and 'tax_id' in dataJson and 'role_name' in dataJson and 'account_id' in dataJson and 'formula_temp' in dataJson and len(dataJson) == 7:
            dept_id = dataJson['dept_id']
            maxstep = dataJson['maxstep']
            role_id = dataJson['role_id']
            tax_id = dataJson['tax_id']
            role_name = dataJson['role_name']
            account_id = dataJson['account_id']
            formula_temp = dataJson['formula_temp']
            try:
                delete_role_list = formula_temp['delete']
                role_from_list = formula_temp['role_from']
                role_to_list = formula_temp['role_to']
            except Exception as e:
                return jsonify({'result':'ER','messageText':None,'messageER':str(e) + ' in formula'})          
            
            maxstep = (maxstep)
            try:
                token_header = request.headers['Authorization']
                try:
                    token_header = str(token_header).split(' ')[1]
                except Exception as ex:
                    return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
            except KeyError as ex:
                return redirect(url_paperless)
            try:
                list_result = []
                json_info = {
                    "tax_id": tax_id
                }
                result_CallAPI_00 = CallAPI_POST_oneid(one_url + '/api/get_all_department_in_business',token_header,json_info)
                if result_CallAPI_00['result'] =='OK':
                    if result_CallAPI_00['messageText']['result'] == 'Success':
                        data_ = result_CallAPI_00['messageText']['data']
                        if len(data_) != 0:
                            for uu in range(len(data_)):
                                dept_id_oneid = data_[uu]['dept_id']
                                if dept_id_oneid == dept_id:
                                    department_info = data_[uu]['department'][0]
                                    dept_name_oneid = department_info['dept_name']
                json_info = {
                    "tax_id": tax_id,
                    "dept_id" : dept_id,
                	"role_id" : role_id
                }
                result_CallAPI = CallAPI_POST_oneid(one_url + '/api/get_upper_line_role_in_department',token_header,json_info)
                print(result_CallAPI)
                if result_CallAPI['result'] =='OK':
                    if result_CallAPI['messageText']['result'] == 'Success':
                        data = result_CallAPI['messageText']['data']
                        index_count_sum = 0
                        count_step_num = 0
                        count_role_name = 0
                        if len(data) != 0:
                            for i in range(len(data)):
                                upper_line_role = data[i]['upper_line_role']
                                if len(upper_line_role) != 0:
                                    for yu in range(len(upper_line_role)):
                                        if count_step_num != maxstep:
                                            if upper_line_role[yu]['role_name'] == role_name and count_role_name == 0:
                                                if count_step_num == maxstep:
                                                    pass
                                                else:
                                                    list_account = []
                                                    role_id_get_oneid = upper_line_role[yu]['id']
                                                    role_name_get_oneid = upper_line_role[yu]['role_name']
                                                    json_info = {
                                                        "tax_id": tax_id,
                                                        "dept_id" : "",
                                                        "role_id" : role_id_get_oneid
                                                    }
                                                    result_CallAPI_all_account = CallAPI_GET_oneid(one_url + '/api/v1/service/business/role/' +role_id_get_oneid +'/account?tax_id=' + tax_id,token_header)
                                                    index_count_sum = index_count_sum + 1
                                                    if result_CallAPI_all_account['result'] == 'OK':
                                                        if result_CallAPI_all_account['messageText']['result'] == 'Success':
                                                            data_account = result_CallAPI_all_account['messageText']['data']
                                                            if len(data_account) != 0:
                                                                for ui in range(len(data_account)):
                                                                    if data_account[ui]['account_id'] == account_id:
                                                                        print(data_account[ui])
                                                                        list_account.append({
                                                                            'index_count':index_count_sum,
                                                                            'account_id':data_account[ui]['account_id'],
                                                                            'first_name_th':data_account[ui]['account_detail'][0]['first_name_th'],
                                                                            'last_name_th':data_account[ui]['account_detail'][0]['last_name_th'],
                                                                            'first_name_eng':data_account[ui]['account_detail'][0]['first_name_eng'],
                                                                            'last_name_eng':data_account[ui]['account_detail'][0]['last_name_eng'],
                                                                            'account_title_th':data_account[ui]['account_detail'][0]['account_title_th'],
                                                                            'account_title_eng':data_account[ui]['account_detail'][0]['account_title_eng'],
                                                                            'thai_email':data_account[ui]['account_detail'][0]['thai_email']
                                                                        })
                                                count_role_name = count_role_name + 1
                                                count_step_num = count_step_num + 1
                                                list_result.append({
                                                    'index_detp_role':index_count_sum,
                                                    "role_name":role_name_get_oneid,
                                                    "role_id":role_id_get_oneid,
                                                    "account_details":list_account,
                                                    "dept_id" : dept_id,
                                                    "dept_name":dept_name_oneid
                                                })
                                                # print()
                                                
                                            elif upper_line_role[yu]['role_name'] != role_name:
                                                
                                                if  upper_line_role[yu]['role_name'] not in delete_role_list:
                                                    # print(upper_line_role[yu]['role_name'], 'role_name______OO')
                                                    list_account = []                                        
                                                    role_id_get_oneid = upper_line_role[yu]['id']
                                                    role_name_get_oneid = upper_line_role[yu]['role_name']
                                                    json_info = {
                                                        "tax_id": tax_id,
                                                        "dept_id" : dept_id,
                                                        "role_id" : role_id_get_oneid
                                                    }
                                                    result_CallAPI_01 = CallAPI_GET_oneid(one_url + '/api/v1/service/business/department/' + dept_id + '/role/' + role_id_get_oneid +'/account?tax_id=' +tax_id,token_header)
                                                    print('/api/get_all_account_in_role_in_department')
                                                    index_count_sum = index_count_sum + 1
                                                    if result_CallAPI_01['result'] == 'OK':
                                                        if result_CallAPI_01['messageText']['result'] == 'Success':
                                                            data_account = result_CallAPI_01['messageText']['data']
                                                            print(data_account)
                                                            if data_account != None:
                                                                if type(data_account) is not str:
                                                                    for ui in range(len(data_account)):
                                                                        print(data_account[ui]['account_id'])
                                                                        list_account.append({
                                                                            'index_count':index_count_sum,
                                                                            'account_id':data_account[ui]['account_id'],
                                                                            'first_name_th':data_account[ui]['account_detail'][0]['first_name_th'],
                                                                            'last_name_th':data_account[ui]['account_detail'][0]['last_name_th'],
                                                                            'first_name_eng':data_account[ui]['account_detail'][0]['first_name_eng'],
                                                                            'last_name_eng':data_account[ui]['account_detail'][0]['last_name_eng'],
                                                                            'account_title_th':data_account[ui]['account_detail'][0]['account_title_th'],
                                                                            'account_title_eng':data_account[ui]['account_detail'][0]['account_title_eng'],
                                                                            'thai_email':data_account[ui]['account_detail'][0]['thai_email']
                                                                        })
                                                            else:
                                                                list_account = []
                                                    # print(list_account,'list_account')
                                                    count_step_num = count_step_num + 1
                                                # else:
                                                #     list_account = []
                                            # print(list_account)
                                            # print((role_name_get_oneid))
                                            # if len(list_account) != 0:
                                                    list_result.append({
                                                        'index_detp_role':index_count_sum,
                                                        "role_name":role_name_get_oneid,
                                                        "role_id":role_id_get_oneid,
                                                        "account_details":list_account,
                                                        "dept_id" : dept_id,
                                                        "dept_name":dept_name_oneid
                                                    })
                                                    # print(len(list_result))
                                            # else:
                                            #     list_result.append({
                                            #         'index_detp_role':index_count_sum,
                                            #         "role_name":role_name_get_oneid,
                                            #         "role_id":role_id_get_oneid,
                                            #         "account_details":[],
                                            #         "dept_id" : dept_id,
                                            #         "dept_name":dept_name_oneid
                                            #     })
                                
                                            # print(count_step_num)
                        # print(count_step_num , maxstep)
                        if count_step_num < maxstep:                
                            list_result_select,maxstep,minstep,dept_id_new_upper_line,count_sum_ = department_get_lineupper_v1_methods(maxstep,count_step_num,tax_id,dept_id,token_header,index_count_sum,'')
                            if len(list_result_select) != 0:
                                # print(list_result_select , '--------------------------')
                                for uui in range(len(list_result_select)):
                                    list_result.append(list_result_select[uui])
                            for ii in range(minstep,maxstep):
                                try:
                                    list_result_select_,maxstep,minstep,dept_id_new_upper_line,count_sum_ = department_get_lineupper_v1_methods(maxstep,minstep,tax_id,dept_id_new_upper_line,token_header,count_sum_,'')
                                    if len(list_result_select_) != 0:
                                        for yuu in range(len(list_result_select_)):
                                            list_result.append(list_result_select_[yuu])
                                    # list_result.append(list_result_select_[0])
                                except Exception as e:
                                    pass
                        
                        list_to_pop = []
                        check_from_list_role = False
                        if len(role_from_list) != 0:
                            if len(role_from_list) == len(role_to_list):
                                for index_list in range(len(list_result)):
                                    role_name = list_result[index_list]['role_name']
                                    for zu in range(len(role_from_list)):
                                        if role_from_list[zu] == role_name:
                                            list_to_pop.append(index_list)
                                            check_from_list_role = True
                                            index_list_role_from = zu
                                            temp_account_details_from = list_result[index_list]
                                if check_from_list_role:
                                    for index_list_0 in range(len(list_result)):
                                        role_name = list_result[index_list_0]['role_name']
                                        if role_to_list[index_list_role_from] == role_name:                                            
                                            temp_account_details_to = list_result[index_list_0]
                                            account_details_from = temp_account_details_from['account_details']
                                            account_details_to = temp_account_details_to
                                            for u in range(len(account_details_to['account_details'])):
                                                for ii in range(len(account_details_from)):
                                                    account_details_to['account_details'].append(account_details_from[ii])
                                        else:
                                            pass
                                else:
                                    pass
                            else:
                                return jsonify({'result':'ER','messageText':None,'messageER':'role_from_list incorrect and role_to_list incorrect','status_Code':200}),200
                        for uu in range(len(list_to_pop)):
                            list_result.pop(list_to_pop[uu])
                        print(len(list_result))
                        count_index = 1
                        for oooooo in range(len(list_result)):
                            list_result[oooooo]['index_detp_role'] = count_index
                            count_index = count_index + 1
                        if len(list_result) != 0:
                            return jsonify({'result':'OK','messageText':list_result,'status_Code':200}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'messageER':'data not found','status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':None,'messageER':'Authorization Fail!','status_Code':401}),401
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':'token error','status_Code':401}),401
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':'parameter incorrect','status_Code':200}),200

@status_methods.route('/api/v2/department_get_lineupper', methods=['POST'])
def department_get_lineupper_v2():
    if request.method == 'POST':
        dataJson = request.json
        if 'dept_id' in dataJson and 'maxstep' in dataJson and 'role_id' in dataJson and 'tax_id' in dataJson and 'role_name' in dataJson and 'account_id' in dataJson and 'formula_temp' in dataJson and len(dataJson) == 7:
            dept_id = dataJson['dept_id']
            maxstep = dataJson['maxstep']
            role_id = dataJson['role_id']
            tax_id = dataJson['tax_id']
            role_name = dataJson['role_name']
            account_id = dataJson['account_id']
            formula_temp = dataJson['formula_temp']
            try:
                delete_role_list = formula_temp['delete']
                role_from_list = formula_temp['role_from']
                role_to_list = formula_temp['role_to']
            except Exception as e:
                return jsonify({'result':'ER','messageText':None,'messageER':str(e) + ' in formula'})
            try:
                for uu in range(len(delete_role_list)):
                    dept_id_in_formula = delete_role_list[uu]['dept_id']
                    role_id_in_formula = delete_role_list[uu]['role_id']
            except Exception as e:
                return jsonify({'result':'ER','messageText':None,'messageER':str(e) + ' in formula'})
            maxstep = (maxstep)
            try:
                token_header = request.headers['Authorization']
                try:
                    token_header = str(token_header).split(' ')[1]
                except Exception as ex:
                    return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
            except KeyError as ex:
                return redirect(url_paperless)
            try:
                list_result = []
                json_info = {
                    "tax_id": tax_id
                }
                result_CallAPI_00 = CallAPI_POST_oneid(one_url + '/api/get_all_department_in_business',token_header,json_info)
                if result_CallAPI_00['result'] =='OK':
                    if result_CallAPI_00['messageText']['result'] == 'Success':
                        data_ = result_CallAPI_00['messageText']['data']
                        for uu in range(len(data_)):
                            dept_id_oneid = data_[uu]['dept_id']
                            if dept_id_oneid == dept_id:
                                department_info = data_[uu]['department'][0]
                                dept_name_oneid = department_info['dept_name']
                json_info = {
                    "tax_id": tax_id,
                    "dept_id" : dept_id,
                	"role_id" : role_id
                }
                result_CallAPI = CallAPI_POST_oneid(one_url + '/api/get_upper_line_role_in_department',token_header,json_info)
                if result_CallAPI['result'] =='OK':
                    if result_CallAPI['messageText']['result'] == 'Success':
                        data = result_CallAPI['messageText']['data']
                        index_count_sum = 0
                        count_step_num = 0
                        count_role_name = 0
                        for i in range(len(data)):
                            upper_line_role = data[i]['upper_line_role']
                            for yu in range(len(upper_line_role)):
                                if count_step_num != maxstep:
                                    if upper_line_role[yu]['role_name'] == role_name and count_role_name == 0:
                                        if count_step_num == maxstep:
                                            pass
                                        else:
                                            list_account = []
                                            role_id_get_oneid = upper_line_role[yu]['id']
                                            role_name_get_oneid = upper_line_role[yu]['role_name']
                                            json_info = {
                                                "tax_id": tax_id,
                                                "dept_id" : "",
                                                "role_id" : role_id_get_oneid
                                            }
                                            result_CallAPI_all_account = CallAPI_POST_oneid(one_url + '/api/get_all_account_in_role',token_header,json_info)
                                            index_count_sum = index_count_sum + 1
                                            if result_CallAPI_all_account['result'] == 'OK':
                                                if result_CallAPI_all_account['messageText']['result'] == 'Success':
                                                    data_account = result_CallAPI_all_account['messageText']['data']
                                                    for ui in range(len(data_account)):
                                                        if data_account[ui]['account_id'] == account_id:
                                                            list_account.append({
                                                                'index_count':index_count_sum,
                                                                'account_id':data_account[ui]['account_id'],
                                                                'first_name_th':data_account[ui]['account__detail'][0]['first_name_th'],
                                                                'last_name_th':data_account[ui]['account__detail'][0]['last_name_th'],
                                                                'first_name_eng':data_account[ui]['account__detail'][0]['first_name_eng'],
                                                                'last_name_eng':data_account[ui]['account__detail'][0]['last_name_eng'],
                                                                'account_title_th':data_account[ui]['account__detail'][0]['account_title_th'],
                                                                'account_title_eng':data_account[ui]['account__detail'][0]['account_title_eng'],
                                                                'thai_email':data_account[ui]['account__detail'][0]['thai_email']
                                                            })
                                        count_role_name = count_role_name + 1
                                        count_step_num = count_step_num + 1
                                    elif upper_line_role[yu]['role_name'] != role_name:
                                        list_checks_role_dept = []
                                        for zz in  range(len(delete_role_list)):
                                            dept_id_in_formula = delete_role_list[zz]['dept_id']
                                            role_id_in_formula = delete_role_list[zz]['role_id']
                                            string_role_dept_in_list = dept_id_in_formula + ',' + role_id_in_formula
                                            if string_role_dept_in_list not in  list_checks_role_dept:
                                                list_checks_role_dept.append(string_role_dept_in_list)
                                            print(string_role_dept_in_list)
                                        if dept_id == dept_id_in_formula:
                                            if  upper_line_role[yu]['id'] !=  "":
                                                string_role_dept_in_list = dept_id_in_formula + ',' + role_id_in_formula
                                                if string_role_dept_in_list not in  list_checks_role_dept:
                                                    # list_checks_role_dept.append(string_role_dept_in_list)
                                                    list_account = []                                        
                                                    role_id_get_oneid = upper_line_role[yu]['id']
                                                    role_name_get_oneid = upper_line_role[yu]['role_name']
                                                    json_info = {
                                                        "tax_id": tax_id,
                                                        "dept_id" : dept_id,
                                                        "role_id" : role_id_get_oneid
                                                    }
                                                    result_CallAPI_01 = CallAPI_POST_oneid(one_url + '/api/get_all_account_in_role_in_department',token_header,json_info)
                                                    index_count_sum = index_count_sum + 1
                                                    if result_CallAPI_01['result'] == 'OK':
                                                        if result_CallAPI_01['messageText']['result'] == 'Success':
                                                            data_account = result_CallAPI_01['messageText']['data']
                                                            for ui in range(len(data_account)):
                                                                list_account.append({
                                                                    'index_count':index_count_sum,
                                                                    'account_id':data_account[ui]['account_id'],
                                                                    'first_name_th':data_account[ui]['account__detail'][0]['first_name_th'],
                                                                    'last_name_th':data_account[ui]['account__detail'][0]['last_name_th'],
                                                                    'first_name_eng':data_account[ui]['account__detail'][0]['first_name_eng'],
                                                                    'last_name_eng':data_account[ui]['account__detail'][0]['last_name_eng'],
                                                                    'account_title_th':data_account[ui]['account__detail'][0]['account_title_th'],
                                                                    'account_title_eng':data_account[ui]['account__detail'][0]['account_title_eng'],
                                                                    'thai_email':data_account[ui]['account__detail'][0]['thai_email']
                                                                })
                                                    count_step_num = count_step_num + 1
                                                else:
                                                    list_account = [] 
                                            else:
                                                list_account = []
                                        
                                    if len(list_account) != 0:
                                        list_result.append({
                                            'index_detp_role':index_count_sum,
                                            "role_name":role_name_get_oneid,
                                            "role_id":role_id_get_oneid,
                                            "account_details":list_account,
                                            "dept_id" : dept_id,
                                            "dept_name":dept_name_oneid
                                        })
                        # print(count_step_num , maxstep)
                        if count_step_num < maxstep:
                            
                            list_result_select,maxstep,minstep,dept_id_new_upper_line,count_sum_ = department_get_lineupper_v1_methods(maxstep,count_step_num,tax_id,dept_id,token_header,index_count_sum,'')
                            list_result.append(list_result_select[0])
                            for ii in range(minstep,maxstep):
                                try:
                                    list_result_select_,maxstep,minstep,dept_id_new_upper_line,count_sum_ = department_get_lineupper_v1_methods(maxstep,minstep,tax_id,dept_id_new_upper_line,token_header,count_sum_,'')
                                    list_result.append(list_result_select_[0])
                                except Exception as e:
                                    pass
                        list_to_pop = []
                        check_from_list_role = False
                        if len(role_from_list) != 0:
                            if len(role_from_list) == len(role_to_list):
                                for index_list in range(len(list_result)):
                                    role_name = list_result[index_list]['role_name']
                                    for zu in range(len(role_from_list)):
                                        if role_from_list[zu] == role_name:
                                            list_to_pop.append(index_list)
                                            check_from_list_role = True
                                            index_list_role_from = zu
                                            temp_account_details_from = list_result[index_list]
                                if check_from_list_role:
                                    for index_list_0 in range(len(list_result)):
                                        role_name = list_result[index_list_0]['role_name']
                                        if role_to_list[index_list_role_from] == role_name:                                            
                                            temp_account_details_to = list_result[index_list_0]
                                            account_details_from = temp_account_details_from['account_details']
                                            account_details_to = temp_account_details_to
                                            for u in range(len(account_details_to['account_details'])):
                                                for ii in range(len(account_details_from)):
                                                    account_details_to['account_details'].append(account_details_from[ii])
                                        else:
                                            pass
                                else:
                                    pass
                            else:
                                return jsonify({'result':'ER','messageText':None,'messageER':'role_from_list incorrect and role_to_list incorrect','status_Code':200}),200
                        for uu in range(len(list_to_pop)):
                            list_result.pop(list_to_pop[uu])
                        count_index = 1
                        for oo in range(len(list_result)):
                            list_result[oo]['index_detp_role'] = count_index
                            list_result[oo]['account_details'][0]['index_count'] = count_index
                            count_index = count_index + 1
                        if len(list_result) != 0:
                            return jsonify({'result':'OK','messageText':list_result,'status_Code':200}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'messageER':'data not found','status_Code':200}),200
                    else:
                        return jsonify({'result':'OK','messageText':None,'messageER':'Authorization Fail!','status_Code':401}),401
            except Exception as e:
                return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':'parameter incorrect','status_Code':200}),200

@status_methods.route('/api/v1/admin_get_role', methods=['POST'])
def admin_get_role_v1():
    if request.method == 'POST':
        dataJson = request.json
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
        except KeyError as ex:
            return redirect(url_paperless)
        if 'my_role' in dataJson and 'tax_id' in dataJson and 'secret_key' in dataJson and len(dataJson) == 3:
            my_role = dataJson['my_role']
            tax_id = dataJson['tax_id']
            secret_key = dataJson['secret_key']
            list_result_role = []
            list_department_role = []
            if secret_key == 'itvTW2fzTJ':
                if my_role <= 1:
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
                            # print(list_department_role)
                                    
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
                    return jsonify({'result':'ER','messageText':None,'messageER':'my_role no admin','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':'secret_key incorrect','status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':'parameter incorrect','status_Code':200}),200

@status_methods.route('/api/v1/get_lower_dept_and_role', methods=['POST'])
def get_all_dept_and_role_v1():
    if request.method == 'POST':
        try:
            dataJson = request.json
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        one_access_token = 'Bearer' + token_header
        if 'tax_id' in dataJson and 'account_id' in dataJson and 'dept_id' in dataJson and 'role_id' in dataJson and len(dataJson) == 4:
            taxid = dataJson['tax_id']
            account_id = dataJson['account_id']
            dept_id = dataJson['dept_id']
            myrole_id = dataJson['role_id']
            tmp_result_list_dept = []
            tmp_list_position = []
            result_get_dpt = CallAPI_GET_oneid(one_url+'/api/v1/service/business/department?tax_id=' + taxid,token_header)
            if result_get_dpt['result'] == 'OK':
                msg_get_dpt = result_get_dpt['messageText']
                if msg_get_dpt['result'] == 'Success':
                    msg_one_id_dpt = msg_get_dpt['data']
                    for i in range(len(msg_one_id_dpt)):
                        tmp_result_list_role = []
                        department_info = msg_one_id_dpt[i]['department']
                        parent_dept_id = department_info[0]['parent_dept_id']
                        dept_name = department_info[0]['dept_name']
                        dept_position = department_info[0]['dept_position']
                        dept_id_info = department_info[0]['id']
                        if dept_id_info == dept_id:
                            tmp_result_list_role = []
                            result_get = CallAPI_GET_oneid(one_url+'/api/v1/service/business/department/' + dept_id + '/role?tax_id=' + taxid,token_header)
                            if result_get['result'] == 'OK':
                                mesg_service = result_get['messageText']
                                if mesg_service['result'] == 'Success':
                                    data_oneId = mesg_service['data']
                                    tmp_list_recursive = recursive_find_dept(data_oneId,myrole_id,'role')
                            for u in range(len(data_oneId)):
                                # 
                                role_id = data_oneId[u]['role_id']
                                position_role = data_oneId[u]['dept_role_position']
                                for z in range(len(tmp_list_recursive)):
                                    if position_role == tmp_list_recursive[z]:                                        
                                        if position_role not in tmp_list_position:
                                            tmp_list_position.append(position_role)
                                            role_info = data_oneId[u]['role']
                                            role_info_id = role_info[0]['id']
                                            role_info_name = role_info[0]['role_name']
                                            role_info_level = role_info[0]['role_level']
                                            data_result_role = {}
                                            data_result_role['role_id'] = role_info_id
                                            data_result_role['role_name'] = role_info_name
                                            data_result_role['role_level'] = role_info_level
                                            tmp_result_list_role.append(data_result_role)
                            data_result = {}
                            data_result['dept_id'] = dept_id_info
                            data_result['dept_name'] = dept_name
                            data_result['dept_position'] = dept_position
                            data_result['parent_dept_id'] = parent_dept_id
                            data_result['role'] = tmp_result_list_role
                            tmp_result_list_dept.append(data_result)
                        if parent_dept_id == dept_id:
                            data_result = {}
                            result_get_lower_role = CallAPI_GET_oneid(one_url+'/api/v1/service/business/department/' + dept_id_info + '/role?tax_id=' + taxid,token_header)
                            if result_get_lower_role['result'] == 'OK':
                                mesg_service_lower = result_get_lower_role['messageText']
                                if mesg_service_lower['result'] == 'Success':
                                    data_oneId_lower = mesg_service_lower['data']
                                    for zz in range(len(data_oneId_lower)):
                                        role_info = data_oneId_lower[zz]['role']
                                        role_info_id = role_info[0]['id']
                                        role_info_name = role_info[0]['role_name']
                                        role_info_level = role_info[0]['role_level']
                                        data_result_role = {}
                                        data_result_role['role_id'] = role_info_id
                                        data_result_role['role_name'] = role_info_name
                                        data_result_role['role_level'] = role_info_level
                                        tmp_result_list_role.append(data_result_role)
                                    data_result['dept_id'] = dept_id_info                            
                                    data_result['dept_name'] = dept_name
                                    data_result['dept_position'] = dept_position
                                    data_result['parent_dept_id'] = parent_dept_id
                                    data_result['role'] = tmp_result_list_role
                                    tmp_result_list_dept.append(data_result)
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'service/business/account/ error or token expire'}),401
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'service/business/account/ error or token expire'}),401
                    return jsonify({'result':'OK','messageText':tmp_result_list_dept,'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'service/business/account/ error or token expire'}),401
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'service/business/account/ error or token expire'}),401                
            
@status_methods.route('/api/v1/get_account_in_biz', methods=['POST'])
def department_get_account_in_biz_v1():
    if request.method == 'POST':
        try:
            dataJson = request.json
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
        except KeyError as ex:
            return redirect(url_paperless)
        one_access_token = 'Bearer' + token_header
        if 'tax_id' in dataJson:
            taxid = dataJson['tax_id']
            try:
                tmp_list_account = []        
                result_get = CallAPI_GET_oneid(one_url+'/api/v1/service/business/account?tax_id=' + taxid,token_header)
                if result_get['result'] == 'OK':
                    mesg_get = result_get['messageText']
                    if mesg_get['result'] == 'Success':
                        mesg_resp = mesg_get['data']
                        for i in range(len(mesg_resp)):
                            get_account_detail = mesg_resp[i]['account_detail'][0]
                            tmp_json_account = {}
                            tmp_json_account['account_id'] = get_account_detail['id']
                            tmp_json_account['first_name_th'] = get_account_detail['first_name_th']
                            tmp_json_account['last_name_th'] = get_account_detail['last_name_th']
                            tmp_json_account['first_name_eng'] = get_account_detail['first_name_eng']
                            tmp_json_account['last_name_eng'] = get_account_detail['last_name_eng']
                            tmp_json_account['thai_email'] = get_account_detail['thai_email']
                            tmp_list_account.append(tmp_json_account)
                return jsonify({'result':'OK','messageText':tmp_list_account,'status_Code':200,'messageER':None})
            except Exception as ex:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':str(ex)})
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'})

@status_methods.route('/api/v1/get_role_and_dept', methods=['POST'])
def department_get_lower_account_v1():
    if request.method == 'POST':
        try:
            dataJson = request.json
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
        except KeyError as ex:
            return redirect(url_paperless)
        one_access_token = 'Bearer' + token_header
        if 'tax_id' in dataJson and 'account_id' in dataJson:
            taxid = dataJson['tax_id']
            account_id = dataJson['account_id']
            count_dept = 0
            index_dept = 0
            list_role_res = []
            list_res = []
            result_get = CallAPI_GET_oneid(one_url+'/api/v1/service/business/account/' + account_id + '/department_role?tax_id=' + taxid,token_header)
            if result_get['result'] == 'OK':
                msg_get = result_get['messageText']
                if msg_get['result'] == 'Success':
                    msg_one_id = msg_get['data']
                    print(msg_one_id)
                    for i in range(len(msg_one_id)):
                        json_res = {}
                        role_info = msg_one_id[i]['role'][0]
                        if len(msg_one_id[i]['department']) != 0:
                            department_info = msg_one_id[i]['department'][0]                            
                            json_res['dept_id'] = department_info['id']
                            json_res['dept_name'] = department_info['dept_name']
                            json_res['dept_position'] = department_info['dept_position']                        
                            count_dept += 1
                            list_res.append(json_res)
                        else:
                            list_res = []
                    if 'role' in msg_one_id[0]:
                        json_role = {}
                        json_role['role_id'] = role_info['id']
                        json_role['role_name'] = role_info['role_name']
                        list_role_res.append(json_role)
                    data_result = {
                        "count_dept": count_dept,
                        "dept_detail":list_res
                    }
                    data_role_result = {
                        'role_detail':list_role_res
                    }
                    return jsonify({'result':'OK','messageText':{'account_id':account_id,'department':data_result,'role':data_role_result},'status_Code':200,'messageER':None})
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'service/business/account/ error or token expire'}),401
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'service/business/account/ error or token expire'}),401
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrect'})

def recursive_find_dept(data_oneId,myrole_id,type_rec):
    if type_rec == 'role':
        lower_position_role = []
        count_u = 0
        count_zz = 0
        for i in range(len(data_oneId)):
            role_id = data_oneId[i]['role_id']
            position_role = data_oneId[i]['dept_role_position']
            if role_id == myrole_id:
                myposition_id_info = data_oneId[i]['dept_role_position']
                for u in range(len(data_oneId)):
                    count_u = u + 1
                    lower_position_role.append(myposition_id_info + "." + str(count_u))
            for z in range(len(lower_position_role)):
                tmp_lower_position_role = lower_position_role[z]
                for zz in range(len(data_oneId)):
                    count_zz = zz + 1
                    lower_position_role.append(tmp_lower_position_role + "." + str(count_zz))
        return (lower_position_role)
    elif type_rec == 'dept':
        lower_position_role = []
        count_u = 0
        count_zz = 0
        for i in range(len(data_oneId)):
            dept_id = data_oneId[i]['dept_id']
            position_dept = data_oneId[i]['department'][0]['dept_position']
            # print(position_dept)
            if dept_id == myrole_id:
                myposition_id_info = data_oneId[i]['department'][0]['dept_position']
                for u in range(len(data_oneId)):
                    count_u = u + 1
                    lower_position_role.append(myposition_id_info + "." + str(count_u))
        return (lower_position_role)
            # for z in range(len(lower_position_role)):
            #     tmp_lower_position_role = lower_position_role[z]
            #     for zz in range(5):
            #         count_zz = zz + 1
            #         lower_position_role.append(tmp_lower_position_role + "." + str(count_zz))
            # print(lower_position_role)
        # return (lower_position_role)

@status_methods.route('/api/v1/get_lower_line', methods=['POST'])
def department_get_lower_line_v1():
    if request.method == 'POST':
        try:
            dataJson = request.json
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
        except KeyError as ex:
            return redirect(url_paperless)
        one_access_token = 'Bearer' + token_header
        if 'tax_id' in dataJson and 'account_id' in dataJson and 'role_id' in dataJson and 'dept_id' in dataJson and 'role_name_requirements' in dataJson:
            taxid = dataJson['tax_id']
            accountid = dataJson['account_id']
            myrole_id = dataJson['role_id']
            deptid = dataJson['dept_id']
            role_name_requirements = dataJson['role_name_requirements']
            lower_position_role = []
            lower_position_role_01 = []
            tmp_data_oneId = []
            tmp_data_oneId_dept = []
            tmp_list_recursive = []
            tmp_list_recursive_dept = []
            tmp_position_role = []
            tmp_position_dept = []
            tmp_dept_id = []
            tmp_result_json = []
            count_account = 0
            result_get = CallAPI_GET_oneid(one_url+'/api/v1/service/business/department/' + deptid + '/role?tax_id=' + taxid,token_header)
            if result_get['result'] == 'OK':
                mesg_service = result_get['messageText']
                if mesg_service['result'] == 'Success':
                    data_oneId = mesg_service['data']
                    tmp_list_recursive = recursive_find_dept(data_oneId,myrole_id,'role')
                    for i in range(len(data_oneId)):
                        role_id = data_oneId[i]['role_id']
                        position_role = data_oneId[i]['dept_role_position']
                        if role_id == myrole_id:                            
                            myposition_id_info = data_oneId[i]['dept_role_position']
                        for z in range(len(tmp_list_recursive)):
                            if position_role == tmp_list_recursive[z]:
                                if position_role not in tmp_position_role:
                                    tmp_position_role.append(position_role)
                                    tmp_data_oneId.append(data_oneId[i])
                    result_get_00 = CallAPI_GET_oneid(one_url+'/api/v1/service/business/department?tax_id=' + taxid,token_header)
                    if result_get_00['result'] == 'OK':
                        mesg_service = result_get_00['messageText']
                        if mesg_service['result'] == 'Success':
                            data_oneId_01 = mesg_service['data']
                            for i in range(len(data_oneId_01)):
                                dept_id = data_oneId_01[i]['dept_id']
                                parent_dept_id = data_oneId_01[i]['department'][0]['parent_dept_id']
                                if parent_dept_id == deptid:
                                    tmp_dept_id.append(dept_id)
                    if len(tmp_dept_id) == 0:
                        for u in range(len(tmp_data_oneId)):
                            dept_id_info = tmp_data_oneId[u]['dept_id']
                            role_id_info = tmp_data_oneId[u]['role_id']
                            role_name_info = tmp_data_oneId[u]['role'][0]['role_name']
                            if role_name_requirements != '':
                                if role_name_info == role_name_requirements:
                                    result_get_01 = CallAPI_GET_oneid(one_url+'/api/v1/service/business/department/' +dept_id_info +'/role/' + role_id_info+'/account?tax_id=' + taxid,token_header)
                                    if result_get_01['result'] == 'OK':
                                        mesg_service = result_get_01['messageText']
                                        if mesg_service['result'] == 'Success':
                                            data_oneId_01 = mesg_service['data']
                                            for index_u in range(len(data_oneId_01)):
                                                count_account =count_account + 1
                                                data_result_json = {}
                                                data_result_json['account_id'] = data_oneId_01[index_u]['account_id']
                                                data_result_json['first_name_th'] = data_oneId_01[index_u]['account_detail'][0]['first_name_th']
                                                data_result_json['last_name_th'] = data_oneId_01[index_u]['account_detail'][0]['last_name_th']
                                                data_result_json['first_name_eng'] = data_oneId_01[index_u]['account_detail'][0]['first_name_eng']
                                                data_result_json['last_name_eng'] = data_oneId_01[index_u]['account_detail'][0]['last_name_eng']
                                                data_result_json['account_title_th'] = data_oneId_01[index_u]['account_detail'][0]['account_title_th']
                                                data_result_json['account_title_eng'] = data_oneId_01[index_u]['account_detail'][0]['account_title_eng']
                                                data_result_json['thai_email'] = data_oneId_01[index_u]['account_detail'][0]['thai_email']
                                                tmp_result_json.append(data_result_json)
                            else:
                                result_get_01 = CallAPI_GET_oneid(one_url+'/api/v1/service/business/department/' +dept_id_info +'/role/' + role_id_info+'/account?tax_id=' + taxid,token_header)
                                if result_get_01['result'] == 'OK':
                                    mesg_service = result_get_01['messageText']
                                    if mesg_service['result'] == 'Success':
                                        data_oneId_01 = mesg_service['data']
                                        for index_u in range(len(data_oneId_01)):
                                            count_account =count_account + 1
                                            data_result_json = {}
                                            data_result_json['account_id'] = data_oneId_01[index_u]['account_id']
                                            data_result_json['first_name_th'] = data_oneId_01[index_u]['account_detail'][0]['first_name_th']
                                            data_result_json['last_name_th'] = data_oneId_01[index_u]['account_detail'][0]['last_name_th']
                                            data_result_json['first_name_eng'] = data_oneId_01[index_u]['account_detail'][0]['first_name_eng']
                                            data_result_json['last_name_eng'] = data_oneId_01[index_u]['account_detail'][0]['last_name_eng']
                                            data_result_json['account_title_th'] = data_oneId_01[index_u]['account_detail'][0]['account_title_th']
                                            data_result_json['account_title_eng'] = data_oneId_01[index_u]['account_detail'][0]['account_title_eng']
                                            data_result_json['thai_email'] = data_oneId_01[index_u]['account_detail'][0]['thai_email']
                                            tmp_result_json.append(data_result_json)
                        return jsonify({'result':'OK','messageText':[{'account_detail':tmp_result_json,'account_sum':count_account}],'status_Code':200,'messageER':None}),200
                    else:
                        tmp_result_json = []
                        for kk in range(len(tmp_dept_id)):
                            result_get = CallAPI_GET_oneid(one_url+'/api/v1/service/business/department/' + tmp_dept_id[kk] + '/role?tax_id=' + taxid,token_header)
                            if result_get['result'] == 'OK':
                                mesg_service = result_get['messageText']
                                if mesg_service['result'] == 'Success':
                                    data_oneId = mesg_service['data']
                                    tmp_list_recursive = recursive_find_dept(data_oneId,myrole_id,'role')
                                    for i in range(len(data_oneId)):
                                        role_id = data_oneId[i]['role_id']
                                        position_role = data_oneId[i]['dept_role_position']
                                        if role_id == myrole_id:                            
                                            myposition_id_info = data_oneId[i]['dept_role_position']
                                        for z in range(len(tmp_list_recursive)):
                                            if position_role == tmp_list_recursive[z]:
                                                if position_role not in tmp_position_role:
                                                    tmp_position_role.append(position_role)
                                                    tmp_data_oneId.append(data_oneId[i])
                                    for u in range(len(tmp_data_oneId)):
                                        dept_id_info = tmp_data_oneId[u]['dept_id']
                                        role_id_info = tmp_data_oneId[u]['role_id']
                                        role_name_info = tmp_data_oneId[u]['role'][0]['role_name']
                                        print(tmp_data_oneId[u])
                                        if role_name_info == role_name_requirements:
                                            result_get_01 = CallAPI_GET_oneid(one_url+'/api/v1/service/business/department/' +tmp_dept_id[kk] +'/role/' + role_id_info+'/account?tax_id=' + taxid,token_header)
                                            if result_get_01['result'] == 'OK':
                                                mesg_service = result_get_01['messageText']
                                                if mesg_service['result'] == 'Success':
                                                    data_oneId_01 = mesg_service['data']
                                                    for index_u in range(len(data_oneId_01)):
                                                        count_account =count_account + 1
                                                        data_result_json = {}
                                                        data_result_json['account_id'] = data_oneId_01[index_u]['account_id']
                                                        data_result_json['first_name_th'] = data_oneId_01[index_u]['account_detail'][0]['first_name_th']
                                                        data_result_json['last_name_th'] = data_oneId_01[index_u]['account_detail'][0]['last_name_th']
                                                        data_result_json['first_name_eng'] = data_oneId_01[index_u]['account_detail'][0]['first_name_eng']
                                                        data_result_json['last_name_eng'] = data_oneId_01[index_u]['account_detail'][0]['last_name_eng']
                                                        data_result_json['account_title_th'] = data_oneId_01[index_u]['account_detail'][0]['account_title_th']
                                                        data_result_json['account_title_eng'] = data_oneId_01[index_u]['account_detail'][0]['account_title_eng']
                                                        data_result_json['thai_email'] = data_oneId_01[index_u]['account_detail'][0]['thai_email']
                                                        tmp_result_json.append(data_result_json)
                        return jsonify({'result':'OK','messageText':[{'account_detail':tmp_result_json,'account_sum':count_account}],'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'/api/v1/service/business/department/ service error or token expire'})
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'service error'})
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrct'})

@status_methods.route('/api/v1/get_lower_line_account', methods=['POST'])
def get_lower_line_account_v1():
    if request.method == 'POST':
        try:
            dataJson = request.json
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
        except KeyError as ex:
            return redirect(url_paperless)
        one_access_token = 'Bearer' + token_header
        if 'tax_id' in dataJson and 'account_id' in dataJson and 'role_id_requirements' in dataJson and 'dept_id' in dataJson and 'role_name_requirements' in dataJson:
            tmp_result_json=[]
            dept_id_info = dataJson['dept_id']
            role_id_info = dataJson['role_id_requirements']
            taxid = dataJson['tax_id']
            tmp_list_email = []
            result_get_01 = CallAPI_GET_oneid(one_url+'/api/v1/service/business/department/' +dept_id_info +'/role/' + role_id_info+'/account?tax_id=' + taxid,token_header)
            if result_get_01['result'] == 'OK':
                mesg_service = result_get_01['messageText']
                if mesg_service['result'] == 'Success':
                    data_oneId_01 = mesg_service['data']
                    count_account = 0
                    for index_u in range(len(data_oneId_01)):
                        count_account =count_account + 1
                        data_result_json = {}
                        data_result_json['account_id'] = data_oneId_01[index_u]['account_id']
                        data_result_json['first_name_th'] = data_oneId_01[index_u]['account_detail'][0]['first_name_th']
                        data_result_json['last_name_th'] = data_oneId_01[index_u]['account_detail'][0]['last_name_th']
                        data_result_json['first_name_eng'] = data_oneId_01[index_u]['account_detail'][0]['first_name_eng']
                        data_result_json['last_name_eng'] = data_oneId_01[index_u]['account_detail'][0]['last_name_eng']
                        data_result_json['account_title_th'] = data_oneId_01[index_u]['account_detail'][0]['account_title_th']
                        data_result_json['account_title_eng'] = data_oneId_01[index_u]['account_detail'][0]['account_title_eng']
                        data_result_json['thai_email'] = data_oneId_01[index_u]['account_detail'][0]['thai_email']
                        tmp_list_email.append(data_oneId_01[index_u]['account_detail'][0]['thai_email'])
                        tmp_result_json.append(data_result_json)
                    return jsonify({'result':'OK','messageText':[{'account_detail':tmp_result_json,'account_sum':count_account,'email_thai_list':tmp_list_email}],'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'service/business/department/ error or token expire'}),401
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':'service/business/department/ error or token expire'}),401
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrct'})

@status_methods.route('/api/v1/get_document_lower', methods=['POST'])
@token_required
def get_document_lower_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'email_thai_list' in dataJson and 'document_type' in dataJson and 'start_datetime' in dataJson and 'end_datetime' in dataJson and len(dataJson) == 4:
            email_thai_list = dataJson['email_thai_list']
            document_type = dataJson['document_type']
            start_datetime = dataJson['start_datetime']
            end_datetime = dataJson['end_datetime']
            result_select =select().select_get_document_lower_v1(email_thai_list,document_type,start_datetime,end_datetime)
            if result_select['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_select['messageER']}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter incorrct'})

# 05062563
@status_methods.route('/api/v1/getAll_department', methods=['GET'])
@token_required_v3
def get_department_all_api_v1():
    if 'Authorization' not in request.headers:
        abort(401)    
    try:
        token_header = request.headers['Authorization']
        try:                
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            abort(401)
    except KeyError as ex:
        return redirect(url_paperless)
    tax_id = request.args.get('tax_id')
    if tax_id == None:
        abort(404)
    url = one_url + '/api/v2/service/business/department?tax_id=' + tax_id
    token_header = "Bearer " + token_header
    try:
        response = callAuth_get(url,token_header)
        if response['status'] == 'success':
            messageTmp = response['response']
            messageTmp = messageTmp.json()
            if messageTmp['result'] == 'Success':
                messageData = messageTmp['data']
                return jsonify({'status':'success','message':None,'data':messageData}),200
            else:
                return jsonify({'status':'fail','message':None,'data':[]}),200
        else:
            return jsonify({'status':'fail','message':None,'data':[]}),200
    except Exception as e:
        return jsonify({'status':'fail','message':str(e),'data':None}),200

    