from db.db_Class import *
from config.value import *
# from method.access import *
from method.hashpy import *
from method.other import *
from config.lib import *
from db.db_method import *
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *
from method.document import *
# from method.cal_step import *
# from method.pdfSign import *
from method.callserver import * 
from method.callwebHook import * 
from method.sftp_fucn import *
from api.chat import *

def schedule_check_email_center(ts_start,ts_end,doc_type):
    try:
        doc_type = None
        tmpsidcode = []
        ts = int(time.time())
        date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.now()
        if ts_start == None and ts_end == None:
            dt_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            dt_end = now.replace(hour=23, minute=59, second=59, microsecond=00)
        else:
            ts_start = int(ts_start)
            ts_end = int(ts_end)
            dt_start = datetime.datetime.fromtimestamp(ts_start).strftime('%d/%b/%Y %H:%M:%S')
            dt_end = datetime.datetime.fromtimestamp(ts_end).strftime('%d/%b/%Y %H:%M:%S')
        print('query')
        sql = """
            SELECT
                "step_data_sid" AS "sid",
                "stepnow",
                "stepmax",
                "status_service",
                "send_time",
                "tracking_id",
                "doc_id",
	            tb_doc_detail."documentType",
                "document_status",
                "email_center",
                "biz_info",
                "tb_logerMail".to_mail,
                    "tb_logerMail".status,
                CASE                        
                    WHEN "tb_logerMail".status = 'OK' THEN
                    'Send' ELSE'Resent' 
                END AS "status_resent" 
            FROM
                "tb_send_detail"
                INNER JOIN "tb_step_data" ON "tb_send_detail"."step_data_sid" = "tb_step_data"."sid"
                INNER JOIN "tb_doc_detail" ON "tb_send_detail"."step_data_sid" = "tb_doc_detail"."step_id"
                FULL OUTER JOIN "tb_logerMail" ON "tb_logerMail".sid ILIKE '{%' || "tb_send_detail"."step_data_sid" || '%' 
            WHERE
                "tb_step_data"."update_time" >= :dt_start
                AND "tb_step_data"."update_time" <= :dt_end
                AND "tb_send_detail"."status" = :status
                AND ( "tb_send_detail"."document_status" = :document_status OR "tb_send_detail"."document_status" = :document_status_r ) 
                AND tb_send_detail.email_center != ''
	            AND "tb_logerMail".status = 'ER'
        """
        if doc_type != None:
            sql += """ AND "tb_doc_detail"."documentType"=:doc_type """
        connection = slave.connect()
        result = connection.execute(text(sql),dt_start=dt_start,dt_end=dt_end,document_status='Y',document_status_r='R',status='ACTIVE',doc_type=doc_type)
        resultQuery = [dict(row) for row in result]
        text_str = 'แจ้งเตือนเอกสารไม่ส่งอีเมล์ปลายทาง\n\n'
        text_str += 'เริ่ม ' + str(dt_start) + '\nสิ้นสุด ' + str(dt_end) + '\n'
        text_str += 'ส่งซ้ำเวลา ' + date_time_today + '\n'
        print('resultQuery',len(resultQuery))
        for i in range(len(resultQuery)):
            sidcode = resultQuery[i]['sid']
            status = resultQuery[i]['status']
            status_email = resultQuery[i]['status_resent']
            email_center = resultQuery[i]['email_center']
            tmp_document_id = resultQuery[i]['doc_id']
            document_type = resultQuery[i]['documentType']
            document_status = resultQuery[i]['document_status']
            if sidcode not in tmpsidcode:
                tmpsidcode.append(sidcode)
                if status_email == 'Resent':
                    result_message_text = select().select_mail_sender_v1_text(sidcode,tmp_document_id)
                    print(result_message_text)
                    try:
                        email_list = eval(email_center)
                    except Exception as e:
                        email_list = (email_center)
                    if type(email_list) is list:
                        s_email = []
                        for zemail in range(len(email_list)):
                            email_center_01 = email_list[zemail]['email']
                            attemp_file = email_list[zemail]['attemp_file']
                            file_pdf = email_list[zemail]['file_pdf']
                            s_email.append(email_center_01)
                        result_email_center = mail().send_emailSend_emailcenter_list_v2([sidcode],email_list,document_type)
                        text_str += "เลขที่เอกสาร " + tmp_document_id + "\nสถานะ " + document_status + "\nสถานะส่งซ้ำ " + result_email_center['result'] + "\nส่งไปที่ " + str(s_email) + "\nสาเหตุ " + str(result_email_center['messageText']) + "\n\n"
                    else:
                        result_email_center = mail().send_emailSend_emailcenter(email_center,sidcode,tmpmessage)
                        text_str += "เลขที่เอกสาร " + tmp_document_id + "\nสถานะ " + document_status + "\nสถานะส่งซ้ำ " + result_email_center['result'] + "\nส่งไปที่ " + str(email_center) + "\nสาเหตุ " + str(result_email_center['messageText']) + "\n\n"
            
        tokenChat = 'Bearer A89a857fd25805679a41ad51c3505ae3a6eaf2f84de624a6a8b1689fb1d616973b5f7fff147714ee3b9800cc99b662142'
        botid = 'Be97d0cbdfc67534abc1c5385fb268a36'
        if len(tmpsidcode) != 0:
            send_message_Onechat(tokenChat,'G5e44be95e2563f002c0232b4a5b3d209174e553eba02fc3da27e28ac',botid,text_str,'แจ้งเตือนเอกสารไม่ส่งอีเมล์ปลายทาง')
        else:
            text_str += '\nไม่พบรายการเอกสาร'
            send_message_Onechat(tokenChat,'G5e44be95e2563f002c0232b4a5b3d209174e553eba02fc3da27e28ac',botid,text_str,'แจ้งเตือนเอกสารไม่ส่งอีเมล์ปลายทาง')
        print(text_str)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
    finally:        
        connection.close()