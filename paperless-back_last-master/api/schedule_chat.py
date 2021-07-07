from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from method.callserver import *
from method.hashpy import *
from method.verify import *
from db.db_method import *
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.login import *
from api.group_api import *
from api.group_v2 import *
import os
from datetime import date
import datetime

def fuc_schedule_onechat(tax_id,message):
    try:
        account = []
        tax_id = tax_id
        liketax_id = "'%{}%'".format(tax_id)
        sql = """ select account_id FROM "tb_bizLogin" WHERE biz_information LIKE """ +liketax_id+ """ """
        with slave.connect() as connection:
            result = connection.execute(text(sql))
            connection.close()
        query_result = [dict(row) for row in result] 
        for i in range(len(query_result)):
            account.append(query_result[i]['account_id'])
        account = ["786539012608"]
        url = "https://chat-api.one.th/bc_msg/api/v1/broadcast_group"
        print(url)
        try:
            headers = {
                'content-type': 'application/json',
                'Authorization':token_service
            }
            data_Json = {
                "bot_id" : bot_id,
                "to" : account,
                "message" : message
            }
            r = requests.post(url,json=data_Json,headers=headers,verify=False)
            print(r.text)
            r.raise_for_status()
            return {'result':'OK','msg' :'success'}
        except requests.Timeout as ex:
            return {'result':'ER','msg':'Timeout ' + str(ex)}
        except requests.HTTPError as ex:
            return {'result':'ER','msg':'HTTPError ' + str(ex)}
        except requests.ConnectionError as ex:
            return {'result':'ER','msg':'ConnectionError ' + str(ex)}
        except requests.RequestException as ex:
            return {'result':'ER','msg':'RequestException ' + str(ex)}
        except Exception as ex:
            return {'result':'ER','msg':ex}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','msg': str(e)}
    finally:
        connection.close()
    

def get_taxid_bc_msg():
    try:
        from datetime import datetime
        status = False
        ts = int(time.time())
        today_day = str(datetime.fromtimestamp(ts).strftime('%d'))
        today_hour = str(datetime.fromtimestamp(ts).strftime('%H'))
        today_month = str(datetime.fromtimestamp(ts).strftime('%m'))
        sql = """
            SELECT
                tax_id ,
                broadcast,
                broadcast_message,
                broadcast_datetime
            FROM
                "tb_bizPaperless" 
            WHERE
                broadcast = TRUE 
        """
        connection = slave.connect()
        result = connection.execute(text(sql))
        query_result = [dict(row) for row in result]
        text_str = 'แจ้งเตือน Broadcast ข้อความ\n\n'
        text_str += ''
        for i in range(len(query_result)):
            tax_id_bc = query_result[i]['tax_id']
            message_bc = query_result[i]['broadcast_message']
            datetime_bc = query_result[i]['broadcast_datetime']
            for n in range(len(datetime_bc)):
                day = datetime_bc[n]['day']
                hour = datetime_bc[n]['hour']
                month = datetime_bc[n]['month']
                if today_month in month:
                    if today_day in day:
                        if today_hour in hour:
                            status = True
                if status:
                    message_str = message_bc[n]['message']
                    r = fuc_schedule_onechat(tax_id_bc,message_str)
                    if r['result'] == 'OK':
                        text_str += 'Tax_id ' + tax_id_bc +  ' สถานะการ Broadcast ' + r['result'] + ' สาเหตุ ' +  r['msg']
                    else:                 
                        text_str += 'Tax_id ' + tax_id_bc +  ' สถานะการ Broadcast ' + r['result']+ ' สาเหตุ ' + r['msg']
                    print('bc')
                else:
                    print('nonbc')
        tokenChat = 'Bearer A89a857fd25805679a41ad51c3505ae3a6eaf2f84de624a6a8b1689fb1d616973b5f7fff147714ee3b9800cc99b662142'
        botid = 'Be97d0cbdfc67534abc1c5385fb268a36'
        send_message_Onechat(tokenChat,'G5e44be95e2563f002c0232b4a5b3d209174e553eba02fc3da27e28ac',botid,text_str,'แจ้งเตือน Broadcast ข้อความ')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
    finally:
        connection.close()
    
# fuc_schedule_onechat("4884696279419","ทดสอบจาก Paperless")