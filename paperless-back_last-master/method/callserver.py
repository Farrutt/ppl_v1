#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config.lib import *
from config.value import *
from db.db_method import *

def callPost_Test(path,data):
    url = path
    payload = data
    try:
        response = requests.request("POST", url=url, json=payload, verify=False, stream=True)
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url,None)
            return {'result': 'OK','messageText': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload),url,None)
            return {'result': 'ER','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def callPost(path, data):
    url = path
    payload = data
    print(url)
    try:
        response = requests.request("POST", url=url, json=payload, verify=False, stream=True)
        payload['password'] = ''
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url,None)
            return {'result': 'OK','messageText': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload),url,None)
            return {'result': 'ER','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def func_call_check_mail(data):
    url = url_checkmail
    data_oneMail = data['oneEmail']
    payload = {
        "client_id"  : clientId,
        "secret_key" : secretKey,
        "ref_code"   : ref_code,
        "onemail"    : data_oneMail
    }      
    try:
        tmp_payload_token = ''
        response = requests.request("POST", url=url_checkmail, json=payload, verify=False, stream=True)
        # tmp_payload_token = str(auth_token).split(' ')[1]
        if response.status_code == 200 or response.status_code == 201:
            # insert().insert_tran_log_v1(str(response.json()),'OK',str(payload) + ' ' + '',url,'')
            return {'result': 'OK','messageText': response.json()}
        else:
            # insert().insert_tran_log_v1(str(response.text),'ER',str(payload) + ' ' + '',url,'')
            return {'result': 'ER','messageText': response.json()}
    except requests.HTTPError as err:
        # insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + '',url,'')
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        # insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + '',url,'')
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        # insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + '',url,'')
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        # insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + '',url,'')
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def callPost_v2(path, data):
    url = path
    payload = data
    try:
        response = requests.post(url=url, json=payload, verify=False, stream=True)
        payload['password'] = ''
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url,None)
            return {'result': 'OK','messageText': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload),url,None)
            return {'result': 'ER','messageText': response.text,'status_Code':response.status_code}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def callGET(path, data):
    url = path
    payload = data
    # print(url,payload)
    
    try:
        response = requests.request("GET", url=url,headers={'Authorization': payload}, verify=False, stream=True)
        tmp_payload_token = str(payload).split(' ')[1]
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url,tmp_payload_token)
            return {'result': 'OK','messageText': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload),url,tmp_payload_token)
            return {'result': 'ER','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def callGET_v2(path, data):
    url = path
    payload = data
    # print(url,payload)
    
    try:
        response = requests.get(url=url,headers={'Authorization': payload}, verify=False, stream=True)
        tmp_payload_token = str(payload).split(' ')[1]
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url,tmp_payload_token)
            return {'result': 'OK','messageText': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload),url,tmp_payload_token)
            return {'result': 'ER','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def callAuth_get(path, data):
    url = path
    payload = data
    print(url)
    try:
        response = requests.get(url, headers={'Authorization': payload}, verify=False, stream=True)
        tmp_payload_token = str(payload).split(' ')[1]
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url,tmp_payload_token)
            return {'status': 'success','response': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload),url,tmp_payload_token)
            return {'result': 'fail','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token)
        return {'status': 'HTTPError','message': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token)
        return {'status': 'Timeout','message': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token)
        return {'status': 'ConnectionError','message': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token)
        return {'status': 'fail','message': 'An unexpected error: ' + str(err)}

def callAuth_post(path, data,auth_token):
    url = path
    payload = data
    
    try:
        tmp_payload_token = ''
        response = requests.request("POST",headers={'Authorization': auth_token}, url=url, json=payload, verify=False, stream=True)
        # print(response)
        tmp_payload_token = str(auth_token).split(' ')[1]
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
            return {'result': 'OK','messageText': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
            return {'result': 'ER','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def callAuth_post_v2(path, data,auth_token):
    url = path
    payload = data
    
    try:
        tmp_payload_token = ''
        response = requests.post(headers={'Authorization': auth_token}, url=url, json=payload, verify=False)
        tmp_payload_token = str(auth_token).split(' ')[1]
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
            return {'result': 'OK','messageText': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
            return {'result': 'ER','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def callOneid_Upload(path,data_file,type_document,auth_token):
    url = path
    path_file = data_file
    try:
        files_name = {
            type_document: open(path_file, 'rb')
        }
        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"approveDocument\"; filename=\"" +path_file +"\"\r\nContent-Type: application/pdf\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        headers = {
            'Authorization': auth_token
        }

        response = requests.post(url, files=files_name, headers=headers, verify=False, stream=True)
        tmp_payload_token = str(auth_token).split(' ')[1]
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
            return {'result': 'OK','messageText': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
            return {'result': 'ER','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def CallAPI_POST_oneid(url,header_token,datajson):
    try:
        # tmp_header_token = 'Bearer ' + header_token
        response = requests.request("POST",headers={'Authorization': header_token}, url=url, json=datajson, verify=False, stream=True)
        response = response.json()
        tmp_payload_token = str(header_token).split(' ')[1]
        insert().insert_tran_log_v1(str(response),'OK',str(datajson),url,tmp_payload_token)
        return {'result': 'OK','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(datajson),url,tmp_payload_token)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(datajson),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(datajson),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(ex)}

def CallAPI_GET_oneid(url,header_token):
    try:
        # tmp_header_token = 'Bearer ' + header_token
        response = requests.request("GET",headers={'Authorization': header_token}, url=url, verify=False, stream=True)
        response = response.json()
        tmp_payload_token = str(header_token).split(' ')[1]
        insert().insert_tran_log_v1(str(response),'OK',None,url,tmp_payload_token)
        return {'result': 'OK','messageText': response}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',None,url,tmp_payload_token)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',None,url,tmp_payload_token)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',None,url,tmp_payload_token)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',None,url,tmp_payload_token)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(ex)}

def callGET_other(path):
    url = path
    payload = ''
    tmp_payload_token = ''
    try:
        # print(url)
        response = requests.request("GET", url=url, verify=False, stream=True)
        # print(response.text)
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url,tmp_payload_token)
            return {'result': 'OK','messageText': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload),url,tmp_payload_token)
            return {'result': 'ER','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def callPost_v3(path, data):
    url = path
    payload = data
    
    try:
        auth_token = ''
        tmp_payload_token = ''
        response = requests.post(url=url, json=payload, verify=False)
        # tmp_payload_token = str(auth_token).split(' ')[1]
        if response.status_code == 200 or response.status_code == 201:
            result_response = response.json()
            if 'status' in result_response:
                if result_response['status'] == 200:
                    insert().insert_tran_log_v1(str(response.json()),'OK',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
                    return {'result': 'OK','messageText': response}
                elif result_response['status'] == 400:
                    insert().insert_tran_log_v1(str(response.json()),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
                    return {'result': 'ER','messageText': response}
            else:
                insert().insert_tran_log_v1(str(response.json()),'OK',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
                return {'result': 'OK','messageText': response}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
            return {'result': 'ER','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload) + ' ' + str(auth_token),url,tmp_payload_token)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def callPost_eform_attach(data,headers,data_file):
    url = url_ip_eform +'/api/v2/attract_file'
    data_save_file = data
    files_save = data_file
    try:
        response = requests.post(url,data = data_save_file, files = files_save, headers=headers, verify=False)
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(data_save_file),url,None)
            return {'result': 'OK','messageText': response.json()}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(data_save_file),url,None)
            return {'result': 'ER','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(data_save_file),url,None)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(data_save_file),url,None)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(data_save_file),url,None)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        insert().insert_tran_log_v1(str(err),'ER',str(data_save_file),url,None)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}

def callPost_eform_reject(headers,hash_sid):
    url = url_ip_eform +'/api/v1/cancel_ppl_v1'
    payload = {
        "ppl_id": str(hash_sid),
        "status": "Reject"
    }
    tmp_header = {
        'Authorization': headers
    }
    try:
        response = requests.post(url=url,json=payload, headers=tmp_header, verify=False)
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url,None)
            return {'result': 'OK','messageText': response.json()}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload),url,None)
            return {'result': 'ER','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(err),'ER',str(payload),url,None)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err)}