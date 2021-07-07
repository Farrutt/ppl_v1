#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from method.hashpy import *
from method.verify import *
from db.db_method import *
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onebox import *

if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less

def callPost(path, data):
    url = path
    payload = data
    print(url)
    try:
        time_duration = ''
        response = requests.request("POST", url=url, json=payload, verify=False, stream=True,timeout=10)
        payload['password'] = ''
        time_duration = find_timeduration(response.elapsed.total_seconds())
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url,None,time_duration)
            return {'result': 'OK','messageText': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload),url,None,time_duration)
            return {'result': 'ER','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None,time_duration)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None,time_duration)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None,time_duration)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None,time_duration)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def callPost_v2(path, data):
    url = path
    payload = data
    try:
        time_duration = ''
        response = requests.post(url=url, json=payload, verify=False, stream=True,timeout=10)
        payload['password'] = ''
        time_duration = find_timeduration(response.elapsed.total_seconds())
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url,None,time_duration)
            return {'result': 'OK','messageText': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload),url,None,time_duration)
            return {'result': 'ER','messageText': response,'status_Code':response.status_code}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None,time_duration)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None,time_duration)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None,time_duration)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None,time_duration)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def callGET(path, data):
    url = path
    payload = data
    # print(url,payload)
    
    try:
        time_duration = ''
        response = requests.request("GET", url=url,headers={'Authorization': payload}, verify=False, stream=True,timeout=10)
        tmp_payload_token = str(payload).split(' ')[1]
        time_duration = find_timeduration(response.elapsed.total_seconds())
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url,tmp_payload_token,time_duration)
            return {'result': 'OK','messageText': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload),url,tmp_payload_token,time_duration)
            return {'result': 'ER','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token,time_duration)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token,time_duration)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token,time_duration)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token,time_duration)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def callGET_v2(path, data):
    url = path
    payload = data
    # print(url,payload)
    
    try:
        time_duration = ''
        response = requests.get(url=url,headers={'Authorization': payload}, verify=False, stream=True,timeout=10)
        tmp_payload_token = str(payload).split(' ')[1]
        time_duration = find_timeduration(response.elapsed.total_seconds())
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url,tmp_payload_token,time_duration)
            return {'result': 'OK','messageText': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload),url,tmp_payload_token,time_duration)
            return {'result': 'ER','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token,time_duration)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token,time_duration)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token,time_duration)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token,time_duration)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def callGET_v3(path):
    url = path
    payload = ''
    tmp_payload_token = ''
    try:
        time_duration = ''
        response = requests.get(url=url, verify=False, stream=True,timeout=10)
        # tmp_payload_token = str(payload).split(' ')[1]
        time_duration = find_timeduration(response.elapsed.total_seconds())
        print(response.text)
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url,tmp_payload_token,time_duration)
            return {'result': 'OK','messageText': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload),url,tmp_payload_token,time_duration)
            return {'result': 'ER','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token,time_duration)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token,time_duration)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token,time_duration)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token,time_duration)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def callAuth_get(path, data):
    url = path
    payload = data
    print(url)
    try:
        time_duration = ''
        response = requests.get(url, headers={'Authorization': payload}, verify=False, stream=True,timeout=10)
        tmp_payload_token = str(payload).split(' ')[1]
        time_duration = find_timeduration(response.elapsed.total_seconds())
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url,tmp_payload_token,time_duration)
            return {'status': 'success','response': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload),url,tmp_payload_token,time_duration)
            return {'result': 'fail','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token,time_duration)
        return {'status': 'HTTPError','message': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token,time_duration)
        return {'status': 'Timeout','message': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token,time_duration)
        return {'status': 'ConnectionError','message': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token,time_duration)
        return {'status': 'fail','message': 'An unexpected error: ' + str(err)}

def callAuth_post(path, data,auth_token):
    url = path
    payload = data
    print(url)
    try:
        time_duration = ''
        response = requests.request("POST",headers={'Authorization': auth_token}, url=url, json=payload, verify=False, stream=True,timeout=10)
        tmp_payload_token = str(auth_token).split(' ')[1]
        time_duration = find_timeduration(response.elapsed.total_seconds())
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload) + ' ' + str(auth_token),url,tmp_payload_token,time_duration)
            return {'result': 'OK','messageText': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token,time_duration)
            return {'result': 'ER','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token,time_duration)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token,time_duration)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token,time_duration)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token,time_duration)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def LoginOffline(username,password,ipaddress):
    hash_data_password = hash_512_v2(password)
    select_OfflineLogin = select().select_DataLoginOffline(username,hash_data_password,ipaddress)
    return (select_OfflineLogin)

def generate_tokenPaperless(username,user_email,typeToken='paperless'):
    username = username
    user_email = user_email
    typeToken = typeToken
    iat_time = time.time()
    exp_time = time.time() + 86400
    jsonData = {
        "iat":      int(iat_time),
        "username": username,
        "type":     typeToken,
        "email":    user_email,
        "exp":      int(exp_time)
    }
    jwtencode = encode(jsonData)
    return jwtencode

@status_methods.route('/login_citizen/v2',methods=['POST'])
def func_login_citizen_v2():
    data = request.json
    if 'username' in data and 'password' in data and 'ipz' in data and len(data) == 3:
        username = data['username']
        password = data['password']
        ipaddress = data['ipz']
        try:
            info = {
                "grant_type":  "password",
                "username":     username,
                "password":     password,
                "client_id":    clientId,
                "client_secret":secretKey
            }

            #response = callServer.requestPost(one_url+"/api/oauth/getpwd",info) #prod
            response = callPost(one_url+"/api/oauth/getpwd",info) #uat
            print(response['messageText'].json())
            if response['result'] == 'OK':
                if str(response['messageText']) == '<Response [504]>':
                    result_LoginOffline = LoginOffline(username,password,ipaddress)
                    return jsonify(result_LoginOffline),200
                else:
                    json_pwd = response['messageText'].json()
                    try:
                        username = json_pwd['username']
                    except Exception as ex:
                        return jsonify({'result':'Fail','responseCode':401,'data':None,'errorMessage':'login fail! username not found'}),401
            else:
                result_LoginOffline = LoginOffline(username,password,ipaddress)
                return jsonify(result_LoginOffline),200
                # return jsonify({'result':'Fail','responseCode':500,'data':None,'errorMessage':str(response['messageText']),'messageER':'oneid Service pwd'})
            if json_pwd['result'] == 'Success':
                token_one = json_pwd['token_type']+' '+json_pwd['access_token']
                access_token_one = json_pwd['access_token']
                #response_one = callServer.requestAuth(one_url+'/api/account/',token_one) #prod
                # response_one = callAuth_get(one_url+'/api/account/',token_one) #uat
                
                # print(json_account)
                getBuz = callGET(one_url+"/api/account_and_biz_detail",token_one)
                json_account = getBuz['messageText'].json()
                if getBuz['result'] == 'OK':
                    getBuz = getBuz['messageText'].json()
                else:
                    result_LoginOffline = LoginOffline(username,password,ipaddress)
                    return jsonify(result_LoginOffline),200
                    # return jsonify({'result':'Fail','responseCode':500,'data':None,'errorMessage':str(response['messageText']),'messageER':'oneid Service biz'})
                one_email = json_account['thai_email']
                if one_email != '':
                    ts = time.time()
                    user_id         = json_account['id']
                    user_email      = json_account['thai_email']
                    user_type       = json_account['account_category']
                    try:
                        result_loginChat = login_OneChat(user_id,access_token_one)
                        print()
                        print(result_loginChat)
                    except Exception as e:
                        print(str(e))

                    one_accesstoken = str(json_pwd['access_token'])
                    access_time     = ts
                    refresh_token   = json_pwd['refresh_token']
                    access_token_time = ts + json_pwd['expires_in']
                    access_token_begin = ts
                    hash_data       = hash_512_v2(password)
                    citizen_data    = str(json_account)
                    result_select = select().select_LoginUser(username,user_id,user_email)
                    getBiz_details = getBuz['biz_detail']
                    try:
                        # print(result_select)
                        if result_select['result'] == 'OK':
                            generate_seCode =   'P7Rw2h5GUVE2LpbVNRBO'
                            result_refToken = generate_tokenPaperless(username,user_email)
                            result_update = update().update_LoginUser(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,getBuz,generate_seCode,ipaddress)
                            resultUpdateLog = update().update_LogLoingBiz(username,user_id,getBiz_details)
                        else:
                            result_insert = {}
                            result_insert['result'] = 'OK'
                            generate_seCode = 'P7Rw2h5GUVE2LpbVNRBO'
                            result_refToken = generate_tokenPaperless(username,user_email)
                            result_insert = insert().insert_login(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,getBuz,generate_seCode,ipaddress)
                            result_BizLoing = insert().insert_LogBizLogin(username,user_id,getBiz_details)
                            if result_insert['result'] =='OK':
                                print(result_insert)
                            else:
                                print(result_insert)
                        insert().insert_UserLog(username,user_id,ipaddress,user_email)
                    except Exception as ex:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'ไม่สามารถเชื่อมต่อระบบ One id ได้ ' + str(ex)})
                    try:
                        citizen_data = eval(citizen_data)
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'ไม่สามารถแปลง data เป็น Json ได้'})
                    biz_info = []
                    check_biz_id = []
                    # print(getBuz,'getBuz')
                    if 'biz_detail' in getBuz:                        
                        for i in range(len(getBuz['biz_detail'])):
                            
                            
                            result_Select_Check_biz = select().select_checkBizPaperless(getBuz['biz_detail'][i]['getbiz'][0]['id_card_num'])
                            if result_Select_Check_biz['result'] == 'OK':
                                
                                if getBuz['biz_detail'][i]['getbiz'][0]['id_card_num'] not in check_biz_id:
                                    # print(getBuz['biz_detail'][i]['getbiz'][0]['id_card_num'],'idcard')
                                    check_biz_id.append(getBuz['biz_detail'][i]['getbiz'][0]['id_card_num'])
                                    data_get_my_dep = {
                                        "tax_id": getBuz['biz_detail'][i]['getbiz'][0]['id_card_num']
                                    }
                                    text_one_access = 'Bearer ' + one_accesstoken
                                    resultCallAuth_get_dep = callAuth_post(one_url+'/api/get_my_department_role',data_get_my_dep,text_one_access)
                                    # print(resultCallAuth_get_dep)
                                    dep_id_list = []
                                    dept_name_list = []
                                    position_list = []
                                    jsonData = {}
                                    if resultCallAuth_get_dep['result'] == 'OK':
                                        res_json = resultCallAuth_get_dep['messageText'].json()
                                        # print(res_json,'res_json')
                                        if res_json['data'] != None:
                                            
                                            data_res = res_json['data']
                                            if data_res != '':
                                                for y in range(len(data_res)):
                                                    dep_id = (data_res[y]['dept_id'])
                                                    if dep_id != '':
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
                                                        dep_data = []
                                                        dept_name_list = []
                                                        position_list = []
                                            else:
                                                dep_id_list = []
                                                dep_data = []
                                                dept_name_list = []
                                                position_list = []
                                        else:
                                            jsonData ={}
                                            dep_id_list = []
                                            dep_data = []
                                            dept_name_list = []
                                            position_list = []
                                        # print(getBuz['biz_detail'][i]['getbiz'])
                                        jsonData = {
                                            'id':getBuz['biz_detail'][i]['getbiz'][0]['id'],
                                            'first_name_th':getBuz['biz_detail'][i]['getbiz'][0]['first_name_th'],
                                            'first_name_eng':getBuz['biz_detail'][i]['getbiz'][0]['first_name_eng'],
                                            'id_card_type':getBuz['biz_detail'][i]['getbiz'][0]['id_card_type'],
                                            'id_card_num':getBuz['biz_detail'][i]['getbiz'][0]['id_card_num'],
                                            'role_level':getBuz['biz_detail'][i]['getrole'][0]['role_level'],
                                            'role_id':getBuz['biz_detail'][i]['getrole'][0]['id'],
                                            'role_name':getBuz['biz_detail'][i]['getrole'][0]['role_name'],
                                            'dept_id':dep_id_list,
                                            'dept_name':dept_name_list,
                                            'dept_position':position_list
                                        }
                                        # print(jsonData)
                                        biz_info.append(jsonData)
                    else:
                        biz_info = []
                    return jsonify({'result':'OK','username':username,'one_access_token':one_accesstoken,'paperless_access_token':result_refToken,'one_result_data':citizen_data,'one_biz_detail':biz_info})
                else:
                    return jsonify(json_account)
            else :
                return jsonify(json_pwd)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'Fail','responseCode':500,'data':None,'errorMessage':str(e)})
    else:
        return jsonify({'result':'Fail','responseCode':200,'data':None,'errorMessage':'parameter incorrect'})

@status_methods.route('/api/v3/login_citizen',methods=['POST'])
def login_citizen_api_v3():
    if request.method == 'POST':
        data = request.json
        if 'username' in data and 'password' in data and 'ipz' in data and len(data) == 3:
            username = data['username']
            password = data['password']
            ipaddress = data['ipz']
            try:
                tmp_json = {
                    "grant_type":  "password",
                    "username":     username,
                    "password":     password,
                    "client_id":    clientId,
                    "client_secret":secretKey
                }
                response = callPost_v2(one_url+"/api/oauth/getpwd",tmp_json)
                # print(response)
                if response['result'] == 'OK':
                    tmp_messageText = response['messageText'].json()                    
                    if tmp_messageText['result'] == 'Success':
                        try:
                            username = tmp_messageText['username']
                        except Exception as ex:
                            return jsonify({'result':'Fail','responseCode':401,'data':None,'errorMessage':'login fail! username not found'}),401
                        token_one = tmp_messageText['token_type'] + ' '+ tmp_messageText['access_token']
                        access_token_one = tmp_messageText['access_token']
                        getBuz = callGET_v2(one_url+"/api/account_and_biz_detail",token_one)
                        if getBuz['result'] == 'OK':
                            tmp_account_biz = getBuz['messageText'].json()
                            ts = time.time()
                            user_id         = tmp_account_biz['id']
                            user_email      = tmp_account_biz['thai_email']
                            user_type       = tmp_account_biz['account_category']
                            one_accesstoken = str(tmp_messageText['access_token'])
                            access_time     = ts
                            refresh_token   = tmp_messageText['refresh_token']
                            access_token_time   = ts + tmp_messageText['expires_in']
                            access_token_begin  = ts
                            hash_data       = hash_512_v2(password)
                            citizen_data    = str(tmp_account_biz)
                            getBiz_details  =  tmp_account_biz['biz_detail']
                            result_select   = select().select_LoginUser(username,user_id,user_email)
                            # with concurrent.futures.ThreadPoolExecutor() as executor:
                            #     loginOnechat_result = executor.submit(login_OneChat,user_id,access_token_one)
                            #     info = {
                            #         'accesstoken':one_accesstoken
                            #     }
                            #     oneBox_result = executor.submit(get_account_byuserid,info,one_accesstoken)
                            #     # getaccount_onebox = get_account_byuserid(info,one_accesstoken)
                            #     return_paper = loginOnechat_result.result()
                            #     return_onebox_result = oneBox_result.result()
                            try:
                                result_loginChat = login_OneChat(user_id,access_token_one)
                            except Exception as e:
                                print(str(e))
                            try:
                                info = {
                                    'accesstoken':one_accesstoken
                                }
                                getaccount_onebox = get_account_byuserid(info,one_accesstoken)
                            except Exception as e:
                                print(str(e))
                            try:
                                # print(result_select)
                                if result_select['result'] == 'OK':
                                    generate_seCode =   'P7Rw2h5GUVE2LpbVNRBO'
                                    result_refToken = generate_tokenPaperless(username,user_email)
                                    result_update = update().update_LoginUser(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress)
                                    resultUpdateLog = update().update_LogLoingBiz(username,user_id,getBiz_details)
                                else:
                                    result_insert = {}
                                    result_insert['result'] = 'OK'
                                    generate_seCode = 'P7Rw2h5GUVE2LpbVNRBO'
                                    result_refToken = generate_tokenPaperless(username,user_email)
                                    result_insert = insert().insert_login(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress)
                                    result_BizLoing = insert().insert_LogBizLogin(username,user_id,getBiz_details)
                                insert().insert_UserLog(username,user_id,ipaddress,user_email)
                            except Exception as ex:
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                print(exc_type, fname, exc_tb.tb_lineno)
                                insert().insert_tran_log_v1(str(exc_type + ' ' + fname +  ' ' + exc_tb.tb_lineno),'ER',"","/api/v3/login_citizen","")
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'connection db fail ' + str(ex)})
                            try:
                                citizen_data = eval(citizen_data)
                            except Exception as ex:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'ไม่สามารถแปลง data เป็น Json ได้'})
                            biz_info = []
                            check_biz_id = []
                            if 'biz_detail' in tmp_account_biz:                        
                                for i in range(len(tmp_account_biz['biz_detail'])):
                                    result_Select_Check_biz = select().select_checkBizPaperless(tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num'])
                                    if result_Select_Check_biz['result'] == 'OK':
                                        
                                        if tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num'] not in check_biz_id:
                                            # print(getBuz['biz_detail'][i]['getbiz'][0]['id_card_num'],'idcard')
                                            check_biz_id.append(tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num'])
                                            data_get_my_dep = {
                                                "tax_id": tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num']
                                            }
                                            text_one_access = 'Bearer ' + one_accesstoken
                                            resultCallAuth_get_dep = callGET_v2(one_url+'/api/v1/service/business/account/'+user_id+'/department_role?tax_id=' + tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num'],text_one_access)
                                            # print(resultCallAuth_get_dep)
                                            dep_id_list = []
                                            dept_name_list = []
                                            position_list = []
                                            jsonData = {}
                                            if resultCallAuth_get_dep['result'] == 'OK':
                                                res_json = resultCallAuth_get_dep['messageText'].json()
                                                # print(res_json)
                                                if res_json['data'] != None:
                                                    
                                                    data_res = res_json['data']
                                                    if data_res != '':
                                                        for y in range(len(data_res)):
                                                            dep_id = (data_res[y]['dept_id'])
                                                            # print(dep_id)
                                                            if dep_id != '' and dep_id != None:
                                                                dep_id_list.append(dep_id)
                                                                dep_data = data_res[y]['department']
                                                                for iy in range(len(dep_data)):
                                                                    dept_name_list.append(dep_data[iy]['dept_name'])
                                                                    try:
                                                                        position_list.append(dep_data[iy]['dept_position'])
                                                                    except Exception as e:
                                                                        position_list.append('')
                                                            elif dep_id != None:
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
                                                                dep_data = []
                                                                dept_name_list = []
                                                                position_list = []
                                                    else:
                                                        dep_id_list = []
                                                        dep_data = []
                                                        dept_name_list = []
                                                        position_list = []
                                                else:
                                                    jsonData = {}
                                                    dep_id_list = []
                                                    dep_data = []
                                                    dept_name_list = []
                                                    position_list = []
                                                # print(getBuz['biz_detail'][i]['getbiz'])
                                                jsonData = {
                                                    'id':tmp_account_biz['biz_detail'][i]['getbiz'][0]['id'],
                                                    'first_name_th':tmp_account_biz['biz_detail'][i]['getbiz'][0]['first_name_th'],
                                                    'first_name_eng':tmp_account_biz['biz_detail'][i]['getbiz'][0]['first_name_eng'],
                                                    'id_card_type':tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_type'],
                                                    'id_card_num':tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num'],
                                                    'role_level':tmp_account_biz['biz_detail'][i]['getrole'][0]['role_level'],
                                                    'role_id':tmp_account_biz['biz_detail'][i]['getrole'][0]['id'],
                                                    'role_name':tmp_account_biz['biz_detail'][i]['getrole'][0]['role_name'],
                                                    'dept_id':dep_id_list,
                                                    'dept_name':dept_name_list,
                                                    'dept_position':position_list
                                                }
                                                # print(jsonData)
                                                biz_info.append(jsonData)
                            else:
                                biz_info = []
                            return jsonify({'result':'OK','username':username,'one_access_token':one_accesstoken,'paperless_access_token':result_refToken,'one_result_data':citizen_data,'one_biz_detail':biz_info})
                        else:
                            result_LoginOffline = LoginOffline(username,password,ipaddress)
                            return jsonify(result_LoginOffline),200
                    else:
                        return jsonify(tmp_messageText)
                else:
                    if response['status_Code'] == 401:
                        return jsonify({'result':'Fail','responseCode':401,'data':None,'errorMessage':'login fail! username not found'}),401
                    else:
                        result_LoginOffline = LoginOffline(username,password,ipaddress)
                        return jsonify(result_LoginOffline),200
            except Exception as e:
                print(str(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                insert().insert_tran_log_v1(str(exc_type) + ' ' + fname +  ' ' + str(exc_tb.tb_lineno),'ER',"","/api/v3/login_citizen","")
                return jsonify({'result':'Fail','responseCode':500,'data':None,'errorMessage':str(e)})

def update_datalogin(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress,getBiz_details):
    result_update = update().update_LoginUser(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress)
    resultUpdateLog = update().update_LogLoingBiz(username,user_id,getBiz_details)
    print(result_update)
# ################## LOGIN OLD version
@status_methods.route('/api/v2/login_paperless',methods=['POST'])
def login_citizen_api_v1():
    if request.method == 'POST':
        data = request.json
        if 'username' in data and 'password' in data and 'ipz' in data and len(data) == 3:
            username = data['username']
            password = data['password']
            ipaddress = data['ipz']
            biz_info = []
            check_biz_id = []
            tmp_json = {
                "grant_type":  "password",
                "username":     username,
                "password":     password,
                "client_id":    clientId,
                "client_secret":secretKey,
                "scope": "pic"
            }
            response = callPost_v2(one_url+"/api/oauth/getpwd",tmp_json)
            if response['result'] == 'OK':
                tmp_messageText = response['messageText'].json()
                if tmp_messageText['result'] == 'Success':
                    try:
                        username = tmp_messageText['username']
                        user_id = tmp_messageText['account_id']
                    except Exception as ex:
                        abort(401)
                    token_one = tmp_messageText['token_type'] + ' '+ tmp_messageText['access_token']
                    access_token_one = tmp_messageText['access_token']
                    result_selectdb = select_3().select_citizen_login_v1(username)
                    getBuz = callGET_v2(one_url+"/api/account_and_biz_detail",token_one)
                    # get_picProfile = callGET_v2(one_url+"/api/v2/service/citizen/info",token_one)  
                    # if get_picProfile['result'] == 'OK':  
                    #     tmpdata_pic = (get_picProfile['messageText'].json())  
                    #     if tmpdata_pic['result'] == 'Success':
                    #         tmpdata = tmpdata_pic['data']
                    #         tmppic = tmpdata['pic']
                    #         executor.submit(update_3().update_picprofile_v1,tmppic,username)
                    ts = time.time()
                    try:
                        info = {
                            'accesstoken':access_token_one
                        }
                        executor.submit(login_OneChat,user_id,access_token_one)
                        executor.submit(get_account_byuserid,info,access_token_one)
                    except Exception as e:
                        print(str(e))
                    if result_selectdb['result'] == 'OK':
                        if getBuz['result'] == 'OK':
                            tmp_account_biz = getBuz['messageText'].json()
                            ts = time.time()
                            user_id         = tmp_account_biz['id']
                            user_email      = tmp_account_biz['thai_email']
                            user_type       = tmp_account_biz['account_category']
                            one_accesstoken = str(tmp_messageText['access_token'])
                            access_time     = ts
                            refresh_token   = tmp_messageText['refresh_token']
                            access_token_time   = ts + tmp_messageText['expires_in']
                            access_token_begin  = ts
                            hash_data       = hash_512_v2(password)
                            citizen_data    = str(tmp_account_biz)
                            getBiz_details  =  tmp_account_biz['biz_detail']
                            generate_seCode =   'P7Rw2h5GUVE2LpbVNRBO'
                            result_refToken = generate_tokenPaperless(username,user_email)
                            insert().insert_UserLog(username,user_id,ipaddress,user_email)
                            executor.submit(update_datalogin,user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress,getBiz_details)
                            try:
                                citizen_data = eval(citizen_data)
                            except Exception as ex:
                                abort(401)
                            return jsonify({'result':'OK','username':username,'one_access_token':one_accesstoken,'paperless_access_token':result_refToken,'one_result_data':citizen_data})
                        else:                       
                            abort(401)
                    else:
                        if getBuz['result'] == 'OK':
                            tmp_account_biz = getBuz['messageText'].json()
                            ts = time.time()
                            user_id         = tmp_account_biz['id']
                            user_email      = tmp_account_biz['thai_email']
                            user_type       = tmp_account_biz['account_category']
                            one_accesstoken = str(tmp_messageText['access_token'])
                            access_time     = ts
                            refresh_token   = tmp_messageText['refresh_token']
                            access_token_time   = ts + tmp_messageText['expires_in']
                            access_token_begin  = ts
                            hash_data       = hash_512_v2(password)
                            citizen_data    = str(tmp_account_biz)
                            getBiz_details  =  tmp_account_biz['biz_detail']
                            generate_seCode = 'P7Rw2h5GUVE2LpbVNRBO'
                            result_refToken = generate_tokenPaperless(username,user_email)
                            result_insert = insert().insert_login(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress)
                            result_BizLoing = insert().insert_LogBizLogin(username,user_id,getBiz_details)
                            insert().insert_UserLog(username,user_id,ipaddress,user_email)
                        else:
                            abort(401)
                try:
                    citizen_data = eval(citizen_data)
                except Exception as ex:
                    abort(401)
                    
                return jsonify({'result':'OK','username':username,'one_access_token':one_accesstoken,'paperless_access_token':result_refToken,'one_result_data':citizen_data})
            else:
                abort(401)
        else:
            abort(404)

################### LOGIN NEW version
@status_methods.route('/api/v1/login_paperless',methods=['POST'])
def login_citizen_api_v2():
    if request.method == 'POST':
        data = request.json
        if 'username' in data and 'password' in data and 'ipz' in data and len(data) == 3:
            username = data['username']
            password = data['password']
            ipaddress = data['ipz']
            biz_info = []
            check_biz_id = []
            tmp_json = {
                "grant_type":  "password",
                "username":     username,
                "password":     password,
                "client_id":    clientId,
                "client_secret":secretKey,
                "scope": "pic"
            }
            response = callPost_v2(one_url+"/api/oauth/getpwd",tmp_json)
            if response['result'] == 'OK':
                tmp_messageText = response['messageText'].json()
                if tmp_messageText['result'] == 'Success':
                    try:
                        username = tmp_messageText['username']
                        user_id = tmp_messageText['account_id']
                    except Exception as ex:
                        abort(401)
                    token_one = tmp_messageText['token_type'] + ' '+ tmp_messageText['access_token']
                    access_token_one = tmp_messageText['access_token']
                    result_selectdb = select_3().select_citizen_login_v1(username)
                    getBuz = callGET_v2(one_url+"/api/account_and_biz_detail",token_one)
                    ts = time.time()
                    try:
                        info = {
                            'accesstoken':access_token_one
                        }
                        executor.submit(login_OneChat,user_id,access_token_one)
                        executor.submit(get_account_byuserid,info,access_token_one)
                    except Exception as e:
                        current_app.logger.info(str(e))
                    email_list = []
                    if result_selectdb['result'] == 'OK':
                        if getBuz['result'] == 'OK':
                            result_citizen  = result_selectdb['messageText'][0]
                            tmp_account_biz = getBuz['messageText'].json()
                            ts = time.time()
                            user_id         = tmp_account_biz['id']
                            user_email      = tmp_account_biz['thai_email']
                            user_email2     = tmp_account_biz['thai_email2']
                            email_list.append(user_email)
                            email_list.append(user_email2)
                            if 'thai_email3' in str(tmp_account_biz):
                                if tmp_account_biz['thai_email3'] != None:
                                    user_email3     = tmp_account_biz['thai_email3']
                                    email_list.append(user_email3)
                            user_type       = tmp_account_biz['account_category']
                            update_time     = tmp_account_biz['last_update']
                            update_time_old     = result_citizen['update_time']
                            one_accesstoken = str(tmp_messageText['access_token'])
                            access_time     = ts
                            refresh_token   = tmp_messageText['refresh_token']
                            access_token_time   = ts + tmp_messageText['expires_in']
                            access_token_begin  = ts
                            hash_data       = hash_512_v2(password)
                            citizen_data    = str(tmp_account_biz)
                            getBiz_details  =  tmp_account_biz['biz_detail']
                            generate_seCode =   'P7Rw2h5GUVE2LpbVNRBO'
                            result_refToken = generate_tokenPaperless(username,user_email)
                            update_4().update_login_logBiz_userLog(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress,getBiz_details,email_list,update_time,update_time_old)
                        else:                       
                            abort(401)
                    else:
                        if getBuz['result'] == 'OK':
                            tmp_account_biz = getBuz['messageText'].json()
                            ts = time.time()
                            user_id         = tmp_account_biz['id']
                            user_email      = tmp_account_biz['thai_email']
                            user_email2     = tmp_account_biz['thai_email2']
                            email_list.append(user_email)
                            email_list.append(user_email2)
                            if 'thai_email3' in str(tmp_account_biz):
                                if tmp_account_biz['thai_email3'] != None:
                                    user_email3     = tmp_account_biz['thai_email3']
                                    email_list.append(user_email3)
                            user_type       = tmp_account_biz['account_category']
                            update_time     = tmp_account_biz['last_update']
                            one_accesstoken = str(tmp_messageText['access_token'])
                            access_time     = ts
                            refresh_token   = tmp_messageText['refresh_token']
                            access_token_time   = ts + tmp_messageText['expires_in']
                            access_token_begin  = ts
                            hash_data       = hash_512_v2(password)
                            citizen_data    = str(tmp_account_biz)
                            getBiz_details  =  tmp_account_biz['biz_detail']
                            generate_seCode = 'P7Rw2h5GUVE2LpbVNRBO'
                            result_refToken = generate_tokenPaperless(username,user_email)
                            insert_4().insert_login_logBiz_userLog(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress,getBiz_details,email_list,update_time)
                        else:
                            abort(401)
                try:
                    citizen_data = eval(citizen_data)
                except Exception as ex:
                    abort(401)
                enaccess = endcode_access(one_accesstoken)
                return jsonify({'result':'OK','username':username,'one_access_token':one_accesstoken,'enaccess':enaccess,'paperless_access_token':result_refToken,'one_result_data':citizen_data})
            else:
                abort(401)
        else:
            abort(404)

@status_methods.route('/api/v1/logintoken_paperless',methods=['POST'])
def logintoken_paperless_api_v1():
    if request.method == 'POST':
        data = request.json
        if 'code' in data and 'scope' in data and 'ipz' in data and len(data) == 3:
            code = data['code']
            scope = data['scope']
            ipaddress = data['ipz']
            biz_info = []
            check_biz_id = []
            tmp_json = {
                "grant_type":  "authorization_code",
                "code":     code,
                "scope":     scope,
                "client_id":    clientId,
                "client_secret":secretKey
            }
            url = one_url+"/api/oauth/getcode?grant_type=authorization_code&code=" + code + "&scope=&client_id="+clientId +"&client_secret="+secretKey
            response = callGET_v3(url)
            print(response)
            if response['result'] == 'OK':
                tmp_messageText = response['messageText'].json()
                if tmp_messageText['result'] == 'Success':
                    try:
                        username = tmp_messageText['username']
                        user_id = tmp_messageText['account_id']
                    except Exception as ex:
                        abort(401)
                    token_one = tmp_messageText['token_type'] + ' '+ tmp_messageText['access_token']
                    access_token_one = tmp_messageText['access_token']
                    result_selectdb = select_3().select_citizen_login_v1(username)
                    getBuz = callGET_v2(one_url+"/api/account_and_biz_detail",token_one)
                    ts = time.time()
                    try:
                        info = {
                            'accesstoken':access_token_one
                        }
                        executor.submit(login_OneChat,user_id,access_token_one)
                        executor.submit(get_account_byuserid,info,access_token_one)
                    except Exception as e:
                        print(str(e))
                    print(result_selectdb)
                    if result_selectdb['result'] == 'OK':
                        if getBuz['result'] == 'OK':
                            tmp_account_biz = getBuz['messageText'].json()
                            ts = time.time()
                            user_id         = tmp_account_biz['id']
                            user_email      = tmp_account_biz['thai_email']
                            user_type       = tmp_account_biz['account_category']
                            one_accesstoken = str(tmp_messageText['access_token'])
                            access_time     = ts
                            refresh_token   = tmp_messageText['refresh_token']
                            access_token_time   = ts + tmp_messageText['expires_in']
                            access_token_begin  = ts
                            hash_data       = hash_512_v2(password)
                            citizen_data    = str(tmp_account_biz)
                            getBiz_details  =  tmp_account_biz['biz_detail']
                            generate_seCode =   'P7Rw2h5GUVE2LpbVNRBO'
                            result_refToken = generate_tokenPaperless(username,user_email)
                            executor.submit(update_datalogin,user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress,getBiz_details)
                            try:
                                citizen_data = eval(citizen_data)
                            except Exception as ex:
                                abort(401)
                            return jsonify({'result':'OK','username':username,'one_access_token':one_accesstoken,'paperless_access_token':result_refToken,'one_result_data':citizen_data})
                        else:                       
                            abort(401)
                    else:
                        if getBuz['result'] == 'OK':
                            tmp_account_biz = getBuz['messageText'].json()
                            ts = time.time()
                            user_id         = tmp_account_biz['id']
                            user_email      = tmp_account_biz['thai_email']
                            user_type       = tmp_account_biz['account_category']
                            one_accesstoken = str(tmp_messageText['access_token'])
                            access_time     = ts
                            refresh_token   = tmp_messageText['refresh_token']
                            access_token_time   = ts + tmp_messageText['expires_in']
                            access_token_begin  = ts
                            hash_data       = hash_512_v2(password)
                            citizen_data    = str(tmp_account_biz)
                            getBiz_details  =  tmp_account_biz['biz_detail']
                            generate_seCode = 'P7Rw2h5GUVE2LpbVNRBO'
                            result_refToken = generate_tokenPaperless(username,user_email)
                            result_insert = insert().insert_login(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress)
                            result_BizLoing = insert().insert_LogBizLogin(username,user_id,getBiz_details)
                        else:
                            abort(401)
                try:
                    citizen_data = eval(citizen_data)
                except Exception as ex:
                    abort(401)
                    
                return jsonify({'result':'OK','username':username,'one_access_token':one_accesstoken,'paperless_access_token':result_refToken,'one_result_data':citizen_data})
            else:
                abort(401)
        else:
            abort(404)

@status_methods.route('/api/v1/auth_token',methods=['GET'])
def auth_token_api_v1():
    if request.method == 'GET':
        if 'Authorization' not in request.headers:
            abort(401)
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        
        auth_toekn = token_header
        try:
            tokenaccess = str(auth_toekn)
        except Exception as e:
            abort(401)
        try:
            tokenaccess = str(tokenaccess).split(' ')[1]
        except Exception as e:
            tokenaccess = str(tokenaccess)
        result_token = token_required_func(tokenaccess)
        if result_token['result'] == 'ER':
            abort(401)
        citizen_data = str(result_token['citizen_data'])
        username = str(result_token['username']).lower()
        userId = result_token['user_id']
        emailUser = result_token['email']
        bizinfo = str(result_token['biz_info'])
        access_token_begin = int(time.time())
        access_time = datetime.datetime.fromtimestamp(access_token_begin).strftime('%Y-%m-%d %H:%M:%S')
        access_token_time = access_token_begin + 86400
        one_accesstoken = tokenaccess
        resultUpdate = update().token_formChat_v1(userId,username,str(tokenaccess),citizen_data,bizinfo)
        print(resultUpdate)
        if resultUpdate['result'] == 'OK':
            res_selectCheckLoginUser = select().select_LoginUser(username,userId,emailUser)
            if res_selectCheckLoginUser['result'] == 'OK':
                insert().insert_tran_log_v1(str(citizen_data),'OK',str(auth_toekn),one_url+"/api/account_and_biz_detail",tokenaccess)
                return jsonify(res_selectCheckLoginUser),200
            else:
                generate_seCode =   'P7Rw2h5GUVE2LpbVNRBO'
                result_refToken = generate_tokenPaperless(username,emailUser)
                result_insert = insert().insert_login(userId,username,access_token_begin,None,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,None,getBuz,generate_seCode,None)
                if result_insert['result'] == 'OK':
                    insert().insert_tran_log_v1(str(citizen_data),'OK',str(auth_toekn),one_url+"/api/account_and_biz_detail",tokenaccess)
                    res_selectCheckLoginUser = select().select_LoginUser(username,userId,emailUser)
                    return jsonify(res_selectCheckLoginUser),200
                else:
                    return jsonify(result_insert),200
        else:
            insert().insert_tran_log_v1(str('cant update login'),'ER',str(auth_toekn),one_url+"/api/account_and_biz_detail",tokenaccess)
            return jsonify({'result':'ER','status_Code':200,'data':None,'messageER':'cant update login'}),200

@status_methods.route('/api/token/v1',methods=['POST'])
def checktokenV1():
    if request.method == 'POST':
        dataJson = request.json
        if 'type_property' in dataJson and 'page' in dataJson and len(dataJson) == 2:
            page_token = dataJson['page']
            type_property = dataJson['type_property']
            result_Check = check_and_decode_tokenfrom_chat(page_token)
            auth_toekn = ""
            tokenaccess = ""
            if result_Check['result'] == 'OK':
                auth_toekn = result_Check['messageText']
                try:
                    tokenaccess = str(auth_toekn)
                except Exception as e:
                    abort(401)
                # print(tokenaccess)
                try:
                    tokenaccess = str(tokenaccess).split(' ')[1]
                except Exception as e:
                    tokenaccess = str(tokenaccess)
                # tokenaccess = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjViZWJjNzJiZDFmNzg5MGRkOGQ2YTJjZmFjOTUzMjliZTE2MTRhZGNjYmIzNTQ5M2IwNzM0NzliN2E1Njc4ZTdjOGUzMmFlZmM2ZGI0NmJlIiwia2lkIjoiIn0.eyJhdWQiOiIxMzYiLCJqdGkiOiI1YmViYzcyYmQxZjc4OTBkZDhkNmEyY2ZhYzk1MzI5YmUxNjE0YWRjY2JiMzU0OTNiMDczNDc5YjdhNTY3OGU3YzhlMzJhZWZjNmRiNDZiZSIsImlhdCI6MTU4NTgwODI4MCwibmJmIjoxNTg1ODA4MjgwLCJleHAiOjE1ODU4MDg1ODAsInN1YiI6Ijc4NjUzOTAxMjYwOCIsInVzZXJuYW1lIjoiamlyYXl1a25vdCJ9.G2ZIL5hmUXx50L__yskoYVSYH8xMeNNXfh5hUMsKok_v8rs6YcsznSPPdTzbpZYWpAOU2hwmng9n3UdDxCA7IzfB6TbEKnAuACrlPuGTDusBrqV4HD96_cct7ZavkgExsVHf3M5RSZoIqYTUuVdp6XcZ1ELDPwlmKM6TiqZv0j1apm644HIaEnL_bBJt5kFHN-34rkkWPVrBo39PmNj1sW3GUifEzGQX4o7pwNZuQLME3TEcw-DkaHTd4kqRX0ottesfsyz7eO-FNif_Jl-mX1EveAQJECtIG904JIFLfwsHaZcmknvFQ0z-f5CddUK74KcsdVyrhOh_9LPeOac_TQ'
                # tokenaccess = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjViZWJjNzJiZDFmNzg5MGRkOGQ2YTJjZmFjOTUzMjliZTE2MTRhZGNjYmIzNTQ5M2IwNzM0NzliN2E1Njc4ZTdjOGUzMmFlZmM2ZGI0NmJlIiwia2lkIjoiIn0.eyJhdWQiOiIxMzYiLCJqdGkiOiI1YmViYzcyYmQxZjc4OTBkZDhkNmEyY2ZhYzk1MzI5YmUxNjE0YWRjY2JiMzU0OTNiMDczNDc5YjdhNTY3OGU3YzhlMzJhZWZjNmRiNDZiZSIsImlhdCI6MTU4NTgxMzI1NSwibmJmIjoxNTg1ODEzMjU1LCJleHAiOjE1ODU4MTM1NTUsInN1YiI6Ijc4NjUzOTAxMjYwOCIsInVzZXJuYW1lIjoiamlyYXl1a25vdCJ9.uUMMWlv1dk0CqF8pRkvNyKJjMivh-S33wj_rolMOlIvWZedRyy333QcJOQGTzew6TJHemIEXg3yt-oGB_8LwSkY2nMZlwYR-i1gm0chqo8RR4bx3CYHCqhwvoc5r5Uss12D7r_9QOM7YR3LDBe6eK188d7LrzIrPzDeJALNUnWjmTFGWiReqGzTKZcy3vATiqTjYyHB67KIeXQpbHUi_mzoQwtKh239_AlaMn_1SaEeL_cKe5hsHR49YauSFbIK87gs9mvDr7xO3PqH8GaKAi6uxCp_o25R74p9_3jWzzWSeCm2ydCwGaC35Z5xJBBXEnptna2XgNvz8RkBK8zR2tA'
                # tokenaccess = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImRhY2E3ZDJiOGE4NjIwMTUwODM0ZDA3YWYyMzllODI4YTA0YjQ0ZTAwZGI2YTBjN2Q1Y2NmNjBkNjdmMzEzY2Y3OTEyN2ViMzQ4YTM3NWVhIn0.eyJhdWQiOiIxMzYiLCJqdGkiOiJkYWNhN2QyYjhhODYyMDE1MDgzNGQwN2FmMjM5ZTgyOGEwNGI0NGUwMGRiNmEwYzdkNWNjZjYwZDY3ZjMxM2NmNzkxMjdlYjM0OGEzNzVlYSIsImlhdCI6MTU4NzEzMDEwNiwibmJmIjoxNTg3MTMwMTA2LCJleHAiOjE1ODcyMTY1MDYsInN1YiI6IjM4OTgxNzgzNTAwOCIsInNjb3BlcyI6W119.Myofu7diIr7BvJwD5EStbp5Mf5JwYzAuOoSEB7YZF8p9uyGld60lemVXy8BXVri9AZi413xrANZtLiazLBORIldokt-HXd8-pod0xCsbDD2ekyMTpJNWeMJUdLGeoNs1qSg71zNeTb8Pmy3pdMP-Y5vibOvQK4vkqg0U7FtZ-B19J-5tSJnjHrzuESOwo1ff82g_zlor0kX1whE8e9hMXcUB10-Xs_rgchbj9rkaWWX6lcYz7mFIifivEEwETToAbQmSy-kWk2mnu1GK53htAlnE93EzXkb5gFi60Y5UT_y8hPGSkj5IBXRFHkj9e-pgBr6x30Fjh2-1zSgiq8iiHAkLbE3FJdh4yEUD9Z6bD2r_bloo9R3ZuzpdmTnWfNY8QVW7xEVrPPHxeHI2JeNwvzVYN_vbc-rYv2CC0_MpnPNRzYDam0AJBMEQJ0mpAHCwOQvXpKws36pFFI1lvgnCz4061_PGVDpnc8Mslf8MRTh28We0Vz1Y8UD4c-Y3R8goUrA8JbeBGmcA2RSZSRYD7fpyxHKs5J6MjeCrRxb3YIhMMHVogI_eZPSS9AXYTTw3DQc6P2mh22Elzaw8qlIO9X_qHxktaXunMxUqieuA3GsyEYoCF-9ZTwe42hZL9BRiaQxLiY1IKJKiYYwy4otJM5DVwP_dLICVlhv9EJxNCWI'
                result_token = token_required_func(tokenaccess)
                # print(result_token)
                if result_token['result'] == 'ER':
                    abort(401)
                citizen_data = str(result_token['citizen_data'])
                username = str(result_token['username']).lower()
                userId = result_token['user_id']
                emailUser = result_token['email']
                bizinfo = str(result_token['biz_info'])
                access_token_begin = int(time.time())
                access_time = datetime.datetime.fromtimestamp(access_token_begin).strftime('%Y-%m-%d %H:%M:%S')
                access_token_time = access_token_begin + 86400
                one_accesstoken = tokenaccess
                resultUpdate = update().token_formChat_v1(userId,username,str(tokenaccess),citizen_data,bizinfo)
                print(resultUpdate)
                if resultUpdate['result'] == 'OK':
                    res_selectCheckLoginUser = select().select_LoginUser(username,userId,emailUser)
                    if res_selectCheckLoginUser['result'] == 'OK':
                        res_selectCheckLoginUser['type_property'] = type_property
                        insert().insert_tran_log_v1(str(citizen_data),'OK',str(auth_toekn),one_url+"/api/account_and_biz_detail",tokenaccess)
                        return jsonify(res_selectCheckLoginUser),200
                    else:
                        generate_seCode =   'P7Rw2h5GUVE2LpbVNRBO'
                        result_refToken = generate_tokenPaperless(username,emailUser)
                        result_insert = insert().insert_login(userId,username,access_token_begin,None,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,None,getBuz,generate_seCode,None)
                        if result_insert['result'] == 'OK':
                            insert().insert_tran_log_v1(str(citizen_data),'OK',str(auth_toekn),one_url+"/api/account_and_biz_detail",tokenaccess)
                            res_selectCheckLoginUser = select().select_LoginUser(username,userId,emailUser)
                            return jsonify(res_selectCheckLoginUser),200
                        else:
                            return jsonify(result_insert),200
                else:
                    insert().insert_tran_log_v1(str('cant update login'),'ER',str(auth_toekn),one_url+"/api/account_and_biz_detail",tokenaccess)
                    return jsonify({'result':'ER','status_Code':200,'data':None,'messageER':'cant update login'}),200
            else:
                insert().insert_tran_log_v1(str('token error'),'ER',str(auth_toekn),one_url+"/api/account_and_biz_detail",tokenaccess)
                return jsonify({'result':'ER','status_Code':401,'data':None,'messageER':'token error'}),401
        else:
            return jsonify({'result':'ER','status_Code':200,'data':None,'messageER':'parameter incorrect'})

@status_methods.route('/api/v1/stoken_Login',methods=['POST'])
def stoken_Login_api_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'stoken' in dataJson and len(dataJson) == 1:
            page_token = dataJson['stoken']
            url_login_stoken = one_url + '/api/oauth/shared-token'
            info = {
                "client_id": clientId,
                "client_secret": secretKey,
                "refcode": ref_code,
                "shared_token": page_token
            }
            r_Service = callPost(url_login_stoken,info)
            if r_Service['result'] == 'OK':
                tmp_message = r_Service['messageText'].json()
                if tmp_message['result'] == 'Success':
                    tmptoken_type = tmp_message['token_type']
                    tokenaccess = tmp_message['access_token']
                    auth_toekn = tokenaccess
            else:
                r_Decode = check_and_decode_tokenfrom_chat(page_token)
                if r_Decode['result'] == 'OK':
                    tokenaccess = r_Decode['messageText']
                    auth_toekn = tokenaccess
                else:
                    abort(401)
            result_token = token_required_func(tokenaccess)
            if result_token['result'] == 'ER':
                abort(401)
            citizen_data = str(result_token['citizen_data'])
            username = str(result_token['username']).lower()
            userId = result_token['user_id']
            emailUser = result_token['email']
            bizinfo = str(result_token['biz_info'])
            access_token_begin = int(time.time())
            access_time = datetime.datetime.fromtimestamp(access_token_begin).strftime('%Y-%m-%d %H:%M:%S')
            access_token_time = access_token_begin + 86400
            one_accesstoken = tokenaccess
            resultUpdate = update().token_formChat_v1(userId,username,str(tokenaccess),citizen_data,bizinfo)
            print(resultUpdate)
            if resultUpdate['result'] == 'OK':
                res_selectCheckLoginUser = select().select_LoginUser(username,userId,emailUser)
                if res_selectCheckLoginUser['result'] == 'OK':
                    insert().insert_tran_log_v1(str(citizen_data),'OK',str(auth_toekn),one_url+"/api/account_and_biz_detail",tokenaccess)
                    return jsonify(res_selectCheckLoginUser),200
                else:
                    generate_seCode =   'P7Rw2h5GUVE2LpbVNRBO'
                    result_refToken = generate_tokenPaperless(username,emailUser)
                    result_insert = insert().insert_login(userId,username,access_token_begin,None,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,None,getBuz,generate_seCode,None)
                    if result_insert['result'] == 'OK':
                        insert().insert_tran_log_v1(str(citizen_data),'OK',str(auth_toekn),one_url+"/api/account_and_biz_detail",tokenaccess)
                        res_selectCheckLoginUser = select().select_LoginUser(username,userId,emailUser)
                        return jsonify(res_selectCheckLoginUser),200
                    else:
                        return jsonify(result_insert),200
            else:
                insert().insert_tran_log_v1(str('cant update login'),'ER',str(auth_toekn),one_url+"/api/account_and_biz_detail",tokenaccess)
                return jsonify({'result':'ER','status_Code':200,'data':None,'messageER':'cant update login'}),200
        else:
            abort(401)

@status_methods.route('/api/login_url/v1', methods=['POST'])
def login_url_chat_api_v3():
    if request.method == 'POST':
        dataJson = request.json
        if 'ipz' in dataJson and 'todo' in dataJson and 'sid' in dataJson and len(dataJson) == 3:
            res_select = select().select_Loglogin_ForLoingUrl(dataJson['ipz'],dataJson['todo'])
            print(res_select)
            if res_select['result'] == 'OK':
                res_select_CheckSID = select().select_Loglogin_CheckSID(dataJson['sid'])
                if res_select_CheckSID['result'] == 'OK':
                    username = str(res_select['messageText']['username']).lower()
                    userId = res_select['messageText']['userId']
                    emailUser = res_select['messageText']['emailUser']
                    res_selectCheckLoginUser = select().select_LoginUser(username,userId,emailUser)
                    if res_selectCheckLoginUser['result'] == 'OK':
                        return jsonify(res_selectCheckLoginUser),200
                    else:
                        return jsonify(res_selectCheckLoginUser),401
                else:
                    return jsonify(res_select_CheckSID),401
            else:
                return jsonify(res_select),401
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    else:
        return jsonify({'result':'ER','messageText':'Method Not Allowed','status_Code':405}),405

@status_methods.route('/api/v1/logout', methods=['GET'])
def logout_api_v1():
    if request.method == 'GET':
        # try:
        #     token_header = request.headers['Authorization']
        #     try:                
        #         token_header = str(token_header).split(' ')[1]
        #     except Exception as ex:
        #         return jsonify({'result':'ER','messageText':None,'messageER':'Unauthorized','status_Code':401}),401
        # except KeyError as ex:
        #     return redirect(url_paperless)
        # try:
        #     token_non_type = token_header
        #     token_header = 'Bearer ' + token_header
        #     result_verify = verify().verify_one_id(token_header)
        #     if result_verify['result'] != 'OK':
        #         return jsonify({'result':'ER','messageText':None,'messageER':'Unauthorized','status_Code':401}),401
        # except Exception as e:
        #     return jsonify({'result':'ER','messageText':None,'messageER':'Unauthorized' + str(e),'status_Code':401}),401
        # tmp_hash_token = hashlib.sha512(str(token_non_type).encode('utf-8')).hexdigest()
        # try:
        #     update().update_hashtoken_for_logout_v1(tmp_hash_token)
        # except Exception as e:
        #     return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':str(e),'data':None}})
        url = one_url + '/api/oauth/logout?redirect_url=' + url_paperless
        print(url)
        response = callGET_v3(url)
        return redirect(url_paperless)

@status_methods.route('/api/v1/register_ppl',methods=['POST'])
def register_ppl_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'Authorization' in request.headers:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                abort(401)
        else:
            return redirect(url_paperless)
        try:
            token_non_type = token_header
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                abort(401)
        except Exception as e:
            abort(401)
        if 'user_id' in dataJson and len(dataJson) == 1:
            tmp_user_id = dataJson['user_id']
            if 'messageText' not in result_verify:
                abort(401)
            tmpcontext = result_verify['messageText'].json()
            if 'id' in tmpcontext:
                if tmpcontext['id'] == tmp_user_id:
                    token_header = str(token_header).split(' ')[1]
                    ipaddress = None
                    tmp_account_biz = tmpcontext
                    username = tmp_account_biz['username']
                    ts = time.time()
                    user_id         = tmp_account_biz['id']
                    user_email      = tmp_account_biz['thai_email']
                    user_type       = tmp_account_biz['account_category']
                    one_accesstoken = str(token_header)
                    access_time     = ts
                    refresh_token   = None
                    access_token_time   = ts + 86400
                    access_token_begin  = ts
                    hash_data       = ''
                    citizen_data    = str(tmp_account_biz)
                    getBiz_details  =  tmp_account_biz['biz_detail']
                    tmp_message = None
                    tmp_todo = None
                    tmp_doing = None
                    tmp_done = None           
                    result_select = select().select_profile_for_get_project_v1(username,user_email)
                    if result_select['result'] == 'OK':
                        tmp_message = result_select['messageText']
                        tmp_status_taskchat = tmp_message['status_taskchat']
                        if tmp_status_taskchat == False:
                            result_getProject = sendtask_getProject_tochat_v1(user_id,token_header)
                            # print(result_getProject)
                            if result_getProject['result'] == 'OK':
                                tmp_message = result_getProject['messageText']
                                if tmp_message['status'] != 'fail':
                                    tmp_data = tmp_message['data'][0]
                                    tmp_state = tmp_data['state']
                                    if len(tmp_state) != 0:
                                        for u in range(len(tmp_state)):
                                            tmp_name_state = str(tmp_state[u]['name']).replace(' ','').lower()
                                            tmp_state_id = tmp_state[u]['state_id']
                                            if tmp_name_state == 'todo':
                                                tmp_todo = tmp_state_id
                                            elif tmp_name_state == 'doing':
                                                tmp_doing = tmp_state_id
                                            elif tmp_name_state == 'done':
                                                tmp_done = tmp_state_id
                        result = insert().insert_userProfile(str(username).replace(' ','').lower(),user_id,user_email,tmp_message,tmp_todo,tmp_doing,tmp_done)
                    else:
                        tmp_message = result_select['messageText']
                        tmp_status_taskchat = False
                        if 'status_taskchat' in tmp_message:
                            tmp_status_taskchat = tmp_message['status_taskchat']
                        if tmp_status_taskchat == False:
                            result_getProject = sendtask_getProject_tochat_v1(user_id,token_header)
                            if result_getProject['result'] == 'OK':
                                tmp_message = result_getProject['messageText']
                                if tmp_message['status'] != 'fail':
                                    tmp_data = tmp_message['data'][0]
                                    tmp_state = tmp_data['state']
                                    if len(tmp_state) != 0:
                                        for u in range(len(tmp_state)):
                                            tmp_name_state = str(tmp_state[u]['name']).replace(' ','').lower()
                                            tmp_state_id = tmp_state[u]['state_id']
                                            if tmp_name_state == 'todo':
                                                tmp_todo = tmp_state_id
                                            elif tmp_name_state == 'doing':
                                                tmp_doing = tmp_state_id
                                            elif tmp_name_state == 'done':
                                                tmp_done = tmp_state_id
                        result = insert().insert_userProfile(str(username).replace(' ','').lower(),user_id,user_email,tmp_message,tmp_todo,tmp_doing,tmp_done)
                    result_select   = select().select_LoginUser(username,user_id,user_email)
                    try:
                        # print(result_select)
                        if result_select['result'] == 'OK':
                            generate_seCode =   'P7Rw2h5GUVE2LpbVNRBO'
                            result_refToken = generate_tokenPaperless(username,user_email)
                            result_update = update().update_LoginUser(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress)
                            resultUpdateLog = update().update_LogLoingBiz(username,user_id,getBiz_details)
                        else:
                            result_insert = {}
                            result_insert['result'] = 'OK'
                            generate_seCode = 'P7Rw2h5GUVE2LpbVNRBO'
                            result_refToken = generate_tokenPaperless(username,user_email)
                            result_insert = insert().insert_login(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress)
                            result_BizLoing = insert().insert_LogBizLogin(username,user_id,getBiz_details)
                        insert().insert_UserLog(username,user_id,ipaddress,user_email)
                    except Exception as ex:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        insert().insert_tran_log_v1('error','ER',"","/api/v3/login_citizen","")
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'connection db fail ' + str(ex)})
                    try:
                        citizen_data = eval(citizen_data)
                    except Exception as ex:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'ไม่สามารถแปลง data เป็น Json ได้'})
                    biz_info = []
                    check_biz_id = []
                    if 'biz_detail' in tmp_account_biz:                        
                        for i in range(len(tmp_account_biz['biz_detail'])):
                            result_Select_Check_biz = select().select_checkBizPaperless(tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num'])
                            if result_Select_Check_biz['result'] == 'OK':
                                
                                if tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num'] not in check_biz_id:
                                    # print(getBuz['biz_detail'][i]['getbiz'][0]['id_card_num'],'idcard')
                                    check_biz_id.append(tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num'])
                                    data_get_my_dep = {
                                        "tax_id": tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num']
                                    }
                                    text_one_access = 'Bearer ' + one_accesstoken
                                    resultCallAuth_get_dep = callGET_v2(one_url+'/api/v1/service/business/account/'+user_id+'/department_role?tax_id=' + tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num'],text_one_access)
                                    # print(resultCallAuth_get_dep)
                                    dep_id_list = []
                                    dept_name_list = []
                                    position_list = []
                                    jsonData = {}
                                    if resultCallAuth_get_dep['result'] == 'OK':
                                        res_json = resultCallAuth_get_dep['messageText'].json()
                                        # print(res_json)
                                        if res_json['data'] != None:
                                            
                                            data_res = res_json['data']
                                            if data_res != '':
                                                for y in range(len(data_res)):
                                                    dep_id = (data_res[y]['dept_id'])
                                                    # print(dep_id)
                                                    if dep_id != '' and dep_id != None:
                                                        dep_id_list.append(dep_id)
                                                        dep_data = data_res[y]['department']
                                                        for iy in range(len(dep_data)):
                                                            dept_name_list.append(dep_data[iy]['dept_name'])
                                                            try:
                                                                position_list.append(dep_data[iy]['dept_position'])
                                                            except Exception as e:
                                                                position_list.append('')
                                                    elif dep_id != None:
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
                                                        dep_data = []
                                                        dept_name_list = []
                                                        position_list = []
                                            else:
                                                dep_id_list = []
                                                dep_data = []
                                                dept_name_list = []
                                                position_list = []
                                        else:
                                            jsonData = {}
                                            dep_id_list = []
                                            dep_data = []
                                            dept_name_list = []
                                            position_list = []
                                        # print(getBuz['biz_detail'][i]['getbiz'])
                                        jsonData = {
                                            'id':tmp_account_biz['biz_detail'][i]['getbiz'][0]['id'],
                                            'first_name_th':tmp_account_biz['biz_detail'][i]['getbiz'][0]['first_name_th'],
                                            'first_name_eng':tmp_account_biz['biz_detail'][i]['getbiz'][0]['first_name_eng'],
                                            'id_card_type':tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_type'],
                                            'id_card_num':tmp_account_biz['biz_detail'][i]['getbiz'][0]['id_card_num'],
                                            'role_level':tmp_account_biz['biz_detail'][i]['getrole'][0]['role_level'],
                                            'role_id':tmp_account_biz['biz_detail'][i]['getrole'][0]['id'],
                                            'role_name':tmp_account_biz['biz_detail'][i]['getrole'][0]['role_name'],
                                            'dept_id':dep_id_list,
                                            'dept_name':dept_name_list,
                                            'dept_position':position_list
                                        }
                                        # print(jsonData)
                                        biz_info.append(jsonData)
                    else:
                        biz_info = []
                    return jsonify({'result':'OK','messageText':{'message':'succuess','data':None},'messageER':None,'status_Code':200}),200
                else:
                    abort(401)
            else:
                abort(401)
        else:
            abort(404)

