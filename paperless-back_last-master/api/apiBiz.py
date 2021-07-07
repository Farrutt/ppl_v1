#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from controller.mail_string import *
from controller.validate import *
from db.db_method import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from method.cal_file import *

if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
def check_email(email):
    if(re.search(regex,email)):
        print("Valid Email")
        return True
    else:
        print("Invalid Email")
        return False

def callAPIOneid_post(path, data,auth_token):
    url = path
    payload = data
    try:
        time_duration = ''
        response = requests.request("POST",headers={'Authorization': auth_token}, url=url, json=payload, verify=False, stream=True)
        tmp_one_access_token = str(auth_token).split(' ')[1]
        time_duration = find_timeduration(response.elapsed.total_seconds())
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload), url,tmp_one_access_token,time_duration)
            return {'result': 'OK','messageText': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload), url,tmp_one_access_token,time_duration)
            return {'result': 'ER','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload), url,tmp_one_access_token,time_duration)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload), url,tmp_one_access_token,time_duration)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload), url,tmp_one_access_token,time_duration)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as ex:
        insert().insert_tran_log_v1(str(err),'ER',str(payload), url,tmp_one_access_token,time_duration)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(ex)}

def callAPI_OneId(token,method,path,payload):
    try:
        time_duration = ''
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer"+" "+token
        }
        if method == "POST":
            response = requests.request("POST", url=path, headers=headers, json=payload, verify=False)
            time_duration = find_timeduration(response.elapsed.total_seconds())
            if response.status_code == 200 or response.status_code == 201:
                insert().insert_tran_log_v1(str(response.json()),'OK',str(payload), path,token,time_duration)
            else:
                insert().insert_tran_log_v1(str(response.text),'ER',str(payload), path,token,time_duration)
        if method == "GET":
            response = requests.get(path, headers=headers, verify=False)
            time_duration = find_timeduration(response.elapsed.total_seconds())
            if response.status_code == 200 or response.status_code == 201:
                insert().insert_tran_log_v1(str(response.json()),'OK',str(payload), path,token,time_duration)
            else:
                insert().insert_tran_log_v1(str(response.text),'ER',str(payload), path,token,time_duration)
        return response
    except Exception as ex:
        return  jsonify({'result':'ER','messageText':ex})

def update_insert_bizprofile(tax_id,biz_info,token_header):
    print('update')
    tax_id = tax_id
    biz_info = biz_info
    token_header = token_header
    status_shraed = True
    try:
        biz_info = biz_info
        for i in range(len(biz_info)):
            taxId = tax_id            
            getBizinfo_base = select().select_BizProfile(taxId)
            path_Url = one_url + '/api/get_business_account_role/' + taxId
            if getBizinfo_base['result'] == 'OK':
                getRole = callAPI_OneId(token_header,"GET",path_Url,"")
                getRole = getRole.json()
                if getRole['result'] == 'Success':
                    update().update_BizProfile(taxId,biz_info[i],getRole['data'])
                else:
                    if status_shraed == False:
                        return jsonify({'status':'fail','message':'Authorization Fail!','data':None}),200
                    else:
                        pass
            else:
                getRole = callAPI_OneId(token_header,"GET",path_Url,"")
                getRole = getRole.json()
                print(getRole)
                if getRole['result'] == 'Success':
                    insert().insert_BizProfile(taxId,biz_info[i],getRole['data'])
                else:
                    if status_shraed == False:
                        return jsonify({'status':'fail','message':'Authorization Fail!','data':None}),200
                    else:
                        pass
    except Exception as ex:
        print(str(ex))
        return {'result':'ER','messageText':str(ex)}

@status_methods.route('/api/getbiz/v1',methods=['GET'])
@token_required
def getBiz_info_api():
    if request.method == 'GET':
        if (request.args.get('user')) != None:
            user_id = str(request.args.get('user')).replace(' ','')
            res_selectUserBiz = select().select_UserBiz(user_id)
            if res_selectUserBiz['result'] == 'OK':
                return jsonify(res_selectUserBiz),200
            else:
                return jsonify(res_selectUserBiz),200
        else:
            return jsonify({'result':'ER','messageText':'parameter incorrect!','status_Code':404}),404

@status_methods.route('/api/getbiz/v2',methods=['GET'])
def getBiz_info_api_v2():
    if request.method == 'GET':
        token_header = request.headers['Authorization']
        try:
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
        url = one_url + "/api/account_and_biz_detail"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer"+" "+token_header
        }
        try:
            response = requests.get(url, headers=headers, verify=False)
            response = response.json()
        except requests.Timeout as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except requests.HTTPError as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except requests.ConnectionError as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except requests.RequestException as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401
        except Exception as ex:
            return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401,'service':'oneid'}),401

        if 'result' in response:
            if response['result'] == 'Fail':
                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
        else:
            biz_info = []
            username_Resp = response['username']
            if (request.args.get('username')) != None:
                username = str(request.args.get('username')).replace(' ','')
                # False = user
                #  True = email
                if check_email(username):
                    email_User = response['thai_email']
                    if email_User == username:
                        if 'biz_detail' in response:
                            getbiz = response['biz_detail']

                            for i in range(len(getbiz)):
                                jsonData = {
                                    'id':getbiz[i]['getbiz'][0]['id'],
                                    'first_name_th':getbiz[i]['getbiz'][0]['first_name_th'],
                                    'first_name_eng':getbiz[i]['getbiz'][0]['first_name_eng'],
                                    'id_card_type':getbiz[i]['getbiz'][0]['id_card_type'],
                                    'id_card_num':getbiz[i]['getbiz'][0]['id_card_num'],
                                    'role_level':getbiz[i]['getrole'][0]['role_level'],
                                    'role_name':getbiz[i]['getrole'][0]['role_name']
                                }
                                biz_info.append(jsonData)
                        for i in range(len(biz_info)):
                            taxId = biz_info[i]['id_card_num']
                            getBizinfo_base = select().select_BizProfile(biz_info[i]['id_card_num'])
                            path_Url = one_url + '/api/get_business_account_role/' + biz_info[i]['id_card_num']
                            if getBizinfo_base['result'] == 'OK':
                                getRole = callAPI_OneId(token_header,"GET",path_Url,"")
                                getRole = getRole.json()
                                if getRole['result'] == 'Success':
                                    update().update_BizProfile(taxId,biz_info[i],getRole['data'])
                                else:
                                    return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
                            else:
                                getRole = callAPI_OneId(token_header,"GET",path_Url,"")
                                getRole = getRole.json()
                                if getRole['result'] == 'Success':
                                    insert().insert_BizProfile(taxId,biz_info[i],getRole['data'])
                                else:
                                    return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
                        return jsonify({'result':'OK','messageText':biz_info,'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
                else:
                    pass
                if username_Resp == username:
                    if 'biz_detail' in response:
                        getbiz = response['biz_detail']

                        for i in range(len(getbiz)):
                            jsonData = {
                                'id':getbiz[i]['getbiz'][0]['id'],
                                'first_name_th':getbiz[i]['getbiz'][0]['first_name_th'],
                                'first_name_eng':getbiz[i]['getbiz'][0]['first_name_eng'],
                                'id_card_type':getbiz[i]['getbiz'][0]['id_card_type'],
                                'id_card_num':getbiz[i]['getbiz'][0]['id_card_num'],
                                'role_level':getbiz[i]['getrole'][0]['role_level'],
                                'role_name':getbiz[i]['getrole'][0]['role_name']
                            }
                            biz_info.append(jsonData)
                    for i in range(len(biz_info)):
                        taxId = biz_info[i]['id_card_num']
                        getBizinfo_base = select().select_BizProfile(biz_info[i]['id_card_num'])
                        path_Url = one_url + '/api/get_business_account_role/' + biz_info[i]['id_card_num']
                        if getBizinfo_base['result'] == 'OK':
                            getRole = callAPI_OneId(token_header,"GET",path_Url,"")
                            getRole = getRole.json()
                            if getRole['result'] == 'Success':
                                update().update_BizProfile(taxId,biz_info[i],getRole['data'])
                            else:
                                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
                        else:
                            getRole = callAPI_OneId(token_header,"GET",path_Url,"")
                            getRole = getRole.json()
                            if getRole['result'] == 'Success':
                                insert().insert_BizProfile(taxId,biz_info[i],getRole['data'])
                            else:
                                return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
                    return jsonify({'result':'OK','messageText':biz_info,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401

@status_methods.route('/api/v3/getbiz_info_details',methods=['GET'])
def getBiz_info_api_v3():
    if request.method == 'GET':
        token_header = request.headers['Authorization']
        try:
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
        url = one_url + "/api/account_and_biz_detail"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer"+" "+token_header
        }
        try:
            time_duration = ''
            response = requests.get(url, headers=headers, verify=False)
            time_duration = find_timeduration(response.elapsed.total_seconds())
            if response.status_code == 200 or response.status_code == 201:                
                response = response.json()
                insert().insert_tran_log_v1(str(response),'OK',str(''), url,token_header,time_duration)
            else:
                insert().insert_tran_log_v1(str(response),'ER',str(''), url,token_header,time_duration)
                response = response.json()
        except requests.Timeout as ex:
            abort(401)
        except requests.HTTPError as ex:
            abort(401)
        except requests.ConnectionError as ex:
            abort(401)
        except requests.RequestException as ex:
            abort(401)
        except Exception as ex:
            abort(401)
        status_shraed = False
        result_data = token_required_func(token_header)
        if result_data['result'] == 'OK':
            tmpemail = result_data['email']
            tmpusername = result_data['username']
            tmpemail = result_data['email']
            tmpuser_id = result_data['user_id']
            tmpcitizen = result_data['citizen_data']
            if 'result' in response:
                del response['result']
            response = eval(tmpcitizen)
            response['username'] = tmpusername
            status_shraed = True
        if 'result' in response:
            if response['result'] == 'Fail':
                abort(401)
        else:
            biz_info = []
            username_Resp = response['username']
            if (request.args.get('username')) != None:
                username = str(request.args.get('username')).replace(' ','')
                if check_email(username):
                    email_User = response['thai_email']
                    if email_User == username:
                        if 'biz_detail' in response:
                            getbiz = response['biz_detail']
                            for i in range(len(getbiz)):
                                result_Select_Check_biz = select().select_checkBizPaperless(getbiz['biz_detail'][i]['getbiz'][0]['id_card_num'])
                                if result_Select_Check_biz['result'] == 'OK':
                                    if getbiz['biz_detail'][i]['getbiz'][0]['id_card_num'] not in check_biz_id:
                                        check_biz_id.append(getbiz['biz_detail'][i]['getbiz'][0]['id_card_num'])
                                        data_get_my_dep = {
                                            "tax_id": getbiz['biz_detail'][i]['getbiz'][0]['id_card_num']
                                        }
                                        data_get_my_dep = {
                                            "tax_id": getbiz[i]['getbiz'][0]['id_card_num']
                                        }
                                        text_one_access = 'Bearer ' + token_header
                                        resultCallAuth_get_dep = callAPIOneid_post(one_url+'/api/get_my_department_role',data_get_my_dep,text_one_access)
                                        dep_id_list = []
                                        dept_name_list = []
                                        position_list = []
                                        if resultCallAuth_get_dep['result'] == 'OK':
                                            res_json = resultCallAuth_get_dep['messageText'].json()
                                            if res_json['data'] != None:
                                                data_res = res_json['data']
                                                if data_res != '':
                                                    for y in range(len(data_res)):
                                                        dep_id = (data_res[y]['dept_id'])
                                                        if dep_id != '' and dep_id != None:
                                                            dep_id_list.append(dep_id)
                                                            dep_data = data_res[y]['department']
                                                            for iy in range(len(dep_data)):
                                                                dept_name_list.append(dep_data[iy]['dept_name'])
                                                                try:
                                                                    position_list.append(dep_data[iy]['dept_position'])
                                                                except Exception as e:
                                                                    position_list.append('')
                                                        else:
                                                            dep_id_list = []
                                                            dep_data = None
                                                            dept_name_list = []
                                                            position_list = []
                                                else:
                                                    dep_id_list = []
                                                    dep_data = None
                                                    dept_name_list = []
                                                    position_list = []
                                        jsonData = {
                                            'id':getbiz[i]['getbiz'][0]['id'],
                                            'first_name_th':getbiz[i]['getbiz'][0]['first_name_th'],
                                            'first_name_eng':getbiz[i]['getbiz'][0]['first_name_eng'],
                                            'id_card_type':getbiz[i]['getbiz'][0]['id_card_type'],
                                            'id_card_num':getbiz[i]['getbiz'][0]['id_card_num'],
                                            'role_level':getbiz[i]['getrole'][0]['role_level'],
                                            'role_id':getbiz[i]['getrole'][0]['id'],
                                            'role_name':getbiz[i]['getrole'][0]['role_name'],
                                            'dept_id':dep_id_list,
                                            'dept_name':dept_name_list,
                                            'dept_position':position_list,
                                            'data_details_biz':result_Select_Check_biz['messageText']
                                        }
                                        biz_info.append(jsonData)
                        for i in range(len(biz_info)):
                            taxId = biz_info[i]['id_card_num']
                            getBizinfo_base = select().select_BizProfile(biz_info[i]['id_card_num'])
                            path_Url = one_url + '/api/get_business_account_role/' + biz_info[i]['id_card_num']
                            if getBizinfo_base['result'] == 'OK':
                                getRole = callAPI_OneId(token_header,"GET",path_Url,"")
                                getRole = getRole.json()
                                if getRole['result'] == 'Success':
                                    update().update_BizProfile(taxId,biz_info[i],getRole['data'])
                                else:
                                    return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
                            else:
                                getRole = callAPI_OneId(token_header,"GET",path_Url,"")
                                getRole = getRole.json()
                                if getRole['result'] == 'Success':
                                    insert().insert_BizProfile(taxId,biz_info[i],getRole['data'])
                                else:
                                    return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
                        return jsonify({'result':'OK','messageText':biz_info,'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
                else:
                    pass
                if username_Resp == username:
                    if 'biz_detail' in response:
                        getbiz = response['biz_detail']
                        check_biz_id = []
                        for i in range(len(getbiz)): 
                            result_Select_Check_biz = select().select_checkBizPaperless(getbiz[i]['getbiz'][0]['id_card_num'])
                            if result_Select_Check_biz['result'] == 'OK':
                                if getbiz[i]['getbiz'][0]['id_card_num'] not in check_biz_id:
                                    check_biz_id.append(getbiz[i]['getbiz'][0]['id_card_num'])
                                    data_get_my_dep = {
                                        "tax_id": getbiz[i]['getbiz'][0]['id_card_num']
                                    }               
                                    text_one_access = 'Bearer ' + token_header
                                    resultCallAuth_get_dep = callAPIOneid_post(one_url+'/api/get_my_department_role',data_get_my_dep,text_one_access)
                                    dep_id_list = []
                                    tmp_role_id_list = []
                                    dept_name_list = []
                                    position_list = []
                                    list_role_level = []
                                    low_role_id = []
                                    low_role_name = []
                                    dep_data = None
                                    if resultCallAuth_get_dep['result'] == 'OK':
                                        res_json = resultCallAuth_get_dep['messageText'].json()
                                        if res_json['data'] != None:
                                            data_res = res_json['data']                                            
                                            if data_res != '':
                                                for y in range(len(data_res)):
                                                    dep_id = (data_res[y]['dept_id'])
                                                    tmp_role_id = (data_res[y]['role_id'])
                                                    tmp_role_detail = data_res[y]['role'][0]
                                                    tmp_role_level = tmp_role_detail['role_level']
                                                    tmp_role_name = tmp_role_detail['role_name']
                                                    if dep_id != '' and dep_id != None:
                                                        dep_id_list.append(dep_id)
                                                        dep_data = data_res[y]['department']
                                                        for iy in range(len(dep_data)):
                                                            dept_name_list.append(dep_data[iy]['dept_name'])
                                                            try:
                                                                position_list.append(dep_data[iy]['dept_position'])
                                                            except Exception as e:
                                                                position_list.append('')
                                                    if tmp_role_id != '' and tmp_role_id != None:
                                                        tmp_role_id_list.append(tmp_role_id)
                                                        low_role_id.append(tmp_role_level)
                                                        low_role_name.append(tmp_role_name)
                                    jsonData = {
                                        'id':getbiz[i]['getbiz'][0]['id'],
                                        'first_name_th':getbiz[i]['getbiz'][0]['first_name_th'],
                                        'first_name_eng':getbiz[i]['getbiz'][0]['first_name_eng'],
                                        'id_card_type':getbiz[i]['getbiz'][0]['id_card_type'],
                                        'id_card_num':getbiz[i]['getbiz'][0]['id_card_num'],
                                        'role_level':getbiz[i]['getrole'][0]['role_level'],
                                        'role_id':getbiz[i]['getrole'][0]['id'],
                                        'role_name':getbiz[i]['getrole'][0]['role_name'],
                                        'role_id_detail':tmp_role_id_list,
                                        'role_level_detail':low_role_id,
                                        'role_name_detail':low_role_name,
                                        'dept_id':dep_id_list,
                                        'dept_name':dept_name_list,
                                        'dept_position':position_list,
                                        'data_details_biz':result_Select_Check_biz['messageText']
                                    }
                                    biz_info.append(jsonData)
                    for i in range(len(biz_info)):
                        print(biz_info[i]['id_card_num'])
                        taxId = biz_info[i]['id_card_num']
                        getBizinfo_base = select().select_BizProfile(biz_info[i]['id_card_num'])
                        path_Url = one_url + '/api/get_business_account_role/' + biz_info[i]['id_card_num']
                        if getBizinfo_base['result'] == 'OK':
                            getRole = callAPI_OneId(token_header,"GET",path_Url,"")
                            getRole = getRole.json()
                            if getRole['result'] == 'Success':
                                update().update_BizProfile(taxId,biz_info[i],getRole['data'])
                            else:
                                if status_shraed == False:
                                    return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
                                else:
                                    pass
                        else:
                            getRole = callAPI_OneId(token_header,"GET",path_Url,"")
                            getRole = getRole.json()
                            if getRole['result'] == 'Success':
                                insert().insert_BizProfile(taxId,biz_info[i],getRole['data'])
                            else:
                                if status_shraed == False:
                                    return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
                                else:
                                    pass
                    return jsonify({'result':'OK','messageText':biz_info,'status_Code':200}),200
                else:
                    abort(401)
            else:
                abort(404)

@status_methods.route('/api/v4/getbiz_info_details',methods=['GET'])
def getBiz_info_api_v4():
    if request.method == 'GET':
        token_header = request.headers['Authorization']
        try:
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            abort(401)
        url = one_url + "/api/account_and_biz_detail"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer"+" "+token_header
        }
        try:
            time_duration = ''
            response = requests.get(url, headers=headers, verify=False)
            time_duration = find_timeduration(response.elapsed.total_seconds())
            if response.status_code == 200 or response.status_code == 201:                
                response = response.json()
                insert().insert_tran_log_v1(str(response),'OK',str(''), url,token_header,time_duration)
            else:
                insert().insert_tran_log_v1(str(response),'ER',str(''), url,token_header,time_duration)
                response = response.json()
        except requests.Timeout as ex:
            abort(401)
        except requests.HTTPError as ex:
            abort(401)
        except requests.ConnectionError as ex:
            abort(401)
        except requests.RequestException as ex:
            abort(401)
        except Exception as ex:
            abort(401)
        # return ''
        if 'result' in response:
            if response['result'] == 'Fail':
                abort(401)
        else:
            biz_info = []
            username_Resp = response['username']
            if (request.args.get('username')) != None:
                username = str(request.args.get('username')).replace(' ','')
                if check_email(username):
                    email_User = response['thai_email']
                    if email_User == username:
                        if 'biz_detail' in response:
                            getbiz = response['biz_detail']
                            for i in range(len(getbiz)):
                                result_Select_Check_biz = select().select_checkBizPaperless(getbiz['biz_detail'][i]['getbiz'][0]['id_card_num'])
                                if result_Select_Check_biz['result'] == 'OK':
                                    if getbiz['biz_detail'][i]['getbiz'][0]['id_card_num'] not in check_biz_id:
                                        check_biz_id.append(getbiz['biz_detail'][i]['getbiz'][0]['id_card_num'])
                                        data_get_my_dep = {
                                            "tax_id": getbiz['biz_detail'][i]['getbiz'][0]['id_card_num']
                                        }
                                        data_get_my_dep = {
                                            "tax_id": getbiz[i]['getbiz'][0]['id_card_num']
                                        }
                                        text_one_access = 'Bearer ' + token_header
                                        resultCallAuth_get_dep = callAPIOneid_post(one_url+'/api/get_my_department_role',data_get_my_dep,text_one_access)
                                        dep_id_list = []
                                        dept_name_list = []
                                        position_list = []
                                        if resultCallAuth_get_dep['result'] == 'OK':
                                            res_json = resultCallAuth_get_dep['messageText'].json()
                                            if res_json['data'] != None:
                                                data_res = res_json['data']
                                                
                                                
                                                if data_res != '':
                                                    for y in range(len(data_res)):
                                                        dep_id = (data_res[y]['dept_id'])
                                                        if dep_id != '' and dep_id != None:
                                                            dep_id_list.append(dep_id)
                                                            dep_data = data_res[y]['department']
                                                            for iy in range(len(dep_data)):
                                                                dept_name_list.append(dep_data[iy]['dept_name'])
                                                                try:
                                                                    position_list.append(dep_data[iy]['dept_position'])
                                                                except Exception as e:
                                                                    position_list.append('')
                                                        else:
                                                            dep_id_list = []
                                                            dep_data = None
                                                            dept_name_list = []
                                                            position_list = []
                                                else:
                                                    dep_id_list = []
                                                    dep_data = None
                                                    dept_name_list = []
                                                    position_list = []
                                        jsonData = {
                                            'id':getbiz[i]['getbiz'][0]['id'],
                                            'first_name_th':getbiz[i]['getbiz'][0]['first_name_th'],
                                            'first_name_eng':getbiz[i]['getbiz'][0]['first_name_eng'],
                                            'id_card_type':getbiz[i]['getbiz'][0]['id_card_type'],
                                            'id_card_num':getbiz[i]['getbiz'][0]['id_card_num'],
                                            'role_level':getbiz[i]['getrole'][0]['role_level'],
                                            'role_id':getbiz[i]['getrole'][0]['id'],
                                            'role_name':getbiz[i]['getrole'][0]['role_name'],
                                            'dept_id':dep_id_list,
                                            'dept_name':dept_name_list,
                                            'dept_position':position_list,
                                            'data_details_biz':result_Select_Check_biz['messageText']
                                        }
                                        biz_info.append(jsonData)
                        # for i in range(len(biz_info)):
                        #     taxId = biz_info[i]['id_card_num']
                        #     getBizinfo_base = select().select_BizProfile(biz_info[i]['id_card_num'])
                        #     path_Url = one_url + '/api/get_business_account_role/' + biz_info[i]['id_card_num']
                        #     if getBizinfo_base['result'] == 'OK':
                        #         getRole = callAPI_OneId(token_header,"GET",path_Url,"")
                        #         getRole = getRole.json()
                        #         if getRole['result'] == 'Success':
                        #             update().update_BizProfile(taxId,biz_info[i],getRole['data'])
                        #         else:
                        #             return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
                        #     else:
                        #         getRole = callAPI_OneId(token_header,"GET",path_Url,"")
                        #         getRole = getRole.json()
                        #         if getRole['result'] == 'Success':
                        #             insert().insert_BizProfile(taxId,biz_info[i],getRole['data'])
                        #         else:
                        #             return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
                        return jsonify({'result':'OK','messageText':biz_info,'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
                else:
                    pass
                return ''
                if username_Resp == username:
                    if 'biz_detail' in response:
                        getbiz = response['biz_detail']
                        check_biz_id = []
                        for i in range(len(getbiz)): 
                            result_Select_Check_biz = select().select_checkBizPaperless(getbiz[i]['getbiz'][0]['id_card_num'])
                            if result_Select_Check_biz['result'] == 'OK':
                                if getbiz[i]['getbiz'][0]['id_card_num'] not in check_biz_id:
                                    check_biz_id.append(getbiz[i]['getbiz'][0]['id_card_num'])
                                    data_get_my_dep = {
                                        "tax_id": getbiz[i]['getbiz'][0]['id_card_num']
                                    }               
                                    text_one_access = 'Bearer ' + token_header
                                    resultCallAuth_get_dep = callAPIOneid_post(one_url+'/api/get_my_department_role',data_get_my_dep,text_one_access)
                                    dep_id_list = []
                                    tmp_role_id_list = []
                                    dept_name_list = []
                                    position_list = []
                                    list_role_level = []
                                    low_role_id = []
                                    low_role_name = []
                                    dep_data = None
                                    if resultCallAuth_get_dep['result'] == 'OK':
                                        res_json = resultCallAuth_get_dep['messageText'].json()
                                        if res_json['data'] != None:
                                            data_res = res_json['data']                                            
                                            if data_res != '':
                                                for y in range(len(data_res)):
                                                    dep_id = (data_res[y]['dept_id'])
                                                    tmp_role_id = (data_res[y]['role_id'])
                                                    tmp_role_detail = data_res[y]['role'][0]
                                                    tmp_role_level = tmp_role_detail['role_level']
                                                    tmp_role_name = tmp_role_detail['role_name']
                                                    if dep_id != '' and dep_id != None:
                                                        dep_id_list.append(dep_id)
                                                        dep_data = data_res[y]['department']
                                                        for iy in range(len(dep_data)):
                                                            dept_name_list.append(dep_data[iy]['dept_name'])
                                                            try:
                                                                position_list.append(dep_data[iy]['dept_position'])
                                                            except Exception as e:
                                                                position_list.append('')
                                                    if tmp_role_id != '' and tmp_role_id != None:
                                                        tmp_role_id_list.append(tmp_role_id)
                                                        low_role_id.append(tmp_role_level)
                                                        low_role_name.append(tmp_role_name)
                                    jsonData = {
                                        'id':getbiz[i]['getbiz'][0]['id'],
                                        'first_name_th':getbiz[i]['getbiz'][0]['first_name_th'],
                                        'first_name_eng':getbiz[i]['getbiz'][0]['first_name_eng'],
                                        'id_card_type':getbiz[i]['getbiz'][0]['id_card_type'],
                                        'id_card_num':getbiz[i]['getbiz'][0]['id_card_num'],
                                        'role_level':getbiz[i]['getrole'][0]['role_level'],
                                        'role_id':getbiz[i]['getrole'][0]['id'],
                                        'role_name':getbiz[i]['getrole'][0]['role_name'],
                                        'role_id_detail':tmp_role_id_list,
                                        'role_level_detail':low_role_id,
                                        'role_name_detail':low_role_name,
                                        'dept_id':dep_id_list,
                                        'dept_name':dept_name_list,
                                        'dept_position':position_list,
                                        'data_details_biz':result_Select_Check_biz['messageText']
                                    }
                                    biz_info.append(jsonData)
                    # for i in range(len(biz_info)):
                    #     print(biz_info[i]['id_card_num'])
                    #     taxId = biz_info[i]['id_card_num']
                    #     getBizinfo_base = select().select_BizProfile(biz_info[i]['id_card_num'])
                    #     path_Url = one_url + '/api/get_business_account_role/' + biz_info[i]['id_card_num']
                    #     if getBizinfo_base['result'] == 'OK':
                    #         getRole = callAPI_OneId(token_header,"GET",path_Url,"")
                    #         getRole = getRole.json()
                    #         if getRole['result'] == 'Success':
                    #             update().update_BizProfile(taxId,biz_info[i],getRole['data'])
                    #         else:
                    #             return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
                    #     else:
                    #         getRole = callAPI_OneId(token_header,"GET",path_Url,"")
                    #         getRole = getRole.json()
                    #         if getRole['result'] == 'Success':
                    #             insert().insert_BizProfile(taxId,biz_info[i],getRole['data'])
                    #         else:
                    #             return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401
                    return jsonify({'result':'OK','messageText':biz_info,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':'Authorization Fail!','status_Code':401}),401

@status_methods.route('/api/v2/getbiz_info',methods=['GET'])
def getBiz_info_api_v5():
    if request.method == 'GET':
        username = request.args.get('username')
        token_header = request.headers['Authorization']
        try:
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            return jsonify({'result':'ER','messageText':'Bearer Token Error!'})
        url = one_url + "/api/account_and_biz_detail"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer"+" "+token_header
        }
        try:
            time_duration = ''
            response = requests.get(url, headers=headers, verify=False)
            time_duration = find_timeduration(response.elapsed.total_seconds())
            if response.status_code == 200 or response.status_code == 201:                
                response = response.json()
                insert().insert_tran_log_v1(str(response),'OK',str(''), url,token_header,time_duration)
            else:
                insert().insert_tran_log_v1(str(response),'ER',str(''), url,token_header,time_duration)
                response = response.json()
        except requests.Timeout as ex:
            abort(401)
        except requests.HTTPError as ex:
            abort(401)
        except requests.ConnectionError as ex:
            abort(401)
        except requests.RequestException as ex:
            abort(401)
        except Exception as ex:
            abort(401)
        status_shraed = False
        result_data = token_required_func(token_header)
        if result_data['result'] == 'OK':
            tmpemail = result_data['email']
            tmpusername = result_data['username']
            tmpemail = result_data['email']
            tmpuser_id = result_data['user_id']
            tmpcitizen = result_data['citizen_data']
            if 'result' in response:
                del response['result']
            response = eval(tmpcitizen)
            response['username'] = tmpusername
            status_shraed = True
        if 'result' in response:
            if response['result'] == 'Fail':
                abort(401)
        else:
            tmptax_id = []
            biz_info = []
            username_Resp = response['username']
            if username != None:
                username = str(request.args.get('username')).replace(' ','')
                if username_Resp == username:
                    if 'biz_detail' in response:
                        getbiz = response['biz_detail']
                        check_biz_id = []
                        for i in range(len(getbiz)): 
                            if getbiz[i]['getbiz'][0]['id_card_num'] not in tmptax_id:
                                tmp = {}
                                tmp['first_name_th'] = getbiz[i]['getbiz'][0]['first_name_th']
                                tmp['first_name_eng'] = getbiz[i]['getbiz'][0]['first_name_eng']
                                tmp['id_card_num'] = getbiz[i]['getbiz'][0]['id_card_num']
                                tmp['id_card_type'] = getbiz[i]['getbiz'][0]['id_card_type']
                                tmp['id'] = getbiz[i]['getbiz'][0]['id']
                                tmptax_id.append(tmp['id_card_num'])
                                biz_info.append(tmp)    
                    return jsonify({'result':'OK','messageText':biz_info,'status_Code':200}),200
                else:
                    abort(401)
            else:
                abort(404)

@status_methods.route('/api/v1/getbiz_info',methods=['GET'])
@token_required_v3
def getBiz_info_api_newv1():
    if request.method == 'GET':
        tmptax_id = []
        biz_info = []
        username = request.args.get('username')  
        if username != None: 
            username = str(request.args.get('username')).replace(' ','')
            result_db = select_3().select_citizen_login_v1(username)      
            if result_db['result'] == 'OK':  
                data = result_db['messageText'][0]
                username_db = data['username']
                citizen_data = data['citizen_data']                
                if username_db == username:
                    if 'biz_detail' in citizen_data:
                        citizen_data = eval(citizen_data)
                        getbiz = citizen_data['biz_detail']
                        for i in range(len(getbiz)): 
                            if getbiz[i]['getbiz'][0]['id_card_num'] not in tmptax_id:
                                # if select_4().select_status_business_v1(getbiz[i]['getbiz'][0]['id_card_num']):
                                tmp = {}
                                tmp['first_name_th'] = getbiz[i]['getbiz'][0]['first_name_th']
                                tmp['first_name_eng'] = getbiz[i]['getbiz'][0]['first_name_eng']
                                tmp['id_card_num'] = getbiz[i]['getbiz'][0]['id_card_num']
                                tmp['id_card_type'] = getbiz[i]['getbiz'][0]['id_card_type']
                                tmp['id'] = getbiz[i]['getbiz'][0]['id']
                                tmp['business_status'] = select_4().select_status_business_v1(getbiz[i]['getbiz'][0]['id_card_num'])
                                tmptax_id.append(tmp['id_card_num'])
                                biz_info.append(tmp)    
                    return jsonify({'result':'OK','messageText':biz_info,'status_Code':200}),200
                else:
                    abort(401)
            else:
                abort(401)
        else:
            return jsonify({'result':'ER','messageText':'parameter incorrect!','status_Code':404}),404

@status_methods.route('/api/v1/gettransaction_taxid',methods=['GET'])
def gettransaction_taxid():
    result = select_1().select_sum_document_bytaxid('5513213355654')
    if result['result'] == 'OK' :
        return jsonify({'result':'OK','status_Code':200,'messageText':{'data':None,'message':result['messageText']},'messageER':None}),200
    else:
        return jsonify({'result':'ER','status_Code':200,'messageText':{'data':None,'message':'fail'},'messageER':None}),200

@status_methods.route('/api/v2/getbiz_info_details',methods=['GET'])
def getBiz_info_api_v6():
    if request.method == 'GET':
        token_header = request.headers['Authorization']
        try:
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            return jsonify({'status':'fail','message':'Bearer Token Error!','data':None}),200
        url = one_url + "/api/account_and_biz_detail"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer"+" "+token_header
        }
        try:
            time_duration = ''
            response = requests.get(url, headers=headers, verify=False)
            time_duration = find_timeduration(response.elapsed.total_seconds())
            if response.status_code == 200 or response.status_code == 201:                
                response = response.json()
                insert().insert_tran_log_v1(str(response),'OK',str(''), url,token_header,time_duration)
            else:
                insert().insert_tran_log_v1(str(response),'ER',str(''), url,token_header,time_duration)
                response = response.json()
        except requests.Timeout as ex:
            abort(401)
        except requests.HTTPError as ex:
            abort(401)
        except requests.ConnectionError as ex:
            abort(401)
        except requests.RequestException as ex:
            abort(401)
        except Exception as ex:
            abort(401)
        status_shraed = False
        result_data = token_required_func(token_header)
        if result_data['result'] == 'OK':
            tmpemail = result_data['email']
            tmpusername = result_data['username']
            tmpemail = result_data['email']
            tmpuser_id = result_data['user_id']
            tmpcitizen = result_data['citizen_data']
            if 'result' in response:
                del response['result']
            response = eval(tmpcitizen)
            response['username'] = tmpusername
            status_shraed = True
        if 'result' in response:
            if response['result'] == 'Fail':
                abort(401)
        else:
            biz_info = []
            checktax_id = []
            username_Resp = response['username']
            if (request.args.get('username')) != None:
                username = str(request.args.get('username')).replace(' ','')
                tax_id = str(request.args.get('tax_id')).replace(' ','')
                if username_Resp == username:
                    if 'biz_detail' in response:
                        getbiz = response['biz_detail']
                        check_biz_id = []
                        result_Select_Check_biz = select().select_checkBizPaperless_v2(tax_id)
                        if result_Select_Check_biz['result'] == 'OK':
                            if tax_id not in check_biz_id:
                                check_biz_id.append(tax_id)
                                data_get_my_dep = {
                                    "tax_id":tax_id
                                }               
                                text_one_access = 'Bearer ' + token_header
                                resultCallAuth_get_dep = callAPIOneid_post(one_url+'/api/get_my_department_role',data_get_my_dep,text_one_access)
                                dep_id_list = []
                                dept_name_list = []
                                position_list = []
                                list_role_level = []
                                dep_data = None
                                if resultCallAuth_get_dep['result'] == 'OK':
                                    res_json = resultCallAuth_get_dep['messageText'].json()
                                    if res_json['data'] != None:
                                        data_res = res_json['data']                                            
                                        if data_res != '':
                                            for y in range(len(data_res)):
                                                low_role_name = []
                                                low_role_id = []
                                                tmp_role_id_list = []
                                                dep_id = (data_res[y]['dept_id'])
                                                tmp_role_id = (data_res[y]['role_id'])
                                                tmp_role_detail = data_res[y]['role'][0]
                                                tmp_role_level = tmp_role_detail['role_level']
                                                tmp_role_name = tmp_role_detail['role_name']
                                                if dep_id != '' and dep_id != None:
                                                    dep_id_list.append(dep_id)
                                                    dep_data = data_res[y]['department']
                                                    for iy in range(len(dep_data)):
                                                        dept_name_list.append(dep_data[iy]['dept_name'])
                                                        try:
                                                            position_list.append(dep_data[iy]['dept_position'])
                                                        except Exception as e:
                                                            position_list.append('')
                                                if tmp_role_id != '' and tmp_role_id != None:
                                                    tmp_role_id_list.append(tmp_role_id)
                                                    low_role_id.append(tmp_role_level)
                                                    low_role_name.append(tmp_role_name)
                                for i in range(len(getbiz)):
                                    if getbiz[i]['getbiz'][0]['id_card_num'] == tax_id :
                                        if tax_id not in checktax_id:
                                            r_convert = 0
                                            if result_Select_Check_biz['messageText']['storageNow'] != None:
                                                r_convert = convert_bytes_storage(result_Select_Check_biz['messageText']['storageNow'])
                                            r_storageMax = result_Select_Check_biz['messageText']['storageMax']
                                            r_transactionMax = result_Select_Check_biz['messageText']['transactionMax']
                                            r_transactionNow = result_Select_Check_biz['messageText']['transactionNow']
                                            if r_transactionNow == None:
                                                r_transactionNow = 0
                                            if r_transactionMax == None:
                                                r_transactionMax = 0
                                            if r_storageMax == None:
                                                r_storageMax = 0
                                            checktax_id.append(tax_id)
                                            jsonData = {
                                                'id':getbiz[i]['getbiz'][0]['id'],
                                                'first_name_th':getbiz[i]['getbiz'][0]['first_name_th'],
                                                'first_name_eng':getbiz[i]['getbiz'][0]['first_name_eng'],
                                                'id_card_type':getbiz[i]['getbiz'][0]['id_card_type'],
                                                'id_card_num':getbiz[i]['getbiz'][0]['id_card_num'],
                                                'role_level':getbiz[i]['getrole'][0]['role_level'],
                                                'role_id':getbiz[i]['getrole'][0]['id'],
                                                'role_name':getbiz[i]['getrole'][0]['role_name'],
                                                'role_id_detail':tmp_role_id_list,
                                                'role_level_detail':low_role_id,
                                                'role_name_detail':low_role_name,
                                                'dept_id':dep_id_list,
                                                'dept_name':dept_name_list,
                                                'dept_position':position_list,
                                                'theme_color':result_Select_Check_biz['messageText']['theme_color'],
                                                'path_logo':result_Select_Check_biz['messageText']['path_logo'],
                                                'business_status':result_Select_Check_biz['messageText']['status'],
                                                'detail_use':{
                                                    "storageNow":r_convert,
                                                    "storageMax":r_storageMax,
                                                    "transactionMax":r_transactionMax,
                                                    "transactionNow":r_transactionNow
                                                }
                                            }
                                            biz_info.append(jsonData)
                    for i in range(len(biz_info)):
                        taxId = tax_id
                        getBizinfo_base = select().select_BizProfile(taxId)
                        path_Url = one_url + '/api/get_business_account_role/' + taxId
                        if getBizinfo_base['result'] == 'OK':
                            getRole = callAPI_OneId(token_header,"GET",path_Url,"")
                            getRole = getRole.json()
                            if getRole['result'] == 'Success':
                                update().update_BizProfile(taxId,biz_info[i],getRole['data'])
                            else:
                                if status_shraed == False:
                                    return jsonify({'status':'fail','message':'Authorization Fail!','data':None}),200
                                else:
                                    pass
                        else:
                            getRole = callAPI_OneId(token_header,"GET",path_Url,"")
                            getRole = getRole.json()
                            if getRole['result'] == 'Success':
                                insert().insert_BizProfile(taxId,biz_info[i],getRole['data'])
                            else:
                                if status_shraed == False:
                                    return jsonify({'status':'fail','message':'Authorization Fail!','data':None}),200
                                else:
                                    pass
                    return jsonify({'status':'success','message':'get biz details success','data':biz_info}),200
                else:
                    abort(401)
            else:
                abort(404)

@status_methods.route('/api/v1/getbiz_info_details',methods=['GET'])
@token_required_v3
def getBiz_info_api_newv2():
    if request.method == 'GET':
        biz_info = []
        checktax_id = []
        token_header = request.headers['Authorization']
        try:
            token_header = str(token_header).split(' ')[1]
        except Exception as ex:
            return jsonify({'status':'fail','message':'Bearer Token Error!','data':None}),200
        username = request.args.get('username')
        if username != None:
            username = str(request.args.get('username')).replace(' ','')
            tax_id = str(request.args.get('tax_id')).replace(' ','')
            result_db = select_3().select_citizenlogin_bizpaperless(username,tax_id)               
            if result_db['result'] == 'OK':
                data = result_db['messageText'][0]
                username_db = data['username']
                citizen_data = data['citizen_data']
                print(username_db)
                if username_db == username:
                    if 'biz_detail' in citizen_data:
                        citizen_data = eval(citizen_data)
                        getbiz = citizen_data['biz_detail']
                        check_biz_id = []
                        result_Select_Check_biz = result_db['messageText2']
                        if tax_id not in check_biz_id:
                            check_biz_id.append(tax_id)
                            data_get_my_dep = {
                                "tax_id":tax_id
                            }               
                            text_one_access = 'Bearer ' + token_header
                            resultCallAuth_get_dep = callAPIOneid_post(one_url+'/api/get_my_department_role',data_get_my_dep,text_one_access)
                            dep_id_list = []
                            dept_name_list = []
                            position_list = []
                            list_role_level = []
                            low_role_name = []
                            low_role_id = []
                            tmp_role_id_list = []
                            dep_data = None
                            if resultCallAuth_get_dep['result'] == 'OK':
                                res_json = resultCallAuth_get_dep['messageText'].json()
                                if res_json['data'] != None:
                                    data_res = res_json['data']                                            
                                    if data_res != '':
                                        for y in range(len(data_res)):
                                            dep_id = (data_res[y]['dept_id'])
                                            tmp_role_id = (data_res[y]['role_id'])
                                            tmp_role_detail = data_res[y]['role'][0]
                                            tmp_role_level = tmp_role_detail['role_level']
                                            tmp_role_name = tmp_role_detail['role_name']
                                            print(tmp_role_id)
                                            print(tmp_role_name)
                                            if dep_id != '' and dep_id != None:
                                                dep_id_list.append(dep_id)
                                                dep_data = data_res[y]['department']
                                                for iy in range(len(dep_data)):
                                                    dept_name_list.append(dep_data[iy]['dept_name'])
                                                    try:
                                                        position_list.append(dep_data[iy]['dept_position'])
                                                    except Exception as e:
                                                        position_list.append('')
                                            if tmp_role_id != '' and tmp_role_id != None:
                                                tmp_role_id_list.append(tmp_role_id)
                                                low_role_id.append(tmp_role_level)
                                                low_role_name.append(tmp_role_name)
                            for i in range(len(getbiz)):
                                if getbiz[i]['getbiz'][0]['id_card_num'] == tax_id :
                                    if tax_id not in checktax_id:
                                        r_convert = 0
                                        if result_Select_Check_biz['storageNow'] != None:
                                            r_convert = convert_bytes_storage(result_Select_Check_biz['storageNow'])
                                        r_storageMax = result_Select_Check_biz['storageMax']
                                        r_transactionMax = result_Select_Check_biz['transactionMax']
                                        r_transactionNow = result_Select_Check_biz['transactionNow']
                                        if r_transactionNow == None:
                                            r_transactionNow = 0
                                        if r_transactionMax == None:
                                            r_transactionMax = 0
                                        if r_storageMax == None:
                                            r_storageMax = 0
                                        checktax_id.append(tax_id)
                                        if result_Select_Check_biz['eform_status'] == None:
                                            result_Select_Check_biz['eform_status'] = False
                                        jsonData = {
                                            'id':getbiz[i]['getbiz'][0]['id'],
                                            'first_name_th':getbiz[i]['getbiz'][0]['first_name_th'],
                                            'first_name_eng':getbiz[i]['getbiz'][0]['first_name_eng'],
                                            'id_card_type':getbiz[i]['getbiz'][0]['id_card_type'],
                                            'id_card_num':getbiz[i]['getbiz'][0]['id_card_num'],
                                            'role_level':getbiz[i]['getrole'][0]['role_level'],
                                            'role_id':getbiz[i]['getrole'][0]['id'],
                                            'role_name':getbiz[i]['getrole'][0]['role_name'],
                                            'role_id_detail':tmp_role_id_list,
                                            'role_level_detail':low_role_id,
                                            'role_name_detail':low_role_name,
                                            'dept_id':dep_id_list,
                                            'dept_name':dept_name_list,
                                            'dept_position':position_list,
                                            'theme_color':result_Select_Check_biz['theme_color'],
                                            'path_logo':result_Select_Check_biz['path_logo'],
                                            'business_status':result_Select_Check_biz['status'],
                                            'eform_status':result_Select_Check_biz['eform_status'],
                                            'detail_use':{
                                                "storageNow":r_convert,
                                                "storageMax":r_storageMax,
                                                "transactionMax":r_transactionMax,
                                                "transactionNow":r_transactionNow
                                            }
                                        }
                                        biz_info.append(jsonData)            
                                        # print(tax_id,biz_info,text_one_access)    
                    executor.submit(update_insert_bizprofile,tax_id,biz_info,token_header)                    
                    return jsonify({'status':'success','message':'get biz details success','data':biz_info}),200
                else:
                    abort(401)
            else:
                abort(401)
        else:
            abort(404)

@status_methods.route('/api/getbiz_tx/v1',methods=['POST'])
@token_required
def getBiz_taxV1():
    if request.method == 'POST':
        dataJson = request.json
        if 'userId' in dataJson and 'tax' in dataJson and len(dataJson) == 2:
            userId = dataJson['userId']
            taxId = dataJson['tax']
            result_SelectBizTax = select().select_UserBizAndTax(userId,taxId)
            if result_SelectBizTax['result'] == 'OK':
                return jsonify(result_SelectBizTax),200
            else:
                return jsonify(result_SelectBizTax),200
        else:
            return jsonify({'result':'ER','messageText':'parameter incorrect!','status_Code':404}),404

@status_methods.route('/api/biz/v1', methods=['POST'])
@token_required
def biz_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'taxId' in dataJson and 'roleId' in dataJson and len(dataJson) == 2:
            taxId = dataJson['taxId']
            roldId = dataJson['roleId']
            result_SelectBizv1 = select().select_biz_v1(taxId,roldId)
            if result_SelectBizv1['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_SelectBizv1['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':result_SelectBizv1['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'parameter incorrect!','status_Code':404}),404

@status_methods.route('/api/biz/sender/v1', methods=['POST'])
@token_required
def biz_sender_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'taxId' in dataJson and 'sender_username' in dataJson and 'roleId' in dataJson and len(dataJson) == 3:
            taxId = dataJson['taxId']
            senderUsername = dataJson['sender_username']
            roldId = dataJson['roleId']
            result_BizSender_v1 = select().select_biz_Sender_V1(taxId,senderUsername)
            if result_BizSender_v1['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_BizSender_v1['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':result_BizSender_v1['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'parameter incorrect!','status_Code':404}),404

@status_methods.route('/api/biz/recipient/v1', methods=['POST'])
@token_required
def biz_recipient_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'taxId' in dataJson and 'email_recipient' in dataJson and 'roleId' in dataJson and len(dataJson) == 3:
            taxId = dataJson['taxId']
            emailUser = dataJson['email_recipient']
            roldId = dataJson['roleId']
            result_SelectRecipient = select().select_biz_recipient_v1(taxId,emailUser)
            if result_SelectRecipient['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_SelectRecipient['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':result_SelectRecipient['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'parameter incorrect!','status_Code':404}),404

@status_methods.route('/api/biz/getrole/v1/<string:username>/<string:taxId>', methods=['GET'])
@token_required
def biz_getRole_v1(username,taxId):
    if request.method == 'GET':
        get_user = username
        get_taxId = taxId
        result_GetRole = select().select_biz_getRole_v1(get_taxId)
        if result_GetRole['result'] == 'OK':
            return jsonify({'result':'OK','messageText':result_GetRole['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':result_GetRole['messageText'],'status_Code':200}),200

@status_methods.route('/api/biz/template/v1', methods=['POST','GET','PUT'])
@token_required
def biz_template_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Name' in dataJson and 'step_Upload' in dataJson and 'step_Description' in dataJson and 'templateString' in dataJson and 'template_biz' in dataJson and 'qrCode_position' in dataJson and len(dataJson) == 11:
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_Data ให้เป็น Json ได้'}),200
            try:
                eval(dataJson['step_Upload'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล step_Upload ให้เป็น Json ได้'}),200
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            res_insert_template = insert().insert_paper_template_biz_v1(dataJson['step_Code'],dataJson['step_Data'],dataJson['step_Max'],dataJson['username'],dataJson['email'],st,dataJson['step_Name'],dataJson['step_Upload'],dataJson['step_Description'],dataJson['templateString'],dataJson['template_biz'],dataJson['qrCode_position'])
            if res_insert_template['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'insert success!','status_Code':200}),200
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
    elif request.method == 'GET':
        if (request.args.get('username')) != None and (request.args.get('taxid')) != None:
            username = str(request.args.get('username')).replace(' ','')
            taxId = str(request.args.get('taxid')).replace(' ','')
            result_selectBizTemplate = select().select_biz_tamplate_v1(username,taxId)
            if result_selectBizTemplate['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_selectBizTemplate['messageText'],'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_selectBizTemplate['messageER']}),200
    elif request.method == 'PUT':
        dataJson = request.json
        if 'step_Name' in dataJson and 'step_Code' in dataJson and 'step_Data' in dataJson and 'step_Max' in dataJson and 'username' in dataJson and 'email' in dataJson and 'step_Description' in dataJson and 'templateString' in dataJson and 'qrCode_position' in dataJson and len(dataJson) == 9:
            try:
                eval(dataJson['step_Data'])
            except Exception as ex:
                return jsonify({'result': 'ER', 'messageText': 'ไม่สามารถแปลงข้อมูล Step ให้เป็น Json ได้'}),200
            res_step_update = update().update_step_table_v3(dataJson['step_Code'], dataJson['step_Data'], dataJson['step_Max'], dataJson['username'], dataJson['email'], dataJson['step_Name'],dataJson['step_Description'],dataJson['templateString'],dataJson['qrCode_position'])
            if res_step_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':'Update OK!','status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':'Can,t to Update!','status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
