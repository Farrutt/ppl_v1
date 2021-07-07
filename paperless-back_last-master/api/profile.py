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
from controller.mail_string import *
from controller.validate import *
from db.db_method import *
# from db.db_method_1 import *
# from db.db_method_2 import *
# from db.db_method_3 import *
# from db.db_method_4 import *
# from db.db_method_5 import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from api.file import *
from method.sftp_fucn import *
from method.callwebHook import *

@status_methods.route('/api/profile',methods=['POST','PUT','GET'])
@token_required
def profile_api():
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
        tmp_message = None
        tmp_todo = None
        tmp_doing = None
        tmp_done = None
        if 'username' in dataJson and 'userid' in dataJson and 'email_thai' in dataJson and len(dataJson) == 3:
            tmp_userid = dataJson['userid']
            result_getProject = sendtask_getProject_tochat_v1(tmp_userid,token_header)
            if result_getProject['result'] == 'OK':
                tmp_message = result_getProject['messageText']
                if 'data' in tmp_message:
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
                    else:
                        tmp_message = None
                        tmp_todo = None
                        tmp_doing = None
                        tmp_done = None
                else:
                    tmp_message = None
                    tmp_todo = None
                    tmp_doing = None
                    tmp_done = None
            result = insert().insert_userProfile(str(dataJson['username']).replace(' ','').lower(),dataJson['userid'],dataJson['email_thai'],tmp_message,tmp_todo,tmp_doing,tmp_done)
            if result['result'] == 'OK':
                return jsonify({'result':'OK','messageER':None,'messageText':'insert user ok','status_Code':200})
            else:
                return jsonify({'result':'ER','messageER':'duplicate Username!','messageText':None,'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'PUT':
        dataJson = request.json
        if 'username' in dataJson and 'userid' in dataJson and 'webhook' in dataJson and 'signString' in dataJson and 'email' in dataJson:
            result_update = update().update_userProfile(dataJson)
            if result_update['result'] == 'OK':
                return jsonify({'result':'OK','messageER':None,'messageText':result_update['messageText'],'status_Code':200})
            else:
                return jsonify({'result':'ER','messageER':result_update['messageText'],'messageText':None,'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        if (request.args.get('username')) != None:
            username_oneth = str(request.args.get('username')).replace(' ','')
            res_selectUserProfile = select().select_UserProfile(username_oneth)
            if res_selectUserProfile['result'] == 'OK':
                return jsonify(res_selectUserProfile),200
            else:
                return jsonify(res_selectUserProfile),200
        else:
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404

@status_methods.route('/api/v1/profile',methods=['POST','PUT','GET'])
@token_required_v3
def profile_api_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'username' in dataJson and 'userid' in dataJson and 'email_thai' in dataJson:
            tmpemail_thai2 = None
            tmpemail_thai3 = None
            employee_email = None
            if 'email_thai2' in dataJson:
                tmpemail_thai2 = dataJson['email_thai2']
            if 'email_thai3' in dataJson:
                tmpemail_thai3 = dataJson['email_thai3']
            if 'employee_email' in dataJson:
                employee_email = dataJson['employee_email']
            tmp_message = None
            tmp_todo = None
            tmp_doing = None
            tmp_done = None           
            tmp_userid = dataJson['userid']
            result_select = select().select_profile_for_get_project_v1(dataJson['username'],dataJson['email_thai'])
            if result_select['result'] == 'OK':
                tmp_message = result_select['messageText']
                tmp_status_taskchat = tmp_message['status_taskchat']
                tmp_sign_ca = tmp_message['sign_ca']
                if tmp_sign_ca == None or tmp_sign_ca == 'N':
                    token_auth = 'Bearer ' + token_header
                    result_data = credentials_list_v3("","","","","",token_auth)
                    if result_data['result'] == 'OK':
                        tmpmsg = result_data['msg']
                        if 'totalResult' in tmpmsg:
                            if tmpmsg['totalResult'] > 0:
                                tmp_sign_ca = 'Y'
                if tmp_status_taskchat == False:
                    result_getProject = sendtask_getProject_tochat_v1(tmp_userid,token_header)
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
                result = insert().insert_userprofile_v1(str(dataJson['username']).replace(' ','').lower(),dataJson['userid'],dataJson['email_thai'],tmpemail_thai2,tmpemail_thai3,employee_email,tmp_message,tmp_todo,tmp_doing,tmp_done,signca=tmp_sign_ca)
                # result = insert().insert_userProfile(str(dataJson['username']).replace(' ','').lower(),dataJson['userid'],dataJson['email_thai'],tmp_message,tmp_todo,tmp_doing,tmp_done,p_signca=tmp_sign_ca)
                result_insert = insert_3().insert_status_notification_v2(tmp_userid)
                if result['result'] == 'OK':
                    return jsonify({'result':'OK','messageER':None,'messageText':{'data':None,'message':'success get project success'},'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageER':{'data':None,'message':result['messageText']},'messageText':None,'status_Code':200}),200
            else:
                tmp_message = result_select['messageText']
                tmp_status_taskchat = False
                tmp_sign_ca = 'N'
                token_auth = 'Bearer ' + token_header
                result_data = credentials_list_v3("","","","","",token_auth)
                if result_data['result'] == 'OK':
                    tmpmsg = result_data['msg']
                    if 'totalResult' in tmpmsg:
                        if tmpmsg['totalResult'] > 0:
                            tmp_sign_ca = 'Y'
                if 'status_taskchat' in tmp_message:
                    tmp_status_taskchat = tmp_message['status_taskchat']
                if tmp_status_taskchat == False:
                    result_getProject = sendtask_getProject_tochat_v1(tmp_userid,token_header)
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
                # print(str(dataJson['username']).replace(' ','').lower(),dataJson['userid'],dataJson['email_thai'],tmpemail_thai2,tmpemail_thai3,tmp_message,tmp_todo,tmp_doing,tmp_done,tmp_sign_ca)
                result = insert().insert_userprofile_v1(str(dataJson['username']).replace(' ','').lower(),dataJson['userid'],dataJson['email_thai'],tmpemail_thai2,tmpemail_thai3,employee_email,tmp_message,tmp_todo,tmp_doing,tmp_done,signca=tmp_sign_ca)
                # result = insert().insert_userProfile(str(dataJson['username']).replace(' ','').lower(),dataJson['userid'],dataJson['email_thai'],tmp_message,tmp_todo,tmp_doing,tmp_done,p_signca=tmp_sign_ca)
                result_insert = insert_3().insert_status_notification_v2(tmp_userid)
                if result['result'] == 'OK':
                    return jsonify({'result':'OK','messageER':None,'messageText':{'data':None,'message':'success non get project'},'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageER':{'data':None,'message':result['messageText']},'messageText':None,'status_Code':200}),200
        else:
            abort(404)
    elif request.method == 'PUT':
        dataJson = request.json
        if 'username' in dataJson and 'userid' in dataJson and 'webhook' in dataJson and 'email' in dataJson and 'signString' in dataJson and 'options_profile' in dataJson and len(dataJson) == 6:
            tmp_userid = dataJson['userid']
            result_update = update().update_userProfile_v1(dataJson)
            result_insert = insert_3().insert_status_notification_v2(tmp_userid)
            if result_update['result'] == 'OK':
                return jsonify({'result':'OK','messageER':None,'messageText':{'message':result_update['messageText'],'data':None},'status_Code':200})
            else:
                return jsonify({'result':'ER','messageER':{'message':result_update['messageText'],'data':None},'messageText':None,'status_Code':200}),200
        else:
            abort(404)
            return jsonify({'result':'ER','messageText':'Parameter Fail!','status_Code':404}),404
    elif request.method == 'GET':
        tmp_username = request.args.get('username')
        if tmp_username != None:
            username_oneth = str(tmp_username).replace(' ','')
            res_selectUserProfile = select_4().select_data_Userprofile_v1(username_oneth)
            if res_selectUserProfile['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'data':res_selectUserProfile['data'],'message':'get data success'},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'data':res_selectUserProfile['data'],'message':'get data fail'},'status_Code':200}),200
        else:
            abort(404)

def profile_func_v1(tmp_userid,tmp_username,tmp_emailthai,tmp_token_header):
    tmp_message = None
    tmp_todo = None
    tmp_doing = None
    tmp_done = None
    result_select = select().select_profile_for_get_project_v1(tmp_username,tmp_emailthai)
    if result_select['result'] == 'OK':
        tmp_message = result_select['messageText']
        tmp_status_taskchat = tmp_message['status_taskchat']
        if tmp_status_taskchat == False:
            result_getProject = sendtask_getProject_tochat_v1(tmp_userid,tmp_token_header)
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
        result = insert().insert_userProfile(str(tmp_username).replace(' ','').lower(),tmp_userid,tmp_emailthai,tmp_message,tmp_todo,tmp_doing,tmp_done)
        if result['result'] == 'OK':
            return jsonify({'result':'OK','messageER':None,'messageText':{'data':None,'message':'success get project success'},'status_Code':200}),200
            # return jsonify({'result':'OK','messageER':None,'messageText':result['messageText'],'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageER':{'data':None,'message':result['messageText']},'messageText':None,'status_Code':200}),200
    else:
        tmp_message = result_select['messageText']
        tmp_status_taskchat = False
        if 'status_taskchat' in tmp_message:
            tmp_status_taskchat = tmp_message['status_taskchat']
        if tmp_status_taskchat == False:
            result_getProject = sendtask_getProject_tochat_v1(tmp_userid,tmp_token_header)
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
        result = insert().insert_userProfile(str(tmp_username).replace(' ','').lower(),tmp_userid,tmp_emailthai,tmp_message,tmp_todo,tmp_doing,tmp_done)
        if result['result'] == 'OK':
            return jsonify({'result':'OK','messageER':None,'messageText':{'data':None,'message':'success non get project'},'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageER':{'data':None,'message':result['messageText']},'messageText':None,'status_Code':200}),200

@status_methods.route('/api/v1/showtheme',methods=['POST'])
def showtheme_setting():
    list_id_card_num = []
    if request.method == 'POST':
        dataForm = request.form
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
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
            print('list_id_card_num',list_id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)}),401
        if 'tax_id' in dataForm :
            tmp_tax_id = dataForm['tax_id']
            if tmp_tax_id in list_id_card_num :
                result_update = select_1().select_theme(tmp_tax_id)
                if result_update['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':result_update['messageText'],'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':tmp_tax_id +' update fail ' + result_update['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'user not in business'+str(tmp_tax_id)}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404



