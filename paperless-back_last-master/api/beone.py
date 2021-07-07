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
from method.sftp_fucn import *

def step_1_login_dms_v1(token_header):
    try:
        url = url_dms + "/api/v1/login"
        payload = {
            "username":"ppl01",
            "password":"ppl@Pass01",
            "url":url_req_dms
        }
        headers = {
            'Content-Type': "application/json",
            # 'Authorization': auth_token
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        # print(response)
        insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url,token_header)
        return {'result':'OK','msg':(response.json())}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url,token_header)
        return {'result':'ER','msg':ex}

def step_2_upload_dms_v1(dms_token,dms_key_data_01,file_path,filename_andtype,attm_file,path_attm_file,property_data,token_header):
    try:
        url = url_dms + "/api/v2/node/6bf91cb1-4ae9-4f87-864b-069b8d6807c9"
        result_dataJson = {}
        list_file_path = []
        json_data = {}
        # dms_key_data = dms_key_data_01['dms_key']
        # dms_key_cust_num = dms_key_data_01['cust_num']
        url_domain_dms = url_req_dms
        path_attm_file = '.' + path_attm_file
        if type(file_path) is str:
            json_data['files[]'] = (filename_andtype,open(file_path, 'rb'))            
            # json_data['name'] = filename_andtype
            # json_data['relativePath'] = dms_key_cust_num + '/'+ dms_key_data 
            list_file_path.append(json_data)
        # property_data = property_data
        json_data['url'] = url_req_dms
        json_data['data'] = property_data
        # property_data = {"properties":[{"name":"Doc7.doc","relativePath":"0022/อินเทอร์เน็ตประเทศไทย"}]}
        # result_dataJson['url'] = url_domain_dms
        # result_dataJson['data'] = str(property_data)
        print(json_data)
        # print(tuple(property_data.items()))
        m = MultipartEncoder(
            fields=json_data
        )
        r = requests.post(url, data=m, headers={'Content-Type': m.content_type,'Authorization': dms_token})
        # print(r.text)
        # file_ = open(file_path, "r",encoding='utf-8')
        # payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"files[]\"; filename=\"" + str(open(file_path, "r").read()) +"\"\r\nContent-Type: application/pdf\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"url\"\r\n\r\n" + url_domain_dms +"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"data\"\r\n\r\n" +str(property_data) +"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        # headers = {
        #     'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        #     'Authorization': dms_token
        # }

        # response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)
        # print(response.text)
        insert().insert_tran_log_v1(str(r.json()),'OK',str(json_data),url,token_header)
        return {'result':'OK','msg':r.json()}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(json_data),url,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(json_data),url,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(json_data),url,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(json_data),url,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(json_data),url,token_header)
        return {'result':'ER','msg':ex}

    

    