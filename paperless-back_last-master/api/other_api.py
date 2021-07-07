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
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from api.file import *
from api.onebox import *
from method.sftp_fucn import *
from method.callwebHook import *
from api.beone import *
# from api.api3 import *



if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less

@status_methods.route('/api/v3/other_service', methods=['POST'])
# @token_required_v3
def other_service_api_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
                token_required = token_required_func(token_header)
                username = token_required['username']
                user_id = token_required['user_id']

            except Exception as ex:
                abort(401)
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'sidCode' in dataJson and len(dataJson) == 1:
            now = datetime.datetime.now()
            sid_code = dataJson['sidCode']
            json_data = [
                {"name_service":"RPA","status":True,"other":[{"path_folder":"/Create/CSPOC","url_path":""}]},
                {"name_service":"DMS","status":False,"other":[{"path_folder":"","url_path":""}]},
                {"name_service":"WEBHOOK","status":True,"other":[{"path_folder":"","url_path":"https://google.co.th"}]},
                # {"name_service":"EFORM","status":True,"other":[{"path_folder":"","url_path":""}]},
                {"name_service":"ONEBOX","status":True,"other":[{"path_folder":"","url_path":""}]}
            ]
            tax_id = ['0107544000094','5513213355654','7200767062847','5201285728555','3897235192540','0105538109282','5292833186265','0105538109282','0105544049695']
            result_documenttype = select().select_document_type_forOthers_v1(sid_code,tax_id)
            result_select = select().select_sid_code_status_v1(sid_code)
            # print(result_documenttype , 'result_select')
            # return ''
            tmp_list_service = []
            if result_documenttype['result'] == 'OK':
                tmp_message = result_documenttype['messageText']
                if tmp_message != None:
                    # print(result_documenttype, ' result_documenttype')
                    tmp_documentType = result_select['messageText']['Document_Details'][0]['document_type']
                    tmp_relativePath = tmp_documentType + '/' + str(now.year) + '/' + str('{:02d}'.format(now.month))
                    # print()
                    # print(tmp_relativePath)
                    tmp_message = eval(tmp_message)
                    for y in range(len(json_data)):
                        tmp_data = json_data[y]
                        for t in range(len(tmp_message)):
                            tmp_message_data = tmp_message[t]
                            if 'name_service' in tmp_message_data:
                                if tmp_data['name_service'] == tmp_message_data['name_service']:
                                    tmp_data = tmp_message_data
                                    tmp_list_service.append(tmp_data)
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'non business','data':None},'status_Code':200}),200
            if len(tmp_list_service) != 0:                                 
                json_data =  tmp_list_service
            else:
                json_data = json_data
            if result_select['result'] == 'OK':
                get_status_file = result_select['messageText']['Document_Details'][0]['status_file_code']
                get_documentType = result_select['messageText']['Document_Details'][0]['document_type']
                # print(get_status_file)
                # get_status_file = 'Y'
                if get_status_file == 'Y':
                    result_select_data = select().select_ForWebHook(sid_code)
                    # print(result_select_data, 'result_select_data')
                    if get_documentType == 'QTS':
                        r = select_1().select_info_document(sid_code)
                        print(r)
                    list_documentType = ['cspoc','cs','scs','tm']
                    for u in range(len(json_data)):
                        data = json_data[u]
                        if data['name_service'] == 'RPA':
                            if data['status'] == True:
                                print('RPA')
                                result_select_action = select().select_get_action_and_status('robot')
                                # print(result_select_action)
                                if result_select_action['result'] == 'OK':
                                    if result_select_action['messageText']['status'] == True:
                                        resultselect_attm_file = select().select_attm_file_v1_for_chat_api_to_robot(sid_code)
                                        # print(resultselect_attm_file)
                                        if resultselect_attm_file['result'] == 'OK':
                                            doc_id = resultselect_attm_file['messageText']['document_Id']
                                            pathFolder = resultselect_attm_file['messageText']['pathfolder']
                                            json_Data_File = resultselect_attm_file['messageText']['json_data']
                                            username_sender = resultselect_attm_file['messageText']['sender_username']
                                            document_Type = resultselect_attm_file['messageText']['document_Type']
                                            if document_Type in list_documentType:
                                                result_file_last_pdf  =select().select_file_sign_last_to_email(sid_code)
                                                if result_file_last_pdf['result'] == 'OK':
                                                    pdf_base64_sign = result_file_last_pdf['messageText']
                                                    file_name_sign_pdf = result_file_last_pdf['file_name']
                                                    
                                                    sftp_robot().send_file_tosftp_new_v2(json_Data_File,pathFolder,'',document_Type,doc_id,pdf_base64_sign,file_name_sign_pdf,sid_code)
                                                    insert().insert_transaction_servicelog_v1(data['name_service'],'OK',sid_code,'upload sftp complete',token_header)
                                                else:
                                                    insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'data not found file',token_header)
                                        else:
                                            doc_id = resultselect_attm_file['messageText']['document_Id']
                                            username_sender = resultselect_attm_file['messageText']['sender_username']
                                            document_Type = resultselect_attm_file['messageText']['document_Type']
                                            if document_Type in list_documentType:
                                                result_file_last_pdf  =select().select_file_sign_last_to_email(sid_code)
                                                if result_file_last_pdf['result'] == 'OK':
                                                    pdf_base64_sign = result_file_last_pdf['messageText']
                                                    file_name_sign_pdf = result_file_last_pdf['file_name']
                                                    
                                                    sftp_robot().send_file_tosftp_new_v2('','','',document_Type,doc_id,pdf_base64_sign,file_name_sign_pdf,sid_code)
                                                    insert().insert_transaction_servicelog_v1(data['name_service'],'OK',sid_code,'upload sftp complete and not attachment file',token_header)
                                                else:
                                                    insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'data not found file',token_header)
                                            # insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'data not found attachment')
                        elif data['name_service'] == 'WEBHOOK':
                            if data['status'] == True:
                                response = None
                                print('WEBHOOK')
                                result_select = select().select_ForWebHook(sid_code)
                                # print(result_select['result'] + '' +result_select['messageText'])
                                if result_select['result'] == 'OK' and str(result_select['messageText']['webHook']).replace(' ','') != '':
                                    del(result_select['messageText']['email_center'])
                                    # result_select['messageText']['PDF_String'] = None
                                    # print(result_select)
                                    webhook_Data = result_select['messageText']
                                    try:
                                        # print(result_select['messageText']['webHook'])
                                        response = requests.post(result_select['messageText']['webHook'], json=webhook_Data,headers={'Content-Type': 'application/json'},timeout=10,verify=False)
                                        logger.info('webhook success')
                                        insert().insert_tran_log_v1('','OK',str(webhook_Data),result_select['messageText']['webHook'],'','')
                                    except requests.HTTPError as err:
                                        logger.info('webhook fail')
                                        insert().insert_tran_log_v1('','ER',str(webhook_Data),result_select['messageText']['webHook'],'','')
                                        pass
                                    except requests.Timeout as err:
                                        logger.info('webhook fail')
                                        insert().insert_tran_log_v1('','ER',str(webhook_Data),result_select['messageText']['webHook'],'','')
                                        pass
                                    except requests.ConnectionError as err:
                                        logger.info('webhook fail')
                                        insert().insert_tran_log_v1('','ER',str(webhook_Data),result_select['messageText']['webHook'],'','')
                                        pass
                                    except Exception as ex:
                                        logger.info('webhook fail')
                                        logger.info(str(ex))
                                        insert().insert_tran_log_v1('','ER',str(webhook_Data),result_select['messageText']['webHook'],'','')
                                        pass
                        elif data['name_service'] == 'DMS':
                            if data['status'] == True:
                                print('DMS')
                                datajson_properties = {}
                                data_properties_to_dms = {}
                                tmp_file_name = result_select_data['messageText']['fileName']
                                result_select_action = select().select_get_action_and_status('dms')
                                if result_select_action['result'] == 'OK':
                                    if result_select_action['messageText']['status'] == True:                                        
                                        result_docuemnt_data = select().select_pty_file_pdf_v1(sid_code)
                                        if result_docuemnt_data['result'] == 'OK':
                                            msg_data = result_docuemnt_data['msg']['options_page']
                                            if 'service_properties' in msg_data:
                                                tmp_service_properties = msg_data['service_properties']
                                                for z in range(len(tmp_service_properties)):
                                                    tmp_name_service = tmp_service_properties[z]['name_service']
                                                    tmp_other = tmp_service_properties[z]['other']
                                                    for iu in range(len(tmp_other)):
                                                        if 'properties' in tmp_other[iu]:
                                                            tmp_properties = tmp_other[iu]['properties']
                                                            for zyu in range(len(tmp_properties)):
                                                                tmp_name_data = tmp_properties[zyu]['name'] 
                                                                tmp_value_data =tmp_properties[zyu]['value'] 
                                                                if str(tmp_name_data).replace(' ','') != '':
                                                                    datajson_properties['Doc:'+tmp_name_data] = tmp_value_data
                                                if datajson_properties != {}:
                                                    result_login = step_1_login_dms_v1(token_header)
                                                    if result_login['result'] == 'OK':
                                                        insert().insert_transaction_servicelog_v1(data['name_service'],'OK',sid_code,'login ok ' + str(result_login['msg']),token_header)
                                                        result_attm_file = select().select_attm_file_v1_for_chat_api_to_robot(sid_code)
                                                        if result_attm_file['result'] == 'OK':
                                                            doc_id = result_attm_file['messageText']['document_Id']
                                                            pathFolder = result_attm_file['messageText']['pathfolder']
                                                            json_Data_File = result_attm_file['messageText']['json_data']
                                                            username_sender = result_attm_file['messageText']['sender_username']
                                                            document_Type = result_attm_file['messageText']['document_Type']                                                        
                                                            
                                                            result_file_last_pdf  =select().select_file_sign_last_to_email(sid_code)
                                                            if result_file_last_pdf['result'] == 'OK':
                                                                path = path_global_1 + '/storage/pdf/' + doc_id
                                                                # path = './storage/pdf/' + doc_id
                                                                if not os.path.exists(path):
                                                                    os.makedirs(path) 
                                                                pdf_base64_sign = result_file_last_pdf['messageText']
                                                                file_name_sign_pdf = result_file_last_pdf['file_name']
                                                                with open(path + '/' + file_name_sign_pdf, "wb") as fh:
                                                                    fh.write(base64.b64decode(pdf_base64_sign))
                                                                path_pdf = path + '/' + file_name_sign_pdf
                                                                token_dms = result_login['msg']['entry']['id']
                                                                for x in range(len(json_Data_File)): 
                                                                    path_pdf_attm = '.' + pathFolder  + json_Data_File[x]['file_name_new']
                                                                    # print(datajson_properties)
                                                                    datajson_properties['name'] = json_Data_File[x]['file_name_original']
                                                                    datajson_properties['relativePath'] = tmp_relativePath
                                                                    data_properties_to_dms = {
                                                                        "properties":[datajson_properties]
                                                                    }
                                                                    # print(datajson_properties)
                                                                    data_properties_to_dms = str(data_properties_to_dms) 
                                                                    step_2_upload_dms_v1(token_dms,'',path_pdf_attm,json_Data_File[x]['file_name_original'],'','',data_properties_to_dms,token_header)
                                                                datajson_properties['name'] = tmp_file_name
                                                                datajson_properties['relativePath'] = tmp_relativePath
                                                                data_properties_to_dms = {
                                                                    "properties":[datajson_properties]
                                                                }
                                                                data_properties_to_dms = str(data_properties_to_dms) 
                                                                step_2_upload_dms_v1(token_dms,'',path_pdf,file_name_sign_pdf,'','',data_properties_to_dms,token_header)
                                                                insert().insert_transaction_servicelog_v1(data['name_service'],'OK',sid_code,'have attm file ' + str(result_attm_file['messageText']),token_header)
                                                            else:
                                                                insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'cant upload pdf sign file' + str(result_file_last_pdf['messageText']),token_header) 
                                                        else:
                                                            doc_id = result_attm_file['messageText']['document_Id']
                                                            username_sender = result_attm_file['messageText']['sender_username']
                                                            document_Type = result_attm_file['messageText']['document_Type']  
                                                            result_file_last_pdf  =select().select_file_sign_last_to_email(sid_code)                                                     
                                                            if result_file_last_pdf['result'] == 'OK':
                                                                path = path_global_1 + '/storage/pdf/' + doc_id
                                                                # path = './storage/pdf/' + doc_id
                                                                if not os.path.exists(path):
                                                                    os.makedirs(path) 
                                                                pdf_base64_sign = result_file_last_pdf['messageText']
                                                                file_name_sign_pdf = result_file_last_pdf['file_name']
                                                                with open(path + '/' + file_name_sign_pdf, "wb") as fh:
                                                                    fh.write(base64.b64decode(pdf_base64_sign))
                                                                path_pdf = path + '/' + file_name_sign_pdf
                                                                token_dms = result_login['msg']['entry']['id']
                                                                datajson_properties['name'] = tmp_file_name
                                                                datajson_properties['relativePath'] = tmp_relativePath
                                                                data_properties_to_dms = {
                                                                    "properties":[datajson_properties]
                                                                }
                                                                data_properties_to_dms = str(data_properties_to_dms)
                                                                step_2_upload_dms_v1(token_dms,'',path_pdf,file_name_sign_pdf,'','',data_properties_to_dms,token_header)
                                                                insert().insert_transaction_servicelog_v1(data['name_service'],'OK',sid_code,'dont have attm file' + str(result_attm_file['messageText']),token_header)
                                                            else:
                                                                insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'cant upload pdf sign file' + str(result_file_last_pdf['messageText']),token_header)
                        elif data['name_service'] == 'ONEBOX':
                            if data['status'] == True:
                                print('ONEBOX')
                                result_tax_id = select_3().select_tax_id_to_onebox_v2(sid_code,tax_id)
                                doc_name_type = result_tax_id['messageText2']
                                result_dept = select_3().select_deptname_onebox(sid_code)
                                dept_name = result_dept['messageText']
                                taxid = result_tax_id['messageText']
                                result_user = select().select_user_first(sid_code)
                                if result_user['result'] == 'OK':
                                    username_first = result_user['messageText']['username']
                                    userid_first = result_user['messageText']['userid']
                                    result_save_onebox = get_pdf_to_onebox_v2(sid_code,username_first,userid_first,taxid,dept_name,doc_name_type,token_header)
                return jsonify({'result':'OK','messageText':[{'messageCode':get_status_file}],'messageER':None,'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':'parameter incorrct','status_Code':200}),200

@status_methods.route('/api/v2/other_service', methods=['POST'])
@token_required
def other_service_api_v2():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'Bearer Token Error!','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'sidCode' in dataJson and len(dataJson) == 1:
            arr_status = []
            for z in range(len(dataJson['sidCode'])):
                now = datetime.datetime.now()
                sid_code = dataJson['sidCode'][z]
                json_data = [
                    {"name_service":"RPA","status":True,"other":[{"path_folder":"/Create/CSPOC","url_path":""}]},
                    {"name_service":"DMS","status":False,"other":[{"path_folder":"","url_path":""}]},
                    {"name_service":"WEBHOOK","status":True,"other":[{"path_folder":"","url_path":"https://google.co.th"}]},
                    # {"name_service":"EFORM","status":True,"other":[{"path_folder":"","url_path":""}]},
                    {"name_service":"ONEBOX","status":True,"other":[{"path_folder":"","url_path":""}]}
                ]
                result_documenttype = select().select_document_type_forOthers_v1(sid_code)
                result_select = select().select_sid_code_status_v1(sid_code)
                # print(result_select , 'result_select')
                print(result_documenttype)
                tmp_list_service = []
                if result_documenttype['result'] == 'OK':
                    tmp_message = result_documenttype['messageText']
                    if tmp_message != None:
                        # print(result_select, ' result_documenttype')
                        tmp_documentType = result_select['messageText']['Document_Details'][0]['document_type']
                        tmp_relativePath = tmp_documentType + '/' + str(now.year) + '/' + str('{:02d}'.format(now.month))
                        # print()
                        # print(tmp_relativePath)
                        tmp_message = eval(tmp_message)
                        for y in range(len(json_data)):
                            tmp_data = json_data[y]
                            for t in range(len(tmp_message)):
                                tmp_message_data = tmp_message[t]
                                if tmp_data['name_service'] == tmp_message_data['name_service']:
                                    tmp_data = tmp_message_data
                                    tmp_list_service.append(tmp_data)

                if len(tmp_list_service) != 0:                                 
                    json_data =  tmp_list_service
                else:
                    json_data = json_data
                if result_select['result'] == 'OK':
                    get_status_file = result_select['messageText']['Document_Details'][0]['status_file_code']
                    # print(get_status_file)
                    # get_status_file = 'Y'
                    if get_status_file == 'Y':
                        result_select_data = select().select_ForWebHook(sid_code)
                        # print(result_select_data, 'result_select_data')
                        
                        list_documentType = ['cspoc','cs','scs','tm']
                        for u in range(len(json_data)):
                            data = json_data[u]
                            if data['name_service'] == 'RPA':
                                if data['status'] == True:
                                    print('RPA')
                                    result_select_action = select().select_get_action_and_status('robot')
                                    # print(result_select_action)
                                    if result_select_action['result'] == 'OK':
                                        if result_select_action['messageText']['status'] == True:
                                            resultselect_attm_file = select().select_attm_file_v1_for_chat_api_to_robot(sid_code)
                                            # print(resultselect_attm_file)
                                            if resultselect_attm_file['result'] == 'OK':
                                                doc_id = resultselect_attm_file['messageText']['document_Id']
                                                pathFolder = resultselect_attm_file['messageText']['pathfolder']
                                                json_Data_File = resultselect_attm_file['messageText']['json_data']
                                                username_sender = resultselect_attm_file['messageText']['sender_username']
                                                document_Type = resultselect_attm_file['messageText']['document_Type']
                                                if document_Type in list_documentType:
                                                    result_file_last_pdf  =select().select_file_sign_last_to_email(sid_code)
                                                    if result_file_last_pdf['result'] == 'OK':
                                                        pdf_base64_sign = result_file_last_pdf['messageText']
                                                        file_name_sign_pdf = result_file_last_pdf['file_name']
                                                        
                                                        sftp_robot().send_file_tosftp_new_v2(json_Data_File,pathFolder,'',document_Type,doc_id,pdf_base64_sign,file_name_sign_pdf)
                                                        insert().insert_transaction_servicelog_v1(data['name_service'],'OK',sid_code,'upload sftp complete',token_header)
                                                    else:
                                                        insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'data not found file',token_header)
                                            else:
                                                doc_id = resultselect_attm_file['messageText']['document_Id']
                                                username_sender = resultselect_attm_file['messageText']['sender_username']
                                                document_Type = resultselect_attm_file['messageText']['document_Type']
                                                if document_Type in list_documentType:
                                                    result_file_last_pdf  =select().select_file_sign_last_to_email(sid_code)
                                                    if result_file_last_pdf['result'] == 'OK':
                                                        pdf_base64_sign = result_file_last_pdf['messageText']
                                                        file_name_sign_pdf = result_file_last_pdf['file_name']
                                                        
                                                        sftp_robot().send_file_tosftp_new_v2('','','',document_Type,doc_id,pdf_base64_sign,file_name_sign_pdf)
                                                        insert().insert_transaction_servicelog_v1(data['name_service'],'OK',sid_code,'upload sftp complete and not attachment file',token_header)
                                                    else:
                                                        insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'data not found file',token_header)
                                                # insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'data not found attachment')
                            elif data['name_service'] == 'WEBHOOK':
                                if data['status'] == True:
                                    print('WEBHOOK')
                                    result_select = select().select_ForWebHook(sid_code)
                                    # print(result_select)
                                    if result_select['result'] == 'OK' and str(result_select['messageText']['webHook']).replace(' ','') != '':
                                        del(result_select['messageText']['email_center'])
                                        result_select['messageText']['PDF_String'] = None
                                        # print(result_select)
                                        webhook_Data = result_select['messageText']
                                        try:
                                            response = requests.post(result_select['messageText']['webHook'], json=webhook_Data,headers={'Content-Type': 'application/json'},timeout=10,verify=False)
                                        except requests.HTTPError as err:
                                            pass
                                        except requests.Timeout as err:
                                            pass
                                        except requests.ConnectionError as err:
                                            pass
                                        except Exception as ex:
                                            pass
                            elif data['name_service'] == 'DMS':
                                if data['status'] == True:
                                    print('DMS')
                                    datajson_properties = {}
                                    data_properties_to_dms = {}
                                    tmp_file_name = result_select_data['messageText']['fileName']
                                    result_select_action = select().select_get_action_and_status('dms')
                                    if result_select_action['result'] == 'OK':
                                        if result_select_action['messageText']['status'] == True:                                        
                                            result_docuemnt_data = select().select_pty_file_pdf_v1(sid_code)
                                            if result_docuemnt_data['result'] == 'OK':
                                                msg_data = result_docuemnt_data['msg']['options_page']
                                                if 'service_properties' in msg_data:
                                                    tmp_service_properties = msg_data['service_properties']
                                                    for z in range(len(tmp_service_properties)):
                                                        tmp_name_service = tmp_service_properties[z]['name_service']
                                                        tmp_other = tmp_service_properties[z]['other']
                                                        for iu in range(len(tmp_other)):
                                                            if 'properties' in tmp_other[iu]:
                                                                tmp_properties = tmp_other[iu]['properties']
                                                                for zyu in range(len(tmp_properties)):
                                                                    tmp_name_data = tmp_properties[zyu]['name'] 
                                                                    tmp_value_data =tmp_properties[zyu]['value'] 
                                                                    if str(tmp_name_data).replace(' ','') != '':
                                                                        datajson_properties['Doc:'+tmp_name_data] = tmp_value_data
                                                    if datajson_properties != {}:
                                                        result_login = step_1_login_dms_v1(token_header)
                                                        if result_login['result'] == 'OK':
                                                            insert().insert_transaction_servicelog_v1(data['name_service'],'OK',sid_code,'login ok ' + str(result_login['msg']),token_header)
                                                            result_attm_file = select().select_attm_file_v1_for_chat_api_to_robot(sid_code)
                                                            if result_attm_file['result'] == 'OK':
                                                                doc_id = result_attm_file['messageText']['document_Id']
                                                                pathFolder = result_attm_file['messageText']['pathfolder']
                                                                json_Data_File = result_attm_file['messageText']['json_data']
                                                                username_sender = result_attm_file['messageText']['sender_username']
                                                                document_Type = result_attm_file['messageText']['document_Type']                                                        
                                                                
                                                                result_file_last_pdf  =select().select_file_sign_last_to_email(sid_code)
                                                                if result_file_last_pdf['result'] == 'OK':
                                                                    path = './storage/pdf/' + doc_id
                                                                    if not os.path.exists(path):
                                                                        os.makedirs(path) 
                                                                    pdf_base64_sign = result_file_last_pdf['messageText']
                                                                    file_name_sign_pdf = result_file_last_pdf['file_name']
                                                                    with open(path + '/' + file_name_sign_pdf, "wb") as fh:
                                                                        fh.write(base64.b64decode(pdf_base64_sign))
                                                                    path_pdf = path + '/' + file_name_sign_pdf
                                                                    token_dms = result_login['msg']['entry']['id']
                                                                    for x in range(len(json_Data_File)): 
                                                                        path_pdf_attm = '.' + pathFolder  + json_Data_File[x]['file_name_new']
                                                                        # print(datajson_properties)
                                                                        datajson_properties['name'] = json_Data_File[x]['file_name_original']
                                                                        datajson_properties['relativePath'] = tmp_relativePath
                                                                        data_properties_to_dms = {
                                                                            "properties":[datajson_properties]
                                                                        }
                                                                        # print(datajson_properties)
                                                                        data_properties_to_dms = str(data_properties_to_dms) 
                                                                        step_2_upload_dms_v1(token_dms,'',path_pdf_attm,json_Data_File[x]['file_name_original'],'','',data_properties_to_dms,token_header)
                                                                    datajson_properties['name'] = tmp_file_name
                                                                    datajson_properties['relativePath'] = tmp_relativePath
                                                                    data_properties_to_dms = {
                                                                        "properties":[datajson_properties]
                                                                    }
                                                                    data_properties_to_dms = str(data_properties_to_dms) 
                                                                    step_2_upload_dms_v1(token_dms,'',path_pdf,file_name_sign_pdf,'','',data_properties_to_dms,token_header)
                                                                    insert().insert_transaction_servicelog_v1(data['name_service'],'OK',sid_code,'have attm file ' + str(result_attm_file['messageText']),token_header)
                                                                else:
                                                                    insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'cant upload pdf sign file' + str(result_file_last_pdf['messageText']),token_header) 
                                                            else:
                                                                doc_id = result_attm_file['messageText']['document_Id']
                                                                username_sender = result_attm_file['messageText']['sender_username']
                                                                document_Type = result_attm_file['messageText']['document_Type']  
                                                                result_file_last_pdf  =select().select_file_sign_last_to_email(sid_code)                                                     
                                                                if result_file_last_pdf['result'] == 'OK':
                                                                    path = './storage/pdf/' + doc_id
                                                                    if not os.path.exists(path):
                                                                        os.makedirs(path) 
                                                                    pdf_base64_sign = result_file_last_pdf['messageText']
                                                                    file_name_sign_pdf = result_file_last_pdf['file_name']
                                                                    with open(path + '/' + file_name_sign_pdf, "wb") as fh:
                                                                        fh.write(base64.b64decode(pdf_base64_sign))
                                                                    path_pdf = path + '/' + file_name_sign_pdf
                                                                    token_dms = result_login['msg']['entry']['id']
                                                                    datajson_properties['name'] = tmp_file_name
                                                                    datajson_properties['relativePath'] = tmp_relativePath
                                                                    data_properties_to_dms = {
                                                                        "properties":[datajson_properties]
                                                                    }
                                                                    data_properties_to_dms = str(data_properties_to_dms)
                                                                    step_2_upload_dms_v1(token_dms,'',path_pdf,file_name_sign_pdf,'','',data_properties_to_dms,token_header)
                                                                    insert().insert_transaction_servicelog_v1(data['name_service'],'OK',sid_code,'dont have attm file' + str(result_attm_file['messageText']),token_header)
                                                                else:
                                                                    insert().insert_transaction_servicelog_v1(data['name_service'],'ER',sid_code,'cant upload pdf sign file' + str(result_file_last_pdf['messageText']),token_header)
                            elif data['name_service'] == 'ONEBOX':
                                if data['status'] == True:
                                    print('ONEBOX')                               
                arr_status.append(get_status_file)   
            return jsonify({'result':'OK','messageText':[{'messageCode':arr_status}],'messageER':None,'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':'parameter incorrct','status_Code':200}),200

@status_methods.route('/api/v1/logging', methods=['POST'])
@token_required
def logging_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'messageER' in dataJson and 'status' in dataJson and 'url' and len(dataJson) == 3:
            messageER = dataJson['messageER']
            status = dataJson['status']
            url = dataJson['url']
            insert().insert_tran_log_v1(messageER,status,'',url)
            callWebHook_slack_v1(messageER,status,url)
            return jsonify({'result':'OK','messageText':None,'messageER':None,'status_Code':200}),200