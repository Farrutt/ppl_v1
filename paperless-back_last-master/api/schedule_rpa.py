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

# r = select().select_file_sign_last_to_email('05f5db38-941d-45b9-be2f-7c36a489fdac')
# print(r)

def other_service_rqp(sid_code,get_status_file,name_service,taxid,status_service):
    # status_service = []
    tmpjsonres = {"service":name_service,"status":False,"message":None}
    token_header = ''
    try:
        if get_status_file == 'Y':
            list_documentType = ['cspoc','cs','scs','tm','scst','po','cerhr','spo','tms','poc','pcm','chman','csact','csnib','csttm','cstdc','csims','csman','csinb','spr','qtnw','qt','qts','cspa']
            if name_service == 'RPA':
                    info_r = status_service
                    print('RPA')
                    result_select_action = select_4().select_get_action_and_status_v2('robot')
                    if result_select_action['result'] == 'OK':
                        if result_select_action['messageText']['status'] == True:
                            resultselect_attm_file = select().select_attm_file_v1_for_chat_api_to_robot(sid_code)
                            if resultselect_attm_file['result'] == 'OK':
                                doc_id = resultselect_attm_file['messageText']['document_Id']
                                pathFolder = resultselect_attm_file['messageText']['pathfolder']
                                json_Data_File = resultselect_attm_file['messageText']['json_data']
                                username_sender = resultselect_attm_file['messageText']['sender_username']
                                document_Type = resultselect_attm_file['messageText']['document_Type']
                                print('document_Type',document_Type)
                                if document_Type in list_documentType or 'cs' in document_Type:
                                    result_file_last_pdf  = select().select_file_sign_last_to_email(sid_code)
                                    if result_file_last_pdf['result'] == 'OK':
                                        pdf_base64_sign = result_file_last_pdf['messageText']
                                        file_name_sign_pdf = result_file_last_pdf['file_name']    
                                        print(taxid)                                            
                                        r_robot = sftp_robot().send_file_tosftp_new_v2(json_Data_File,pathFolder,'',document_Type,doc_id,pdf_base64_sign,file_name_sign_pdf,sid_code,tax_id=taxid)
                                        if 'result' in r_robot:
                                            if r_robot['result'] == 'OK':
                                                tmpjsonres = {"service":name_service,"status":True,"message":"success"}                                                        
                                                insert().insert_transaction_servicelog_v1(name_service,'OK',sid_code,'upload sftp complete',token_header)
                                            else:
                                                tmpjsonres = {"service":name_service,"status":False,"message":r_robot['messageER']}
                                                insert().insert_transaction_servicelog_v1(name_service,'ER',sid_code,str(r_robot['messageER']),token_header)
                                    else:
                                        tmpjsonres = {"service":name_service,"status":False,"message":"data not found file"}
                                        insert().insert_transaction_servicelog_v1(name_service,'ER',sid_code,'data not found file',token_header)
                            else:
                                doc_id = resultselect_attm_file['messageText']['document_Id']
                                username_sender = resultselect_attm_file['messageText']['sender_username']
                                document_Type = resultselect_attm_file['messageText']['document_Type']
                                print('document_Type',document_Type)
                                folder_name = resultselect_attm_file['messageText']['folder_name']
                                pathtemp_eform = ""
                                json_data_details = ""
                                pathnonperfix = ""
                                check_filename = []
                                if folder_name != None:
                                    url = url_ip_eform + '/api/v1/get_attract_file/?folder_name=' + folder_name
                                    result_eform = callGET_other(url)
                                    folder_name = str(uuid.uuid4())
                                    pathtemp_eform = path_global_1 +'/storage/temp/' + folder_name +'/'
                                    pathnonperfix = '/storage/temp/' + folder_name +'/'
                                    if not os.path.exists(pathtemp_eform):
                                        os.makedirs(pathtemp_eform)
                                    if result_eform['result'] == 'OK':
                                        tmpmessage = result_eform['messageText'].json()
                                        if tmpmessage['result'] == 'OK':
                                            tmpdata = tmpmessage['messageText'][0]
                                            pathfolder = tmpdata['folder_path']
                                            json_data_details = tmpdata['file_name']
                                            folder_name = tmpdata['folder_name']
                                            print(json_data_details)
                                            for nz in range(len(json_data_details)):
                                                tmpfile_name_original = json_data_details[nz]['file_name_original']
                                                if tmpfile_name_original not in check_filename:
                                                    check_filename.append(tmpfile_name_original)
                                                else:
                                                    tmpfile_name_original = str(nz) + '-' + tmpfile_name_original
                                                tmpurl_download = json_data_details[nz]['url_download']
                                                r = requests.get(tmpurl_download,verify=False)
                                                with open(pathtemp_eform + tmpfile_name_original,'wb') as f: 
                                                    f.write(r.content)
                                                print(pathtemp_eform + tmpfile_name_original)
                                # return ''
                                if document_Type in list_documentType:
                                    result_file_last_pdf  =select().select_file_sign_last_to_email(sid_code)
                                    if result_file_last_pdf['result'] == 'OK':
                                        pdf_base64_sign = result_file_last_pdf['messageText']
                                        file_name_sign_pdf = result_file_last_pdf['file_name']   
                                        print(taxid)                                             
                                        r_robot = sftp_robot().send_file_tosftp_new_v2(json_data_details,pathnonperfix,'',document_Type,doc_id,pdf_base64_sign,file_name_sign_pdf,sid_code,tax_id=taxid)
                                        if 'result' in r_robot:
                                            if r_robot['result'] == 'OK':
                                                tmpjsonres = {"service":name_service,"status":True,"message":"success"}                                                        
                                                insert().insert_transaction_servicelog_v1(name_service,'OK',sid_code,'upload sftp complete',token_header)
                                            else:
                                                tmpjsonres = {"service":name_service,"status":False,"message":r_robot['messageER']}
                                                insert().insert_transaction_servicelog_v1(name_service,'ER',sid_code,str(r_robot['messageER']),token_header)
                                    else:
                                        tmpjsonres = {"service":name_service,"status":False,"message":"data not found file"}
                                        insert().insert_transaction_servicelog_v1(name_service,'ER',sid_code,'data not found file',token_header)
                                # insert().insert_transaction_servicelog_v1(name_service,'ER',sid_code,'data not found attachment')]
                    # print(tmpjsonres)         
                    statusRPA = False
                    for x in range(len(status_service)):
                        if status_service[x]['service'] == 'RPA':
                            status_service[x] = tmpjsonres
                            statusRPA = True
                    if statusRPA == False:
                        status_service.append(tmpjsonres)                          
                    if len(status_service) == 0:  
                        status_service.append(tmpjsonres)
        elif get_status_file == 'R':
            list_documentType = ['cerhr']
            result_select_data = select().select_ForWebHook(sid_code)
            if name_service == 'RPA':
                    tmpjsonres = {"service":name_service,"status":False,"message":None}
                    print('RPA')
                    result_select_action = select_4().select_get_action_and_status_v2('robot')
                    # print(result_select_action)
                    if result_select_action['result'] == 'OK':
                        if result_select_action['messageText']['status'] == True:
                            resultselect_attm_file = select().select_attm_file_v1_for_chat_api_to_robot(sid_code)
                            # print(resultselect_attm_file , 'resultselect_attm_file')
                            if resultselect_attm_file['result'] == 'OK':
                                doc_id = resultselect_attm_file['messageText']['document_Id']
                                pathFolder = resultselect_attm_file['messageText']['pathfolder']
                                json_Data_File = resultselect_attm_file['messageText']['json_data']
                                username_sender = resultselect_attm_file['messageText']['sender_username']
                                document_Type = resultselect_attm_file['messageText']['document_Type']
                                print('document_Type',document_Type)
                                if document_Type in list_documentType:
                                    result_file_last_pdf  = select().select_file_sign_last_to_email(sid_code)
                                    if result_file_last_pdf['result'] == 'OK':
                                        pdf_base64_sign = result_file_last_pdf['messageText']
                                        file_name_sign_pdf = result_file_last_pdf['file_name']                                                
                                        r_robot = sftp_robot().send_file_tosftp_new_v2(json_Data_File,pathFolder,'',document_Type,doc_id,pdf_base64_sign,file_name_sign_pdf,sid_code,get_status_file)
                                        if 'result' in r_robot:
                                            if r_robot['result'] == 'OK':
                                                tmpjsonres = {"service":name_service,"status":True,"message":"success"}                                                        
                                                insert().insert_transaction_servicelog_v1(name_service,'OK',sid_code,'upload sftp complete',token_header)
                                            else:
                                                tmpjsonres = {"service":name_service,"status":False,"message":r_robot['messageER']}
                                                insert().insert_transaction_servicelog_v1(name_service,'ER',sid_code,str(r_robot['messageER']),token_header)
                                    else:
                                        tmpjsonres = {"service":name_service,"status":False,"message":"data not found file"}
                                        insert().insert_transaction_servicelog_v1(name_service,'ER',sid_code,'data not found file',token_header)
                            else:
                                doc_id = resultselect_attm_file['messageText']['document_Id']
                                username_sender = resultselect_attm_file['messageText']['sender_username']
                                document_Type = resultselect_attm_file['messageText']['document_Type']
                                print('document_Type',document_Type)
                                folder_name = resultselect_attm_file['messageText']['folder_name']
                                pathtemp_eform = ""
                                json_data_details = ""
                                pathnonperfix = ""
                                if folder_name != None:
                                    url = url_ip_eform + '/api/v1/get_attract_file/?folder_name=' + folder_name
                                    result_eform = callGET_other(url)
                                    folder_name = str(uuid.uuid4())
                                    pathtemp_eform = path_global_1 +'/storage/temp/' + folder_name +'/'
                                    pathnonperfix = '/storage/temp/' + folder_name +'/'
                                    if not os.path.exists(pathtemp_eform):
                                        os.makedirs(pathtemp_eform)
                                    if result_eform['result'] == 'OK':
                                        tmpmessage = result_eform['messageText'].json()
                                        if tmpmessage['result'] == 'OK':
                                            tmpdata = tmpmessage['messageText'][0]
                                            pathfolder = tmpdata['folder_path']
                                            json_data_details = tmpdata['file_name']
                                            folder_name = tmpdata['folder_name']
                                            for nz in range(len(json_data_details)):
                                                tmpfile_name_original = json_data_details[nz]['file_name_original']
                                                tmpurl_download = json_data_details[nz]['url_download']
                                                r = requests.get(tmpurl_download,verify=False)
                                                with open(pathtemp_eform + tmpfile_name_original,'wb') as f: 
                                                    f.write(r.content)
                                                print(pathtemp_eform + tmpfile_name_original)
                                if document_Type in list_documentType:
                                    result_file_last_pdf  =select().select_file_sign_last_to_email(sid_code)
                                    if result_file_last_pdf['result'] == 'OK':
                                        pdf_base64_sign = result_file_last_pdf['messageText']
                                        file_name_sign_pdf = result_file_last_pdf['file_name']                                                
                                        r_robot = sftp_robot().send_file_tosftp_new_v2(json_data_details,pathnonperfix,'',document_Type,doc_id,pdf_base64_sign,file_name_sign_pdf,sid_code,get_status_file)
                                        if 'result' in r_robot:
                                            if r_robot['result'] == 'OK':
                                                tmpjsonres = {"service":name_service,"status":True,"message":"success"}                                                        
                                                insert().insert_transaction_servicelog_v1(name_service,'OK',sid_code,'upload sftp complete',token_header)
                                            else:
                                                tmpjsonres = {"service":name_service,"status":False,"message":r_robot['messageER']}
                                                insert().insert_transaction_servicelog_v1(name_service,'ER',sid_code,str(r_robot['messageER']),token_header)
                                    else:
                                        tmpjsonres = {"service":name_service,"status":False,"message":"data not found file"}
                                        insert().insert_transaction_servicelog_v1(name_service,'ER',sid_code,'data not found file',token_header)
                                # insert().insert_transaction_servicelog_v1(name_service,'ER',sid_code,'data not found attachment')]
                          
                    statusRPA = False
                    for x in range(len(status_service)):
                        if status_service[x]['service'] == 'RPA':
                            status_service[x] = tmpjsonres
                            statusRPA = True
                    if statusRPA == False:
                        status_service.append(tmpjsonres)                          
                    if len(status_service) == 0:  
                        status_service.append(tmpjsonres)
            call_webhookService(sid_code)  
        else:
            call_webhookService(sid_code)
        print(sid_code,status_service)
        r_update = update_4().update_status_service(sid_code,str(status_service))
        return tmpjsonres
    except Exception as e:
        print(str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return ''
        # return redirect(url_paperless)

def schedule_check_servicedoc(ts_start,ts_end,doc_type):
    try:
        ts = int(time.time())
        date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        arr_resendrpa = []
        now = datetime.datetime.now()
        if ts_start == None and ts_end == None:
            dt_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            dt_end = now.replace(hour=23, minute=59, second=59, microsecond=00)
        else:
            ts_start = int(ts_start)
            ts_end = int(ts_end)
            dt_start = datetime.datetime.fromtimestamp(ts_start).strftime('%d/%b/%Y %H:%M:%S')
            dt_end = datetime.datetime.fromtimestamp(ts_end).strftime('%d/%b/%Y %H:%M:%S')
        # dt_start = '2020-12-14 00:00:00'
        # dt_end = '2020-12-14 23:59:00'
        print(dt_start,',',dt_end)
        print('in')
        # "tb_step_data"."update_time" > :dt_start AND "tb_step_data"."update_time" < :dt_end 
        # AND "tb_doc_detail"."documentType"=:doc_type
        sql = '''select "step_data_sid","stepnow","stepmax","status_service","send_time","tracking_id","doc_id","document_status","biz_info"
            FROM 
                "tb_send_detail" 
                INNER JOIN "tb_step_data" ON "tb_send_detail"."step_data_sid" = "tb_step_data"."sid" 
                INNER JOIN "tb_doc_detail" ON "tb_send_detail"."step_data_sid" = "tb_doc_detail"."step_id"
            where 
                "tb_step_data"."update_time" > :dt_start AND "tb_step_data"."update_time" < :dt_end 
                AND "tb_send_detail"."status" = :status
                AND ("tb_send_detail"."document_status" = :document_status OR "tb_send_detail"."document_status" = :document_status_r) 
        '''
        if doc_type != None:
            sql += ''' AND "tb_doc_detail"."documentType"=:doc_type'''
        connection = slave.connect()
        result = connection.execute(text(sql),dt_start=dt_start,dt_end=dt_end,document_status='Y',document_status_r='R',status='ACTIVE',doc_type=doc_type)
        resultQuery = [dict(row) for row in result]
        print('resultQuery',len(resultQuery))
        tmplistdocid = []
        text_str = 'แจ้งเตือนเอกสารไม่ส่งเข้า Bot RPA \n\nประเภทเอกสาร ' + str(doc_type) + '\nเอกสาร Approve หรือ Reject เวลา ' + '\nเริ่ม ' + str(dt_start) + '\nสิ้นสุด ' + str(dt_end) + '\nส่งซ้ำเวลา ' + date_time_today
        if len(resultQuery) != None:
            for x in range(len(resultQuery)):
                rowinfo = resultQuery[x]
                sidCode = rowinfo['step_data_sid']
                biz_info = eval(str(rowinfo['biz_info']))
                # print('biz_info',biz_info)
                if biz_info != None:
                    taxid = biz_info['id_card_num']
                else :
                    taxid = biz_info
                print(rowinfo['status_service'])
                if rowinfo['status_service'] != None and rowinfo['status_service'] != 'None':
                    if rowinfo['status_service'] == '[]':
                        print('non status service')
                        result_resend_rpa = {}
                        result_resend_rpa['status'] = 'ยังไม่ได้ส่ง'
                        result_resend_rpa['message'] = 'None'
                        name_service = 'RPA'
                        document_status  = rowinfo['document_status']
                        print(document_status)
                        result_resend_rpa = other_service_rqp(sidCode,document_status,'RPA',taxid,rowinfo['status_service'])
                        print('result_resend_rpa',result_resend_rpa)
                        print(rowinfo['doc_id'])
                        tmplistdocid.append(rowinfo['doc_id'])
                        text_str += '\n' + rowinfo['doc_id'] + ' สถานะเอกสาร : ' + document_status + ' สถานะส่งซ้ำ : ' + str(result_resend_rpa['status']) + ' สาเหตุุ : ' + str(result_resend_rpa['message'])
                        # print(sidCode)
                        # other_service_cost()
                        
                        tmp = {
                            'sid' : sidCode,
                            'doc_id' : rowinfo['doc_id'],
                            'status_service' :str(rowinfo['status_service'])
                        }
                        arr_resendrpa.append(tmp)
                    else :
                        result_resend_rpa = {}
                        result_resend_rpa['status'] = 'ยังไม่ได้ส่ง'
                        rowinfo['status_service'] = eval(str(rowinfo['status_service']))
                        for i in range(len(rowinfo['status_service'])):
                            print(rowinfo['status_service'][i])
                            if rowinfo['status_service'][i] != {}:
                                if rowinfo['status_service'][i]['service'] == 'RPA':
                                    if rowinfo['status_service'][i]['status'] == False:
                                        name_service = rowinfo['status_service'][i]['service']
                                        document_status  = rowinfo['document_status']
                                        result_resend_rpa = other_service_rqp(sidCode,document_status,name_service,taxid,rowinfo['status_service'])
                                        print('result_resend_rpa',result_resend_rpa)
                                        print(rowinfo['doc_id'])
                                        tmplistdocid.append(rowinfo['doc_id'])
                                        text_str += '\n' + rowinfo['doc_id'] + ' สถานะเอกสาร : ' + document_status + ' สถานะส่งซ้ำ : ' + str(result_resend_rpa['status']) + ' สาเหตุุ : ' + str(result_resend_rpa['message'])
                                        # print(sidCode)
                                        # other_service_cost()
                                        
                                        tmp = {
                                            'sid' : sidCode,
                                            'doc_id' : rowinfo['doc_id'],
                                            'status_service' :str(rowinfo['status_service'])
                                        }
                                        arr_resendrpa.append(tmp)
        now = str(now).split(' ')
        fn_dt = now[0]
        pathfileresend = path_global_1 + '/storage/resend_rpa/' + str(fn_dt)
        if not os.path.exists(pathfileresend):
            os.makedirs(pathfileresend)
        unique_filename = str(uuid.uuid4())
        fn_resend = pathfileresend + '/' + unique_filename + '.txt'
        arr_resendrpa = str(arr_resendrpa)
        with open(fn_resend,'wb') as fs:
            fs.write(arr_resendrpa.encode('utf-8-sig'))
        tokenChat = 'Bearer A89a857fd25805679a41ad51c3505ae3a6eaf2f84de624a6a8b1689fb1d616973b5f7fff147714ee3b9800cc99b662142'
        botid = 'Be97d0cbdfc67534abc1c5385fb268a36'
        if len(tmplistdocid) != 0:
            send_message_Onechat(tokenChat,'G5e44be95e2563f002c0232b4a5b3d209174e553eba02fc3da27e28ac',botid,text_str,'แจ้งเตือนเอกสารไม่ส่งเข้า Bot RPA')
        else:
            text_str += '\nไม่พบรายการเอกสาร'
            send_message_Onechat(tokenChat,'G5e44be95e2563f002c0232b4a5b3d209174e553eba02fc3da27e28ac',botid,text_str,'แจ้งเตือนเอกสารไม่ส่งเข้า Bot RPA')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageText':'notfound data' + str(e)}
    finally:
        pass
        connection.close()


