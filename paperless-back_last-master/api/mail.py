#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config.lib import *
from config.value import *
from method.callserver import *
from db.db_method import *
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *

class mail:
    def sendMailCenter_group_v2(self,sidCode,EmailCenter):
        self.sidCode = sidCode
        self.EmailCenter = EmailCenter
        # self.document_type = document_type
        try:
            list_email_file = []
            msg = MIMEMultipart('alternative')
            unique_foldername = str(uuid.uuid4())
            path = path_global_1 + '/storage/file_mail/' + unique_foldername +'/'
            # path = './storage/file_mail/' + unique_foldername +'/'
            str_text = ''
            email_Send = []
            if not os.path.exists(path):
                os.makedirs(path)
            print('self.EmailCenter',self.EmailCenter)
            for i in self.EmailCenter:
                email_Send.append(i['email'])
            print('email_Send',email_Send)
            print('sidCode',type(self.sidCode))
            print('type',type(self.sidCode))
            for sid in self.sidCode:
                files = []
                result_base64 = select().select_file_sign_last_to_email(sid)
                resultselect_ = select().select_attm_file_v1_for_chat_api_to_robot(sid)
                result_Document = select().select_documentId_Mail(sid)
                print('result_Document',result_Document)
                filename_tmpOrg = result_Document['messageText']['file_Name']
                if resultselect_['result'] == 'OK':
                    doc_id = resultselect_['messageText']['document_Id']
                    pathFolder = resultselect_['messageText']['pathfolder']
                    pathFolder = path_global_1+ pathFolder
                    # pathFolder = os.getcwd() + pathFolder
                    json_Data_File = resultselect_['messageText']['json_data']
                    tmp_folder_name = resultselect_['messageText']['folder_name']
                    username_sender = resultselect_['messageText']['sender_username']
                    # document_Type = resultselect_['messageText']['document_Type']
                    str_text += '<br>เลขที่เอกสาร ' + doc_id + '<br>' 
                    str_text += 'รายการเอกสาร <br>- ไฟล์หลัก : ' + filename_tmpOrg + '<br>- ไฟล์แนบ<br>'
                    list_file_username = []
                    if json_Data_File != None:
                        for u in range(len(json_Data_File)):
                            # tmpurl_download = json_Data_File[u]['url_download']
                            # tmpurl_view_pdf = json_Data_File[u]['url_view_pdf']
                            tmpfile_name_new = json_Data_File[u]['file_name_new']
                            tmpurl_download = myUrl_domain + 'storage/downloadfile/v1/' + tmp_folder_name +"/"+tmpfile_name_new
                            tmpurl_view_pdf = myUrl_domain + 'storage/viewfile/v1/'+tmp_folder_name+"/"+tmpfile_name_new
                            list_file_username.append({'file_name_new':json_Data_File[u]['file_name_new'],'file_name_original':json_Data_File[u]['file_name_original']})
                            tmp_filename_org = json_Data_File[u]['file_name_original']
                            tmptypeFile = str(tmp_filename_org)
                            tmptypeFile = (tmptypeFile).split('.')[-1]
                            if str(tmptypeFile).lower() == 'pdf':
                                str_text += tmp_filename_org + ' <a href=' + tmpurl_download+'>ดาวน์โหลดไฟล์</a>&nbsp;&nbsp;<a href=' + tmpurl_view_pdf+'>ดูเอกสาร</a><br>'
                            else:
                                str_text += tmp_filename_org + ' <a href=' + tmpurl_download+'>ดาวน์โหลดไฟล์</a><br>'
                        # for r, d, f in os.walk(pathFolder):
                        #     for file in f:
                        #         current_app.logger.info(file)
                        #         for i in range(len(list_file_username)):
                        #             if list_file_username[i]['file_name_new'] == file:
                        #                 files.append({'path_file':os.path.join(r, file),'file_name_original':list_file_username[i]['file_name_original']})
                else:
                    doc_id = None
                    pathFolder = None
                    json_Data_File = None
                    username_sender = None
                    # document_Type = None
                    doc_id = resultselect_['messageText']['document_Id']
                    pathFolder = resultselect_['messageText']['pathfolder']
                    tmpFolder_name = resultselect_['messageText']['folder_name']
                    str_text += '<br>เลขที่เอกสาร ' + doc_id + '<br>' 
                    str_text += 'รายการเอกสาร <br>- ไฟล์หลัก : ' + filename_tmpOrg + '<br>- ไฟล์แนบ<br>'
                    if tmpFolder_name != None:
                        url_GetfileEFORM = url_ip_eform + '/api/v1/get_attract_file/?folder_name=' + tmpFolder_name
                        result_Data = callGET_other(url_GetfileEFORM)
                        if result_Data['result'] == 'OK':
                            tmpDataMesg = result_Data['messageText'].json()
                            if tmpDataMesg['result'] == 'OK':
                                tmpMesg = tmpDataMesg['messageText']   
                                tmpfilename = tmpMesg[0]['file_name']
                                list_file_name = []
                                # path = './storage/' + tmpFolder_name +'/'
                                # path_indb = '/storage/' + tmpFolder_name +'/'
                                # if not os.path.exists(path):
                                #     os.makedirs(path)
                                for x in range(len(tmpfilename)):
                                    tmpurl_download = tmpfilename[x]['url_download']
                                    tmpurl_view_pdf = tmpfilename[x]['url_view_pdf']
                                    tmpfile_name_new = tmpfilename[x]['file_name_new']
                                    tmp_filename_org = tmpfilename[x]['file_name_original']
                                    tmptypeFile = str(tmp_filename_org)
                                    tmptypeFile = (tmptypeFile).split('.')[-1]
                                    if str(tmptypeFile).lower() == 'pdf':
                                        str_text += tmp_filename_org + ' <a href=' + tmpurl_download+'>ดาวน์โหลดไฟล์</a>&nbsp;&nbsp;<a href=' + tmpurl_view_pdf+'>ดูเอกสาร</a><br>'
                                    else:
                                        str_text += tmp_filename_org + ' <a href=' + tmpurl_download+'>ดาวน์โหลดไฟล์</a><br>'
                                    # with open(path + tmpfile_name_new + tmptypeFile, 'wb') as f:
                                    #     f.write(r.content)
                    
                    
                # if len(files) != 0:
                #     for file in range(len(files)):
                #         part = MIMEBase('application', "octet-stream")
                #         part.set_payload(open(files[file]['path_file'], "rb").read())
                #         encoders.encode_base64(part)
                #         part.add_header('Content-Disposition', 'attachment', filename=files[file]['file_name_original'])
                #         msg.attach(part)
                file_string = result_base64['messageText']
                unique_filename = str(uuid.uuid4())
                with open(path + unique_filename + ".pdf", "wb") as fh:
                    fh.write(base64.b64decode(file_string))
                path_file_to_mail = path + unique_filename + ".pdf"
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(path_file_to_mail, "rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename= filename_tmpOrg)
                msg.attach(part)
                list_email_file.append({'sid':sid,'file_pdf':path_file_to_mail,'file_pdf_name':filename_tmpOrg,'document_id':doc_id})
                str_text += '<br>'
            To = email_Send
            host = "mailtx.inet.co.th"
            # myUrl_tracking = url_paperless + "tracking?id=" + result_Document['messageText']['tracking_id']
            Subject = ''
            Title = "Paperless"
            From = "paperless-"+"@one.th"        
            msg['Subject'] = Title
            msg['From'] = From
            msg['To'] = ', '.join(To)
            Url_file = "None"
            string_qrCode = "None"
            html = "<!DOCTYPE html><html><head><meta charset=\"UTF-8\"></head><body><p><b>แจ้งเตือนระบบ Paperless </b</p><br>" + str_text +"</br></br>" + "" +"<br><br><i><br>ขอบคุณที่ใช้บริการ<br>Send From Paperless</i>" \
            "<p><i>© Copyright 2020, Internet Thailand Public Company Limited.</i><br><br>กรุณาอย่าตอบกลับอีเมลนี้</p></body></html>"
            part2 = MIMEText(html, 'html',"utf-8")
            msg.attach(part2)
            s = smtplib.SMTP(host)
            # s.set_debuglevel(1)
            s.sendmail(From, To, msg.as_string())
            s.quit()
            print('ok')
            res_insert = insert().insert_sendEmail(self.sidCode,'OK', msg['To'],From,string_qrCode,Url_file)
            return {'result':'OK','messageText':None}
        except Exception as ex:
            print(str(ex))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            res_insert = insert().insert_sendEmail(self.sidCode,str(ex), msg['To'],From,string_qrCode,Url_file)
            return {'result':'ER','messageText': str(ex)}
        except SMTPException as ex:
            print(str(ex))
            res_insert = insert().insert_sendEmail(self.sidCode,str(ex), msg['To'],From,string_qrCode,Url_file)
            return {'result':'ER','messageText': str(ex)}
    
    def sendmail_group_center(self,group_id):
        self.group_id = group_id

    def send_email_test(self):
        smtp_server = "mailtx.inet.co.th"
        sender = 'jirayu.ko@one.th'
        receivers = ['jirayu.ko@mandala.co.th']

        msg = MIMEText('This is test mail')

        msg['Subject'] = 'Test mail'
        msg['From'] = sender
        msg['To'] = 'jirayu.ko@mandala.co.th'

        with smtplib.SMTP(smtp_server) as server:
            server.sendmail(sender, receivers, msg.as_string())
            print("Successfully sent email")
        # sender = 'jirayu.ko@one.th'
        # receivers = ['jirayuknot55@gmail.com']
        # 
        # message = """From: From Person <from@fromdomain.com>
        # To: To Person <to@todomain.com>
        # Subject: SMTP e-mail test

        # This is a test e-mail message.
        # """

        # try:
        #     smtpObj = smtplib.SMTP(smtp_server)
        #     smtpObj.sendmail(sender, receivers, message)         
        #     print("Successfully sent email")
        # except SMTPException:
        #     print("Error: unable to send email")
    def send_serviceLog_toemail(self,to_message, to_email,sender_email,path_file,file_name,date,time):
        self.to_message = to_message
        self.to_email = to_email
        self.sender_email = sender_email
        self.path_file = path_file
        self.file_name = file_name
        self.to_subject = 'รายงานผลการโยนไฟล์ของวันที่ ' + date
        string_text_mail = self.to_subject
        msg = MIMEMultipart()
        mail_body = string_text_mail
        msg.attach(MIMEText(mail_body))
        msg['From'] = self.sender_email
        
        send_toemail = ['tivanonj@inet.co.th']
        # send_toemail = ['jirayu.ko@mandala.co.th']
        send_to_cc = ['jirayu.ko@mandala.co.th','sarawut.si@inet.co.th','phakinee.pa@inet.co.th','nichapatn@inet.co.th','kannika.bo@inet.co.th','servicereport@inet.co.th','inet-cost@inet.co.th']
        # send_to_cc = ['sarawut.si@inet.co.th']
        toaddrs = send_toemail + send_to_cc
        msg['To'] = ', '.join(send_toemail)
        msg['CC'] = ', '.join(send_to_cc)
        msg['Subject'] = self.to_subject
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(path_file, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=file_name)
        msg.attach(part)
        
        from_address =  "inet-design@inet.co.th" 
        to_address = send_toemail
        try:
            server = smtplib.SMTP(smtp_server)
            server.set_debuglevel(1)
            server.sendmail(from_address, toaddrs, msg.as_string())
            server.quit()
            print('success')
            insert().insert_log_mail_sender(self.to_email,self.sender_email,'send mail success')
            return {'result':'OK','messageER':None}
        except Exception as e:
            print(str(e))
            insert().insert_log_mail_sender(self.to_email,self.sender_email,str(e))
            return {'result':'ER','messageER':str(e)}

    def send_to_email(self,to_email,sender_email,to_subject,to_message,sid_code):
        self.sid_code = sid_code        
        self.to_email = to_email
        self.sender_email = sender_email
        self.to_subject = to_subject
        self.to_message = to_message
        files = []
        list_file_username = []
        path = path_global_1 + '/storage/mail/' + self.sid_code + '/'
        # path = './storage/mail/' + self.sid_code + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        path_getcwd = path_global_1 + '/storage/mail/' + self.sid_code + '/'    
        # path_getcwd = os.getcwd() + '/storage/mail/' + self.sid_code + '/'
        smtp_server = "mailtx.inet.co.th"
        msg = MIMEMultipart()
        result_Document = select().select_documentId_Mail(self.sid_code)
        result_base64 = select().select_file_sign_last_to_email(self.sid_code)
        if result_Document['result'] == 'OK':
            resultselect_00 = select().select_attm_file_v1_for_chat_api_to_robot(self.sid_code)
            tmpdocument_type = result_Document['messageText']['document_type']
            file_id = result_Document['messageText']['file_id']
            file_name = result_Document['messageText']['file_Name']
            if resultselect_00['result'] == 'OK':
                json_data_res = resultselect_00['messageText']['json_data']
                self.path_foldername = resultselect_00['messageText']['pathfolder']
                document_Id_data = resultselect_00['messageText']['document_Id']
                # print(self.path_foldername)
                path_file = path_global_1 + self.path_foldername
                # path_file = os.getcwd() + self.path_foldername
                self.to_subject = 'เอกสารเลขที่ ' + str(document_Id_data)
                msg['Subject'] =  self.to_subject
                msg['To'] = self.to_email
                msg['From'] = "paperless-"+tmpdocument_type+"@one.th"
                to_address = self.to_email
                from_address =  "paperless-"+tmpdocument_type+"@one.th"
                msg['CC'] = self.sender_email
                string_text_mail = ''       
                for u in range(len(json_data_res)):
                    list_file_username.append({'file_name_new':json_data_res[u]['file_name_new'],'file_name_original':json_data_res[u]['file_name_original']})
                for r, d, f in os.walk(path_file):
                    for file in f:
                        for i in range(len(list_file_username)):
                            if list_file_username[i]['file_name_new'] == file:                                
                                files.append({'path_file':os.path.join(r, file),'file_name_original':list_file_username[i]['file_name_original'],'data_type':'two'})
                if file_id != None:
                    string_text_mail_sign = 'นำส่งโดย ' + self.sender_email + ' \n\n'
                    resultselect_ = select().select_pdfstring_to_fileid(file_id)
                    if resultselect_['result'] == 'OK':
                        pdf_base64_last = resultselect_['messageText']['pdf_string']
                        unique_filename = str(uuid.uuid4())
                        with open(path + file_name ,"wb") as f:
                            f.write(base64.b64decode((pdf_base64_last)))
                        files.append({'path_file':path_getcwd + file_name,'file_name_original':file_name,'data_type':'main'})
                    string_text_mail_sign += '- เอกสารที่ถูกลงลายเซ็น -' + '\n'
                    count_index = 1
                    for index in range(len(files)):                        
                        data_doc_type = files[index]['data_type']
                        file_name_original_data = files[index]['file_name_original']
                        if data_doc_type == 'main':
                            string_text_mail_sign += 'เอกสารที่ถูกลงลายเซ็น' + ' \n - ชื่อไฟล์ ' + file_name_original_data + '\n'
                            count_index = count_index + 1
                    string_text_mail_att = '- เอกสารไฟล์แนบ -' + '\n'
                    count_index_att = 1
                    for index in range(len(files)):                        
                        data_doc_type = files[index]['data_type']
                        file_name_original_data = files[index]['file_name_original']
                        if data_doc_type != 'main':
                            string_text_mail_att += 'ไฟล์แนบลำดับที่ ' + str(count_index_att) + ' \n - ชื่อไฟล์ ' + file_name_original_data + '\n'
                            count_index_att = count_index_att + 1
                    string_text_mail += string_text_mail_sign + '\n' + string_text_mail_att  + '\n\n\nเอกสารส่งจากระบบ paperless'
                    for file in range(len(files)):
                        part = MIMEBase('application', "octet-stream")
                        part.set_payload(open(files[file]['path_file'], "rb").read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', 'attachment', filename=files[file]['file_name_original'])
                        msg.attach(part)
                    mail_body = string_text_mail
                    msg.attach(MIMEText(mail_body))
                    try:
                        server = smtplib.SMTP(smtp_server)
                        server.sendmail(from_address, to_address, msg.as_string())
                        server.quit()
                        print('success')
                        insert().insert_log_mail_sender(self.to_email,self.sender_email,'send mail success')
                        return {'result':'OK','messageER':None}
                    except Exception as e:
                        print(str(e))
                        insert().insert_log_mail_sender(self.to_email,self.sender_email,str(e))
                        return {'result':'ER','messageER':str(e)}
                else:
                    insert().insert_log_mail_sender(self.to_email,self.sender_email,'not found file')
                    return {'result':'ER','messageER':None}
            else:
                # json_data_res = resultselect_00['messageText']['json_data']
                # self.path_foldername = resultselect_00['messageText']['pathfolder']
                document_Id_data = result_Document['messageText']['document_id']
                # path_file = os.getcwd() + self.path_foldername
                self.to_subject = 'เอกสารเลขที่ ' + str(document_Id_data)
                msg['Subject'] =  self.to_subject
                msg['To'] = self.to_email
                msg['From'] = "noreply-paperless@one.th"  
                to_address = self.to_email
                from_address =  "noreply-paperless@one.th"  
                msg['CC'] = self.sender_email
                string_text_mail = ''
                unique_foldername = str(uuid.uuid4())
                path = path_global_1 + '/storage/mail/' + self.sid_code + '/'
                # path = './storage/mail/' + self.sid_code + '/'
                if not os.path.exists(path):
                    os.makedirs(path)
                path_getcwd = path_global_1 + '/storage/mail/' + self.sid_code + '/'    
                # path_getcwd = os.getcwd() + '/storage/mail/' + self.sid_code + '/'
                file_string = result_base64['messageText']
                if file_id != None:
                    string_text_mail_sign = 'นำส่งโดย ' + self.sender_email + ' \n\n'
                    resultselect_ = select().select_pdfstring_to_fileid(file_id)
                    # print(resultselect_)
                    if resultselect_['result'] == 'OK':
                        pdf_base64_last = resultselect_['messageText']['pdf_string']
                        unique_filename = str(uuid.uuid4())
                        # print(pdf_base64_last)
                        with open(path + file_name ,"wb") as f:
                            f.write(base64.b64decode((pdf_base64_last)))
                        files.append({'path_file':path_getcwd + file_name,'file_name_original':file_name,'data_type':'main'})
                    string_text_mail_sign += '- เอกสารที่ถูกลงลายเซ็น -' + '\n'
                    count_index = 1
                    print(files)
                    for index in range(len(files)):                        
                        data_doc_type = files[index]['data_type']
                        file_name_original_data = files[index]['file_name_original']
                        if data_doc_type == 'main':
                            string_text_mail_sign += 'เอกสารที่ถูกลงลายเซ็น' + ' \n - ชื่อไฟล์ ' + file_name_original_data + '\n'
                            count_index = count_index + 1
                    string_text_mail_att = '- เอกสารไฟล์แนบ -' + '\n'
                    count_index_att = 1
                    for index in range(len(files)):                        
                        data_doc_type = files[index]['data_type']
                        file_name_original_data = files[index]['file_name_original']
                        if data_doc_type != 'main':
                            string_text_mail_att += 'ไฟล์แนบลำดับที่ ' + str(count_index_att) + ' \n - ชื่อไฟล์ ' + file_name_original_data + '\n'
                            count_index_att = count_index_att + 1
                        if count_index_att == 1:
                            string_text_mail_att = 'ไม่พบไฟล์แนบ'
                    string_text_mail += string_text_mail_sign + '\n' + string_text_mail_att  + '\n\n\nเอกสารส่งจากระบบ paperless'
                    for file in range(len(files)):
                        part = MIMEBase('application', "octet-stream")
                        part.set_payload(open(files[file]['path_file'], "rb").read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', 'attachment', filename=files[file]['file_name_original'])
                        msg.attach(part)
                    mail_body = string_text_mail
                    msg.attach(MIMEText(mail_body))
                    # part = MIMEBase('application', "octet-stream")
                    # part.set_payload(open(path_file_to_mail, "rb").read())
                    # encoders.encode_base64(part)
                    # part.add_header('Content-Disposition', 'attachment', filename= result_Document['messageText']['file_Name'])
                    # msg.attach(part)
                    try:
                        server = smtplib.SMTP(smtp_server)
                        server.sendmail(from_address, to_address, msg.as_string())
                        server.set_debuglevel(2)
                        server.ehlo()
                        server.quit()
                        # print(server)
                        insert().insert_log_mail_sender(self.to_email,self.sender_email,'send mail success')
                        return {'result':'OK','messageER':None}
                    except Exception as e:
                        insert().insert_log_mail_sender(self.to_email,self.sender_email,str(e))
                        return {'result':'ER','messageER':str(e)}
                # insert().insert_log_mail_sender(self.to_email,self.sender_email,'not found sid')
                # return {'result':'ER','messageER':None}
        else:
            insert().insert_log_mail_sender(self.to_email,self.sender_email,'not found sid')
            return {'result':'ER','messageER':None}

    def send_email_v2(self,email_User,tracking,name_file,message,url_sign, sidCode):
        self.email_User = email_User
        self.tracking = tracking
        self.name_file = name_file
        self.message = message
        self.url_sign = url_sign
        self.sidCode = sidCode
        # Subject = 'Paperless'
        host = "mailtx.inet.co.th"
        result_Document = select().select_documentId_Mail(self.sidCode)
        if result_Document['result'] == 'OK':
            Subject = "เลขที่เอกสาร " + result_Document['messageText']['document_id']
        else:
            Subject = "เลขที่เอกสาร " + " ไม่พบเลขที่เอกสาร"
        to = self.email_User
        trackingId = self.tracking
        name_file = self.name_file
        messageForUser = self.message
        url_file = self.url_sign
        From = "paperless-bot@one.th"
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Subject
        msg['From'] = From
        msg['To'] = to
        myUrl_tracking = url_paperless + "tracking?id=" + trackingId
        string_qrCode = qr_Code.gen_qrcode(url_file)
        hash_string_qrCode = hashlib.sha256(str(string_qrCode).encode('utf8')).hexdigest()
        url_sendEmail = myUrl_domain + 'api/qrcode/' + str(hash_string_qrCode)  +'.jpg'
        html = "<!DOCTYPE html><html><head><meta charset=\"UTF-8\"></head><body><p><b>" + Subject +"<br>เลขติดตามสถานะเอกสาร : <a href=" + myUrl_tracking +">" + trackingId +"</a>" +"</p><p>ลิงค์เข้าระบบลงลายเซ็น <b><a href=" + url_file +">กดที่นี่เพื่อเข้าระบบ</a>" + "</b></p></br><img src=" + url_sendEmail + " width=\"250\" height=\"250\"><p>" + messageForUser + "</p><i><br>ขอบคุณที่ใช้บริการ<br>Send From Paperless</i>" \
        "<p><i>© Copyright 2020, Internet Thailand Public Company Limited.</i><br><br>กรุณาอย่าตอบกลับอีเมลนี้</p></body></html>"
        part2 = MIMEText(html, 'html',"utf-8")
        msg.attach(part2)
        try:
            s = smtplib.SMTP(host)
            s.sendmail(From, to, msg.as_string())
            s.quit()
            res_insert = insert().insert_sendEmail(self.sidCode,'OK',to,From,string_qrCode,url_file)
            return {'result':'OK','messageText':None}
        except Exception as ex:
            res_insert = insert().insert_sendEmail(self.sidCode,str(ex),to,From,string_qrCode,url_file)
            return {'result':'ER','messageText': str(ex)}
    
    def send_email(self,setjson_email,sidCode):
        self.setjson_email = setjson_email
        self.sidCode       = sidCode
        Host = "mailtx.inet.co.th"
        result_Document = select().select_documentId_Mail(self.sidCode)
        if result_Document['result'] == 'OK':
            Subject = "เลขที่เอกสาร " + result_Document['messageText']['document_id']
        else:
            Subject = "เลขที่เอกสาร " + " ไม่พบเลขที่เอกสาร"
        To = self.setjson_email['emailUser']
        TrackingId = self.setjson_email['tracking']
        Name_file = self.setjson_email['name_file']
        messageForUser = self.setjson_email['message']
        Url_file = self.setjson_email['url_sign']
        From = "noreply-paperless@one.th"
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Subject
        msg['From'] = From
        msg['To'] = To
        myUrl_tracking = url_paperless + "tracking?id=" + TrackingId
        string_qrCode = qr_Code.gen_qrcode(Url_file)
        hash_string_qrCode = hashlib.sha256(str(string_qrCode).encode('utf8')).hexdigest()
        url_sendEmail = myUrl_domain + 'api/qrcode/' + str(hash_string_qrCode)  +'.jpg'
        html = "<!DOCTYPE html><html><head><meta charset=\"UTF-8\"></head><body><p><b>" + Subject +"</br>เลขติดตามสถานะเอกสาร : <a href=" + myUrl_tracking +">" + TrackingId +"</a>" +"</p><p>ลิงค์เข้าระบบลงลายเซ็น <b><a href=" + Url_file +">กดที่นี่เพื่อเข้าระบบ</a>" + "</b></p></br><img src=" + url_sendEmail + " width=\"250\" height=\"250\"><p>" + messageForUser + "</p><i><br>ขอบคุณที่ใช้บริการ<br>Send From Paperless</i>" \
        "<p><i>© Copyright 2020, Internet Thailand Public Company Limited.</i><br><br>กรุณาอย่าตอบกลับอีเมลนี้</p></body></html>"
        part2 = MIMEText(html, 'html',"utf-8")
        msg.attach(part2)
        try:
            s = smtplib.SMTP(Host)
            s.sendmail(From, To, msg.as_string())
            s.quit()
            res_insert = insert().insert_sendEmail(self.sidCode,'OK',To,From,string_qrCode,Url_file)
            return {'result':'OK','messageText':None}
        except Exception as ex:
            res_insert = insert().insert_sendEmail(self.sidCode,str(ex),To,From,string_qrCode,Url_file)
            return {'result':'ER','messageText': str(ex)}

    def send_email_next(self,setjson_email,sidCode):
        self.setjson_email = setjson_email
        self.sidCode       = sidCode
        print(self.setjson_email)
        Host = "mailtx.inet.co.th"
        result_Document = select().select_documentId_Mail(self.sidCode)
        if result_Document['result'] == 'OK':
            Subject = "เลขที่เอกสาร " + result_Document['messageText']['document_id']
        else:
            Subject = "เลขที่เอกสาร " + " ไม่พบเลขที่เอกสาร"
        To = self.setjson_email['email']
        print(To)
        TrackingId = self.setjson_email['tracking']
        Name_file = self.setjson_email['name_file']
        messageForUser = self.setjson_email['message']
        Url_file = self.setjson_email['url_sign']
        From = "noreply-paperless@one.th"
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Subject
        msg['From'] = From
        msg['To'] = To
        myUrl_tracking = url_paperless + "tracking?id=" + TrackingId
        string_qrCode = qr_Code.gen_qrcode(Url_file)
        hash_string_qrCode = hashlib.sha256(str(string_qrCode).encode('utf8')).hexdigest()
        url_sendEmail = myUrl_domain + 'api/qrcode/' + str(hash_string_qrCode)  +'.jpg'
        html = "<!DOCTYPE html><html><head><meta charset=\"UTF-8\"></head><body><p><b>" + Subject +"</br>เลขติดตามสถานะเอกสาร : <a href=" + myUrl_tracking +">" + TrackingId +"</a>" +"</p><p>ลิงค์เข้าระบบลงลายเซ็น <b><a href=" + Url_file +">กดที่นี่เพื่อเข้าระบบ</a>" + "</b></p></br><img src=" + url_sendEmail + " width=\"250\" height=\"250\"><p>" + messageForUser + "</p><i><br>ขอบคุณที่ใช้บริการ<br>Send From Paperless</i>" \
        "<p><i>© Copyright 2020, Internet Thailand Public Company Limited.</i><br><br>กรุณาอย่าตอบกลับอีเมลนี้</p></body></html>"
        part2 = MIMEText(html, 'html',"utf-8")
        msg.attach(part2)
        try:
            s = smtplib.SMTP(Host)
            s.sendmail(From, To, msg.as_string())
            s.quit()
            res_insert = insert().insert_sendEmail(self.sidCode,'OK',To,From,string_qrCode,Url_file)
            return {'result':'OK','messageText':None}
        except Exception as ex:
            res_insert = insert().insert_sendEmail(self.sidCode,str(ex),To,From,string_qrCode,Url_file)
            return {'result':'ER','messageText': str(ex)}

    def send_emailSender(self,email,sidCode,messageText_Recp):
        self.messageText_Recp = messageText_Recp
        self.email = email
        self.sidCode = sidCode
        Host = "mailtx.inet.co.th"
        result_Document = select().select_documentId_Mail(self.sidCode)
        if result_Document['result'] != 'OK':
            return {'result':'ER','messageText':'not found'}
        myUrl_tracking = url_paperless + "tracking?id=" + result_Document['messageText']['tracking_id']
        Title = "Paperless"
        Subject = "<br>"
        if result_Document['result'] == 'OK':
            Subject += "** รายละเอียดเอกสารภายในระบบ paperless **<br>- เลขที่เอกสาร " + result_Document['messageText']['document_id'] + "<br>" + "- เลขที่ติดตามสถานะเอกสาร <a href=" + myUrl_tracking + ">" + result_Document['messageText']['tracking_id'] +'</a><br>- ชื่อไฟล์เอกสาร ' + result_Document['messageText']['file_Name'] +""
        else:
            Subject += "- เลขที่เอกสาร " + " ไม่พบเลขที่เอกสาร"
        print(Subject)
        # To = self.setjson_email['email']
        To = self.email
        # print(To)
        # TrackingId = self.setjson_email['tracking']
        # Name_file = self.setjson_email['name_file']
        # messageForUser = self.setjson_email['message']
        # Url_file = self.setjson_email['url_sign']
        From = "noreply-paperless@one.th"
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Title
        msg['From'] = From
        msg['To'] = To
        #
        Url_file = "None"
        string_qrCode = "None"
        # hash_string_qrCode = hashlib.sha256(str(string_qrCode).encode('utf8')).hexdigest()
        # url_sendEmail = myUrl_domain + 'api/qrcode/' + str(hash_string_qrCode)  +'.jpg'
        html = "<!DOCTYPE html><html><head><meta charset=\"UTF-8\"></head><body><p><b>แจ้งเตือนระบบ Paperless <br>" + Subject +"</br></br></p>" + self.messageText_Recp +"<br><br><i><br>ขอบคุณที่ใช้บริการ<br>Send From Paperless</i>" \
        "<p><i>© Copyright 2020, Internet Thailand Public Company Limited.</i><br><br>กรุณาอย่าตอบกลับอีเมลนี้</p></body></html>"
        part2 = MIMEText(html, 'html',"utf-8")
        msg.attach(part2)
        try:
            s = smtplib.SMTP(Host)
            s.sendmail(From, To, msg.as_string())
            s.quit()
            res_insert = insert().insert_sendEmail(self.sidCode,'OK',To,From,string_qrCode,Url_file)
            return {'result':'OK','messageText':None}
        except Exception as ex:
            res_insert = insert().insert_sendEmail(self.sidCode,str(ex),To,From,string_qrCode,Url_file)
            return {'result':'ER','messageText': str(ex)}
    
    def send_emailSend_emailcenter(self,email,sidCode,messageText_Recp):
        self.messageText_Recp = messageText_Recp
        self.email = email
        self.sidCode = sidCode
        result_base64 = select().select_file_sign_last_to_email(self.sidCode)
        resultselect_ = select().select_attm_file_v1_for_chat_api_to_robot(self.sidCode)
        files = []
        msg = MIMEMultipart('alternative')
        if resultselect_['result'] == 'OK':
            doc_id = resultselect_['messageText']['document_Id']
            pathFolder = resultselect_['messageText']['pathfolder']
            pathFolder = os.getcwd() + pathFolder
            json_Data_File = resultselect_['messageText']['json_data']
            username_sender = resultselect_['messageText']['sender_username']
            document_Type = resultselect_['messageText']['document_Type']
            list_file_username = []
            for u in range(len(json_Data_File)):
                list_file_username.append({'file_name_new':json_Data_File[u]['file_name_new'],'file_name_original':json_Data_File[u]['file_name_original']})
            # print(list_file_username)
            for r, d, f in os.walk(pathFolder):
                for file in f:
                    print(file)
                    for i in range(len(list_file_username)):
                        if list_file_username[i]['file_name_new'] == file:
                            files.append({'path_file':os.path.join(r, file),'file_name_original':list_file_username[i]['file_name_original']})
        else:
            doc_id = None
            pathFolder = None
            json_Data_File = None
            username_sender = None
            document_Type = None
        if len(files) != 0:
            for file in range(len(files)):
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(files[file]['path_file'], "rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=files[file]['file_name_original'])
                msg.attach(part)
        unique_foldername = str(uuid.uuid4())
        path = './storage/file_mail/' + unique_foldername +'/'
        if not os.path.exists(path):
            os.makedirs(path)
        file_string = result_base64['messageText']
        unique_filename = str(uuid.uuid4())
        with open(path + unique_filename + ".pdf", "wb") as fh:
            fh.write(base64.b64decode(file_string))
        path_file_to_mail = path + unique_filename + ".pdf"
        Host = "mailtx.inet.co.th"
        result_Document = select().select_documentId_Mail(self.sidCode)
        if result_Document['result'] != 'OK':
            return {'result':'ER','messageText':'not found'}
        myUrl_tracking = url_paperless + "tracking?id=" + result_Document['messageText']['tracking_id']
        Title = "Paperless"
        Subject = "<br>"
        if result_Document['result'] == 'OK':
            Subject += "** รายละเอียดเอกสารภายในระบบ paperless **<br>- เลขที่เอกสาร " + result_Document['messageText']['document_id'] + "<br>" + "- เลขที่ติดตามสถานะเอกสาร <a href=" + myUrl_tracking + ">" + result_Document['messageText']['tracking_id'] +'</a><br>- ชื่อไฟล์เอกสาร ' + result_Document['messageText']['file_Name'] +""
        else:
            Subject += "- เลขที่เอกสาร " + " ไม่พบเลขที่เอกสาร"
        print(Subject)
        To = self.email
       
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(path_file_to_mail, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename= result_Document['messageText']['file_Name'])
        msg.attach(part)
        From = "noreply-paperless@one.th"
        
        msg['Subject'] = Title
        msg['From'] = From
        msg['To'] = To
        Url_file = "None"
        string_qrCode = "None"
        html = "<!DOCTYPE html><html><head><meta charset=\"UTF-8\"></head><body><p><b>แจ้งเตือนระบบ Paperless <br>" + Subject +"</br></br></p>" + self.messageText_Recp +"<br><br><i><br>ขอบคุณที่ใช้บริการ<br>Send From Paperless</i>" \
        "<p><i>© Copyright 2020, Internet Thailand Public Company Limited.</i><br><br>กรุณาอย่าตอบกลับอีเมลนี้</p></body></html>"
        part2 = MIMEText(html, 'html',"utf-8")
        msg.attach(part2)
        try:
            s = smtplib.SMTP(Host)
            s.sendmail(From, To, msg.as_string())
            s.quit()
            res_insert = insert().insert_sendEmail(self.sidCode,'OK',To,From,string_qrCode,Url_file)
            return {'result':'OK','messageText':None}
        except Exception as ex:
            res_insert = insert().insert_sendEmail(self.sidCode,str(ex),To,From,string_qrCode,Url_file)
            return {'result':'ER','messageText': str(ex)}

    def sendEmail_center_group(self,sidCode,EmailCenter,document_type):
        self.sidCode = sidCode
        self.EmailCenter = EmailCenter
        self.document_type = document_type
        try:
            list_email_file = []
            msg = MIMEMultipart('alternative')
            unique_foldername = str(uuid.uuid4())
            path = path_global_1 + '/storage/file_mail/' + unique_foldername +'/'
            # path = './storage/file_mail/' + unique_foldername +'/'
            str_text = ''
            email_Send = []
            if not os.path.exists(path):
                os.makedirs(path)
            for i in self.EmailCenter:
                email_Send.append(i['email'])
            for sid in self.sidCode:
                files = []
                result_base64 = select().select_file_sign_last_to_email(sid)
                resultselect_ = select().select_attm_file_v1_for_chat_api_to_robot(sid)
                result_Document = select().select_documentId_Mail(sid)
                filename_tmpOrg = result_Document['messageText']['file_Name']
                if resultselect_['result'] == 'OK':
                    doc_id = resultselect_['messageText']['document_Id']
                    pathFolder = resultselect_['messageText']['pathfolder']
                    pathFolder = path_global_1+ pathFolder
                    # pathFolder = os.getcwd() + pathFolder
                    json_Data_File = resultselect_['messageText']['json_data']
                    tmp_folder_name = resultselect_['messageText']['folder_name']
                    username_sender = resultselect_['messageText']['sender_username']
                    document_Type = resultselect_['messageText']['document_Type']
                    str_text += '<br>เลขที่เอกสาร ' + doc_id + '<br>' 
                    str_text += 'รายการเอกสาร <br>- ไฟล์หลัก : ' + filename_tmpOrg + '<br>- ไฟล์แนบ<br>'
                    list_file_username = []
                    if json_Data_File != None:
                        for u in range(len(json_Data_File)):
                            # tmpurl_download = json_Data_File[u]['url_download']
                            # tmpurl_view_pdf = json_Data_File[u]['url_view_pdf']
                            tmpfile_name_new = json_Data_File[u]['file_name_new']
                            tmpurl_download = myUrl_domain + 'storage/downloadfile/v1/' + tmp_folder_name +"/"+tmpfile_name_new
                            tmpurl_view_pdf = myUrl_domain + 'storage/viewfile/v1/'+tmp_folder_name+"/"+tmpfile_name_new
                            list_file_username.append({'file_name_new':json_Data_File[u]['file_name_new'],'file_name_original':json_Data_File[u]['file_name_original']})
                            tmp_filename_org = json_Data_File[u]['file_name_original']
                            tmptypeFile = str(tmp_filename_org)
                            tmptypeFile = (tmptypeFile).split('.')[-1]
                            if str(tmptypeFile).lower() == 'pdf':
                                str_text += tmp_filename_org + ' <a href=' + tmpurl_download+'>ดาวน์โหลดไฟล์</a>&nbsp;&nbsp;<a href=' + tmpurl_view_pdf+'>ดูเอกสาร</a><br>'
                            else:
                                str_text += tmp_filename_org + ' <a href=' + tmpurl_download+'>ดาวน์โหลดไฟล์</a><br>'
                        # for r, d, f in os.walk(pathFolder):
                        #     for file in f:
                        #         print(file)
                        #         for i in range(len(list_file_username)):
                        #             if list_file_username[i]['file_name_new'] == file:
                        #                 files.append({'path_file':os.path.join(r, file),'file_name_original':list_file_username[i]['file_name_original']})
                else:
                    doc_id = None
                    pathFolder = None
                    json_Data_File = None
                    username_sender = None
                    document_Type = None
                    doc_id = resultselect_['messageText']['document_Id']
                    pathFolder = resultselect_['messageText']['pathfolder']
                    tmpFolder_name = resultselect_['messageText']['folder_name']
                    str_text += '<br>เลขที่เอกสาร ' + doc_id + '<br>' 
                    str_text += 'รายการเอกสาร <br>- ไฟล์หลัก : ' + filename_tmpOrg + '<br>- ไฟล์แนบ<br>'
                    if tmpFolder_name != None:
                        url_GetfileEFORM = url_ip_eform + '/api/v1/get_attract_file/?folder_name=' + tmpFolder_name
                        result_Data = callGET_other(url_GetfileEFORM)
                        if result_Data['result'] == 'OK':
                            tmpDataMesg = result_Data['messageText'].json()
                            if tmpDataMesg['result'] == 'OK':
                                tmpMesg = tmpDataMesg['messageText']   
                                tmpfilename = tmpMesg[0]['file_name']
                                list_file_name = []
                                # path = './storage/' + tmpFolder_name +'/'
                                # path_indb = '/storage/' + tmpFolder_name +'/'
                                # if not os.path.exists(path):
                                #     os.makedirs(path)
                                for x in range(len(tmpfilename)):
                                    tmpurl_download = tmpfilename[x]['url_download']
                                    tmpurl_view_pdf = tmpfilename[x]['url_view_pdf']
                                    tmpfile_name_new = tmpfilename[x]['file_name_new']
                                    tmp_filename_org = tmpfilename[x]['file_name_original']
                                    tmptypeFile = str(tmp_filename_org)
                                    tmptypeFile = (tmptypeFile).split('.')[-1]
                                    if str(tmptypeFile).lower() == 'pdf':
                                        str_text += tmp_filename_org + ' <a href=' + tmpurl_download+'>ดาวน์โหลดไฟล์</a>&nbsp;&nbsp;<a href=' + tmpurl_view_pdf+'>ดูเอกสาร</a><br>'
                                    else:
                                        str_text += tmp_filename_org + ' <a href=' + tmpurl_download+'>ดาวน์โหลดไฟล์</a><br>'
                                    # with open(path + tmpfile_name_new + tmptypeFile, 'wb') as f:
                                    #     f.write(r.content)
                    
                    
                # if len(files) != 0:
                #     for file in range(len(files)):
                #         part = MIMEBase('application', "octet-stream")
                #         part.set_payload(open(files[file]['path_file'], "rb").read())
                #         encoders.encode_base64(part)
                #         part.add_header('Content-Disposition', 'attachment', filename=files[file]['file_name_original'])
                #         msg.attach(part)
                file_string = result_base64['messageText']
                unique_filename = str(uuid.uuid4())
                with open(path + unique_filename + ".pdf", "wb") as fh:
                    fh.write(base64.b64decode(file_string))
                path_file_to_mail = path + unique_filename + ".pdf"
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(path_file_to_mail, "rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename= filename_tmpOrg)
                msg.attach(part)
                list_email_file.append({'sid':sid,'file_pdf':path_file_to_mail,'file_pdf_name':filename_tmpOrg,'document_id':doc_id})
                str_text += '<br>'
            To = email_Send
            host = "mailtx.inet.co.th"
            # myUrl_tracking = url_paperless + "tracking?id=" + result_Document['messageText']['tracking_id']
            Subject = ''
            Title = "Paperless"
            From = "paperless-"+self.document_type+"@one.th"        
            msg['Subject'] = Title
            msg['From'] = From
            msg['To'] = ', '.join(To)
            Url_file = "None"
            string_qrCode = "None"
            html = "<!DOCTYPE html><html><head><meta charset=\"UTF-8\"></head><body><p><b>แจ้งเตือนระบบ Paperless </b</p><br>" + str_text +"</br></br>" + "" +"<br><br><i><br>ขอบคุณที่ใช้บริการ<br>Send From Paperless</i>" \
            "<p><i>© Copyright 2020, Internet Thailand Public Company Limited.</i><br><br>กรุณาอย่าตอบกลับอีเมลนี้</p></body></html>"
            part2 = MIMEText(html, 'html',"utf-8")
            msg.attach(part2)
            s = smtplib.SMTP(host)
            # s.set_debuglevel(1)
            s.sendmail(From, To, msg.as_string())
            s.quit()
            print('ok')
            res_insert = insert().insert_sendEmail(self.sidCode,'OK',To,From,string_qrCode,Url_file)
            return {'result':'OK','messageText':None}
        except Exception as ex:
            print(str(ex))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            res_insert = insert().insert_sendEmail(self.sidCode,str(ex),To,From,string_qrCode,Url_file)
            return {'result':'ER','messageText': str(ex)}

    def send_emailSend_emailcenter_list_v2(self,sidCode,EmailCenter,document_type):
        self.sidCode = sidCode
        self.EmailCenter = EmailCenter
        self.document_type = document_type
        try:
            list_email_file = []
            msg = MIMEMultipart('alternative')
            unique_foldername = str(uuid.uuid4())
            path = path_global_1 + '/storage/file_mail/' + unique_foldername +'/'
            # path = './storage/file_mail/' + unique_foldername +'/'
            str_text = ''
            email_Send = []
            if not os.path.exists(path):
                os.makedirs(path)
            for i in self.EmailCenter:
                email_Send.append(i['email'])
            for sid in self.sidCode:
                files = []
                result_base64 = select().select_file_sign_last_to_email(sid)
                resultselect_ = select().select_attm_file_v1_for_chat_api_to_robot(sid)
                result_Document = select().select_documentId_Mail(sid)
                filename_tmpOrg = result_Document['messageText']['file_Name']
                if resultselect_['result'] == 'OK':
                    doc_id = resultselect_['messageText']['document_Id']
                    pathFolder = resultselect_['messageText']['pathfolder']
                    pathFolder = path_global_1+ pathFolder
                    # pathFolder = os.getcwd() + pathFolder
                    json_Data_File = resultselect_['messageText']['json_data']
                    tmp_folder_name = resultselect_['messageText']['folder_name']
                    username_sender = resultselect_['messageText']['sender_username']
                    document_Type = resultselect_['messageText']['document_Type']
                    str_text += '<br>เลขที่เอกสาร ' + doc_id + '<br>' 
                    str_text += 'รายการเอกสาร <br>- ไฟล์หลัก : ' + filename_tmpOrg + '<br>- ไฟล์แนบ<br>'
                    list_file_username = []
                    if json_Data_File != None:
                        for u in range(len(json_Data_File)):
                            # tmpurl_download = json_Data_File[u]['url_download']
                            # tmpurl_view_pdf = json_Data_File[u]['url_view_pdf']
                            tmpfile_name_new = json_Data_File[u]['file_name_new']
                            tmpurl_download = myUrl_domain + 'storage/downloadfile/v1/' + tmp_folder_name +"/"+tmpfile_name_new
                            tmpurl_view_pdf = myUrl_domain + 'storage/viewfile/v1/'+tmp_folder_name+"/"+tmpfile_name_new
                            list_file_username.append({'file_name_new':json_Data_File[u]['file_name_new'],'file_name_original':json_Data_File[u]['file_name_original']})
                            tmp_filename_org = json_Data_File[u]['file_name_original']
                            tmptypeFile = str(tmp_filename_org)
                            tmptypeFile = (tmptypeFile).split('.')[-1]
                            if str(tmptypeFile).lower() == 'pdf':
                                str_text += tmp_filename_org + ' <a href=' + tmpurl_download+'>ดาวน์โหลดไฟล์</a>&nbsp;&nbsp;<a href=' + tmpurl_view_pdf+'>ดูเอกสาร</a><br>'
                            else:
                                str_text += tmp_filename_org + ' <a href=' + tmpurl_download+'>ดาวน์โหลดไฟล์</a><br>'
                        # for r, d, f in os.walk(pathFolder):
                        #     for file in f:
                        #         print(file)
                        #         for i in range(len(list_file_username)):
                        #             if list_file_username[i]['file_name_new'] == file:
                        #                 files.append({'path_file':os.path.join(r, file),'file_name_original':list_file_username[i]['file_name_original']})
                else:
                    doc_id = None
                    pathFolder = None
                    json_Data_File = None
                    username_sender = None
                    document_Type = None
                    doc_id = resultselect_['messageText']['document_Id']
                    pathFolder = resultselect_['messageText']['pathfolder']
                    tmpFolder_name = resultselect_['messageText']['folder_name']
                    str_text += '<br>เลขที่เอกสาร ' + doc_id + '<br>' 
                    str_text += 'รายการเอกสาร <br>- ไฟล์หลัก : ' + filename_tmpOrg + '<br>- ไฟล์แนบ<br>'
                    if tmpFolder_name != None:
                        url_GetfileEFORM = url_ip_eform + '/api/v1/get_attract_file/?folder_name=' + tmpFolder_name
                        result_Data = callGET_other(url_GetfileEFORM)
                        if result_Data['result'] == 'OK':
                            tmpDataMesg = result_Data['messageText'].json()
                            if tmpDataMesg['result'] == 'OK':
                                tmpMesg = tmpDataMesg['messageText']   
                                tmpfilename = tmpMesg[0]['file_name']
                                list_file_name = []
                                # path = './storage/' + tmpFolder_name +'/'
                                # path_indb = '/storage/' + tmpFolder_name +'/'
                                # if not os.path.exists(path):
                                #     os.makedirs(path)
                                for x in range(len(tmpfilename)):
                                    tmpurl_download = tmpfilename[x]['url_download']
                                    tmpurl_view_pdf = tmpfilename[x]['url_view_pdf']
                                    tmpfile_name_new = tmpfilename[x]['file_name_new']
                                    tmp_filename_org = tmpfilename[x]['file_name_original']
                                    tmptypeFile = str(tmp_filename_org)
                                    tmptypeFile = (tmptypeFile).split('.')[-1]
                                    if str(tmptypeFile).lower() == 'pdf':
                                        str_text += tmp_filename_org + ' <a href=' + tmpurl_download+'>ดาวน์โหลดไฟล์</a>&nbsp;&nbsp;<a href=' + tmpurl_view_pdf+'>ดูเอกสาร</a><br>'
                                    else:
                                        str_text += tmp_filename_org + ' <a href=' + tmpurl_download+'>ดาวน์โหลดไฟล์</a><br>'
                                    # with open(path + tmpfile_name_new + tmptypeFile, 'wb') as f:
                                    #     f.write(r.content)
                    
                    
                # if len(files) != 0:
                #     for file in range(len(files)):
                #         part = MIMEBase('application', "octet-stream")
                #         part.set_payload(open(files[file]['path_file'], "rb").read())
                #         encoders.encode_base64(part)
                #         part.add_header('Content-Disposition', 'attachment', filename=files[file]['file_name_original'])
                #         msg.attach(part)
                file_string = result_base64['messageText']
                unique_filename = str(uuid.uuid4())
                with open(path + unique_filename + ".pdf", "wb") as fh:
                    fh.write(base64.b64decode(file_string))
                path_file_to_mail = path + unique_filename + ".pdf"
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(path_file_to_mail, "rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename= filename_tmpOrg)
                msg.attach(part)
                list_email_file.append({'sid':sid,'file_pdf':path_file_to_mail,'file_pdf_name':filename_tmpOrg,'document_id':doc_id})
                str_text += '<br>'
            To = email_Send
            host = "mailtx.inet.co.th"
            # myUrl_tracking = url_paperless + "tracking?id=" + result_Document['messageText']['tracking_id']
            Subject = ''
            Title = "Paperless"
            From = "paperless-"+self.document_type+"@one.th"        
            msg['Subject'] = Title
            msg['From'] = From
            msg['To'] = ', '.join(To)
            Url_file = "None"
            string_qrCode = "None"
            html = "<!DOCTYPE html><html><head><meta charset=\"UTF-8\"></head><body><p><b>แจ้งเตือนระบบ Paperless </b</p><br>" + str_text +"</br></br>" + "" +"<br><br><i><br>ขอบคุณที่ใช้บริการ<br>Send From Paperless</i>" \
            "<p><i>© Copyright 2020, Internet Thailand Public Company Limited.</i><br><br>กรุณาอย่าตอบกลับอีเมลนี้</p></body></html>"
            part2 = MIMEText(html, 'html',"utf-8")
            msg.attach(part2)
            s = smtplib.SMTP(host)
            # s.set_debuglevel(1)
            s.sendmail(From, To, msg.as_string())
            s.quit()
            print('ok')
            res_insert = insert().insert_sendEmail(self.sidCode,'OK',To,From,string_qrCode,Url_file)
            return {'result':'OK','messageText':None}
        except Exception as ex:
            print(str(ex))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            res_insert = insert().insert_sendEmail(self.sidCode,str(ex),To,From,string_qrCode,Url_file)
            return {'result':'ER','messageText': str(ex)}

    def send_emailSend_emailcenter_list(self,email,sidCode,messageText_Recp,attemp_status,file_pdf):
        self.messageText_Recp = messageText_Recp
        self.email = email
        self.sidCode = sidCode
        self.attemp_status = attemp_status
        self.file_pdf   = file_pdf
        result_base64 = select().select_file_sign_last_to_email(self.sidCode)
        resultselect_ = select().select_attm_file_v1_for_chat_api_to_robot(self.sidCode)
        # print(resultselect_)
        files = []
        msg = MIMEMultipart('alternative')
        if resultselect_['result'] == 'OK':
            doc_id = resultselect_['messageText']['document_Id']
            pathFolder = resultselect_['messageText']['pathfolder']
            pathFolder = os.getcwd() + pathFolder
            json_Data_File = resultselect_['messageText']['json_data']
            username_sender = resultselect_['messageText']['sender_username']
            document_Type = resultselect_['messageText']['document_Type']
            list_file_username = []
            for u in range(len(json_Data_File)):
                list_file_username.append({'file_name_new':json_Data_File[u]['file_name_new'],'file_name_original':json_Data_File[u]['file_name_original']})
            # print(list_file_username)
            for r, d, f in os.walk(pathFolder):
                for file in f:
                    for i in range(len(list_file_username)):
                        if list_file_username[i]['file_name_new'] == file:
                            files.append({'path_file':os.path.join(r, file),'file_name_original':list_file_username[i]['file_name_original']})
        else:
            doc_id = None
            pathFolder = None
            json_Data_File = None
            username_sender = None
            document_Type = None
        # print(self.attemp_status)
        if self.attemp_status == 'true':
            if len(files) != 0:
                for file in range(len(files)):
                    part = MIMEBase('application', "octet-stream")
                    part.set_payload(open(files[file]['path_file'], "rb").read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment', filename=files[file]['file_name_original'])
                    msg.attach(part)
        else:
            pass
        unique_foldername = str(uuid.uuid4())
        path = './storage/file_mail/' + unique_foldername +'/'
        if not os.path.exists(path):
            os.makedirs(path)
        file_string = result_base64['messageText']
        unique_filename = str(uuid.uuid4())
        with open(path + unique_filename + ".pdf", "wb") as fh:
            fh.write(base64.b64decode(file_string))
        path_file_to_mail = path + unique_filename + ".pdf"
        Host = "mailtx.inet.co.th"
        result_Document = select().select_documentId_Mail(self.sidCode)
        if result_Document['result'] != 'OK':
            return {'result':'ER','messageText':'not found'}
        myUrl_tracking = url_paperless + "tracking?id=" + result_Document['messageText']['tracking_id']
        Title = "Paperless"
        Subject = "<br>"
        if result_Document['result'] == 'OK':
            Subject += "** รายละเอียดเอกสารภายในระบบ paperless **<br>- เลขที่เอกสาร " + result_Document['messageText']['document_id'] + "<br>" + "- เลขที่ติดตามสถานะเอกสาร <a href=" + myUrl_tracking + ">" + result_Document['messageText']['tracking_id'] +'</a><br>- ชื่อไฟล์เอกสาร ' + result_Document['messageText']['file_Name'] +""
        else:
            Subject += "- เลขที่เอกสาร " + " ไม่พบเลขที่เอกสาร"
        To = self.email
        if self.file_pdf == 'true':
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(path_file_to_mail, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename= result_Document['messageText']['file_Name'])
            msg.attach(part)
        From = "noreply-paperless@one.th"
        
        msg['Subject'] = Title
        msg['From'] = From
        msg['To'] = To
        Url_file = "None"
        string_qrCode = "None"
        html = "<!DOCTYPE html><html><head><meta charset=\"UTF-8\"></head><body><p><b>แจ้งเตือนระบบ Paperless <br>" + Subject +"</br></br></p>" + self.messageText_Recp +"<br><br><i><br>ขอบคุณที่ใช้บริการ<br>Send From Paperless</i>" \
        "<p><i>© Copyright 2020, Internet Thailand Public Company Limited.</i><br><br>กรุณาอย่าตอบกลับอีเมลนี้</p></body></html>"
        part2 = MIMEText(html, 'html',"utf-8")
        msg.attach(part2)
        try:
            s = smtplib.SMTP(Host)
            s.sendmail(From, To, msg.as_string())
            s.quit()
            res_insert = insert().insert_sendEmail(self.sidCode,'OK',To,From,string_qrCode,Url_file)
            return {'result':'OK','messageText':None}
        except Exception as ex:
            res_insert = insert().insert_sendEmail(self.sidCode,str(ex),To,From,string_qrCode,Url_file)
            return {'result':'ER','messageText': str(ex)}

    def insert_logEmail(self,arralist):
        n = 0
        self.arralist = arralist
        arr_result=[]
        try:
            for i in self.arralist:
                if i['result'] == 'OK':
                    statusId = 'Y'
                if i['result'] == 'ER':
                    statusId = 'ER'
                if i['result'] == 'NO':
                    statusId = 'N'
                email_one = i['email']
                sidCode = i['sid']
                statusSign = 'N'
                step_num = i['step_num']
                urlsign = i['urlSign']
                try:
                    propertyMail = i['property']
                except Exception as ex:
                    propertyMail = None

                n = n + 1
                if n == 1:
                    res_in = insert().insert_transactionMail(sidCode,statusId,str(n),email_one,statusSign,step_num,True,urlsign,propertyMail)
                else:
                    res_in = insert().insert_transactionMail(sidCode,statusId,str(n),email_one,statusSign,step_num,True,urlsign,propertyMail)
                arr_result.append(res_in)
            print(arr_result)
            return {'result':'OK','messageText':arr_result,'status_Code':200}
        except Exception as ex:
            return {'result':'ER','messageText':str(ex),'status_Code':200}

    def select_transactionMail(self,sidCode):
        self.sidCode = sidCode
        resultSelect = select().select_MailTostep(self.sidCode)
        return resultSelect

    def check_sendToMail(self,list_data):
        self.list_data = list_data
        k = 1
        i = 0
        listarr_check_statusSign = []
        listarr_check_stepNum = []
        listarr_check_transactionCode = []
        listarr_check_sidCode = []
        listarr_check_email_User = []
        temp = ''
        for n in self.list_data:
            if int(n['stepNum']) >= k:
                i = i + 1
                listarr_check_statusSign.append(n['statusSign'])
                listarr_check_email_User.append(n['email_User'])
                listarr_check_stepNum.append(n['stepNum'])
                listarr_check_transactionCode.append(str(n['transactionCode']))
                listarr_check_sidCode.append(n['sidCode'])
        for o in range(len(listarr_check_statusSign)):
            if listarr_check_statusSign[o] == 'Y':
                temp = {'statusSign':listarr_check_statusSign[o],'email_User':listarr_check_email_User[o],'stepNum':listarr_check_stepNum[o],'transactionCode':str(listarr_check_transactionCode[o]),'sid':str(listarr_check_sidCode[o])}
        return {'result':'OK','msg':temp}

    def check_EmailProfile(self,email_thai):
        self.email_thai = email_thai
        resulUserProfile = select().select_EmailUserprofile(self.email_thai)
        if resulUserProfile['result'] == 'OK':
            return (resulUserProfile)
        else:
            return (resulUserProfile)

class qr_Code:
    def gen_qrcode(url):
        path = 'temp/qr/'
        if not os.path.exists(path):
            os.makedirs(path)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        data = url
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image()
        unique_qrcode = str(uuid.uuid4())
        img.save(path + unique_qrcode + ".jpg")
        path_qrcode = path + unique_qrcode + ".jpg"
        with open(path_qrcode, "rb") as imageFile:
            str_qr = base64.b64encode(imageFile.read())
        str_qr = (str_qr).decode('utf8')
        os.remove(path_qrcode)
        return str_qr

class mail_to_robot:
    def send_to_robot(self,path_foldername,json_data,username_sender,doc_id):
        self.path_foldername = path_foldername
        self.json_data = json_data
        self.username_sender = username_sender
        self.doc_id = doc_id
        smtp_server = "mailtx.inet.co.th"                          # for smtp.gmail.com
        from_address = "noreply-paperless@one.th"
        to_address = "robot.rpa@inet.co.th"                  # e.g. username2@gmail.com
        subject = "Pre-SO_" + self.doc_id
        mail_body = ""
        path_file = os.getcwd() + self.path_foldername
        msg = MIMEMultipart()
        msg['Subject'] =  subject
        msg['To'] = to_address
        msg.attach(MIMEText(mail_body))
        files = []
        list_file_username = []
        for u in range(len(json_data)):
            username_json =json_data[u]['username']
            if username_json == self.username_sender:
                list_file_username.append({'file_name_new':json_data[u]['file_name_new'],'file_name_original':json_data[u]['file_name_original']})
        print(list_file_username)
        for r, d, f in os.walk(path_file):
            for file in f:
                print(file)
                for i in range(len(list_file_username)):
                    if list_file_username[i]['file_name_new'] == file:
                        if '.xls' in file or '.xlsx' in file:
                            files.append({'path_file':os.path.join(r, file),'file_name_original':list_file_username[i]['file_name_original']})

        for file in range(len(files)):
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(files[file]['path_file'], "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=files[file]['file_name_original'])
            msg.attach(part)
        try:
            server = smtplib.SMTP(smtp_server)
            server.sendmail(from_address, to_address, msg.as_string())
            server.quit()
        except Exception as e:
            print(e)

def send_Mail_for_service_v1(type_service,sid,tracking,name_file,data):
    dataJson = {
        'type_service' : type_service,
        'sid' : sid ,
        'tracking' : tracking,
        'name_file' : name_file,
        'data' : data
    }
    result_list = []
    if 'type_service' in dataJson:
        if dataJson['type_service'].lower() == 'first':
            if 'sid' in dataJson and 'tracking' in dataJson and 'name_file' in dataJson and 'data' in dataJson:
                for i in range(len(dataJson['data'])):
                    if dataJson['data'][i]['step_num'] == "1":
                        result_Email = mail().check_EmailProfile(dataJson['data'][i]['email'])
                        if result_Email['result'] == 'OK':
                            dataJson['data'][i]['emailUser'] = result_Email['messageText']['emailUser']
                            result_mailStatus = mail().send_email(dataJson['data'][i],dataJson['sid'])
                        else:
                            dataJson['data'][i]['emailUser'] = dataJson['data'][i]['email']
                            result_mailStatus = mail().send_email(dataJson['data'][i],dataJson['sid'])
                        if result_mailStatus['result'] == 'OK':
                            result_list.append({'result':'OK','email':dataJson['data'][i]['email'],'sid':dataJson['sid'],'step_num':dataJson['data'][i]['step_num'],'urlSign':dataJson['data'][i]['url_sign']})
                        else:
                            result_list.append({'result':'ER','email':dataJson['data'][i]['email'],'sid':dataJson['sid'],'step_num':dataJson['data'][i]['step_num'],'urlSign':dataJson['data'][i]['url_sign']})
                    else:
                        result_list.append({'result':'NO','email':dataJson['data'][i]['email'],'sid':dataJson['sid'],'step_num':dataJson['data'][i]['step_num'],'urlSign':dataJson['data'][i]['url_sign']})
                result_insertMail = mail().insert_logEmail(result_list)
                if result_insertMail['result'] == 'OK':
                    return ({'result':'OK','messageText':'Send To Email Successfully!','status_Code':200,'messageER':None})
                else:
                    return ({'result':'ER','messageText':None,'status_Code':200,'messageER':result_insertMail['messageText']})
            else:
                return ({'result':'ER','messageText':None,'status_Code':200,'messageER':'param fail'})
        elif dataJson['type_service'].lower() == 'next':
            value_sid = dataJson['sid']
            result_MailTransaction = mail().select_transactionMail(dataJson['sid'])
            result_MailCheck = mail().check_sendToMail(result_MailTransaction)
            result_Array = []
            logmail_list = []
            for i in range(len(result_MailTransaction)):
                if result_MailTransaction[i]['statusSign'] == 'Y':
                    result_MailTransaction[i]['statusSign'] = 'Complete'
                else:
                    result_MailTransaction[i]['statusSign'] = 'Incomplete'
                result_Array.append({
                    'emailUser':result_MailTransaction[i]['email_User'],
                    'statusSign':result_MailTransaction[i]['statusSign'],
                    'stepNum':int(result_MailTransaction[i]['stepNum']),
                    'datetime_string':result_MailTransaction[i]['datetime_string']
                })
            if result_MailCheck['result'] == 'OK':
                try:
                    if str(result_MailCheck['msg']).replace(' ','') != '':
                        print(result_MailCheck)
                        arr_tc = select().select_transactioneMail_next(result_MailCheck)
                        print(arr_tc)
                    else:
                        return ({'result':'OK','messageText':None,'status_Code':200,'messageER':None})
                except Exception as ex:
                    return ({'result':'ER','messageText':None,'status_Code':200,'messageER':'Not Found DATA!'})
            for k in arr_tc:
                json_nextEmail = {}
                result_Email = mail().check_EmailProfile(k['email_User'])
                if result_Email['result'] == 'OK':
                    json_nextEmail = {'email':result_Email['messageText']['emailUser'],'url_sign':k['urlSign'],'tracking':dataJson['tracking'],'name_file':dataJson['name_file'],'message':'','step_num':k['stepNum']}
                    result_sendMailAuto = mail().send_email_next(json_nextEmail,value_sid)
                    if result_sendMailAuto['result'] == 'OK':
                        logmail_list.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                    else:
                        logmail_list.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                else:
                    json_nextEmail = {'email':k['email_User'],'url_sign':k['urlSign'],'tracking':dataJson['tracking'],'name_file':dataJson['name_file'],'message':'','step_num':k['stepNum']}
                    result_sendMailAuto = mail().send_email_next(json_nextEmail,value_sid)
                    if result_sendMailAuto['result'] == 'OK':
                        logmail_list.append({'result':'OK','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
                    else:
                        logmail_list.append({'result':'ER','email':(k['email_User']),'sid':dataJson['sid'],'transactionCode':k['transactionCode'],'stepNum':k['stepNum']})
            # print(logmail_list, ' logmail_list')
            if len(logmail_list) != 0:
                result_updateEmail = update().update_SendToMail_(logmail_list)
                print(result_updateEmail)
            else:
                res_select = select().select_ForWebHook(value_sid)
                
                res_select['messageText']['PDF_String'] = None
                # print(res_select, ' res_select')
                arr_step = []
                result_Array = sorted(result_Array, key=lambda k: k['stepNum'], reverse=False)
                for count in range(len(result_Array)):
                    count_res = count + 1
                    try:
                        email_User = result_Array[count]['emailUser']
                        statusSign = result_Array[count]['statusSign']
                        datetime_string = result_Array[count]['datetime_string']
                        if result_Array[count]['stepNum'] not in arr_step:
                            arr_step.append(result_Array[count]['stepNum'])
                    except Exception as ex:
                        email_User = ''
                        statusSign = ''
                msg_toChat = ''
                print(result_Array)
                
                for n in arr_step:
                    msg_toChat += '<br>ลำดับที่ ' + str(n)
                    for count in range(len(result_Array)):
                        try:
                            email_User = result_Array[count]['emailUser']
                            statusSign = result_Array[count]['statusSign']
                            if statusSign == 'Complete':
                                statusSign = 'เซ็นแล้ว'
                            else:
                                statusSign = 'ยังไม่เซ็น'
                            datetime_string = result_Array[count]['datetime_string']
                        except Exception as ex:
                            email_User = ''
                            statusSign = ''
                        if result_Array[count]['stepNum'] == n:
                            msg_toChat += '<br>- ' + email_User +'  ' + statusSign + ''
                if res_select['result'] == 'OK':
                    print(msg_toChat)
                    # print(res_select['messageText'])
                    try:
                        email_list = eval(res_select['messageText']['email_center'])
                    except Exception as e:
                        email_list = (res_select['messageText']['email_center'])
                    print(email_list)
                    if type(email_list) is list:
                        for zemail in range(len(email_list)):
                            email_center_01 = email_list[zemail]['email']
                            attemp_file = email_list[zemail]['attemp_file']
                            file_pdf = email_list[zemail]['file_pdf']
                            result_email_center = mail().send_emailSend_emailcenter_list(email_center_01,value_sid,msg_toChat,attemp_file,file_pdf)
                    else:
                        print(res_select['messageText']['email_center'])
                        result_email_center = mail().send_emailSend_emailcenter(res_select['messageText']['email_center'],value_sid,msg_toChat)
                        print(result_email_center)
                    # email_center_01 = email_list['email']
                    
                    result_Email = mail().check_EmailProfile(res_select['messageText']['emailSender'])
                    if result_Email['result'] == 'OK':
                        emailsender = result_Email['messageText']['emailUser']
                        resultSenderMail = mail().send_emailSender(emailsender,value_sid,msg_toChat)
                        if resultSenderMail['result'] == 'OK':
                            return ({'result':'OK','messageText':'sender mail ok ' + emailsender,'status_Code':200,'messageER':None})
                        else:
                            return ({'result':'OK','messageText':'sender mail fail ' + emailsender,'status_Code':200,'messageER':None})
                    else:
                        emailsender = res_select['messageText']['emailSender']
                        resultSenderMail = mail().send_emailSender(emailsender,value_sid,msg_toChat)
                        if resultSenderMail['result'] == 'OK':
                            return ({'result':'OK','messageText':'sender mail ok ' + emailsender,'status_Code':200,'messageER':None})
                        else:
                            return ({'result':'OK','messageText':'sender mail fail ' + emailsender,'status_Code':200,'messageER':None})
            return ({'result':'OK','messageText':None,'status_Code':200,'messageER':None})

def send_Mail_for_service_v2(sidcode):
    sidcode = sidcode
    try:
        # sidcode = dataJson['sid_code']
        result_message = select_4().select_chat_sender_v1(sidcode)
        tmp_u = 0
        tmp_statusEmail = False
        if result_message['result'] == 'OK':
            tmp_messageText = result_message['data']
            tmp_tracking = tmp_messageText['tracking_id']
            tmp_name_file = tmp_messageText['filename']
            tmp_document_id = tmp_messageText['document_id']
            tmp_data = result_message['messageText']
            for u in range(len(tmp_data)):
                tmp_status_ppl = tmp_data[u]['status_ppl']
                tmp_email = tmp_data[u]['email']
                if 'Reject' in tmp_status_ppl:
                    tmp_get_message = result_message['data']
                    tmp_document_id = tmp_get_message['document_id']
                    tmp_sender_email = tmp_get_message['sender_email']
                    tmp_sender_name = tmp_get_message['sender_name']
                    email_sender = mail().check_EmailProfile(tmp_sender_email)
                    tmp_statusEmail = email_sender['messageText']['statusEmail'] 
                    if email_sender['result'] == 'OK':
                        tmp_sender_email = email_sender['messageText']['emailUser']
                    if tmp_statusEmail == True:
                        result_message_text = select().select_mail_sender_v1_text(sidcode,tmp_document_id)
                        tmpmessage = result_message_text['messageText']
                        result_sendemail_sender = mail().send_emailSender(tmp_sender_email,sidcode,tmpmessage)
                    return jsonify({'result':'OK','messageText':{'message':'document reject','data':None},'messageER':None,'status_Code':200}),200
                elif 'Complete' in tmp_status_ppl or 'Approve' in tmp_status_ppl:
                    tmp_u = u + 1
                    print(tmp_u,len(tmp_data))
                    if tmp_u == len(tmp_data):
                        tmp_statusEmail = False
                        document_type = tmp_document_id.split('-')[0]
                        result_message_text = select().select_mail_sender_v1_text(sidcode,tmp_document_id)
                        tmpmessage = result_message_text['messageText']
                        res_select = select().select_ForWebHook(sidcode)
                        if 'messageText' in res_select:
                            if 'PDF_String' in res_select['messageText']:
                                res_select['messageText']['PDF_String'] = None
                        try:
                            email_list = eval(res_select['messageText']['email_center'])
                        except Exception as e:
                            email_list = (res_select['messageText']['email_center'])
                        if type(email_list) is list:
                            s_email = []
                            for zemail in range(len(email_list)):
                                email_center_01 = email_list[zemail]['email']
                                attemp_file = email_list[zemail]['attemp_file']
                                file_pdf = email_list[zemail]['file_pdf']
                                s_email.append(email_center_01)
                            result_email_center = mail().send_emailSend_emailcenter_list_v2([sidcode],email_list,document_type)
                        else:
                            result_email_center = mail().send_emailSend_emailcenter(res_select['messageText']['email_center'],sidcode,tmpmessage)
                            tmp_get_message = result_message['data']
                            tmp_document_id = tmp_get_message['document_id']
                            tmp_sender_email = tmp_get_message['sender_email']
                            tmp_sender_name = tmp_get_message['sender_name']
                            email_sender = mail().check_EmailProfile(tmp_sender_email)
                            tmp_statusEmail = email_sender['messageText']['statusEmail']
                            if email_sender['result'] == 'OK':
                                tmp_sender_email = email_sender['messageText']['emailUser']
                            if tmp_statusEmail == True:
                                tmpmessage = result_message_text['messageText']
                                result_sendemail_sender = mail().send_emailSender(tmp_sender_email,sidcode,tmpmessage)
                    # return jsonify({'result':'OK','messageText':{'message':'document succuess','data':None},'messageER':None,'status_Code':200}),200
                else:
                    tmp_statusEmail = False
                    tmp_url = None
                    for z in range(len(tmp_email)):
                        result_Url = select().select_geturl(tmp_email[z],sidcode)
                        if result_Url['result'] == 'OK':
                            tmp_url = result_Url['messageText']
                        email_profile = mail().check_EmailProfile(tmp_email[z])
                        tmp_statusEmail = email_profile['messageText']['statusEmail'] 
                        if email_profile['result'] == 'OK':
                            tmp_messageText = email_profile['messageText']
                            tmp_email[z] = tmp_messageText['emailUser']
                        if tmp_statusEmail == True:
                            result_mailStatus = mail().send_email_v2(tmp_email[z],tmp_tracking,tmp_name_file,'',tmp_url, sidcode)
                            if result_mailStatus['result'] == 'OK':
                                print(result_mailStatus)
                    result_message_text = select().select_mail_sender_v1_text(sidcode,tmp_document_id)
                    tmp_get_message = result_message['data']
                    tmp_document_id = tmp_get_message['document_id']
                    tmp_sender_email = tmp_get_message['sender_email']
                    tmp_sender_name = tmp_get_message['sender_name']
                    email_sender = mail().check_EmailProfile(tmp_sender_email)
                    tmp_statusEmail = email_sender['messageText']['statusEmail'] 
                    if email_sender['result'] == 'OK':
                        tmp_sender_email = email_sender['messageText']['emailUser']
                    if tmp_statusEmail == True:                                
                        result_message_text = select().select_mail_sender_v1_text(sidcode,tmp_document_id)
                        tmpmessage = result_message_text['messageText']
                        result_sendemail_sender = mail().send_emailSender(tmp_sender_email,sidcode,tmpmessage)
                    return jsonify({'result':'OK','messageText':{'message':'send email succuess','data':None},'messageER':None,'status_Code':200}),200                    
        return jsonify({'result':'OK','messageText':{'message':'send email succuess','data':None},'messageER':None,'status_Code':200}),200
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        logger.info(e)
