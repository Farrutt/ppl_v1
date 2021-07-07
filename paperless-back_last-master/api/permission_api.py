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



if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less


@status_methods.route('/api/v2/set_permission', methods=['POST'])
# @token_required
def set_permission_v2():  #สร้างรูปแบบ permission ลงใน db 
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
                token_required = token_required_func(token_header)
                username = token_required['username']
                email = token_required['email']
                print ('username: ',username)
                print ('email: ',email)
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            result_level = select().select_level_admin_v1(username,email)
            result_level_eval = eval(str(result_level))
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                if level_admin == None :
                    return jsonify({'result':'OK','messageText':None,'status_Code':200,'messageER':'level_admin not found'}),200
                elif int(level_admin) == 1 :
                    return jsonify({'result':'OK','messageText':None,'status_Code':200,'messageER':'level_admin 1 can not set permission'}),200
                elif int(level_admin) == 0 :
                    datajson = request.json
                    if 'name' in datajson and 'role_level' in datajson and 'permission_doc_type' in datajson and 'permission_doc_format' in datajson and 'permission_cancel_doc' in datajson and 'permission_view_doc' in datajson and 'permission_sign_doc' in datajson and 'permission_create_doc' in datajson and 'permission_send_approve' in datajson and len(datajson) == 9:
                        name = datajson['name']
                        role_level = datajson['role_level']
                        permission_doc_type = datajson['permission_doc_type']
                        permission_doc_format = datajson['permission_doc_format']
                        permission_cancel_doc = datajson['permission_cancel_doc']
                        permission_view_doc = datajson['permission_view_doc']
                        permission_sign_doc = datajson['permission_sign_doc']
                        permission_create_doc = datajson['permission_create_doc']
                        permission_send_approve = datajson['permission_send_approve']

                        result_select = select_4().select_permission_v2(name)
                        if result_select['result'] == 'OK':
                            result_insert = insert_4().insert_permission_v2(name,role_level,permission_doc_type,permission_doc_format,permission_cancel_doc,permission_view_doc,permission_sign_doc,permission_create_doc,permission_send_approve)
                            return jsonify({'result':'OK','messageText':result_insert['messageText'],'messageER':None,'status_Code':200}),200
                        else:
                            return jsonify({'result':'OK','messageText':result_select['messageText'],'messageER':None,'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'parameter incorrect','data':[]}}),200   
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'your level_admin can not set permission','data':[]}}),200   

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200
        finally:
            db.session.close()



@status_methods.route('/api/v2/update_permission', methods=['POST'])
# @token_required
def update_permission_v2(): # update รูปแบบ permission ใน db
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
                token_required = token_required_func(token_header)
                username = token_required['username']
                email = token_required['email']
                print ('username: ',username)
                print ('email: ',email)
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            result_level = select().select_level_admin_v1(username,email)
            result_level_eval = eval(str(result_level))
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                if level_admin == None :
                    return jsonify({'result':'OK','messageText':None,'status_Code':200,'messageER':'level_admin not found'}),200
                elif int(level_admin) == 1 :
                    return jsonify({'result':'OK','messageText':None,'status_Code':200,'messageER':'level_admin 1 can not set permission'}),200
                elif int(level_admin) == 0 :
                    datajson = request.json
                    if 'id' in datajson and 'name' in datajson and 'role_level' in datajson and 'permission_doc_type' in datajson and 'permission_doc_format' in datajson and 'permission_cancel_doc' in datajson and 'permission_view_doc' in datajson and 'permission_sign_doc' in datajson and 'permission_create_doc' in datajson and 'permission_send_approve' in datajson and len(datajson) == 10:
                        id_permis = datajson['id']
                        name = datajson['name']
                        role_level = datajson['role_level']
                        permission_doc_type = datajson['permission_doc_type']
                        permission_doc_format = datajson['permission_doc_format']
                        permission_cancel_doc = datajson['permission_cancel_doc']
                        permission_view_doc = datajson['permission_view_doc']
                        permission_sign_doc = datajson['permission_sign_doc']
                        permission_create_doc = datajson['permission_create_doc']
                        permission_send_approve = datajson['permission_send_approve']
                        # result_select = permis_select().select_permission_v2(name)
                        # if result_select['result'] == 'ER':
                        result_update = update_4().update_permission_v2(id_permis,name,role_level,permission_doc_type,permission_doc_format,permission_cancel_doc,permission_view_doc,permission_sign_doc,permission_create_doc,permission_send_approve)
                        return jsonify({'result':'OK','messageText':result_update['messageText'],'messageER':None,'status_Code':200}),200
                        # else:
                            # return jsonify({'result':'OK','messageText':result_select['messageText'],'messageER':None,'status_Code':200}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'parameter incorrect','data':[]}}),200   
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'your level_admin can not set permission','data':[]}}),200   
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200
        finally:
            db.session.close()



@status_methods.route('/api/v2/get_permission',methods=['GET'])
def get_detail_permission_v2(): # get permission ออกมาตาม id
    if request.method == 'GET':
        try:
            if request.args.get('permission_id') != None :
                permission_id = request.args.get('permission_id')
                result = select_4().select_permission_detail_v2(permission_id)
                if result['result'] == 'OK':            
                    return jsonify({'result':'OK','messageText':{'message':'success' ,'data': result['messageText']},'status_Code':200,'messageER':None})
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result['messageText'],'data':None}})
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404
        except Exception as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':str(ex)}),404
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'method incorrct'}),404



@status_methods.route('/api/v1/insert_permission_userid',methods=['POST'])
def insert_permission_userid(): # insert permission_id ให้กับ user ตาม id ที่ใส่มา
    if request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            token_header = str(token_header).split(' ')[1]
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
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
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        try:   
            result_level = select().select_level_admin_v1(username,email)
            result_level_eval = eval(str(result_level))      
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                print(username,email,level_admin)
                if int(level_admin) == 0:                    
                    dataJson = request.json
                    if 'id_user' in dataJson and 'permission_id' in dataJson:
                        id_user =  dataJson['id_user']
                        permission = dataJson['permission_id']
                        result_select = select_4().select_permission_id(permission)
                        if result_select['result'] == 'OK':
                            result = insert_4().insert_permission_user(id_user,permission)
                            if result['result'] == 'OK':            
                                return jsonify({'result':'OK','messageText':'succuess','status_Code':200,'messageER':None})
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result['messageText'],'data':None}})      
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_select['messageText']})      
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrct'}),404
                else:
                    return jsonify({'result':'OK','messageText':None,'status_Code':404,'messageER':'level admin not set permission'}),200
            else:
                return jsonify({'result':'OK','messageText':None,'status_Code':404,'messageER':'level admin incorret'}),200
        except Exception as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'insert permission fail!'}),200
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'method incorrct'}),404



@status_methods.route('/api/v1/set_permission_all',methods=['POST'])
def set_permission_all(): # เซ็ท permission (id default) ให้กับทุก user ที่เป็น null ในฟิล permission_id 
    if request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            token_header = str(token_header).split(' ')[1]
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
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
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        try:   
            result_level = select().select_level_admin_v1(username,email)
            result_level_eval = eval(str(result_level))      
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                print(username,email,level_admin)
                if int(level_admin) == 0:                    
                    permission_id = '14b8cf08-9476-4906-be15-da7e01b977ee'
                    result = insert_4().insert_permission_all(permission_id)
                    if result['result'] == 'OK':            
                        return jsonify({'result':'OK','messageText':{'message':'success' ,'data': result['messageText']},'status_Code':200,'messageER':None})
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result['messageText'],'data':None}})  
                else:
                    return jsonify({'result':'OK','messageText':None,'status_Code':404,'messageER':'level admin not set permission'}),200
            else:
                return jsonify({'result':'OK','messageText':None,'status_Code':404,'messageER':'level admin incorret'}),200
        except Exception as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':str(ex)}),404
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'method incorrct'}),404   



@status_methods.route('/api/v1/set_permission_all_with_id',methods=['POST'])
def set_permission_all_with_id():# เซ็ท permission (id ที่ใส่) ให้กับทุก user ที่เป็น null ในฟิล permission_id 
    if request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            token_header = str(token_header).split(' ')[1]
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
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
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        try:   
            result_level = select().select_level_admin_v1(username,email)
            result_level_eval = eval(str(result_level))      
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                print(username,email,level_admin)
                if int(level_admin) == 0:   
                    dataJson = request.json
                    if 'permission_id' in dataJson:
                        permission_id =  dataJson['permission_id']
                        print(permission_id)
                        result = insert_4().insert_permission_all_v2(permission_id)
                        if result['result'] == 'OK':            
                            return jsonify({'result':'OK','messageText':{'message':'success' ,'data': result['messageText']},'status_Code':200,'messageER':None})
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result['messageText'],'data':None}})
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404  
                else:
                    return jsonify({'result':'OK','messageText':None,'status_Code':404,'messageER':'level admin not set permission'}),200
            else:
                return jsonify({'result':'OK','messageText':None,'status_Code':404,'messageER':'level admin incorret'}),200
        except Exception as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':str(ex)}),404
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'method incorrct'}),404   

@status_methods.route('/api/v1/remove_permission', methods=['POST'])
# @token_required
def remove_permission():  #ลบ permission
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
                token_required = token_required_func(token_header)
                username = token_required['username']
                email = token_required['email']
                print ('username: ',username)
                print ('email: ',email)
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            result_level = select().select_level_admin_v1(username,email)
            result_level_eval = eval(str(result_level))
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                if level_admin == None :
                    return jsonify({'result':'OK','messageText':None,'status_Code':200,'messageER':'level_admin not found'}),200
                elif int(level_admin) == 1 :
                    return jsonify({'result':'OK','messageText':None,'status_Code':200,'messageER':'level_admin 1 can not set permission'}),200
                elif int(level_admin) == 0 :
                    datajson = request.json
                    if 'id' in datajson and len(datajson) == 1:
                        id_permis = datajson['id']
                        # result_remove_permis = delete_4().set_null_user(id_permis)
                        # return jsonify({'result':'OK','messageText':'Remove permission success','status_Code':200,'messageER':None}),200
                        result_delete_permis = delete_4().remove_permission(id_permis)
                        if result_delete_permis['result'] == 'OK':
                            result_remove_permis = delete_4().set_null_user(id_permis)
                            return jsonify({'result':'OK','messageText':'Remove permission success','status_Code':200,'messageER':None}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_delete_permis['messageER']}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'parameter fails'}),200   
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'your level_admin can not set permission','data':[]}}),200   
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200
        finally:
            db.session.close()