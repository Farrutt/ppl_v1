# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from config.lib import *
from api.api import *
from api.api2 import *
from api.api3 import *
from api.login import *
from api.apiBiz import *
from api.file import *
from api.dashboard import *
from api.template_api import *
from api.sendmail_api import *
from api.document_api import *
from api.chat_api import *
from api.image_api import *
from api.department_api import *
from api.mail_api import *
from api.auth_api import *
from api.dashboard_admin import *
from api.other_api import *
from api.sio import *
from api.register import *
from api.excel_report import *
from api.profile import *
from api.step_api import *
from api.onebox import *
from api.mail import *
# from api.onebox_api import *
from api.schedule_log import *
from api.group_api import *
from db.db_method2 import *
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *

if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less

def manageai_document_tesseract_main_v1(sid,data):
    result_id = insert_3().insert_transaction_ocrv1(sid,data)
    print(result_id)

def manageai_document_tesseract_v1(sid,data):
    try:
        token_header = None
        url = url_manageai + '/tesseract' 
        response = requests.request("POST", url, json=data,verify=False)
        if response.status_code == 200 or response.status_code == 201:
            manageai_document_tesseract_main_v1(sid,str(response.json()))
            insert().insert_tran_log_v1(str(response.json()),'OK',str(data),url,token_header)
            return response.json()
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(data),url,token_header)
            return response.json()
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(data),url,token_header)
        return {'result':'ER','msg':ex}