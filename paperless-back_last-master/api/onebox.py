#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config.lib import *
from config.value import *
from db.db_method import *
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *
from db.db_Class import *
from method.access import *
from method.hashpy import *
from method.other import *

def start_run_background(account_id,folder_id,dept_id,headers,token_header):
    try:
        check_permis_fol = check_permission_folder(folder_id,account_id,headers,token_header)
        if check_permis_fol['result'] == 'OK':
            eval_data = eval(str(check_permis_fol['messageText']))
            status_permis = eval_data['data']['permission_folder_check']
            if status_permis == 'False':
                update_permis_fol = update_permission_account(folder_id,account_id,dept_id,headers,token_header)
            else:
                pass
        return ''
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def get_department_account(tax_id,headers,token_header,account_id):
    time_duration = ''
    try:
        # Prod
        # url = url_mainbox + "/api/get_account_byuserid"
        # Uat
        url = url_mainbox + "/api/get_account_and_department"
        data = {
           'tax_id': tax_id,
           'account_id' : account_id
        }
        response_depart = requests.post(url, json = data, headers=headers, verify=False)
        time_duration = str(int(response_depart.elapsed.total_seconds() * 1000))    

        if response_depart.status_code == 200 or response_depart.status_code == 201:
            insert().insert_tran_log_v1(str(response_depart.json()),'OK',str(data),url,token_header,time_duration)
            response_depart = response_depart.json()
            return {'result':'OK','messageText':response_depart}
        else:
            insert().insert_tran_log_v1(str(response_depart.text),'ER',str(data),url,token_header,time_duration)
            return {'result':'ER','messageText':response_depart}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}


def create_folder_onebox_with_permis(data,headers,token_header):
    time_duration = ''
    try:
        # Prod
        # url = url_mainbox + '/api/create_folder'
        # Uat
        url = url_mainbox + "/api/create_folder_with_permission"
        response_folder = requests.post(url, json = data, headers=headers, verify=False)
        time_duration = str(int(response_folder.elapsed.total_seconds() * 1000))

        if response_folder.status_code == 200 or response_folder.status_code == 201:
            insert().insert_tran_log_v1(str(response_folder.json()),'OK',str(data),url,token_header,time_duration)
            response_folder = response_folder.json()
            return {'result':'OK','messageText':response_folder}
        else:
            insert().insert_tran_log_v1(str(response_folder.text),'ER',str(data),url,token_header,time_duration)
            return {'result':'ER','messageText':response_folder['errorMessage']}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def check_permission_folder(folder_id,account_id,headers,token_header):
    time_duration = ''
    try:
        # Prod
        # url = url_mainbox + "/api/get_account_byuserid"
        # Uat
        url = url_mainbox + "/api/get_folder_info"
        data = {
           'folder_id': folder_id,
           'account_id': account_id
        }
        response_depart = requests.post(url, json = data, headers=headers, verify=False)
        time_duration = str(int(response_depart.elapsed.total_seconds() * 1000))    

        if response_depart.status_code == 200 or response_depart.status_code == 201:
            insert().insert_tran_log_v1(str(response_depart.json()),'OK',str(data),url,token_header,time_duration)
            response_depart = response_depart.json()
            return {'result':'OK','messageText':response_depart}
        else:
            insert().insert_tran_log_v1(str(response_depart.text),'ER',str(data),url,token_header,time_duration)
            return {'result':'ER','messageText':response_depart}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def update_permission_account(folder_id,account_id,dept_id,headers,token_header):
    time_duration = ''
    try:
        # Prod
        # url = url_mainbox + "/api/get_account_byuserid"
        # Uat
        url = url_mainbox + "/api/setting_folder_permission"
        data = {
                    "folder_id": folder_id,
                    "account_id": account_id,
                    "account_id_to_setting": [],
                    "department_id_to_setting": [
                        {
                            "id": dept_id,
                            "permission": {
                                "view_only": "True",
                                "download": "True",
                                "edit": "True"
                            }
                        }
                    ]
                }
        response_depart = requests.post(url, json = data, headers=headers, verify=False)
        time_duration = str(int(response_depart.elapsed.total_seconds() * 1000))    

        if response_depart.status_code == 200 or response_depart.status_code == 201:
            insert().insert_tran_log_v1(str(response_depart.json()),'OK',str(data),url,token_header,time_duration)
            response_depart = response_depart.json()
            return {'result':'OK','messageText':response_depart}
        else:
            insert().insert_tran_log_v1(str(response_depart.text),'ER',str(data),url,token_header,time_duration)
            return {'result':'ER','messageText':response_depart}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}


def get_account_byuserid(data,one_accesstoken):
    time_duration = ''
    try:
        dataJson = ''
        # token_onebox = token_onebox
        headers = {
            'content-type': 'application/json',
            'Authorization':token_onebox
        }
        url = url_mainbox + '/api/v2/get_account_byuserid'
        token_header = one_accesstoken
        response = requests.post(url, json=data, headers=headers,verify=False )
        # print(response)
        time_duration = str(int(response.elapsed.total_seconds() * 1000))
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(data),url,token_header,time_duration)
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(data),url,token_header,time_duration)
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','msg':ex}

def select_account_id_onebox(data,headers,token_header):    
    time_duration = ''
    try:
        # Prod
        # url = url_mainbox + "/api/get_account_byuserid"
        # Uat
        url = url_mainbox + "/api/get_account_byuserid"
        response_account = requests.post(url, json = data, headers=headers, verify=False)
        time_duration = str(int(response_account.elapsed.total_seconds() * 1000))    

        if response_account.status_code == 200 or response_account.status_code == 201:
            insert().insert_tran_log_v1(str(response_account.json()),'OK',str(data),url,token_header,time_duration)
            response_account = response_account.json()
            return {'result':'OK','messageText':response_account}
        else:
            insert().insert_tran_log_v1(str(response_account.text),'ER',str(data),url,token_header,time_duration)
            return {'result':'ER','messageText':response_account}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def select_folder_onebox(account_id,data_account_id,headers,token_header):
    
    time_duration = ''
    try:
        # Prod
        # url = url_mainbox + "/api/get_mainfolder_byaccountid"
        # Uat
        
        url = url_mainbox + "/api/get_mainfolder_byaccountid"
        response_folder = requests.post(url, json = data_account_id, headers=headers, verify=False)
        time_duration = str(int(response_folder.elapsed.total_seconds() * 1000))

        if response_folder.status_code == 200 or response_folder.status_code == 201:
            insert().insert_tran_log_v1(str(response_folder.json()),'OK',str(data_account_id),url,token_header,time_duration)
            response_folder = response_folder.json()
            return {'result':'OK','messageText':response_folder}
        else:
            insert().insert_tran_log_v1(str(response_folder.text),'ER',str(data_account_id),url,token_header,time_duration)
            return {'result':'ER','messageText':response_folder}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_account_id),url,token_header,time_duration)
        return {'result':'ER','messageText':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_account_id),url,token_header,time_duration)
        return {'result':'ER','messageText':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_account_id),url,token_header,time_duration)
        return {'result':'ER','messageText':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_account_id),url,token_header,time_duration)
        return {'result':'ER','messageText':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data_account_id),url,token_header,time_duration)
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def save_file_onebox(data_save_file,files_save,headers,st2,data_userName,token_header):
    try:
        list_response = []
        # Prod
        # url = url_mainbox + "/api/savefile"
        # Uat
        
        url = url_mainbox + "/api/savefile"
        response_file = requests.post(url,data = data_save_file, files = files_save, headers=headers, verify=False)
        time_duration = ''
        time_duration = str(int(response_file.elapsed.total_seconds() * 1000))
        response_file = response_file.json()
        # print ('RESPONSE:',response_file)
        tmperrmessage = 'fail'
        if response_file['status'] == 'ER':
            tmp_response = {}
            for i in range(2):
                # response_file = requests.post(url4,data = data_save_file, files = files_save, headers=headers, verify=False)
                # response_file = response_file.json()
                response_file = requests.post(url,data = data_save_file, files = files_save, headers=headers, verify=False)
                response_file = response_file.json()
                if response_file['status'] == 'OK':
                    tmp_response['file_name_original'] = response_file['data']['filename']
                    tmp_response['file_id'] = response_file['data']['id']
                    tmp_response['size_file'] = response_file['data']['size_file']
                    tmp_response['file_upload_datetime'] = str(st2)
                    tmp_response['username'] = data_userName
                    tmp_response['status'] = response_file['data']['status_file']
                    list_response.append(tmp_response)
                    break
                else:
                    tmp_response['errorCode'] = response_file['errorCode']
                    tmp_response['errorMessage'] = response_file['errorMessage']
                    tmp_response['status'] = response_file['status']
                    tmp_response['file_name'] = response_file['data']['filename']
                    list_response.append(tmp_response)
                if 'errorMessage' in response_file:
                    tmperrmessage = response_file['errorMessage']
        elif response_file['status'] == 'OK':
            tmp_response = {}
            tmp_response['file_name_original'] = response_file['data']['filename']
            tmp_response['file_id'] = response_file['data']['id']
            tmp_response['size_file'] = response_file['data']['size_file']
            tmp_response['file_upload_datetime'] = str(st2)
            tmp_response['username'] = data_userName
            tmp_response['status'] = response_file['data']['status_file']
            list_response.append(tmp_response)
            # print ('list_response: ',list_response)
        return {'result':'OK','messageText':list_response}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_save_file),url,token_header,time_duration)
        return {'result':'ER','messageText':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_save_file),url,token_header,time_duration)
        return {'result':'ER','messageText':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_save_file),url,token_header,time_duration)
        return {'result':'ER','messageText':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data_save_file),url,token_header,time_duration)
        return {'result':'ER','messageText':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data_save_file),url,token_header,time_duration)
        return {'result':'ER','messageText':tmperrmessage,'status_Code':200}


# def save_file_onebox(data_save_file,files_save,headers,st2,data_userName,token_header):
#     try:
#         list_response = []
#         # Prod
#         # url = url_mainbox + "/api/savefile"
#         # Uat
        
#         url = url_mainbox + "/api/savefile"
#         response_file = requests.post(url,data = data_save_file, files = files_save, headers=headers, verify=False)
#         time_duration = ''
#         time_duration = str(int(response_file.elapsed.total_seconds() * 1000))
#         response_file = response_file.json()
    
#         if response_file['status'] == 'ER':
#             tmp_response = {}
#             for i in range(2):
#                 # response_file = requests.post(url4,data = data_save_file, files = files_save, headers=headers, verify=False)
#                 # response_file = response_file.json()
#                 response_file = requests.post(url,data = data_save_file, files = files_save, headers=headers, verify=False)
#                 response_file = response_file.json()
#             tmp_response['errorCode'] = response_file['errorCode']
#             tmp_response['errorMessage'] = response_file['errorMessage']
#             tmp_response['status'] = response_file['status']
#             tmp_response['file_name'] = original_filename
            
#             list_response.append(tmp_response)
#         elif response_file['status'] == 'OK':
#             # print('OK')
#             tmp_response = {}
#             tmp_response['file_name_original'] = response_file['data']['filename']
#             tmp_response['file_id'] = response_file['data']['id']
#             tmp_response['size_file'] = response_file['data']['size_file']
#             tmp_response['file_upload_datetime'] = str(st2)
#             tmp_response['username'] = data_userName
#             tmp_response['status'] = response_file['data']['status_file']

#             list_response.append(tmp_response)
#             print ('list_response: ',list_response)
        
#         return {'result':'OK','messageText':list_response}

#     except requests.Timeout as ex:
#         insert().insert_tran_log_v1(str(ex),'ER',str(data_save_file),url,token_header,time_duration)
#         return {'result':'ER','messageText':'Timeout ' + str(ex)}
#     except requests.HTTPError as ex:
#         insert().insert_tran_log_v1(str(ex),'ER',str(data_save_file),url,token_header,time_duration)
#         return {'result':'ER','messageText':'HTTPError ' + str(ex)}
#     except requests.ConnectionError as ex:
#         insert().insert_tran_log_v1(str(ex),'ER',str(data_save_file),url,token_header,time_duration)
#         return {'result':'ER','messageText':'ConnectionError ' + str(ex)}
#     except requests.RequestException as ex:
#         insert().insert_tran_log_v1(str(ex),'ER',str(data_save_file),url,token_header,time_duration)
#         return {'result':'ER','messageText':'RequestException ' + str(ex)}
#     except Exception as ex:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(exc_type, fname, exc_tb.tb_lineno)
#         insert().insert_tran_log_v1(str(ex),'ER',str(data_save_file),url,token_header,time_duration)
#         return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def download_file_onebox(data,headers,token_header):
    time_duration = ''
    try:
        # Prod
        # url = url_mainbox + '/api/dowloads_file'
        # Uat
        url = url_mainbox + "/api/dowloads_file"
        response_file = requests.get(url, params = data, headers=headers, verify=False)
        time_duration = str(int(response_file.elapsed.total_seconds() * 1000))
        d = response_file.headers['content-disposition']
        fname = re.findall("filename=(.+)", d)[0]
        fname_1 = fname.split('.')[0]
        fname_2 = fname.split('.')[-1]
        filename_all = fname_1 + '.' + fname_2
        # print ('fname: ', fname_1)
        # print ('fname2: ', fname_2)
        
        file_io = io.BytesIO(response_file.content)
        
        sendfile = send_file(file_io,mimetype= 'application/'+fname_2,as_attachment=True,attachment_filename='%s' % str(filename_all))        
        return (sendfile)

    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def get_account_byuserid(data,one_accesstoken):
    time_duration = ''
    try:
        dataJson = ''
        # token_onebox = token_onebox
        headers = {
            'content-type': 'application/json',
            'Authorization':token_onebox
        }
        url = url_mainbox + '/api/v2/get_account_byuserid'
        token_header = one_accesstoken
        response = requests.post(url, json=data, headers=headers,verify=False )
        # print(response)
        time_duration = str(int(response.elapsed.total_seconds() * 1000))
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(data),url,token_header,time_duration)
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(data),url,token_header,time_duration)
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','msg':ex}

def create_folder_onebox(data,headers,token_header):
    time_duration = ''
    try:
        # Prod
        # url = url_mainbox + '/api/create_folder'
        # Uat
        url = url_mainbox + "/api/create_folder"
        response_folder = requests.post(url, json = data, headers=headers, verify=False)
        time_duration = str(int(response_folder.elapsed.total_seconds() * 1000))

        if response_folder.status_code == 200 or response_folder.status_code == 201:
            insert().insert_tran_log_v1(str(response_folder.json()),'OK',str(data),url,token_header,time_duration)
            response_folder = response_folder.json()
            return {'result':'OK','messageText':response_folder}
        else:
            insert().insert_tran_log_v1(str(response_folder.text),'ER',str(data),url,token_header,time_duration)
            return {'result':'ER','messageText':response_folder['errorMessage']}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def get_sub_folder_onebox(data,headers,token_header):
    time_duration = ''
    try:
        # Prod
        # url = url_mainbox + '/api/get_subfolder'
        # Uat
        url = url_mainbox + "/api/get_subfolder"
        response_subfolder = requests.post(url, json = data, headers=headers, verify=False)
        time_duration = str(int(response_subfolder.elapsed.total_seconds() * 1000))

        if response_subfolder.status_code == 200 or response_subfolder.status_code == 201:
            insert().insert_tran_log_v1(str(response_subfolder.json()),'OK',str(data),url,token_header,time_duration)
            response_subfolder = response_subfolder.json()
            return {'result':'OK','messageText':response_subfolder}
        else:
            insert().insert_tran_log_v1(str(response_subfolder.text),'ER',str(data),url,token_header,time_duration)
            return {'result':'ER','messageText':response_subfolder}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,time_duration)
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def check_file_in_file(folder_id,account_id,headers,doc_id,token_header):
    try:
        ts = int(time.time())
        year = str(datetime.datetime.fromtimestamp(ts).strftime('%Y'))
        month_day = str(datetime.datetime.fromtimestamp(ts).strftime('%m-%d'))
        
        check_month_day = False
        check_docid = False
        list_temp = ['paperless','pdf',year,month_day,doc_id]
        list_keep = []

        for x in range(len(list_temp)):
            check_year = False
            data_subfolder = {
                'account_id': str(account_id),
                'folder_id' : str(folder_id)
            }
            result_sub_folder = get_sub_folder_onebox(data_subfolder,headers,token_header)
            if result_sub_folder['result'] == 'OK':
                if result_sub_folder['messageText']['status'] == 'OK':
                    for a in range(len(result_sub_folder['messageText']['result'])):
                        if result_sub_folder['messageText']['result'][a]['folder_name'] == list_temp[x]:
                            folder_id = result_sub_folder['messageText']['result'][a]['folder_id']
                            check_year = True
                    if check_year == True:
                        folder_id = folder_id
                        pass
                    elif check_year == False:
                        data_folder_file = {
                            'account_id': str(account_id),
                            'parent_folder_id' : str(folder_id), 
                            'folder_name' : str(list_temp[x])
                        }        
                        result_create_folder = create_folder_onebox(data_folder_file,headers,token_header)
                        folder_id = result_create_folder['messageText']['data']['folder_id']

                elif result_sub_folder['messageText']['status'] == 'ER':
                    data_folder_file = {
                            'account_id': str(account_id),
                            'parent_folder_id' : str(folder_id), 
                            'folder_name' : str(list_temp[x])
                        }        
                    result_create_folder = create_folder_onebox(data_folder_file,headers,token_header)
                    folder_id = result_create_folder['messageText']['data']['folder_id']            
            elif result_sub_folder['result'] == 'ER':
                return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}
        return {'result':'OK','messageText':folder_id}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data_subfolder),url,token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def check_file_in_file_attach(folder_id,account_id,headers,doc_id,token_header):
    try:
        ts = int(time.time())
        year = str(datetime.datetime.fromtimestamp(ts).strftime('%Y'))
        month_day = str(datetime.datetime.fromtimestamp(ts).strftime('%m-%d'))
       
        list_temp = ['paperless','attach_folder',doc_id]
        list_keep = []
        # print ('doc_id: ',doc_id)
        for x in range(len(list_temp)):
            # print (x)
            check_year = False
            # print ('account_id: ',account_id)
            # print ('folder_id: ',folder_id)
            data_subfolder = {
                'account_id': str(account_id),
                'folder_id' : str(folder_id)
            }
            result_sub_folder = get_sub_folder_onebox(data_subfolder,headers,token_header)
            if result_sub_folder['result'] == 'OK':
                if result_sub_folder['messageText']['status'] == 'OK':
                    for a in range(len(result_sub_folder['messageText']['result'])):
                        if result_sub_folder['messageText']['result'][a]['folder_name'] == list_temp[x]:
                            folder_id = result_sub_folder['messageText']['result'][a]['folder_id']
                            check_year = True
                    if check_year == True:
                        folder_id = folder_id
                        pass
                    elif check_year == False:
                        data_folder_file = {
                            'account_id': str(account_id),
                            'parent_folder_id' : str(folder_id), 
                            'folder_name' : str(list_temp[x])
                        }        
                        result_create_folder = create_folder_onebox(data_folder_file,headers,token_header)
                        folder_id = result_create_folder['messageText']['data']['folder_id']

                elif result_sub_folder['messageText']['status'] == 'ER':
                    data_folder_file = {
                            'account_id': str(account_id),
                            'parent_folder_id' : str(folder_id), 
                            'folder_name' : str(list_temp[x])
                        }        
                    result_create_folder = create_folder_onebox(data_folder_file,headers,token_header)
                    folder_id = result_create_folder['messageText']['data']['folder_id']            
            elif result_sub_folder['result'] == 'ER':
                return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}
        return {'result':'OK','messageText':folder_id}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data_subfolder),url,token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def check_file_in_file_attach_push(folder_id,account_id,headers,folder_name,token_header):
    try:
        ts = int(time.time())
        year = str(datetime.datetime.fromtimestamp(ts).strftime('%Y'))
        month_day = str(datetime.datetime.fromtimestamp(ts).strftime('%m-%d'))
       
        list_temp = ['paperless','attach_folder',folder_name]
        list_keep = []
        for x in range(len(list_temp)):
            check_year = False
            data_subfolder = {
                'account_id': str(account_id),
                'folder_id' : str(folder_id)
            }
            result_sub_folder = get_sub_folder_onebox(data_subfolder,headers,token_header)
            if result_sub_folder['result'] == 'OK':
                if result_sub_folder['messageText']['status'] == 'OK':
                    for a in range(len(result_sub_folder['messageText']['result'])):
                        if result_sub_folder['messageText']['result'][a]['folder_name'] == list_temp[x]:
                            folder_id = result_sub_folder['messageText']['result'][a]['folder_id']
                            check_year = True
                    if check_year == True:
                        folder_id = folder_id
                        pass
                    elif check_year == False:
                        data_folder_file = {
                            'account_id': str(account_id),
                            'parent_folder_id' : str(folder_id), 
                            'folder_name' : str(list_temp[x])
                        }        
                        result_create_folder = create_folder_onebox(data_folder_file,headers,token_header)
                        folder_id = result_create_folder['messageText']['data']['folder_id']

                elif result_sub_folder['messageText']['status'] == 'ER':
                    data_folder_file = {
                            'account_id': str(account_id),
                            'parent_folder_id' : str(folder_id), 
                            'folder_name' : str(list_temp[x])
                        }        
                    result_create_folder = create_folder_onebox(data_folder_file,headers,token_header)
                    folder_id = result_create_folder['messageText']['data']['folder_id']            
            elif result_sub_folder['result'] == 'ER':
                return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}
        return {'result':'OK','messageText':folder_id}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data_subfolder),url,token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def onebox_save_file_v4(file_pdf,user_id,username,file_name,tax_id,doc_id,token_header):     
      
    ts = int(time.time())
    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    st2 = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
    year = datetime.datetime.fromtimestamp(ts).strftime('%Y')
    month_day = datetime.datetime.fromtimestamp(ts).strftime('%m-%d')
    check_year = False
    check_month_day = False
    check_docid = False
    try:
        # GET account_id จาก oneid
        headers = {
            'Authorization': token_onebox
        }
        data = {
            'user_id': str(user_id)
        }
        result_select_account_id = select_account_id_onebox(data,headers,token_header)
        if result_select_account_id['result'] == 'OK':
            result_select_account_id = result_select_account_id['messageText']
        elif result_select_account_id['result'] == 'ER':
            return {'result':'ER','messageText':None,'messageER':result_select_account_id['messageText'],'status_Code':200}
            # GET folder จาก account_id
        for i in range(len(result_select_account_id['result'])):
            if str(result_select_account_id['result'][i]['taxid']) == str(tax_id):
                account_id = result_select_account_id['result'][i]['account_id']
        data_account_id = {
            'account_id': str(account_id)
        }
        result_select_folder = select_folder_onebox(account_id,data_account_id,headers,token_header)
        if result_select_folder['result'] == 'OK':
            result_select_folder = result_select_folder['messageText']
        elif result_select_folder['result'] == 'ER':
            return {'result':'ER','messageText':None,'messageER':result_select_folder['messageText'],'status_Code':200}
        result_biz_name = select_2().select_bizname_by_taxid(tax_id)
        biz_name = result_biz_name['messageText']
        if biz_name == None:
            folder_id = result_select_folder['result'][0]['folder_id']
        elif biz_name != None:
            for n in range(len(result_select_folder['result'])):
                if str(result_select_folder['result'][n]['folder_name']) == str(biz_name):
                    folder_id = result_select_folder['result'][n]['folder_id']

        check_folder = check_file_in_file(folder_id,account_id,headers,doc_id,token_header)
        if check_folder['result'] == 'OK':
            folder_id_docid = check_folder['messageText']
        elif check_folder['result'] == 'ER':
            return {'result':'ER','messageText':None,'messageER':check_folder['messageText'],'status_Code':200}
        
        data_save_file = {
            'account_id': str(account_id),
            'folder_id' : str(folder_id_docid)
        }
        unique_foldername = str(uuid.uuid4())
        list_file_name = []
        list_response = []
        path = './storage/temp/' + unique_foldername +'/'
        path_indb = '/storage/temp/' + unique_foldername +'/'
        path_folder = '/storage/temp/'
        if not os.path.exists(path):
            os.makedirs(path)
        files = file_pdf
        data_userName = username
        unique_filename = str(uuid.uuid4())
        original_filename = str(file_name).split('.')[0]
        # original_filename = 'เอกสารสำคัญ'
        # check_thai = pythainlp.util.isthai(original_filename)
        # if check_thai == True:
        #     original_filename = romanize(original_filename, engine="thai2rom")
        typefile = str(file_name).split('.')[-1]
        typefile = typefile.split('"')[0]
        with open(path + original_filename + "." + typefile, "wb") as fh:
            file_open = fh 
            fh.write((file_pdf))
            list_file_name.append({'file_name_original':original_filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
        file_open = open(path + original_filename + "." + typefile, "rb")
        files_save = {
            'file' : file_open
        }    
        result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,data_userName,token_header)
        list_response.append(result_save_file)
        file_open.close()
        path_removeFile = os.getcwd() + path_indb 
        shutil.rmtree(path_removeFile)
        # result_insert = insert().insert_transactionfile_copy1(list_response,path_indb,unique_foldername)
        return {'result':'OK','messageText':list_response,'messageER':None,'status_Code':200}
        # return {'result':'OK','messageText':'OK','messageER':None,'status_Code':200}

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data),'',token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def get_pdf_to_onebox_v2(sid,username,user_id,tax_id,dept_name,doc_name_type,token_header):
    try:
        result_select = select().select_get_pdf(sid)
        if result_select['result'] == 'OK':
            file_base = result_select['messageText']['file_base']
            file_pdf = base64.b64decode(file_base)
            result_filename = select_2().select_pdf_filename(sid)
            if result_filename['result'] == 'OK':
                file_name = result_filename['messageText']['file_name']
                doc_id = result_filename['messageText']['doc_id']
                # print(file_pdf,user_id,username,file_name,tax_id,doc_id,dept_name,doc_name_type,token_header)   
                try:   
                    result_onebox = onebox_save_file_v7(file_pdf,user_id,username,file_name,tax_id,doc_id,dept_name,doc_name_type,token_header)
                except UnboundLocalError as e:
                    print(str(e))

                if result_onebox['result'] == 'OK':
                    return {'result':'OK','messageText':'Success','messageER':None,'status_Code':200}
                elif result_onebox['result'] == 'ER':
                    return {'result':'ER','messageText':None,'messageER':result_onebox['messageER'],'status_Code':200}
                # return ('success')
            else:
                return {'result':'ER','messageText':None,'messageER':'Not Found filename','status_Code':200}
        else:
            return {'result':'ER','messageText':None,'messageER':'Not Found','status_Code':200}
    
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(ex),'',token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def check_file_in_file_v2(folder_id,account_id,headers,doc_id,Thai_foldername,name_folder,token_header):
    try:
        ts = int(time.time())
        year = str(datetime.datetime.fromtimestamp(ts).strftime('%Y'))
        month_day = str(datetime.datetime.fromtimestamp(ts).strftime('%m-%d'))
       
        list_temp = ['paperless',Thai_foldername,name_folder,year,month_day,doc_id,'pdf']
        list_keep = []
        for x in range(len(list_temp)):
            check_year = False
            data_subfolder = {
                'account_id': str(account_id),
                'folder_id' : str(folder_id)
            }
            result_sub_folder = get_sub_folder_onebox(data_subfolder,headers,token_header)
            if result_sub_folder['result'] == 'OK':
                if result_sub_folder['messageText']['status'] == 'OK':
                    for a in range(len(result_sub_folder['messageText']['result'])):
                        if result_sub_folder['messageText']['result'][a]['folder_name'] == list_temp[x]:
                            folder_id = result_sub_folder['messageText']['result'][a]['folder_id']
                            check_year = True
                    if check_year == True:
                        folder_id = folder_id
                        pass
                    elif check_year == False:
                        data_folder_file = {
                            'account_id': str(account_id),
                            'parent_folder_id' : str(folder_id), 
                            'folder_name' : str(list_temp[x])
                        }        
                        result_create_folder = create_folder_onebox(data_folder_file,headers,token_header)
                        folder_id = result_create_folder['messageText']['data']['folder_id']

                elif result_sub_folder['messageText']['status'] == 'ER':
                    data_folder_file = {
                            'account_id': str(account_id),
                            'parent_folder_id' : str(folder_id), 
                            'folder_name' : str(list_temp[x])
                        }        
                    result_create_folder = create_folder_onebox(data_folder_file,headers,token_header)
                    folder_id = result_create_folder['messageText']['data']['folder_id']            
            elif result_sub_folder['result'] == 'ER':
                return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}
        return {'result':'OK','messageText':folder_id}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data_subfolder),url,token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def onebox_save_file_v5(file_pdf,user_id,username,file_name,tax_id,doc_id,dept_name,doc_name_type,token_header):     
    ts = int(time.time())
    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    st2 = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
    year = datetime.datetime.fromtimestamp(ts).strftime('%Y')
    month_day = datetime.datetime.fromtimestamp(ts).strftime('%m-%d')
    check_year = False
    check_month_day = False
    check_docid = False
    list_response = []
    list_name_folder = [dept_name,doc_name_type]
    Thai_foldername = ['แผนก','ประเภทเอกสาร']
    try:
        # GET account_id จาก oneid
        headers = {
            'Authorization': token_onebox
        }
        data = {
            'user_id': str(user_id)
        }
        result_select_account_id = select_account_id_onebox(data,headers,token_header)
        # print ('result_select_account_id: ',result_select_account_id)
        if result_select_account_id['result'] == 'OK':
            result_select_account_id = result_select_account_id['messageText']
        elif result_select_account_id['result'] == 'ER':
            return {'result':'ER','messageText':None,'messageER':result_select_account_id['messageText'],'status_Code':200}
            # GET folder จาก account_id
        for i in range(len(result_select_account_id['result'])):
            if str(result_select_account_id['result'][i]['taxid']) == str(tax_id):
                account_id = result_select_account_id['result'][i]['account_id']
        
        data_account_id = {
            'account_id': str(account_id)
        }
        result_select_folder = select_folder_onebox(account_id,data_account_id,headers,token_header)
        # print ('result_select_folder: ',result_select_folder)
        if result_select_folder['result'] == 'OK':
            result_select_folder = result_select_folder['messageText']
        elif result_select_folder['result'] == 'ER':
            return {'result':'ER','messageText':None,'messageER':result_select_folder['messageText'],'status_Code':200}
        result_biz_name = select_2().select_bizname_by_taxid(tax_id)
        biz_name = result_biz_name['messageText']
        if biz_name == None:
            folder_id = result_select_folder['result'][0]['folder_id']
        elif biz_name != None:
            for n in range(len(result_select_folder['result'])):
                if str(result_select_folder['result'][n]['folder_name']) == str(biz_name):
                    folder_id = result_select_folder['result'][n]['folder_id']
        for c in range(len(list_name_folder)):
            check_folder = check_file_in_file_v2(folder_id,account_id,headers,doc_id,str(Thai_foldername[c]),str(list_name_folder[c]),token_header)
            if check_folder['result'] == 'OK':
                folder_id_docid = check_folder['messageText']
            elif check_folder['result'] == 'ER':
                return {'result':'ER','messageText':None,'messageER':check_folder['messageText'],'status_Code':200}
            
            data_save_file = {
                'account_id': str(account_id),
                'folder_id' : str(folder_id_docid)
            }
            unique_foldername = str(uuid.uuid4())
            list_file_name = []
            path = './storage/temp/' + unique_foldername +'/'
            path_indb = '/storage/temp/' + unique_foldername +'/'
            path_folder = '/storage/temp/'
            if not os.path.exists(path):
                os.makedirs(path)
            files = file_pdf
            data_userName = username
            unique_filename = str(uuid.uuid4())
            original_filename = str(file_name).split('.')[0]
            # original_filename = 'เอกสารสำคัญ'
            # check_thai = pythainlp.util.isthai(original_filename)
            # if check_thai == True:
            #     original_filename = romanize(original_filename, engine="thai2rom")
            typefile = str(file_name).split('.')[-1]
            typefile = typefile.split('"')[0]
            with open(path + original_filename + "." + typefile, "wb") as fh:
                file_open = fh 
                fh.write((file_pdf))
                list_file_name.append({'file_name_original':original_filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
            file_open = open(path + original_filename + "." + typefile, "rb")
            files_save = {
                'file' : file_open
            }    
            result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,data_userName,token_header)
            list_response.append(result_save_file)
            file_open.close()
        # result_insert = insert().insert_transactionfile_copy1(list_response,path_indb,unique_foldername)
        return {'result':'OK','messageText':list_response,'messageER':None,'status_Code':200}
        # return {'result':'OK','messageText':'OK','messageER':None,'status_Code':200}

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

    finally:
        path_removeFile = os.getcwd() + path_indb 
        # print (path_removeFile)
        shutil.rmtree(path_removeFile)

def check_file_in_file_v2_2(folder_id,account_id,headers,doc_id,dept_name,token_header):
    try:
        ts = int(time.time())
        year = str(datetime.datetime.fromtimestamp(ts).strftime('%Y'))
        month_day = str(datetime.datetime.fromtimestamp(ts).strftime('%m-%d'))
       
        list_temp = ['paperless','แผนก',dept_name,year,month_day,doc_id]
        list_keep = []
        for x in range(len(list_temp)):
            # print (x)
            check_year = False
            data_subfolder = {
                'account_id': str(account_id),
                'folder_id' : str(folder_id)
            }
            result_sub_folder = get_sub_folder_onebox(data_subfolder,headers,token_header)
            if result_sub_folder['result'] == 'OK':
                if result_sub_folder['messageText']['status'] == 'OK':
                    for a in range(len(result_sub_folder['messageText']['result'])):
                        if result_sub_folder['messageText']['result'][a]['folder_name'] == list_temp[x]:
                            folder_id = result_sub_folder['messageText']['result'][a]['folder_id']
                            check_year = True
                    if check_year == True:
                        folder_id = folder_id
                        pass
                    elif check_year == False:
                        data_folder_file = {
                            'account_id': str(account_id),
                            'parent_folder_id' : str(folder_id), 
                            'folder_name' : str(list_temp[x])
                        }        
                        result_create_folder = create_folder_onebox(data_folder_file,headers,token_header)
                        folder_id = result_create_folder['messageText']['data']['folder_id']

                elif result_sub_folder['messageText']['status'] == 'ER':
                    data_folder_file = {
                            'account_id': str(account_id),
                            'parent_folder_id' : str(folder_id), 
                            'folder_name' : str(list_temp[x])
                        }        
                    result_create_folder = create_folder_onebox(data_folder_file,headers,token_header)
                    folder_id = result_create_folder['messageText']['data']['folder_id']            
            elif result_sub_folder['result'] == 'ER':
                return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}
        return {'result':'OK','messageText':folder_id}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data_subfolder),url,token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def check_file_in_file_attach_v2(folder_id,account_id,headers,doc_id,Thai_foldername,name_folder,token_header):
    try:
        ts = int(time.time())
        year = str(datetime.datetime.fromtimestamp(ts).strftime('%Y'))
        month_day = str(datetime.datetime.fromtimestamp(ts).strftime('%m-%d'))
       
        list_temp = ['paperless',Thai_foldername,name_folder,year,month_day,doc_id,'attach_file']
        list_keep = []
        for x in range(len(list_temp)):
            check_year = False
            data_subfolder = {
                'account_id': str(account_id),
                'folder_id' : str(folder_id)
            }
            result_sub_folder = get_sub_folder_onebox(data_subfolder,headers,token_header)
            if result_sub_folder['result'] == 'OK':
                if result_sub_folder['messageText']['status'] == 'OK':
                    for a in range(len(result_sub_folder['messageText']['result'])):
                        if result_sub_folder['messageText']['result'][a]['folder_name'] == list_temp[x]:
                            folder_id = result_sub_folder['messageText']['result'][a]['folder_id']
                            check_year = True
                    if check_year == True:
                        folder_id = folder_id
                        pass
                    elif check_year == False:
                        data_folder_file = {
                            'account_id': str(account_id),
                            'parent_folder_id' : str(folder_id), 
                            'folder_name' : str(list_temp[x])
                        }        
                        result_create_folder = create_folder_onebox(data_folder_file,headers,token_header)
                        folder_id = result_create_folder['messageText']['data']['folder_id']

                elif result_sub_folder['messageText']['status'] == 'ER':
                    data_folder_file = {
                            'account_id': str(account_id),
                            'parent_folder_id' : str(folder_id), 
                            'folder_name' : str(list_temp[x])
                        }        
                    result_create_folder = create_folder_onebox(data_folder_file,headers,token_header)
                    folder_id = result_create_folder['messageText']['data']['folder_id']            
            elif result_sub_folder['result'] == 'ER':
                return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}
        return {'result':'OK','messageText':folder_id}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data_subfolder),url,token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def save_file_in_com(path,file_name,typefile,data):
    try:
        with open(path + file_name + "." + typefile, "wb") as fh:
            file_open = fh 
            fh.write(base64.decodebytes(data))

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageText':'Fail!','status_Code':200,}

def check_file_in_file_v3(folder_id,account_id,headers,doc_id,Thai_foldername,name_folder,token_header):
    try:
        ts = int(time.time())
        year = str(datetime.datetime.fromtimestamp(ts).strftime('%Y'))
        month_day = str(datetime.datetime.fromtimestamp(ts).strftime('%m-%d'))
       
        list_temp = ['paperless',Thai_foldername,name_folder,doc_id]
        list_keep = []
        for x in range(len(list_temp)):
            check_year = False
            data_subfolder = {
                'account_id': str(account_id),
                'folder_id' : str(folder_id)
            }
            result_sub_folder = get_sub_folder_onebox(data_subfolder,headers,token_header)
            # logger.info(result_sub_folder)
            if result_sub_folder['result'] == 'OK':
                if result_sub_folder['messageText']['status'] == 'OK':
                    for a in range(len(result_sub_folder['messageText']['result'])):
                        if result_sub_folder['messageText']['result'][a]['folder_name'] == list_temp[x]:
                            folder_id = result_sub_folder['messageText']['result'][a]['folder_id']
                            check_year = True
                    if check_year == True:
                        folder_id = folder_id
                        pass
                    elif check_year == False:
                        data_folder_file = {
                            'account_id': str(account_id),
                            'parent_folder_id' : str(folder_id), 
                            'folder_name' : str(list_temp[x])
                        }        
                        result_create_folder = create_folder_onebox(data_folder_file,headers,token_header)
                        folder_id = result_create_folder['messageText']['data']['folder_id']

                elif result_sub_folder['messageText']['status'] == 'ER':
                    data_folder_file = {
                            'account_id': str(account_id),
                            'parent_folder_id' : str(folder_id), 
                            'folder_name' : str(list_temp[x])
                        }        
                    result_create_folder = create_folder_onebox(data_folder_file,headers,token_header)
                    folder_id = result_create_folder['messageText']['data']['folder_id']
            elif result_sub_folder['result'] == 'ER':
                return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}
        return {'result':'OK','messageText':folder_id}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data_subfolder),url,token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def onebox_save_file_v6(file_pdf,user_id,username,file_name,tax_id,doc_id,dept_name,doc_name_type,token_header):     
    ts = int(time.time())
    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    st2 = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
    year = datetime.datetime.fromtimestamp(ts).strftime('%Y')
    month_day = datetime.datetime.fromtimestamp(ts).strftime('%m-%d')
    check_year = False
    check_month_day = False
    check_docid = False
    list_response = []
    # list_name_folder = [dept_name,doc_name_type]
    list_name_folder = dept_name
    list_name_folder2 = doc_name_type
    Thai_foldername = 'แผนก'
    Thai_foldername2 = 'ประเภทเอกสาร'
    count_fol = 0    
    unique_foldername = str(uuid.uuid4())
    path = path_global_1 + '/storage/temp/' + unique_foldername +'/'
    path_indb = '/storage/temp/' + unique_foldername +'/'
    path_folder = '/storage/temp/'
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        # GET account_id จาก oneid
        headers = {
            'Authorization': token_onebox
        }
        data = {
            'user_id': str(user_id)
        }
        result_select_account_id = select_account_id_onebox(data,headers,token_header)
        # print ('result_select_account_id: ',result_select_account_id)
        if result_select_account_id['result'] == 'OK':
            result_select_account_id = result_select_account_id['messageText']
        elif result_select_account_id['result'] == 'ER':
            return {'result':'ER','messageText':None,'messageER':result_select_account_id['messageText'],'status_Code':200}
            # GET folder จาก account_id
        for i in range(len(result_select_account_id['result'])):
            if str(result_select_account_id['result'][i]['taxid']) == str(tax_id):
                account_id = result_select_account_id['result'][i]['account_id']
        
        data_account_id = {
            'account_id': str(account_id)
        }
        result_select_folder = select_folder_onebox(account_id,data_account_id,headers,token_header)
        # print ('result_select_folder: ',result_select_folder)
        if result_select_folder['result'] == 'OK':
            result_select_folder = result_select_folder['messageText']
        elif result_select_folder['result'] == 'ER':
            return {'result':'ER','messageText':None,'messageER':result_select_folder['messageText'],'status_Code':200}
        result_biz_name = select_2().select_bizname_by_taxid(tax_id)
        biz_name = result_biz_name['messageText']
        # print ('biz_name: ',result_select_folder['result'][0]['folder_id'])
        if biz_name == None:
            folder_id = result_select_folder['result'][0]['folder_id']
        elif biz_name != None:
            for n in range(len(result_select_folder['result'])):
                # logger.info(result_select_folder['result'][n]['folder_name'])
                if count_fol == 2:
                    break
                if str(result_select_folder['result'][n]['folder_name']) == 'Private Main Folder' or str(result_select_folder['result'][n]['folder_name']) == 'โฟลเดอร์ส่วนตัว':
                    folder_first_name = 'Private Main Folder'
                    folder_id = result_select_folder['result'][n]['folder_id']
                    count_fol = count_fol+1
                elif str(result_select_folder['result'][n]['folder_name']) == str(biz_name):
                    folder_first_name = str(biz_name)
                    folder_id = result_select_folder['result'][n]['folder_id']
                    count_fol = count_fol+1
                else:
                    continue
                # for c in range(len(list_name_folder)):
                if folder_first_name == 'Private Main Folder':
                    check_folder = check_file_in_file_v3(folder_id,account_id,headers,doc_id,str(Thai_foldername2),str(list_name_folder2),token_header)
                    # logger.info(check_folder)
                elif folder_first_name == str(biz_name):
                    check_folder = check_file_in_file_v3(folder_id,account_id,headers,doc_id,str(Thai_foldername),str(list_name_folder),token_header)
                if check_folder['result'] == 'OK':
                    folder_id_docid = check_folder['messageText']
                elif check_folder['result'] == 'ER':
                    return {'result':'ER','messageText':None,'messageER':check_folder['messageText'],'status_Code':200}
                
                data_save_file = {
                    'account_id': str(account_id),
                    'folder_id' : str(folder_id_docid)
                }
                list_file_name = []
                files = file_pdf
                data_userName = username
                unique_filename = str(uuid.uuid4())
                original_filename = str(file_name).split('.')[0]
                # original_filename = 'เอกสารสำคัญ'
                # check_thai = pythainlp.util.isthai(original_filename)
                # if check_thai == True:
                #     original_filename = romanize(original_filename, engine="thai2rom")
                typefile = str(file_name).split('.')[-1]
                typefile = typefile.split('"')[0]
                with open(path + original_filename + "." + typefile, "wb") as fh:
                    file_open = fh 
                    fh.write((file_pdf))
                    list_file_name.append({'file_name_original':original_filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                file_open = open(path + original_filename + "." + typefile, "rb")
                files_save = {
                    'file' : file_open
                }    
                result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,data_userName,token_header)
                # print(result_save_file)
                list_response.append(result_save_file)
                file_open.close()
        # result_insert = insert().insert_transactionfile_copy1(list_response,path_indb,unique_foldername)
        return {'result':'OK','messageText':list_response,'messageER':None,'status_Code':200}
        # return {'result':'OK','messageText':'OK','messageER':None,'status_Code':200}

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

    finally:
        path_removeFile = path_global_1 + path_indb 
        # print (path_removeFile)
        shutil.rmtree(path_removeFile)

# def check_file_in_file_v4(folder_id,account_id,headers,doc_id,Thai_foldername,name_folder,token_header,dept_id):
#     try:
#         ts = int(time.time())
#         year = str(datetime.datetime.fromtimestamp(ts).strftime('%Y'))
#         month_day = str(datetime.datetime.fromtimestamp(ts).strftime('%m-%d'))
       
#         list_temp = ['paperless',Thai_foldername,name_folder,doc_id]
#         list_keep = []
#         for x in range(len(list_temp)):
#             check_year = False
#             data_subfolder = {
#                 'account_id': str(account_id),
#                 'folder_id' : str(folder_id)
#             }
#             result_sub_folder = get_sub_folder_onebox(data_subfolder,headers,token_header)
#             # logger.info(result_sub_folder)
#             if result_sub_folder['result'] == 'OK':
#                 if result_sub_folder['messageText']['status'] == 'OK':
#                     for a in range(len(result_sub_folder['messageText']['result'])):
#                         if result_sub_folder['messageText']['result'][a]['folder_name'] == list_temp[x]:
#                             folder_id = result_sub_folder['messageText']['result'][a]['folder_id']
#                             check_year = True
#                     if check_year == True:
#                         folder_id = folder_id
#                         pass
#                     elif check_year == False:
#                         data_folder_file = {
#                                             "account_id": str(account_id),
#                                             "account_id_to_setting": [],
#                                             "department_id_to_setting": [
#                                                 {
#                                                     "id": str(dept_id),
#                                                     "permission": {
#                                                         "view_only": "True",
#                                                         "download": "True",
#                                                         "edit": "True"
#                                                     }
#                                                 }
#                                             ],
#                                             "folder_name": str(list_temp[x]),
#                                             "parent_folder_id": str(folder_id)
#                                         }   
#                         print ('aaaaaaaaaaaaaaaaaaaaaaaaaaa')     
#                         result_create_folder = create_folder_onebox_with_permis(data_folder_file,headers,token_header)
#                         folder_id = result_create_folder['messageText']['data']['folder_id']

#                 elif result_sub_folder['messageText']['status'] == 'ER':
#                     data_folder_file = {
#                                             "account_id": str(account_id),
#                                             "account_id_to_setting": [],
#                                             "department_id_to_setting": [
#                                                 {
#                                                     "id": str(dept_id),
#                                                     "permission": {
#                                                         "view_only": "True",
#                                                         "download": "True",
#                                                         "edit": "True"
#                                                     }
#                                                 }
#                                             ],
#                                             "folder_name": str(list_temp[x]),
#                                             "parent_folder_id": str(folder_id)
#                                         }
#                     print ('bbbbbbbbbbbbbbbbbbbbbbbbb')
#                     result_create_folder = create_folder_onebox_with_permis(data_folder_file,headers,token_header)
#                     folder_id = result_create_folder['messageText']['data']['folder_id']
#             elif result_sub_folder['result'] == 'ER':
#                 return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}
#         return {'result':'OK','messageText':folder_id}
#     except Exception as ex:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(exc_type, fname, exc_tb.tb_lineno)
#         insert().insert_tran_log_v1(str(ex),'ER',str(data_subfolder),url,token_header,'')
#         return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def check_file_in_file_v4(folder_id,account_id,headers,doc_id,Thai_foldername,name_folder,token_header,dept_id):
    try:
        ts = int(time.time())
        year = str(datetime.datetime.fromtimestamp(ts).strftime('%Y'))
        month_day = str(datetime.datetime.fromtimestamp(ts).strftime('%m-%d'))
       
        list_temp = ['paperless',Thai_foldername,name_folder,doc_id]
        list_keep = []
        for x in range(len(list_temp)):
            check_year = False
            data_subfolder = {
                'account_id': str(account_id),
                'folder_id' : str(folder_id)
            }
            result_sub_folder = get_sub_folder_onebox(data_subfolder,headers,token_header)
            # print ('result_sub_folder:',result_sub_folder)
            if result_sub_folder['result'] == 'OK':
                if result_sub_folder['messageText']['status'] == 'OK':
                    for a in range(len(result_sub_folder['messageText']['result'])):
                        if result_sub_folder['messageText']['result'][a]['folder_name'] == list_temp[x]:
                            folder_id = result_sub_folder['messageText']['result'][a]['folder_id']
                            check_year = True
                    if check_year == True:
                        folder_id = folder_id
                        if x >= 2:
                            data_back = {
                                'account_id': str(account_id),
                                'folder_id' : str(folder_id),
                                'dept_id' : str(dept_id),
                                'headers' : headers,
                                'token_header' : token_header
                            }
                            start_run_background(account_id,folder_id,dept_id,headers,token_header)
                            # executor.submit(start_run_background,account_id,folder_id,dept_id,headers,token_header)
                        pass
                    elif check_year == False:
                        data_folder_file = {
                                            "account_id": str(account_id),
                                            "account_id_to_setting": [],
                                            "department_id_to_setting": [
                                                {
                                                    "id": str(dept_id),
                                                    "permission": {
                                                        "view_only": "True",
                                                        "download": "True",
                                                        "edit": "True"
                                                    }
                                                }
                                            ],
                                            "folder_name": str(list_temp[x]),
                                            "parent_folder_id": str(folder_id)
                                        }   
                        result_create_folder = create_folder_onebox_with_permis(data_folder_file,headers,token_header)
                        folder_id = result_create_folder['messageText']['data']['folder_id']

                elif result_sub_folder['messageText']['status'] == 'ER':
                    data_folder_file = {
                                            "account_id": str(account_id),
                                            "account_id_to_setting": [],
                                            "department_id_to_setting": [
                                                {
                                                    "id": str(dept_id),
                                                    "permission": {
                                                        "view_only": "True",
                                                        "download": "True",
                                                        "edit": "True"
                                                    }
                                                }
                                            ],
                                            "folder_name": str(list_temp[x]),
                                            "parent_folder_id": str(folder_id)
                                        }
                    result_create_folder = create_folder_onebox_with_permis(data_folder_file,headers,token_header)
                    folder_id = result_create_folder['messageText']['data']['folder_id']
            elif result_sub_folder['result'] == 'ER':
                return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}
        return {'result':'OK','messageText':folder_id}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data_subfolder),url,token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def onebox_save_file_v7(file_pdf,user_id,username,file_name,tax_id,doc_id,dept_name,doc_name_type,token_header):     
    ts = int(time.time())
    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    st2 = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
    year = datetime.datetime.fromtimestamp(ts).strftime('%Y')
    month_day = datetime.datetime.fromtimestamp(ts).strftime('%m-%d')
    check_year = False
    check_month_day = False
    check_docid = False
    list_response = []
    # list_name_folder = [dept_name,doc_name_type]
    list_name_folder = dept_name
    list_name_folder2 = doc_name_type
    Thai_foldername = 'แผนก'
    Thai_foldername2 = 'ประเภทเอกสาร'
    count_fol = 0    
    unique_foldername = str(uuid.uuid4())
    path = path_global_1 + '/storage/temp/' + unique_foldername +'/'
    path_indb = '/storage/temp/' + unique_foldername +'/'
    path_folder = '/storage/temp/'
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        # GET account_id จาก oneid
        headers = {
            'Authorization': token_onebox
        }
        data = {
            'user_id': str(user_id)
        }
        result_select_account_id = select_account_id_onebox(data,headers,token_header)
        # print ('result_select_account_id: ',result_select_account_id)
        if result_select_account_id['result'] == 'OK':
            result_select_account_id = result_select_account_id['messageText']
        elif result_select_account_id['result'] == 'ER':
            return {'result':'ER','messageText':None,'messageER':result_select_account_id['messageText'],'status_Code':200}
            # GET folder จาก account_id
        for i in range(len(result_select_account_id['result'])):
            if str(result_select_account_id['result'][i]['taxid']) == str(tax_id):
                account_id = result_select_account_id['result'][i]['account_id']
        data_account_id = {
            'account_id': str(account_id)
        }
        result_select_folder = select_folder_onebox(account_id,data_account_id,headers,token_header)
        # print ('result_select_folder: ',result_select_folder)
        if result_select_folder['result'] == 'OK':
            result_select_folder = result_select_folder['messageText']
        elif result_select_folder['result'] == 'ER':
            return {'result':'ER','messageText':None,'messageER':result_select_folder['messageText'],'status_Code':200}
        result_biz_name = select_2().select_bizname_by_taxid(tax_id)
        biz_name = result_biz_name['messageText']
        # print ('biz_name: ',result_select_folder['result'][0]['folder_id'])
        if biz_name == None:
            folder_id = result_select_folder['result'][0]['folder_id']
        elif biz_name != None:
            for n in range(len(result_select_folder['result'])):
                # logger.info(result_select_folder['result'][n]['folder_name'])
                if count_fol == 2:
                    break
                if str(result_select_folder['result'][n]['folder_name']) == 'Private Main Folder' or str(result_select_folder['result'][n]['folder_name']) == 'โฟลเดอร์ส่วนตัว':
                    folder_first_name = 'Private Main Folder'
                    folder_id = result_select_folder['result'][n]['folder_id']
                    count_fol = count_fol+1
                elif str(result_select_folder['result'][n]['folder_name']) == str(biz_name):
                    folder_first_name = str(biz_name)
                    folder_id = result_select_folder['result'][n]['folder_id']
                    count_fol = count_fol+1
                else:
                    continue
                # for c in range(len(list_name_folder)):
                result_department = get_department_account(str(tax_id),headers,token_header,account_id)
                if result_department['result'] == 'OK':
                    dept_id = None
                    department_all = result_department['messageText']['result']['department']
                    # print ('depart_name:',dept_name)
                    # print ('result_department:',department_all)
                    # print (len(department_all))
                    for d in range(len(department_all)):
                        if department_all[d]['department_name'] == dept_name:
                            # print (department_all[d]['department_name'])
                            dept_id = department_all[d]['id']
                        elif d == (len(department_all))-1 and dept_id == None:
                            # print (department_all[d]['department_name'])
                            dept_id = None
                    # print ('dept_id:',dept_id)                    
                    if folder_first_name == 'Private Main Folder':
                        # check_folder = check_file_in_file_v3(folder_id,account_id,headers,doc_id,str(Thai_foldername2),str(list_name_folder2),token_header)
                        check_folder = check_file_in_file_v3(folder_id,account_id,headers,doc_id,str(Thai_foldername2),str(list_name_folder2),token_header)
                        # logger.info(check_folder)
                    elif folder_first_name == str(biz_name):
                        # check_folder = check_file_in_file_v3(folder_id,account_id,headers,doc_id,str(Thai_foldername),str(list_name_folder),token_header)
                        if dept_id == None:
                            check_folder = check_file_in_file_v3(folder_id,account_id,headers,doc_id,str(Thai_foldername),str(list_name_folder),token_header)
                        else:
                            check_folder = check_file_in_file_v4(folder_id,account_id,headers,doc_id,str(Thai_foldername),str(list_name_folder),token_header,dept_id)
                    if check_folder['result'] == 'OK':
                        folder_id_docid = check_folder['messageText']
                    elif check_folder['result'] == 'ER':
                        return {'result':'ER','messageText':None,'messageER':check_folder['messageText'],'status_Code':200}
                    
                    data_save_file = {
                        'account_id': str(account_id),
                        'folder_id' : str(folder_id_docid)
                    }
                    list_file_name = []
                    files = file_pdf
                    data_userName = username
                    unique_filename = str(uuid.uuid4())
                    original_filename = str(file_name).split('.')[0]
                    # original_filename = 'เอกสารสำคัญ'
                    # check_thai = pythainlp.util.isthai(original_filename)
                    # if check_thai == True:
                    #     original_filename = romanize(original_filename, engine="thai2rom")
                    typefile = str(file_name).split('.')[-1]
                    typefile = typefile.split('"')[0]
                    try:
                        with open(path + original_filename + "." + typefile, "wb") as fh:
                            file_open = fh 
                            fh.write((file_pdf))
                            list_file_name.append({'file_name_original':original_filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                    except Exception as e:
                        return {'result':'ER','messageText':None,'messageER':result_department['messageText'],'status_Code':200} 
                    file_open = open(path + original_filename + "." + typefile, "rb")
                    files_save = {
                        'file' : file_open
                    }    
                    result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,data_userName,token_header)
                    if result_save_file['result'] == 'ER':
                        return {'result':'ER','messageText':None,'messageER':result_department['messageText'],'status_Code':200}                        
                    list_response.append(result_save_file)
                    file_open.close()
                else:
                    return {'result':'ER','messageText':None,'messageER':result_department['messageText'],'status_Code':200}
        # result_insert = insert().insert_transactionfile_copy1(list_response,path_indb,unique_foldername)
        # return {'result':'OK','messageText':list_response,'messageER':None,'status_Code':200}
        return {'result':'OK','messageText':'OK','messageER':None,'status_Code':200}

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}
    finally:
        path_removeFile = path_global_1 + path_indb 
        shutil.rmtree(path_removeFile)

def get_attach_to_onebox(sid,username,user_id,tax_id,dept_name,doc_name_type,token_header):
    try:
        # result_select = select().select_get_pdf(sid)
        result_select = select_2().select_attach_file_onebox(sid) # เพิ่มใหม่
        if result_select['result'] == 'OK':
            eval_result = eval(str(result_select['messageText']))
            doc_id = eval_result[0]['document_id']
            attempted_folder = eval_result[0]['attempted_folder']
            pathfolder = path_global_1 + str(eval_result[0]['pathfolder'])
            file_name_new = eval(str(eval_result[0]['json_data']))[0]['file_name_new']
            file_name = eval(str(eval_result[0]['json_data']))[0]['file_name_original']
            with open(pathfolder+file_name_new,'rb') as fs:
                file_read = fs.read()
            try:
                result_onebox = onebox_save_attach_file(file_read,user_id,username,file_name,tax_id,doc_id,dept_name,doc_name_type,token_header)
            except UnboundLocalError as e:
                print(str(e))
            if result_onebox['result'] == 'OK':
                return {'result':'OK','messageText':'Success','messageER':None,'status_Code':200}
            elif result_onebox['result'] == 'ER':
                return {'result':'ER','messageText':None,'messageER':result_onebox['messageER'],'status_Code':200}
        else:
            return {'result':'ER','messageText':None,'messageER':'Not Found','status_Code':200}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(ex),'',token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def get_attach_to_onebox_push(sid,username,user_id,tax_id,dept_name,doc_name_type,token_header,file_string,original_filename):
    try:
        list_result = []
        result_filename = select_2().select_pdf_filename(sid)
        if result_filename['result'] == 'OK':
            doc_id = result_filename['messageText']['doc_id']
            file_name = original_filename
            file_read = file_string
            try:
                for i in range(len(file_read)):
                    result_onebox = onebox_save_attach_file(file_read[i],user_id,username,file_name[i],tax_id,doc_id,dept_name,doc_name_type,token_header)
                    list_result.append(result_onebox['messageText'][0])
                    # print ('list_result:',list_result)
            except UnboundLocalError as e:
                print(str(e))
            if result_onebox['result'] == 'OK':
                return {'result':'OK','messageText':list_result,'messageER':None,'status_Code':200}
            elif result_onebox['result'] == 'ER':
                return {'result':'ER','messageText':None,'messageER':result_onebox['messageER'],'status_Code':200}
        else:
            return {'result':'ER','messageText':None,'messageER':'Not Found','status_Code':200}
    except Exception as ex:
        print (str(ex))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(ex),'',token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def onebox_save_attach_file(file_pdf,user_id,username,file_name,tax_id,doc_id,dept_name,doc_name_type,token_header):  
    ts = int(time.time())
    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    st2 = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
    year = datetime.datetime.fromtimestamp(ts).strftime('%Y')
    month_day = datetime.datetime.fromtimestamp(ts).strftime('%m-%d')
    check_year = False
    check_month_day = False
    check_docid = False
    list_response = []
    # list_name_folder = [dept_name,doc_name_type]
    list_name_folder = dept_name
    list_name_folder2 = doc_name_type
    Thai_foldername = 'แผนก'
    Thai_foldername2 = 'ประเภทเอกสาร'
    count_fol = 0    
    unique_foldername = str(uuid.uuid4())
    path = path_global_1 + '/storage/temp/' + unique_foldername +'/'
    path_indb = '/storage/temp/' + unique_foldername +'/'
    path_folder = '/storage/temp/'
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        # GET account_id จาก oneid
        headers = {
            'Authorization': token_onebox
        }
        data = {
            'user_id': str(user_id)
        }
        result_select_account_id = select_account_id_onebox(data,headers,token_header)
        # print ('result_select_account_id: ',result_select_account_id)
        if result_select_account_id['result'] == 'OK':
            result_select_account_id = result_select_account_id['messageText']
        elif result_select_account_id['result'] == 'ER':
            return {'result':'ER','messageText':None,'messageER':result_select_account_id['messageText'],'status_Code':200}
            # GET folder จาก account_id
        for i in range(len(result_select_account_id['result'])):
            if str(result_select_account_id['result'][i]['taxid']) == str(tax_id):
                account_id = result_select_account_id['result'][i]['account_id']
        data_account_id = {
            'account_id': str(account_id)
        }
        result_select_folder = select_folder_onebox(account_id,data_account_id,headers,token_header)
        # print ('result_select_folder: ',result_select_folder)
        if result_select_folder['result'] == 'OK':
            result_select_folder = result_select_folder['messageText']
        elif result_select_folder['result'] == 'ER':
            return {'result':'ER','messageText':None,'messageER':result_select_folder['messageText'],'status_Code':200}
        result_biz_name = select_2().select_bizname_by_taxid(tax_id)
        biz_name = result_biz_name['messageText']
        # print ('biz_name: ',result_select_folder['result'][0]['folder_id'])
        if biz_name == None:
            folder_id = result_select_folder['result'][0]['folder_id']
        elif biz_name != None:
            for n in range(len(result_select_folder['result'])):
                # logger.info(result_select_folder['result'][n]['folder_name'])
                if count_fol == 2:
                    break
                if str(result_select_folder['result'][n]['folder_name']) == 'Private Main Folder' or str(result_select_folder['result'][n]['folder_name']) == 'โฟลเดอร์ส่วนตัว':
                    folder_first_name = 'Private Main Folder'
                    folder_id = result_select_folder['result'][n]['folder_id']
                    count_fol = count_fol+1
                elif str(result_select_folder['result'][n]['folder_name']) == str(biz_name):
                    folder_first_name = str(biz_name)
                    folder_id = result_select_folder['result'][n]['folder_id']
                    count_fol = count_fol+1
                else:
                    continue
                # for c in range(len(list_name_folder)):
                result_department = get_department_account(str(tax_id),headers,token_header,account_id)
                if result_department['result'] == 'OK':
                    dept_id = None
                    department_all = result_department['messageText']['result']['department']
                    for d in range(len(department_all)):
                        if department_all[d]['department_name'] == dept_name:
                            dept_id = department_all[d]['id']
                        elif d == (len(department_all))-1 and dept_id == None:
                            dept_id = None
                    if folder_first_name == 'Private Main Folder':
                        # check_folder = check_file_in_file_v3(folder_id,account_id,headers,doc_id,str(Thai_foldername2),str(list_name_folder2),token_header)
                        check_folder = check_file_in_file_attach_no_permis(folder_id,account_id,headers,doc_id,str(Thai_foldername2),str(list_name_folder2),token_header)
                        # logger.info(check_folder)
                    elif folder_first_name == str(biz_name):
                        # check_folder = check_file_in_file_v3(folder_id,account_id,headers,doc_id,str(Thai_foldername),str(list_name_folder),token_header)
                        if dept_id == None:
                            check_folder = check_file_in_file_attach_no_permis(folder_id,account_id,headers,doc_id,str(Thai_foldername),str(list_name_folder),token_header)
                        else:
                            check_folder = check_file_in_file_attach_permis(folder_id,account_id,headers,doc_id,str(Thai_foldername),str(list_name_folder),token_header,dept_id)
                    if check_folder['result'] == 'OK':
                        folder_id_docid = check_folder['messageText']
                    elif check_folder['result'] == 'ER':
                        return {'result':'ER','messageText':None,'messageER':check_folder['messageText'],'status_Code':200}
                    
                    data_save_file = {
                        'account_id': str(account_id),
                        'folder_id' : str(folder_id_docid)
                    }
                    list_file_name = []
                    files = file_pdf
                    data_userName = username
                    unique_filename = str(uuid.uuid4())
                    original_filename = str(file_name).split('.')[0]
                    # original_filename = 'เอกสารสำคัญ'
                    # check_thai = pythainlp.util.isthai(original_filename)
                    # if check_thai == True:
                    #     original_filename = romanize(original_filename, engine="thai2rom")
                    typefile = str(file_name).split('.')[-1]
                    typefile = typefile.split('"')[0]
                    with open(path + original_filename + "." + typefile, "wb") as fh:
                        file_open = fh 
                        fh.write((file_pdf))
                        list_file_name.append({'file_name_original':original_filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
                    file_open = open(path + original_filename + "." + typefile, "rb")
                    files_save = {
                        'file' : file_open
                    }    
                    result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,data_userName,token_header)
                    list_response.append(result_save_file)
                    file_open.close()
                else:
                    return {'result':'ER','messageText':None,'messageER':result_department['messageText'],'status_Code':200}
        return {'result':'OK','messageText':result_save_file['messageText'],'messageER':None,'status_Code':200}
        # result_insert = insert().insert_transactionfile_copy1(list_response,path_indb,unique_foldername)
        # return {'result':'OK','messageText':list_response,'messageER':None,'status_Code':200}
        # return {'result':'OK','messageText':'OK','messageER':None,'status_Code':200}

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}
    finally:
        path_removeFile = path_global_1 + path_indb 
        # print (path_removeFile)
        shutil.rmtree(path_removeFile)

def check_file_in_file_attach_permis(folder_id,account_id,headers,doc_id,Thai_foldername,name_folder,token_header,dept_id):
    try:
        ts = int(time.time())
        year = str(datetime.datetime.fromtimestamp(ts).strftime('%Y'))
        month_day = str(datetime.datetime.fromtimestamp(ts).strftime('%m-%d'))
       
        list_temp = ['paperless',Thai_foldername,name_folder,doc_id,'Attachment']
        list_keep = []
        for x in range(len(list_temp)):
            check_year = False
            data_subfolder = {
                'account_id': str(account_id),
                'folder_id' : str(folder_id)
            }
            result_sub_folder = get_sub_folder_onebox(data_subfolder,headers,token_header)
            # print ('result_sub_folder:',result_sub_folder)
            if result_sub_folder['result'] == 'OK':
                if result_sub_folder['messageText']['status'] == 'OK':
                    for a in range(len(result_sub_folder['messageText']['result'])):
                        if result_sub_folder['messageText']['result'][a]['folder_name'] == list_temp[x]:
                            folder_id = result_sub_folder['messageText']['result'][a]['folder_id']
                            check_year = True
                    if check_year == True:
                        folder_id = folder_id
                        if x >= 2:
                            data_back = {
                                'account_id': str(account_id),
                                'folder_id' : str(folder_id),
                                'dept_id' : str(dept_id),
                                'headers' : headers,
                                'token_header' : token_header
                            }
                            # executor.submit(start_run_background,account_id,folder_id,dept_id,headers,token_header)
                            run_back = start_run_background(account_id,folder_id,dept_id,headers,token_header)
                        pass
                    elif check_year == False:
                        data_folder_file = {
                                            "account_id": str(account_id),
                                            "account_id_to_setting": [],
                                            "department_id_to_setting": [
                                                {
                                                    "id": str(dept_id),
                                                    "permission": {
                                                        "view_only": "True",
                                                        "download": "True",
                                                        "edit": "True"
                                                    }
                                                }
                                            ],
                                            "folder_name": str(list_temp[x]),
                                            "parent_folder_id": str(folder_id)
                                        }   
                        result_create_folder = create_folder_onebox_with_permis(data_folder_file,headers,token_header)
                        folder_id = result_create_folder['messageText']['data']['folder_id']

                elif result_sub_folder['messageText']['status'] == 'ER':
                    data_folder_file = {
                                            "account_id": str(account_id),
                                            "account_id_to_setting": [],
                                            "department_id_to_setting": [
                                                {
                                                    "id": str(dept_id),
                                                    "permission": {
                                                        "view_only": "True",
                                                        "download": "True",
                                                        "edit": "True"
                                                    }
                                                }
                                            ],
                                            "folder_name": str(list_temp[x]),
                                            "parent_folder_id": str(folder_id)
                                        }
                    result_create_folder = create_folder_onebox_with_permis(data_folder_file,headers,token_header)
                    folder_id = result_create_folder['messageText']['data']['folder_id']
            elif result_sub_folder['result'] == 'ER':
                return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}
        return {'result':'OK','messageText':folder_id}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data_subfolder),url,token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

def check_file_in_file_attach_no_permis(folder_id,account_id,headers,doc_id,Thai_foldername,name_folder,token_header):
    try:
        ts = int(time.time())
        year = str(datetime.datetime.fromtimestamp(ts).strftime('%Y'))
        month_day = str(datetime.datetime.fromtimestamp(ts).strftime('%m-%d'))
       
        list_temp = ['paperless',Thai_foldername,name_folder,doc_id,'Attachment']
        list_keep = []
        for x in range(len(list_temp)):
            check_year = False
            data_subfolder = {
                'account_id': str(account_id),
                'folder_id' : str(folder_id)
            }
            result_sub_folder = get_sub_folder_onebox(data_subfolder,headers,token_header)
            # logger.info(result_sub_folder)
            if result_sub_folder['result'] == 'OK':
                if result_sub_folder['messageText']['status'] == 'OK':
                    for a in range(len(result_sub_folder['messageText']['result'])):
                        if result_sub_folder['messageText']['result'][a]['folder_name'] == list_temp[x]:
                            folder_id = result_sub_folder['messageText']['result'][a]['folder_id']
                            check_year = True
                    if check_year == True:
                        folder_id = folder_id
                        pass
                    elif check_year == False:
                        data_folder_file = {
                            'account_id': str(account_id),
                            'parent_folder_id' : str(folder_id), 
                            'folder_name' : str(list_temp[x])
                        }        
                        result_create_folder = create_folder_onebox(data_folder_file,headers,token_header)
                        folder_id = result_create_folder['messageText']['data']['folder_id']

                elif result_sub_folder['messageText']['status'] == 'ER':
                    data_folder_file = {
                            'account_id': str(account_id),
                            'parent_folder_id' : str(folder_id), 
                            'folder_name' : str(list_temp[x])
                        }        
                    result_create_folder = create_folder_onebox(data_folder_file,headers,token_header)
                    folder_id = result_create_folder['messageText']['data']['folder_id']
            elif result_sub_folder['result'] == 'ER':
                return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}
        return {'result':'OK','messageText':folder_id}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(data_subfolder),url,token_header,'')
        return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}


# def onebox_save_file_v7(file_pdf,user_id,username,file_name,tax_id,doc_id,dept_name,doc_name_type,token_header):     
#     ts = int(time.time())
#     st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
#     st2 = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
#     year = datetime.datetime.fromtimestamp(ts).strftime('%Y')
#     month_day = datetime.datetime.fromtimestamp(ts).strftime('%m-%d')
#     check_year = False
#     check_month_day = False
#     check_docid = False
#     list_response = []
#     # list_name_folder = [dept_name,doc_name_type]
#     list_name_folder = dept_name
#     list_name_folder2 = doc_name_type
#     Thai_foldername = 'แผนก'
#     Thai_foldername2 = 'ประเภทเอกสาร'
#     count_fol = 0    
#     unique_foldername = str(uuid.uuid4())
#     path = path_global_1 + '/storage/temp/' + unique_foldername +'/'
#     path_indb = '/storage/temp/' + unique_foldername +'/'
#     path_folder = '/storage/temp/'
#     if not os.path.exists(path):
#         os.makedirs(path)
#     try:
#         # GET account_id จาก oneid
#         headers = {
#             'Authorization': token_onebox
#         }
#         data = {
#             'user_id': str(user_id)
#         }
#         result_select_account_id = select_account_id_onebox(data,headers,token_header)
#         # print ('result_select_account_id: ',result_select_account_id)
#         if result_select_account_id['result'] == 'OK':
#             result_select_account_id = result_select_account_id['messageText']
#         elif result_select_account_id['result'] == 'ER':
#             return {'result':'ER','messageText':None,'messageER':result_select_account_id['messageText'],'status_Code':200}
#             # GET folder จาก account_id
#         for i in range(len(result_select_account_id['result'])):
#             if str(result_select_account_id['result'][i]['taxid']) == str(tax_id):
#                 account_id = result_select_account_id['result'][i]['account_id']
#         data_account_id = {
#             'account_id': str(account_id)
#         }
#         result_select_folder = select_folder_onebox(account_id,data_account_id,headers,token_header)
#         # print ('result_select_folder: ',result_select_folder)
#         if result_select_folder['result'] == 'OK':
#             result_select_folder = result_select_folder['messageText']
#         elif result_select_folder['result'] == 'ER':
#             return {'result':'ER','messageText':None,'messageER':result_select_folder['messageText'],'status_Code':200}
#         result_biz_name = select_2().select_bizname_by_taxid(tax_id)
#         biz_name = result_biz_name['messageText']
#         # print ('biz_name: ',result_select_folder['result'][0]['folder_id'])
#         if biz_name == None:
#             folder_id = result_select_folder['result'][0]['folder_id']
#         elif biz_name != None:
#             for n in range(len(result_select_folder['result'])):
#                 # logger.info(result_select_folder['result'][n]['folder_name'])
#                 if count_fol == 2:
#                     break
#                 if str(result_select_folder['result'][n]['folder_name']) == 'Private Main Folder' or str(result_select_folder['result'][n]['folder_name']) == 'โฟลเดอร์ส่วนตัว':
#                     folder_first_name = 'Private Main Folder'
#                     folder_id = result_select_folder['result'][n]['folder_id']
#                     count_fol = count_fol+1
#                 elif str(result_select_folder['result'][n]['folder_name']) == str(biz_name):
#                     folder_first_name = str(biz_name)
#                     folder_id = result_select_folder['result'][n]['folder_id']
#                     count_fol = count_fol+1
#                 else:
#                     continue
#                 # for c in range(len(list_name_folder)):
#                 result_department = get_department_account(str(tax_id),headers,token_header)
#                 if result_department['result'] == 'OK':
#                     dept_id = None
#                     department_all = result_department['messageText']['result']['department']
#                     print ('depart_name:',dept_name)
#                     # print ('result_department:',department_all)
#                     # print (len(department_all))
#                     for d in range(len(department_all)):
#                         if department_all[d]['department_name'] == dept_name:
#                             # print (department_all[d]['department_name'])
#                             dept_id = department_all[d]['id']
#                         elif d == (len(department_all))-1 and dept_id == None:
#                             # print (department_all[d]['department_name'])
#                             dept_id = 'no_department'
#                     print ('dept_id:',dept_id)                    
#                     if folder_first_name == 'Private Main Folder':
#                         # check_folder = check_file_in_file_v3(folder_id,account_id,headers,doc_id,str(Thai_foldername2),str(list_name_folder2),token_header)
#                         check_folder = check_file_in_file_v4(folder_id,account_id,headers,doc_id,str(Thai_foldername2),str(list_name_folder2),token_header,dept_id)
#                         print ('check_folder:',check_folder)
#                         # logger.info(check_folder)
#                     elif folder_first_name == str(biz_name):
#                         # check_folder = check_file_in_file_v3(folder_id,account_id,headers,doc_id,str(Thai_foldername),str(list_name_folder),token_header)
#                         check_folder = check_file_in_file_v4(folder_id,account_id,headers,doc_id,str(Thai_foldername),str(list_name_folder),token_header,dept_id)
#                         print ('check_folder222:',check_folder)
#                     if check_folder['result'] == 'OK':
#                         folder_id_docid = check_folder['messageText']
#                     elif check_folder['result'] == 'ER':
#                         return {'result':'ER','messageText':None,'messageER':check_folder['messageText'],'status_Code':200}
                    
#                     data_save_file = {
#                         'account_id': str(account_id),
#                         'folder_id' : str(folder_id_docid)
#                     }
#                     list_file_name = []
#                     files = file_pdf
#                     data_userName = username
#                     unique_filename = str(uuid.uuid4())
#                     original_filename = str(file_name).split('.')[0]
#                     # original_filename = 'เอกสารสำคัญ'
#                     # check_thai = pythainlp.util.isthai(original_filename)
#                     # if check_thai == True:
#                     #     original_filename = romanize(original_filename, engine="thai2rom")
#                     typefile = str(file_name).split('.')[-1]
#                     typefile = typefile.split('"')[0]
#                     with open(path + original_filename + "." + typefile, "wb") as fh:
#                         file_open = fh 
#                         fh.write((file_pdf))
#                         list_file_name.append({'file_name_original':original_filename,'file_name_new':original_filename + '.' + typefile,'file_upload_datetime':str(st),'username':data_userName})
#                     file_open = open(path + original_filename + "." + typefile, "rb")
#                     files_save = {
#                         'file' : file_open
#                     }    
#                     result_save_file = save_file_onebox(data_save_file,files_save,headers,st2,data_userName,token_header)
#                     print ('result_save_file:',result_save_file)
#                     list_response.append(result_save_file)
#                     file_open.close()
#                 else:
#                     return {'result':'ER','messageText':None,'messageER':result_department['messageText'],'status_Code':200}
#         # result_insert = insert().insert_transactionfile_copy1(list_response,path_indb,unique_foldername)
#         # return {'result':'OK','messageText':list_response,'messageER':None,'status_Code':200}
#         return {'result':'OK','messageText':'OK','messageER':None,'status_Code':200}

#     except Exception as ex:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(exc_type, fname, exc_tb.tb_lineno)
#         insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header,'')
#         return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

#     finally:
#         path_removeFile = path_global_1 + path_indb 
#         print (path_removeFile)
#         shutil.rmtree(path_removeFile)

