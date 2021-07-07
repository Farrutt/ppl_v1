#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from db.db_Class import *
from config.value import *
from method.access import *
from method.hashpy import *
from method.other import *
from config.lib import *
from db.db_method_1 import *
from method.cal_users import *
from method.callserver import *
from method.cal_step import *

def sum_biz_info_group(list_biz_group):
    list_tax_id = []
    tmpresult = []
    list_result = []
    try:
        # print ('list_biz_group:',list_biz_group)
        for i in range(len(list_biz_group)):
            tax_id = (list_biz_group[i]['tax_id'])
            role_name = (list_biz_group[i]['role_name'])
            dept_name = (list_biz_group[i]['dept_name'])
            role_level = (list_biz_group[i]['role_level'])
            first_name_eng = (list_biz_group[i]['first_name_eng'])
            first_name_th = (list_biz_group[i]['first_name_th'])
            
            list_tax_id.append(tax_id)

        count_tax_id = Counter(list_tax_id)
        # print ('count_doc_name:',count_tax_id)
        for x,y in count_tax_id.items():
            json = {}
            json['tax_id'] = x
            json['count'] = y
            tmpresult.append(json)
        # print ('tmpresult:',tmpresult)
        for j in range(len(tmpresult)):
            dict_sum = tmpresult[j]
            count_biz = tmpresult[j]['count']
            tax_id_count = tmpresult[j]['tax_id']
            for k in range(len(list_biz_group)):
                tax_id_biz = list_biz_group[k]['tax_id']
                if tax_id_biz == tax_id_count:
                    dict_sum.update(list_biz_group[k])
        # print ('list_result:',tmpresult)
        return {'result':'OK','messageText':tmpresult}
    except Exception as e:
        print(str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageText':str(e)}


def sum_doc_name_group_v2(list_doctype_group):
    list_document_type = []
    tmpresult = []
    try:
        # print('list_doctype_group',list_doctype_group)
        # print(type(list_doctype_group))
        # list_doctype_group = eval(list_doctype_group)
        if type(list_doctype_group) != list :
            list_doctype_group = eval(str(list_doctype_group))
        

        for x in range(len(list_doctype_group)):
            list_doctype_group[x]['count'] = 0

        arr_tmp = []
        for y in range(len(list_doctype_group)):
            tmp = {}
            tmp['document_type'] = list_doctype_group[y]['document_type']
            if 'id_card_num' in str(list_doctype_group):
                tmp['id_card_num'] = list_doctype_group[y]['id_card_num']
            else:
                tmp['id_card_num'] = ''
            if 'document_json' in str(list_doctype_group):
                tmp['document_json'] = list_doctype_group[y]['document_json']
            else:
                tmp['document_json'] = ''
            if 'first_name_th' in str(list_doctype_group):
                tmp['first_name_th'] = list_doctype_group[y]['first_name_th']
            else:
                tmp['first_name_th'] = ''
            tmp['count'] = list_doctype_group[y]['count']
            tmp['key'] = str(tmp['document_type'])+str(tmp['id_card_num'])
            # print(tmp['document_type'],tmp['id_card_num'])
            if tmp['key'] in str(arr_tmp):
                for i in range(len(arr_tmp)):
                    # print(tmp['document_type'],arr_tmp[i]['document_type'])
                    if tmp['document_type'] == arr_tmp[i]['document_type'] and tmp['id_card_num'] == arr_tmp[i]['id_card_num']:
                        # print(tmp['count'])
                        arr_tmp[i]['count'] += 1
            else:
                # print('else')
                tmp['count'] += 1
                arr_tmp.append(tmp)
        return {'result':'OK','messageText':arr_tmp}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {'result':'ER','messageText':str(e)}


def checkDatetime(date_string):
    try:
        date_format = '%Y-%m-%d'
        date_obj = datetime.datetime.strptime(date_string, date_format)
        print(date_obj)
        return True,date_obj
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD")
        return False,''

class insert_2():
    def insert_pdf_togroup_version2(self,group_id,pdf_data):
        self.group_id = group_id
        self.pdf_data = pdf_data
        try:
            tmp_query = tb_group_document_2.query.filter(tb_group_document_2.id==self.group_id,tb_group_document_2.status=='ACTIVE').first()
            if tmp_query != None:
                tmp_query.pdf_org = str(self.pdf_data)             
                db.session.commit()
                return {'result':'OK','messageText':None}
            else:
                return {'result':'ER','messageText':'data not found'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    # v4 ตัด document_type ออก
    def insert_template_group_v4(self,group_name,group_code,template,group_title,step_group,group_data,biz_info,create_by,update_by,use_status,cover_page,group_color,email_middle,timegroup,daygroup_auto,email_step,status_doing_auto):
        self.group_name = group_name
        self.group_code = group_code
        self.template = str(template)
        self.group_title = group_title
        self.step_group = step_group
        self.group_data = group_data
        self.biz_info = biz_info
        self.create_by = create_by
        self.update_by = update_by
        self.use_status = use_status
        self.cover_page = cover_page
        self.status_doing_auto = status_doing_auto
        self.group_color = None
        self.email_middle = None
        self.timegroup = None
        self.daygroup_auto = None
        if email_step != None:
            self.email_step = str(email_step)
        if timegroup != None:
            self.timegroup = str(timegroup)
        if daygroup_auto != None:
            self.daygroup_auto = str(daygroup_auto)
        if email_middle != None:
            self.email_middle = str(email_middle)
        if group_color != None:
            self.group_color = str(group_color).replace(' ','').lower()
            self.group_color = str([{'color':self.group_color}])            
        try:
            tid = str(uuid.uuid4())
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            check_biz = False
            check_code = False
            check_type = False
            biz_num = None

            if self.biz_info != '' and self.biz_info != None:
                if 'id_card_num' in self.biz_info:
                    eval_biz = eval(self.biz_info)
                    if type(eval_biz) == dict:
                        biz_num = eval_biz['id_card_num']
                    elif type(eval_biz) == list:
                        biz_num = eval_biz[0]['id_card_num']
                else:
                    return {'result':'ER','messageText':'This data already exists'}
                search_biz_result = db.session.query(tb_group_template_2).filter(tb_group_template_2.biz_info.contains(biz_num)).all()
                # print
                if search_biz_result != []:
                    check_biz = True
            
                if check_biz == False : # ไม่มี id_card_num
                    insert_result = tb_group_template_2(group_name=self.group_name,group_code=self.group_code,template=self.template,group_title=self.group_title,step_group=self.step_group,status='ACTIVE',create_date=str(st),update_date=str(st),group_data=self.group_data,biz_info=self.biz_info,create_by=self.create_by,update_by=self.update_by,use_status=self.use_status,cover_page=self.cover_page,tid=tid,group_color=self.group_color,email_middle=self.email_middle,timegroup_auto=self.timegroup,daygroup_auto=self.daygroup_auto,email_step=self.email_step,status_doing_auto=self.status_doing_auto)
                    db.session.add(insert_result)
                    db.session.flush()
                    db.session.commit()
                elif check_biz == True : # มี id_card_num อยู่แล้ว
                    for i in range(len(search_biz_result)):
                        tmp_query = search_biz_result[i].__dict__
                    
                        if '_sa_instance_state' in tmp_query:
                            del tmp_query['_sa_instance_state']

                        if tmp_query['group_code'] == self.group_code:
                            check_code = True

                            # if tmp_query['document_type'] == self.document_type:
                            #     check_type = True
                    if check_code == True : # มี group_code
                        return {'result':'ER','messageText':'This data already exists'}
                    elif check_code == False : # ไม่มี group_code
                        insert_result = tb_group_template_2(group_name=self.group_name,group_code=self.group_code,template=self.template,group_title=self.group_title,step_group=self.step_group,status='ACTIVE',create_date=str(st),update_date=str(st)\
                            ,group_data=self.group_data,biz_info=self.biz_info,create_by=self.create_by,update_by=self.update_by,use_status=self.use_status,cover_page=self.cover_page,tid=tid,group_color=self.group_color,email_middle=self.email_middle,timegroup_auto=self.timegroup,daygroup_auto=self.daygroup_auto,email_step=self.email_step,status_doing_auto=self.status_doing_auto)
                        
                        db.session.add(insert_result)
                        db.session.flush()
                        db.session.commit()
                        

                    # elif check_code == True and check_type == False: # มี group_code ไม่มี document_type 
                        
                    #     insert_result = tb_group_template(group_name=self.group_name,group_code=self.group_code,template=self.template,document_type=self.document_type,group_title=self.group_title,step_group=self.step_group,status='ACTIVE',create_date=str(st),update_date=str(st)\
                    #         ,group_data=self.group_data,biz_info=self.biz_info,create_by=self.create_by,update_by=self.update_by,use_status=self.use_status,cover_page=self.cover_page,tid=tid,group_color=self.group_color,email_middle=self.email_middle,timegroup_auto=self.timegroup,daygroup_auto=self.daygroup_auto)
                        
                    #     db.session.add(insert_result)
                    #     db.session.flush()
                    #     db.session.commit()
                        

                    # elif check_code == False and check_type == False: # ไม่มี group_code ไม่มี document_type 
                        
                    #     insert_result = tb_group_template(group_name=self.group_name,group_code=self.group_code,template=self.template,document_type=self.document_type,group_title=self.group_title,step_group=self.step_group,status='ACTIVE',create_date=str(st),update_date=str(st)\
                    #         ,group_data=self.group_data,biz_info=self.biz_info,create_by=self.create_by,update_by=self.update_by,use_status=self.use_status,cover_page=self.cover_page,tid=tid,group_color=self.group_color,email_middle=self.email_middle,timegroup_auto=self.timegroup,daygroup_auto=self.daygroup_auto)
                        
                    #     db.session.add(insert_result)
                    #     db.session.flush()
                    #     db.session.commit()
                        
                return {'result':'OK'}

            elif self.biz_info == '' or self.biz_info == None:              
                
                search_biz_result = db.session.query(tb_group_template_2).filter(tb_group_template_2.biz_info == '').all()

                if search_biz_result != []:
                    check_biz = True
            
                if check_biz == False : # ไม่มี id_card_num
                    insert_result = tb_group_template_2(group_name=self.group_name,group_code=self.group_code,template=self.template,group_title=self.group_title,step_group=self.step_group,status='ACTIVE',create_date=str(st),update_date=str(st)\
                        ,group_data=self.group_data,biz_info=self.biz_info,create_by=self.create_by,update_by=self.update_by,use_status=self.use_status,cover_page=self.cover_page,tid=tid,group_color=self.group_color,email_middle=self.email_middle,timegroup_auto=self.timegroup,daygroup_auto=self.daygroup_auto,email_step=self.email_step,status_doing_auto=self.status_doing_auto)
                    db.session.add(insert_result)
                    db.session.flush()
                    db.session.commit()

                    

                elif check_biz == True : # มี id_card_num อยู่แล้ว
                    for i in range(len(search_biz_result)):
                        tmp_query = search_biz_result[i].__dict__
                    
                        if '_sa_instance_state' in tmp_query:
                            del tmp_query['_sa_instance_state']

                        if tmp_query['group_code'] == self.group_code:
                            check_code = True

                            # if tmp_query['document_type'] == self.document_type:
                            #     check_type = True


                    if check_code == True: # มี group_code
                        return {'result':'ER','messageText':'This data already exists'}

                    elif check_code == False: # ไม่มี group_code
                        insert_result = tb_group_template_2(group_name=self.group_name,group_code=self.group_code,template=self.template,group_title=self.group_title,step_group=self.step_group,status='ACTIVE',create_date=str(st),update_date=str(st),group_data=self.group_data,biz_info=self.biz_info,create_by=self.create_by,update_by=self.update_by,use_status=self.use_status,cover_page=self.cover_page,tid=tid,group_color=self.group_color,email_middle=self.email_middle,timegroup_auto=self.timegroup,daygroup_auto=self.daygroup_auto,email_step=self.email_step,status_doing_auto=self.status_doing_auto)
                        db.session.add(insert_result)
                        db.session.flush()
                        db.session.commit()
                        

                    # elif check_code == True and check_type == False: # มี group_code ไม่มี document_type 
                    #     insert_result = tb_group_template(group_name=self.group_name,group_code=self.group_code,template=self.template,document_type=self.document_type,group_title=self.group_title,step_group=self.step_group,status='ACTIVE',create_date=str(st),update_date=str(st),group_data=self.group_data,biz_info=self.biz_info,create_by=self.create_by,update_by=self.update_by,use_status=self.use_status,cover_page=self.cover_page,tid=tid,group_color=self.group_color,email_middle=self.email_middle,timegroup_auto=self.timegroup,daygroup_auto=self.daygroup_auto)
                    #     db.session.add(insert_result)
                    #     db.session.flush()
                    #     db.session.commit()
                        

                    # elif check_code == False and check_type == False: # ไม่มี group_code ไม่มี document_type 
                    #     insert_result = tb_group_template(group_name=self.group_name,group_code=self.group_code,template=self.template,document_type=self.document_type,group_title=self.group_title,step_group=self.step_group,status='ACTIVE',create_date=str(st),update_date=str(st),group_data=self.group_data,biz_info=self.biz_info,create_by=self.create_by,update_by=self.update_by,use_status=self.use_status,cover_page=self.cover_page,tid=tid,group_color=self.group_color,email_middle=self.email_middle,timegroup_auto=self.timegroup,daygroup_auto=self.daygroup_auto)
                    #     db.session.add(insert_result)
                    #     db.session.flush()
                    #     db.session.commit()
                        

                return {'result':'OK'}

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}


    def secret_key_bi(self,service_name,private_key,sevice_id):
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.service_name = service_name
        self.private_key = private_key
        self.sevice_id = sevice_id
        try:
            with engine.connect() as connection:
                result_insert = connection.execute('INSERT INTO tb_connex ("serviceName", "public", "private", "code", "create_date" ) VALUES (%s,%s,%s,%s,%s) RETURNING "id"',self.service_name,None,self.private_key,self.sevice_id,str(st))
                for row in result_insert:
                    id = dict(row) 
                connection.close()
            if result_insert != None:
                return {'result':'OK','messageText':id}
            else:
                return {'result':'ER','messageText':'fail'}

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    # def insert_draft_v3_sql(self,data_json,data_json_Upload,biz_info,qrCode_position,recipient_email,string_pdf,documentJson,options_page,documentType,sender_email,template,type_file,folder_name,email_center,step_code,attempted_name,attach_data,importance,last_digitsign,time_expire):
    #     self.data_json = data_json
    #     self.data_json_Upload = data_json_Upload
    #     self.biz_info = biz_info
    #     self.qrCode_position = qrCode_position
    #     self.recipient_email = recipient_email
    #     self.string_pdf = string_pdf
    #     self.documentJson = documentJson
    #     self.options_page = options_page
    #     self.documentType = documentType
    #     self.sender_email = sender_email
    #     self.template = template
    #     self.type_file = type_file
    #     self.folder_name = folder_name
    #     self.email_center = email_center
    #     self.step_code = step_code
    #     self.attempted_name = attempted_name
    #     self.attach_data = attach_data
    #     self.importance = importance
    #     self.last_digitsign = last_digitsign
    #     self.time_expire = time_expire
    #     ts = int(time.time())
    #     st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    #     tid = str(uuid.uuid4())
    #     tmp_step_data = {}
    #     tmp_pdf_detail = {}
    #     try:
    #         if self.time_expire != None :
    #             time_ex_eval = eval(self.time_expire)
    #             day = time_ex_eval[0]
    #             hour = time_ex_eval[1]
    #             self.time_expire = (int(day) * 24) + int(hour)
    #         else:
    #             self.time_expire = 0
    #         with engine.connect() as connection:
    #             insert_pdf =  connection.execute('insert into tb_draft_document ("data_json","data_json_Upload","biz_info","qrCode_position","recipient_email","string_pdf","documentJson","options_page","documentType","status","sender_email","update_time", \
    #             "tid","template","type_file","folder_name","email_center","step_code","attempted_name","attach_data","importance","last_digitsign","time_expire")\
    #             values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) \
    #             returning "tid"',self.data_json,self.data_json_Upload,str(self.biz_info),self.qrCode_position,self.recipient_email,self.string_pdf,self.documentJson,self.options_page,self.documentType,'ACTIVE',self.sender_email,str(st),
    #             tid,str(self.template),self.type_file,self.folder_name,self.email_center,self.step_code,\
    #             self.attempted_name,self.attach_data,self.importance,self.last_digitsign,self.time_expire)
    #             connection.close()
    #         return {'result':'OK','messageText':'insert success'}
    #     except Exception as e:
    #         exc_type, exc_obj, exc_tb = sys.exc_info()
    #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #         print(exc_type, fname, exc_tb.tb_lineno)
    #         return {'result':'ER','messageText':str(e)}

    def insert_draft_v3_sql(self,data_json,data_json_Upload,biz_info,qrCode_position,recipient_email,string_pdf,documentJson,options_page,documentType,sender_email,template,type_file,folder_name,email_center,step_code,attempted_name,attach_data,importance,last_digitsign,time_expire,status_ref,list_ref):
        self.data_json = data_json
        self.data_json_Upload = data_json_Upload
        self.biz_info = biz_info
        self.qrCode_position = qrCode_position
        self.recipient_email = recipient_email
        self.string_pdf = string_pdf
        self.documentJson = documentJson
        self.options_page = options_page
        self.documentType = documentType
        self.sender_email = sender_email
        self.template = template
        self.type_file = type_file
        self.folder_name = folder_name
        self.email_center = email_center
        self.step_code = step_code
        self.attempted_name = attempted_name
        self.attach_data = attach_data
        self.importance = importance
        self.last_digitsign = last_digitsign
        self.time_expire = time_expire
        self.status_ref = status_ref
        self.list_ref = list_ref
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        tid = str(uuid.uuid4())
        tmp_step_data = {}
        tmp_pdf_detail = {}
        try:
            if self.time_expire != None :
                time_ex_eval = eval(self.time_expire)
                day = time_ex_eval[0]
                hour = time_ex_eval[1]
                self.time_expire = (int(day) * 24) + int(hour)
            else:
                self.time_expire = 0
            with engine.connect() as connection:
                insert_pdf =  connection.execute('insert into tb_draft_document ("data_json","data_json_Upload","biz_info","qrCode_position","recipient_email","string_pdf","documentJson","options_page","documentType","status","sender_email","update_time", \
                "tid","template","type_file","folder_name","email_center","step_code","attempted_name","attach_data","importance","last_digitsign","time_expire","status_ref","list_ref")\
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) \
                returning "tid"',self.data_json,self.data_json_Upload,str(self.biz_info),self.qrCode_position,self.recipient_email,self.string_pdf,self.documentJson,self.options_page,self.documentType,'ACTIVE',self.sender_email,str(st),
                tid,str(self.template),self.type_file,self.folder_name,self.email_center,self.step_code,\
                self.attempted_name,self.attach_data,self.importance,self.last_digitsign,self.time_expire,self.status_ref,str(self.list_ref))
                connection.close()
            return {'result':'OK','messageText':'insert success'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}


    def insert_draft_v2(self,data_json,data_json_Upload,biz_info,qrCode_position,recipient_email,string_pdf,documentJson,options_page,documentType,sender_email,template,type_file,folder_name,email_center,step_code,attempted_name,attach_data):
        self.data_json = data_json
        self.data_json_Upload = data_json_Upload
        self.biz_info = biz_info
        self.qrCode_position = qrCode_position
        self.recipient_email = recipient_email
        self.string_pdf = string_pdf
        self.documentJson = documentJson
        self.options_page = options_page
        self.documentType = documentType
        self.sender_email = sender_email
        self.template = template
        self.type_file = type_file
        self.folder_name = folder_name
        self.email_center = email_center
        self.step_code = step_code
        self.attempted_name = attempted_name
        self.attach_data = attach_data
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        tid = str(uuid.uuid4())
        tmp_step_data = {}
        tmp_pdf_detail = {}
        try:
            
            search_tid_inTable = db.session.query(paperless_draft).filter(paperless_draft.tid == tid).filter(paperless_draft.status == 'ACTIVE').all()
            if search_tid_inTable != [] and search_tid_inTable != None and search_tid_inTable != '':
                return {'result':'OK','messageText':'Data already exists'}
            elif search_tid_inTable == []:
                insert_result = paperless_draft(data_json=self.data_json,data_json_Upload=self.data_json_Upload,biz_info=str(self.biz_info),qrCode_position=self.qrCode_position,recipient_email=self.recipient_email,string_pdf=self.string_pdf,documentJson=self.documentJson,options_page=self.options_page,documentType=self.documentType,status='ACTIVE',sender_email=self.sender_email,update_time=str(st),tid=tid,template=str(self.template),type_file=self.type_file,folder_name=self.folder_name,email_center=self.email_center,step_code=self.step_code,attempted_name=self.attempted_name,attach_data=self.attach_data)
                db.session.add(insert_result)
                db.session.flush()
                db.session.commit()
                return {'result':'OK','messageText':'insert success'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def insert_template_group_v2(self,group_name,group_code,template,document_type,group_title,step_group,group_data,biz_info,create_by,update_by,use_status):
        self.group_name = group_name
        self.group_code = group_code
        self.template = template
        self.document_type = document_type
        self.group_title = group_title
        self.step_group = step_group
        self.group_data = group_data
        self.biz_info = biz_info
        self.create_by = create_by
        self.update_by = update_by
        self.use_status = use_status

        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        try:
            insert_result = tb_group_template(group_name=self.group_name,group_code=self.group_code,template=self.template,document_type=self.document_type,group_title=self.group_title,step_group=self.step_group,status='ACTIVE',create_date=str(st),update_date=str(st),group_data=self.group_data,biz_info=self.biz_info,create_by=self.create_by,update_by=self.update_by,use_status=self.use_status)
            db.session.add(insert_result)
            db.session.flush()
            db.session.commit()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def insert_template_group_v3(self,group_name,group_code,template,document_type,group_title,step_group,group_data,biz_info,create_by,update_by,use_status,cover_page,group_color,email_middle,timegroup,daygroup_auto,webhook):
        self.group_name = group_name
        self.group_code = group_code
        self.template = str(template)
        self.document_type = document_type
        self.group_title = group_title
        self.step_group = step_group
        self.group_data = group_data
        self.biz_info = biz_info
        self.create_by = create_by
        self.update_by = update_by
        self.use_status = use_status
        self.cover_page = cover_page
        self.webhook = webhook
        self.group_color = None
        self.email_middle = None
        self.timegroup = None
        self.daygroup_auto = None
        if timegroup != None:
            self.timegroup = str(timegroup)
        if daygroup_auto != None:
            self.daygroup_auto = str(daygroup_auto)
        if email_middle != None:
            self.email_middle = str(email_middle)
        if group_color != None:
            self.group_color = str(group_color).replace(' ','').lower()
            self.group_color = str([{'color':self.group_color}])            
        try:
            tid = str(uuid.uuid4())
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
            check_biz = False
            check_code = False
            check_type = False
            biz_num = None
            if self.biz_info != '' and self.biz_info != None:
                if 'id_card_num' in self.biz_info:
                    eval_biz = eval(self.biz_info)
                    if type(eval_biz) == dict:
                        biz_num = eval_biz['id_card_num']
                    elif type(eval_biz) == list:
                        biz_num = eval_biz[0]['id_card_num']
                else:
                    return {'result':'ER','messageText':'This data already exists'}
                search_taxid = "%{}%".format(biz_num)
                sql = '''
                    SELECT ID 
                    FROM
                        tb_group_template 
                    WHERE
                        biz_info LIKE :tax_id 
                        AND group_code = :group_code
                        AND document_type = :document_type 
                        AND status = :status '''
                with slave.connect() as connection:
                    resultsql = connection.execute(text(sql),tax_id=search_taxid,group_code=self.group_code,document_type=self.document_type,status='ACTIVE')
                connection.close()
                query = [dict(row) for row in resultsql]
                # print(search_taxid,self.group_color,self.document_type)
                if len(query) != 0:
                    return {'result':'ER','messageText':'This data already exists'}
                else:
                    with engine.connect() as connection:
                        resultsql = connection.execute('INSERT INTO tb_group_template (group_name,group_code,template,document_type,group_title,step_group,status,create_date,update_date,group_data,biz_info,create_by,update_by,use_status,\
                        cover_page,tid,group_color,email_middle,timegroup_auto,daygroup_auto,webhook) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);',self.group_name,self.group_code,self.template,self.document_type\
                        ,self.group_title,self.step_group,'ACTIVE',str(st),str(st),self.group_data,self.biz_info,self.create_by,self.update_by,self.use_status,self.cover_page,tid,self.group_color,self.email_middle,self.timegroup,self.daygroup_auto,self.webhook)
                    connection.close()
                return {'result':'OK'}
            elif self.biz_info == '' or self.biz_info == None:
                return {'result':'ER','messageText':'can,t create template'}
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}
        finally:
            connection.close()
            db.session.close()

class update_2():
    def update_pdf_ingroup_verson2(self,group_id,pdf_data,email_thai):
        self.group_id = group_id
        self.pdf_data = pdf_data
        self.email_thai = email_thai
        try:
            tmp_query = tb_group_document_2.query.filter(tb_group_document_2.id==self.group_id,tb_group_document_2.status=='ACTIVE').first()
            if tmp_query != None:
                # tmpstatus_group = tmp_query.status_group
                # if tmpstatus_group != None:
                #     tmpstatus_group = eval(tmpstatus_group)
                # for n in range(len(tmpstatus_group)):
                #     tmpemailOne = tmpstatus_group[n]['email_one']
                #     if self.email_thai in tmpemailOne:
                #         tmpstatus_group[n]['status'] = 'Complete'
                # tmp_query.status_group = str(tmpstatus_group)
                tmp_query.pdf_sign = str(self.pdf_data)
                db.session.commit()
                return {'result':'OK','messageText':None}
            else:                
                return {'result':'ER','messageText':'data not found'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print('error',str(e))
            return {'result':'ER','messageText':str(e)} 

    def update_signature_group_version2(self,group_id,emailone,signbase):
        self.group_id = group_id
        self.emailone = emailone
        self.signbase = signbase
        try:
            tmp_query = tb_group_document_2.query.filter(tb_group_document_2.id==self.group_id,tb_group_document_2.status=='ACTIVE').first()
            if tmp_query != None:
                jsontmp_info = tmp_query.__dict__
                tmp_step_group_detail = jsontmp_info['step_group_detail']
                if tmp_step_group_detail != None:
                    tmp_step_group_detail = eval(tmp_step_group_detail)
                    for z in range(len(tmp_step_group_detail)):
                        if self.emailone in tmp_step_group_detail[z]['email_one']:
                            tmp_step_group_detail[z]['sign_base'] = str(self.signbase)
                            tmp_step_group_detail[z]['email_complete'] = str(self.emailone)
                            tmp_query.step_group_detail = str(tmp_step_group_detail)
                            db.session.commit()
                            return {'result':'OK','messageText':None}
                    return {'result':'ER','messageText':'data not found'}
                else:                
                    return {'result':'ER','messageText':'data not found'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print('error',str(e))
            return {'result':'ER','messageText':str(e)} 

    # no document
    def update_toremove_document_ingroup_version2(self,sidcode,group_id,email_updateby):
        self.sidcode = sidcode
        self.group_id = group_id
        self.email_updateby = email_updateby
        try:
            tmp_query = tb_group_document_2.query.filter(tb_group_document_2.id== self.group_id).first()
            if tmp_query != None:
                tmp_sidgroup = eval(tmp_query.sid_group)
                tmp_data_group = eval(tmp_query.data_group)
                tmp_email_group = eval(tmp_query.email_group)
                tmp_group_data_json = eval(tmp_query.group_data_json)
                tmp_step_group = eval(tmp_query.step_group)
                tmp_doctype_group = eval(tmp_query.doctype_group)
                tmp_bizinfo_group = eval(tmp_query.bizinfo_group)
                tmp_maxstep = eval(tmp_query.maxstep)
                tmp_email_middle = eval(tmp_query.email_middle)
                # result_sum = sum_doc_name_group_v3(eval(tmp_query.doctype_group))
                result_sum = sum_doc_name_group_v2(eval(tmp_query.doctype_group))
                # if len(tmp_group_data) != 0 :
                #     tmp_group_step[0]['email_one'] = tmp_group_data[0]['email_one']
                #     tmp_group_step[0]['name_one'] = tmp_group_data[0]['name_one']
                # หา cover_page
                result_sum01 = result_sum['messageText']
                arr_properties = []
                arr_group_title = []
                arr_taxid = []
                arr_namebiz = []
                print('result_sum01',result_sum01)
                for ii in range(len(result_sum01)):
                    id_card_num = result_sum01[ii]['id_card_num']
                    doctype01 = result_sum01[ii]['document_type']
                    first_name_th = result_sum01[ii]['first_name_th']
                    result = select_2().select_DocumentDetail(id_card_num,doctype01)
                    result01 = result['messageText'][0]
                    print('business_json',result01['business_json'])
                    documentType = result01['documentType']
                    document_name = result01['documentJson']['document_name']
                    # id_card_num = result01['business_json']['id_card_num']
                    # first_name_th = result01['business_json']['first_name_th']
                    header_text = 'ประเภทเอกสาร ' + str(document_name)
                    service_other = result01['service_other']
                    for y in range(len(service_other)):
                        if service_other[y]['name_service'] == 'GROUP2':
                            other = service_other[y]['other']
                            arr_header = []
                            arr_coverpage = []
                            for i in range(len(other)):
                                properties = other[i]['properties']
                                for x in range(len(properties)):
                                    properties[x] = eval(str(properties[x]))
                                    if 'sum_display' not in str(properties[x]):
                                        properties[x]['sum_display'] = False
                                    tmp_header_column = {
                                        'display_key': properties[x]['display'],
                                        'display_status': properties[x]['sum_display']
                                    }
                                    arr_header.append(tmp_header_column)
                                    if properties[x]['sum_display'] == True and properties[x]['type'] == 'Number':
                                        arr_coverpage.append(tmp_header_column)
                            #         arr_taxid.append(id_card_num)
                            #         arr_namebiz.append(first_name_th)
                            # count_arr_taxid = Counter(arr_taxid)
                            # count_arr_namebiz = Counter(arr_namebiz)
                            # arr_taxid = []
                            # arr_namebiz = []
                            # for x,y in count_arr_taxid.items():
                            #     arr_taxid.append(x)
                            # for x,y in count_arr_namebiz.items():
                            #     arr_namebiz.append(x)
                            tmp_group_title = {
                                'cover_name': '',
                                'cover_column': arr_header,
                                'document_type': documentType,
                                'name_bizinfo': first_name_th,
                                'tax_id': id_card_num
                            }                                          
                            tmp = {
                                'header_column': arr_coverpage,
                                'header_text': header_text,
                                'body_column': '',
                                'body_sign': '',
                                'document_type': documentType,
                                'name_bizinfo': first_name_th,
                                'tax_id': id_card_num
                            }
                            arr_properties.append(tmp)
                            arr_group_title.append(tmp_group_title)
                    # print('arr_properties',arr_properties)
                tmpcover_page = str(arr_properties)
                tmp_group_title = str(arr_group_title)
                if result_sum['result'] == 'ER':
                    result_sum['messageText'] = []
                for z in range(len(self.sidcode)):
                    tmp_sidcode = self.sidcode[z]
                    index_yu = tmp_sidgroup.index(tmp_sidcode)
                    tmp_data_group.pop(index_yu)
                    tmp_email_group.pop(index_yu)
                    tmp_step_group.pop(index_yu)
                    tmp_doctype_group.pop(index_yu)
                    tmp_bizinfo_group.pop(index_yu)
                    tmp_maxstep.pop(index_yu)
                    tmp_email_middle.pop(index_yu)
                    if 'data_sum' in tmp_group_data_json[0]:
                        tmp_group_data_json.pop(index_yu)
                    else:
                        tmp_group_data_json.pop(index_yu)
                    tmp_sidgroup.remove(tmp_sidcode)
                tmp_query.sid_group = str(tmp_sidgroup)
                tmp_query.data_group = str(tmp_data_group)                
                tmp_query.email_group = str(tmp_email_group)
                tmp_query.group_data_json = str(tmp_group_data_json)
                tmp_query.step_group = str(tmp_step_group)
                tmp_query.doctype_group = str(tmp_doctype_group)
                tmp_query.bizinfo_group = str(tmp_bizinfo_group)
                tmp_query.maxstep = str(tmp_maxstep)
                tmp_query.cover_page = str(tmpcover_page)
                tmp_query.group_title = str(tmp_group_title)
                tmp_query.update_by = self.email_updateby
                tmp_query.email_middle = str(tmp_email_middle)                        
                db.session.commit()
                tmp_db = paper_lesssender.query.filter(paper_lesssender.step_data_sid.in_(self.sidcode)).all()
                for u in range(len(tmp_db)):
                    tmp_groupid = eval(tmp_db[u].group_id)
                    tmp_groupid.remove(self.group_id)
                    tmp_db[u].group_id = str(tmp_groupid)
                    db.session.commit()
            return {'result':'OK','messageText':'success','tmpsid':tmp_sidgroup}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print('error',str(e))
            return {'result':'ER','messageText':str(e)}

    def update_status_ingroup_v1(self,group_id,email_thai):
        self.group_id = group_id
        self.email_thai = email_thai
        tmpstatus = "N"
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        tmpcreatetime = None
        tmpupdatetime = None
        try:
            sql = '''
                SELECT "status_group","updatetime","createtime" FROM "tb_group_document" where id =:tmpgroup_id;
            '''
            connection = engine.connect()
            result = connection.execute(text(sql),tmpgroup_id=self.group_id)
            data = [dict(row) for row in result]
            if len(data) != 0:
                tmpstatus_group = data[0]['status_group']
                tmpupdatetime = data[0]['updatetime']
                tmpcreatetime = data[0]['createtime']
                if tmpstatus_group != None:
                    tmpstatus_group = eval(tmpstatus_group)
                for n in range(len(tmpstatus_group)):
                    tmpemailOne = tmpstatus_group[n]['email_one']
                    if self.email_thai in tmpemailOne:
                        tmpstatus_group[n]['status'] = 'Complete'
                r_status = cal_status_group_v1(tmpstatus_group)
                if r_status['result'] == 'OK':
                    tmpstatus = r_status['messageText']
            if tmpcreatetime == None:
                sql_update = '''
                    UPDATE "tb_group_document" SET "status_group"=:tmpstatus_group,"group_status"=:tmpgroup_status,"updatetime"=:updatetimetmp,"createtime"=:strtimetmp WHERE id=:tmpgroup_id 
                '''
                connection.execute(text(sql_update),tmpstatus_group=str(tmpstatus_group),tmpgroup_status=str(tmpstatus),updatetimetmp=str(st),strtimetmp=str(tmpupdatetime),tmpgroup_id=self.group_id)
            else:                
                sql_update = '''
                    UPDATE "tb_group_document" SET "status_group"=:tmpstatus_group,"group_status"=:tmpgroup_status,"updatetime"=:updatetimetmp WHERE id=:tmpgroup_id 
                '''
                connection.execute(text(sql_update),tmpstatus_group=str(tmpstatus_group),tmpgroup_status=str(tmpstatus),updatetimetmp=str(st),tmpgroup_id=self.group_id)
            connection.close()
            # tmp_query = tb_group_document.query.filter(tb_group_document.id==self.group_id,tb_group_document.status=='ACTIVE').first()
            # if tmp_query != None:
            #     tmpstatus_group = tmp_query.status_group
            #     if tmpstatus_group != None:
            #         tmpstatus_group = eval(tmpstatus_group)
            #     for n in range(len(tmpstatus_group)):
            #         tmpemailOne = tmpstatus_group[n]['email_one']
            #         if self.email_thai in tmpemailOne:
            #             tmpstatus_group[n]['status'] = 'Complete'
            #     r_status = cal_status_group_v1(tmpstatus_group)
            #     tmpstatus = "N"
            #     if r_status['result'] == 'OK':
            #         tmpstatus = r_status['messageText']
            #     tmp_query.status_group = str(tmpstatus_group)
            #     tmp_query.group_status = str(tmpstatus)
            #     db.session.commit()
            return {'result':'OK','messageText':None}
            # else:                
            #     return {'result':'ER','messageText':'data not found'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print('error',str(e))
            return {'result':'ER','messageText':str(e)} 
        finally:
            connection.close()
            
    # no document_type
    def update_status_ingroup_v2(self,group_id,email_thai):
        self.group_id = group_id
        self.email_thai = email_thai
        try:
            tmp_query = tb_group_document_2.query.filter(tb_group_document_2.id==self.group_id,tb_group_document_2.status=='ACTIVE').first()
            if tmp_query != None:
                tmpstatus_group = tmp_query.status_group
                if tmpstatus_group != None:
                    tmpstatus_group = eval(tmpstatus_group)
                for n in range(len(tmpstatus_group)):
                    tmpemailOne = tmpstatus_group[n]['email_one']
                    if self.email_thai in tmpemailOne:
                        tmpstatus_group[n]['status'] = 'Complete'
                r_status = cal_status_group_v1(tmpstatus_group)
                tmpstatus = "N"
                if r_status['result'] == 'OK':
                    tmpstatus = r_status['messageText']
                tmp_query.status_group = str(tmpstatus_group)
                tmp_query.group_status = str(tmpstatus)
                db.session.commit()
                return {'result':'OK','messageText':None}
            else:                
                return {'result':'ER','messageText':'data not found'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print('error',str(e))
            return {'result':'ER','messageText':str(e)} 

    def update_attemp_name_doc(self,folder_name,sid):
        self.folder_name = folder_name
        self.sid = sid
        try:
            with engine.connect() as connection:
                result_insert = connection.execute('UPDATE "tb_doc_detail" SET "attempted_folder"=%s WHERE "step_id"=%s',self.folder_name,self.sid)
                connection.close()
            print ('update_success')
            return {'result':'OK','messageText':'update_success'}
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

    # ตัด document_type ออก
    def update_status_save_onebox(self,folder_name):
        self.folder_name = folder_name
        try:
            with engine.connect() as connection:
                result_insert = connection.execute('UPDATE "tb_transactionfile" SET "status_save_onebox"=true WHERE "folder_name"=%s',self.folder_name)
                connection.close()
            print ('update_success')
            return {'result':'OK','messageText':'update_success'}
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':'Fail!','status_Code':200,'service':'oneid'}

    def delete_template_group_v3(self,id_data,username):
        self.id = id_data
        self.username = username
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        try:
            tmp_query = tb_group_template_2.query.filter(tb_group_template_2.tid==self.id,tb_group_template_2.status=='ACTIVE').first()
            if tmp_query != None:                
                tmp_query.status = 'REJECT'
                tmp_query.update_date = str(st)
                tmp_query.update_by = self.username
                db.session.commit()
                return {'result':'OK'}
            
            else:                
                return {'result':'ER'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def use_status_template_group_v4(self,id_data,use_status,username):
        self.id = id_data
        self.use_status = use_status
        self.username = username
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        try:
            tmp_query = tb_group_template_2.query.filter(tb_group_template_2.id==self.id).first()
            if tmp_query != None:
                tmp_query.use_status = self.use_status
                tmp_query.update_date = str(st)
                tmp_query.update_by = self.username
                db.session.commit()
                return {'result':'OK'}
            
            else:                
                return {'result':'ER'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}


    def update_template_group_v7(self,id_data,group_name=None,group_code=None,template=None,group_title=None,step_group=None,group_data=None,biz_info=None,update_by=None,use_status=None,cover_page=None,group_color=None,email_middle=None,timegroup=None,daygroup=None,email_step=None,status_doing_auto=None):
        self.id = id_data
        self.group_name = group_name
        self.group_code = group_code
        self.template = template
        self.group_title = group_title
        self.step_group = step_group
        self.group_data = group_data
        self.biz_info = biz_info
        self.update_by = update_by
        self.use_status = use_status
        self.cover_page = cover_page
        self.group_color = group_color
        self.timegroup = timegroup
        self.daygroup = daygroup
        self.email_middle = email_middle
        self.status_doing_auto = status_doing_auto
        if email_step != None:
            self.email_step = str(email_step)
        if timegroup != None:
            self.timegroup = str(timegroup)
        if email_middle != None:
            self.email_middle = str(email_middle)
        if daygroup != None:
            self.daygroup = str(daygroup)
        if group_color != None:
            self.group_color = str(group_color).replace(' ','').lower()
            self.group_color = str([{'color':self.group_color}])

        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        check_code = False
        check_type = False
        check_update = False
        check_biz = False
        check_biz_in = False
        check_have = False
        try:
            tmp_query = tb_group_template_2.query.filter(tb_group_template_2.tid==self.id).filter(tb_group_template_2.status!='REJECT').first()
            group_code_db = tmp_query.group_code
            eval_biz_db = eval(tmp_query.biz_info)
            
            if type(eval_biz_db) == list:
                id_card_num_db = (eval(tmp_query.biz_info))[0]['id_card_num']
            elif type(eval_biz_db) == dict:
                id_card_num_db = (eval(tmp_query.biz_info))['id_card_num']
            if self.biz_info != '' and self.biz_info != None:
                if 'id_card_num' in self.biz_info:
                    eval_biz_self = eval(self.biz_info)
                    if type(eval_biz_self) == dict:
                        biz_num_self = eval_biz_self['id_card_num']
                    elif type(eval_biz_self) == list:
                        biz_num_self = eval_biz_self[0]['id_card_num']
                else:
                    return {'result':'ER','messageText':'This data already exists'}
                if group_code_db == self.group_code or document_type_db == document_type or id_card_num_db == biz_num_self:
                    check_have = True
                search_biz_result = db.session.query(tb_group_template_2).filter(tb_group_template_2.biz_info.contains(biz_num_self)).filter(tb_group_template_2.tid != (self.id)).filter(tb_group_template_2.status == 'ACTIVE').all()
                # print (search_biz_result)
                if search_biz_result != []:
                    check_biz = True
                if check_biz == False : # ไม่มี id_card_num
                    check_update = True
                elif check_biz == True : # มี id_card_num อยู่แล้ว
                    for i in range(len(search_biz_result)):
                        tmp_query_dict = search_biz_result[i].__dict__
                        # if '_sa_instance_state' in tmp_query_dict:
                        #     del tmp_query_dict['_sa_instance_state']
                        if biz_num_self in tmp_query_dict['biz_info']:
                            check_biz_in = True
                        # if self.group_code == tmp_query_dict['group_code']:
                        #     self.group_code = tmp_query_dict['group_code']
                        if tmp_query_dict['group_code'] == self.group_code :
                            check_code = True
                            # if tmp_query_dict['document_type'] == self.document_type:
                            #     check_type = True
                            check_have = False
                    if check_code == True and check_biz_in == True: # มี group_code
                        check_update = True
                    elif check_code == False and check_biz_in == True and check_have == True: # ไม่มี group_code
                        check_update = True
                    elif check_code == True and check_biz_in == True and check_have == True: # มี group_code
                        check_update = True
                    elif check_code == False and check_biz_in == True and check_have == True: # ไม่มี group_code
                        check_update = True
                if check_update == True:            
                    if tmp_query != None:
                        tmp_query.status = 'REJECT'
                        insert_result = tb_group_template_2(group_name=self.group_name,group_code=self.group_code,template=str(self.template),group_title=self.group_title,\
                            step_group=self.step_group,status='ACTIVE',create_date=tmp_query.create_date,update_date=str(st),group_data=self.group_data,biz_info=self.biz_info,create_by=tmp_query.create_by,\
                            update_by=self.update_by,use_status=self.use_status,cover_page=self.cover_page,tid=tmp_query.tid,group_color=self.group_color,email_middle=self.email_middle,\
                            timegroup_auto=self.timegroup,daygroup_auto=self.daygroup,email_step=self.email_step,status_doing_auto=self.status_doing_auto)
                        db.session.add(insert_result)
                        db.session.flush()
                        db.session.commit()
                        return {'result':'OK'}
                    else:                
                        return {'result':'ER'}
            elif self.biz_info == '' or self.biz_info == None:              
                search_biz_result = db.session.query(tb_group_template_2).filter(tb_group_template_2.biz_info == '').all()
                if search_biz_result != []:
                    check_biz = True
                if check_biz == False : # ไม่มี id_card_num
                    check_update = True
                elif check_biz == True : # มี id_card_num อยู่แล้ว
                    for i in range(len(search_biz_result)):
                        tmp_query_dict = search_biz_result[i].__dict__
                        # if '_sa_instance_state' in tmp_query_dict:
                        #     del tmp_query_dict['_sa_instance_state']                        
                        if tmp_query_dict['group_code'] == self.group_code:
                            check_code = True
                            # if tmp_query_dict['document_type'] == self.document_type:
                            #     check_type = True
                    if check_code == True : # มี group_code
                        return {'result':'ER','messageText':'This data already exists'}
                    elif check_code == False and check_have == True: # ไม่มี group_code
                        check_update = True
                    elif check_code == True and check_have == True: # มี group_code
                        check_update = True
                    elif check_code == False and check_have == True: # ไม่มี group_code
                        check_update = True
            if check_update == True:            
                if tmp_query != None:                   
                    tmp_query.status = 'REJECT'
                    insert_result = tb_group_template_2(group_name=self.group_name,group_code=self.group_code,template=str(self.template),group_title=self.group_title,step_group=self.step_group,status='ACTIVE',create_date=tmp_query.create_date,update_date=str(st),group_data=self.group_data,biz_info=self.biz_info,create_by=tmp_query.create_by,update_by=self.update_by,use_status=self.use_status,cover_page=self.cover_page,tid=tmp_query.tid,group_color=self.group_color,email_middle=self.email_middle,timegroup_auto=self.timegroup,daygroup_auto=self.daygroup,email_step=self.email_step,status_doing_auto=self.status_doing_auto)
                    db.session.add(insert_result)
                    db.session.flush()
                    db.session.commit()
                    return {'result':'OK'}
                else:                
                    return {'result':'ER'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}


    def update_json_file_attach_v1(self,folder_name_db,list_file,total_size,tmp_query):
        self.folder_name_db = folder_name_db
        self.list_file = list_file
        self.total_size = str(total_size)
        self.tmp_query = tmp_query
        list_json = []
        list_json_last = []
        try:
            tmp_query = self.tmp_query
            # print ('tmp_query11111:',tmp_query)
            if tmp_query == []:
                # print ('ERRRRRRRRRRRRRRRRRRRRRRRRR')
                return {'result':'ER','messageText':'not found folder_name'}
            for k in range(len(tmp_query)):
                # print (k)
                tmp_query2 = tmp_query[k]
                # tmp_query = tmp_query[0]
                if tmp_query2['folder_name'] == self.folder_name_db:
                    json_data = eval(tmp_query2['json_data'])
                    if tmp_query2['storage'] == None or tmp_query2['storage'] == '':
                        # print (type(json_data))
                        # print ('list_file:',(self.list_file))
                        # print ('json_data1111:',json_data)
                        for i in range(len(json_data)):
                            for j in range(len(self.list_file)):
                                if self.list_file[j]['file_name'] == json_data[i]['file_name_new']:
                                    # print ('111111',self.list_file[j]['file_name'])
                                    # print ('222222',json_data[i]['file_name_new'])
                                    # print ('json_dataaaaaaaa:',json_data[i])
                                    # print ('333333',self.list_file[j]['file_size'])
                                    dicts = {"filesize":str(self.list_file[j]['file_size'])}
                                    json_data[i].update(dicts)
                        # print ('json_data2222:',json_data)
                        list_json.append(str(json_data))
                        list_json.append(str(self.total_size))
                        list_json.append(str(self.folder_name_db))
                        list_json = tuple(list_json)
                        list_json_last.append(list_json)
                        # print ('list_json_last:',list_json_last)

                        with engine.connect() as connection:
                            result_insert = connection.execute('UPDATE "tb_transactionfile" SET "json_data"=%s,"storage"=%s WHERE "folder_name"=%s',list_json_last)
                            connection.close()

                        # tmp_query2 = [dict(row2) for row2 in result_insert][0]
                        # print (tmp_query2)
                        # print ('update_success')
                        return {'result':'OK','messageText':'update_success'}
                    elif tmp_query2['storage'] != None and tmp_query2['storage'] != '':
                        # print ('HAVE DATA:',tmp_query2['folder_name'])
                        return {'result':'OK','messageText':'update_success'}
                
        except Exception as e:
            print (str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def delete_draft_document_v2_sql(self,tid):
        self.tid = tid
        try:
            status_update = 'INACTIVE'
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            with engine.connect() as connection:
                query_result = connection.execute('UPDATE "tb_draft_document" SET "status"=%s,"update_time"=%s WHERE "tid"=%s AND "status"=%s returning "tid"',status_update,str(st),self.tid,'ACTIVE')
                connection.close()
                tmp_query = [dict(row) for row in query_result]

            if tmp_query != None and tmp_query != []:
                return {'result':'OK','messageText':'delete success '+tmp_query[0]['tid'],'status_Code':200,'messageER':None}
            else:
                return {'result':'OK','messageText':'Not have data','status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(str(e))
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def delete_draft_document(self,tid):
        try:
            self.tid = tid
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            query_result = db.session.query(paperless_draft).filter(paperless_draft.tid==self.tid).filter(paperless_draft.status=='ACTIVE').first()
            if query_result != None and query_result != []:
                query_result.status = 'INACTIVE'
                query_result.update_time = str(st)
                db.session.commit()
                return {'result':'OK','messageText':'delete success','status_Code':200,'messageER':None}
            else:
                return {'result':'OK','messageText':'Not have data','status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    # def update_draft_document_v2_sql(self,id_data, data_json, data_json_Upload, biz_info,qrCode_position,recipient_email,string_pdf,documentJson,options_page,documentType,template,type_file,folder_name,email_center,step_code,attempted_name,attach_data,importance,last_digitsign,time_expire):
    #     self.tid = id_data
    #     self.data_json = data_json
    #     self.data_json_Upload = data_json_Upload
    #     self.biz_info = biz_info
    #     self.qrCode_position = qrCode_position
    #     self.recipient_email = recipient_email
    #     self.string_pdf = string_pdf
    #     self.documentJson = documentJson
    #     self.options_page = options_page
    #     self.documentType = documentType
    #     self.template = template
    #     self.type_file = type_file
    #     self.folder_name = folder_name
    #     self.email_center = email_center
    #     self.step_code = step_code
    #     self.attempted_name = attempted_name
    #     self.attach_data = attach_data
    #     self.importance = importance
    #     self.last_digitsign = last_digitsign
    #     self.time_expire = time_expire
    #     ts = int(time.time())
    #     st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    #     try:
    #         if self.time_expire != None :
    #             time_ex_eval = eval(self.time_expire)
    #             day = time_ex_eval[0]
    #             hour = time_ex_eval[1]
    #             self.time_expire = (int(day) * 24) + int(hour)
    #         else:
    #             self.time_expire = 0
    #         with engine.connect() as connection:
    #             result = connection.execute(text('SELECT "id","data_json","data_json_Upload","biz_info","qrCode_position","recipient_email","string_pdf",\
    #                     "documentJson","options_page","documentType","status","sender_email","update_time","tid","template","type_file","folder_name",\
    #                     "email_center","step_code","attempted_name","attach_data","importance","last_digitsign","time_expire" FROM "tb_draft_document" WHERE "tid"=:tid AND "status"=:status'),tid=self.tid,status='ACTIVE')
    #             connection.close()
    #             tmp_query = [dict(row) for row in result]
    #         if tmp_query != [] and tmp_query != None and tmp_query != '':
    #             with engine.connect() as connection:
    #                 result_insert = connection.execute('insert into tb_draft_document ("tid","data_json","data_json_Upload","biz_info","qrCode_position","recipient_email",\
    #                 "string_pdf","documentJson","options_page","documentType","status","sender_email",\
    #                 "update_time","template","type_file","folder_name","email_center","step_code","attempted_name",\
    #                 "attach_data","importance","last_digitsign","time_expire")\
    #                 values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) \
    #                 returning "tid"',self.tid,self.data_json,self.data_json_Upload,str(self.biz_info),self.qrCode_position,\
    #                 self.recipient_email,self.string_pdf,self.documentJson,self.options_page,self.documentType,'ACTIVE',\
    #                 tmp_query[0]['sender_email'],str(st),str(self.template),self.type_file,self.folder_name,self.email_center,\
    #                 self.step_code,self.attempted_name,self.attach_data,self.importance,self.last_digitsign,self.time_expire)
    #                 connection.close()
    #             with engine.connect() as connection:
    #                 result_update = connection.execute('UPDATE tb_draft_document SET "status"=%s WHERE "tid"=%s AND id=%s','INACTIVE',self.tid,tmp_query[0]['id'])
    #                 connection.close()
               
    #             return {'result':'OK','messageText':'update success','status_Code':200,'messageER':None}  
    #         else:
    #             return {'result':'OK','messageText':'Not have data','status_Code':200,'messageER':None}
    #     except Exception as e:
    #         exc_type, exc_obj, exc_tb = sys.exc_info()
    #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #         print(exc_type, fname, exc_tb.tb_lineno)
    #         return {'result':'ER','messageText':str(e)}

    def update_draft_document_v2_sql(self,id_data, data_json, data_json_Upload, biz_info,qrCode_position,recipient_email,string_pdf,documentJson,options_page,documentType,template,type_file,folder_name,email_center,step_code,attempted_name,attach_data,importance,last_digitsign,time_expire,status_ref,list_ref):
        self.tid = id_data
        self.data_json = data_json
        self.data_json_Upload = data_json_Upload
        self.biz_info = biz_info
        self.qrCode_position = qrCode_position
        self.recipient_email = recipient_email
        self.string_pdf = string_pdf
        self.documentJson = documentJson
        self.options_page = options_page
        self.documentType = documentType
        self.template = template
        self.type_file = type_file
        self.folder_name = folder_name
        self.email_center = email_center
        self.step_code = step_code
        self.attempted_name = attempted_name
        self.attach_data = attach_data
        self.importance = importance
        self.last_digitsign = last_digitsign
        self.time_expire = time_expire
        self.status_ref = status_ref
        self.list_ref = list_ref
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        try:
            if self.time_expire != None :
                time_ex_eval = eval(self.time_expire)
                day = time_ex_eval[0]
                hour = time_ex_eval[1]
                self.time_expire = (int(day) * 24) + int(hour)
            else:
                self.time_expire = 0
            with slave.connect() as connection:
                result = connection.execute(text('SELECT "id","data_json","data_json_Upload","biz_info","qrCode_position","recipient_email","string_pdf",\
                        "documentJson","options_page","documentType","status","sender_email","update_time","tid","template","type_file","folder_name",\
                        "email_center","step_code","attempted_name","attach_data","importance","last_digitsign","time_expire","status_ref","list_ref" FROM "tb_draft_document" WHERE "tid"=:tid AND "status"=:status'),tid=self.tid,status='ACTIVE')
                connection.close()
                tmp_query = [dict(row) for row in result]
            if tmp_query != [] and tmp_query != None and tmp_query != '':
                with engine.connect() as connection:
                    result_insert = connection.execute('insert into tb_draft_document ("tid","data_json","data_json_Upload","biz_info","qrCode_position","recipient_email",\
                    "string_pdf","documentJson","options_page","documentType","status","sender_email",\
                    "update_time","template","type_file","folder_name","email_center","step_code","attempted_name",\
                    "attach_data","importance","last_digitsign","time_expire","status_ref","list_ref")\
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) \
                    returning "tid"',self.tid,self.data_json,self.data_json_Upload,str(self.biz_info),self.qrCode_position,\
                    self.recipient_email,self.string_pdf,self.documentJson,self.options_page,self.documentType,'ACTIVE',\
                    tmp_query[0]['sender_email'],str(st),str(self.template),self.type_file,self.folder_name,self.email_center,\
                    self.step_code,self.attempted_name,self.attach_data,self.importance,self.last_digitsign,self.time_expire,self.status_ref,str(self.list_ref))
                    connection.close()
                with engine.connect() as connection:
                    result_update = connection.execute('UPDATE tb_draft_document SET "status"=%s WHERE "tid"=%s AND id=%s','INACTIVE',self.tid,tmp_query[0]['id'])
                    connection.close()
               
                return {'result':'OK','messageText':'update success','status_Code':200,'messageER':None}  
            else:
                return {'result':'OK','messageText':'Not have data','status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}


    def update_draft_document(self,id_data, data_json, data_json_Upload, biz_info,qrCode_position,recipient_email,string_pdf,documentJson,options_page,documentType,template,type_file,folder_name,email_center,step_code,attempted_name,attach_data):
        self.tid = id_data
        self.data_json = data_json
        self.data_json_Upload = data_json_Upload
        self.biz_info = biz_info
        self.qrCode_position = qrCode_position
        self.recipient_email = recipient_email
        self.string_pdf = string_pdf
        self.documentJson = documentJson
        self.options_page = options_page
        self.documentType = documentType
        self.template = template
        self.type_file = type_file
        self.folder_name = folder_name
        self.email_center = email_center
        self.step_code = step_code
        self.attempted_name = attempted_name
        self.attach_data = attach_data
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        try:
            tmp_query = paperless_draft.query.filter(paperless_draft.tid==self.tid).filter(paperless_draft.status == 'ACTIVE').first()
            if tmp_query != [] and tmp_query != None and tmp_query != '':
                insert_result = paperless_draft(tid=self.tid,data_json=self.data_json,data_json_Upload=self.data_json_Upload,biz_info=str(self.biz_info),qrCode_position=self.qrCode_position,recipient_email=self.recipient_email,string_pdf=self.string_pdf,documentJson=self.documentJson,options_page=self.options_page,documentType=self.documentType,status='ACTIVE',sender_email=tmp_query.sender_email,update_time=str(st),template=str(self.template),type_file=self.type_file,folder_name=self.folder_name,email_center=self.email_center,step_code=self.step_code,attempted_name=self.attempted_name,attach_data=self.attach_data)
                db.session.add(insert_result)
                db.session.flush()
                tmp_query.status = 'INACTIVE'
                db.session.commit()
                return {'result':'OK','messageText':'update success','status_Code':200,'messageER':None}

            else:
                return {'result':'OK','messageText':'Not have data','status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def add_data(self,tmp_query,group_name,group_code,template,document_type,group_title,step_group,group_data,biz_info,update_by,use_status):
        self.tmp_query = tmp_query
        self.group_name = group_name
        self.group_code = group_code
        self.template = template
        self.document_type = document_type
        self.group_title = group_title
        self.step_group = step_group
        self.group_data = group_data
        self.biz_info = biz_info
        self.update_by = update_by
        self.use_status = use_status
        try:
            if self.tmp_query != None:
                if self.group_name != '':
                    self.tmp_query.group_name = self.group_name
                if group_code != '':
                    self.tmp_query.group_code = self.group_code
                if template != '':
                    self.tmp_query.template = self.template
                if document_type != '':
                    self.tmp_query.document_type = self.document_type
                if group_title != '':
                    self.tmp_query.group_title = self.group_title
                if step_group != '':
                    self.tmp_query.step_group = self.step_group
                self.tmp_query.update_date = str(st)
                if group_data != '':
                    self.tmp_query.group_data = self.group_data
                if biz_info != '':
                    self.tmp_query.biz_info = self.biz_info
                if update_by != '':   
                    self.tmp_query.update_by = self.update_by
                if use_status != '':   
                    self.tmp_query.use_status = self.use_status
                db.session.commit()

            return {'result': 'OK'}

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_json(self,sid,email,step,email_step):
        self.sid = sid
        self.email = email
        self.step = step
        self.email_step = email_step
        list_stepDetails = []
        list_stepDetails_2 = []
        list_DataStep = []
        tmp_2 = {}
        arr_tmp = []
        tmp1 = []
        try:
            query_json = db.session.query(
                    paper_lessdatastep.sid,
                    paper_lessdatastep.data_json)\
                .filter(paper_lessdatastep.sid==self.sid)\
                .first()
            arr_email = self.email_step
            if query_json != None:
                tmp_sid = query_json[0]
                tmpdata_json = query_json[1]
                if tmpdata_json != None:
                    tmpdata_json = eval(tmpdata_json)
                if 'step_num' in tmpdata_json:
                    arr_tmp.append(tmpdata_json)
                    tmpdata_json = arr_tmp
                for x in range(len(tmpdata_json)):
                    tmpstepnum = tmpdata_json[x]['step_num']
                    tmparr_email = []
                    for c in range(len(self.step)):
                        tmp_jsonstepnum = self.step[c]
                        tmp_emailtostep = self.email_step[c]
                        if tmp_jsonstepnum == tmpstepnum:
                            tmpstep_detail = tmpdata_json[x]['step_detail']
                            for z in range(len(tmpstep_detail)):
                                tmp_1 = tmpstep_detail[0]
                        for h in range(len(tmp_emailtostep)):
                            tmpjson1 = {}
                            for key,value in tmp_1.items():
                                tmpjson1[key] = value
                            tmpjson1['one_email'] = tmp_emailtostep[h]
                            tmp1.append(tmpjson1)
            return {'result': 'OK', 'messageText': tmp1}
        except Exception as ex:
            print(ex)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result': 'ER', 'messageText': 'ไม่สามารถเปลี่ยนแปลงลำดับได้','messageER':str(ex)}
        finally:
            db.session.close()

    def delete_template_group_v2(self,id_data,username):
        self.id = id_data
        self.username = username
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        try:
            tmp_query = tb_group_template.query.filter(tb_group_template.tid==self.id,tb_group_template.status=='ACTIVE').first()
            if tmp_query != None:                
                tmp_query.status = 'REJECT'
                tmp_query.update_date = str(st)
                tmp_query.update_by = self.username
                db.session.commit()
                return {'result':'OK'}
            
            else:                
                return {'result':'ER'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}
        finally:
            db.session.close()


    def use_status_template_group_v2(self,id_data,use_status,username):
        self.id = id_data
        self.use_status = use_status
        self.username = username
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        try:
            tmp_query = tb_group_template.query.filter(tb_group_template.id==self.id).first()
            if tmp_query != None:
                tmp_query.use_status = self.use_status
                tmp_query.update_date = str(st)
                tmp_query.update_by = self.username
                db.session.commit()
                return {'result':'OK'}
            
            else:                
                return {'result':'ER'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}
        finally:
            db.session.close()



    def use_status_template_group_v3(self,id_data,use_status,username):
        self.id = id_data
        self.use_status = use_status
        self.username = username
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        try:
            tmp_query = db.session.query(tb_group_template).filter(tb_group_template.id == self.id).update({tb_group_template.use_status: self.use_status}, synchronize_session = False)
            
            return {'result':'OK'}
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}


    def update_template_group_v2(self,id_data,group_name=None,group_code=None,template=None,document_type=None,group_title=None,step_group=None,group_data=None,biz_info=None,update_by=None,use_status=None):
        self.id = id_data
        self.group_name = group_name
        self.group_code = group_code
        self.template = template
        self.document_type = document_type
        self.group_title = group_title
        self.step_group = step_group
        self.group_data = group_data
        self.biz_info = biz_info
        self.update_by = update_by
        self.use_status = use_status

        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')

        try:
            tmp_query = tb_group_template.query.filter(tb_group_template.id==self.id).first()
            if tmp_query != None:
                print (tmp_query)
                tmp_query.group_name = self.group_name
                tmp_query.group_code = self.group_code
                tmp_query.template = self.template
                tmp_query.document_type = self.document_type
                tmp_query.group_title = self.group_title
                tmp_query.step_group = self.step_group
                tmp_query.update_date = str(st)
                tmp_query.group_data = self.group_data
                tmp_query.biz_info = self.biz_info
                tmp_query.update_by = self.update_by
                tmp_query.use_status = self.use_status

                db.session.commit()
                return {'result':'OK'}
            
            else:                
                return {'result':'ER'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_template_group_v3(self,id_data,group_name=None,group_code=None,template=None,document_type=None,group_title=None,step_group=None,group_data=None,biz_info=None,update_by=None,use_status=None):
        self.id = id_data
        self.group_name = group_name
        self.group_code = group_code
        self.template = template
        self.document_type = document_type
        self.group_title = group_title
        self.step_group = step_group
        self.group_data = group_data
        self.biz_info = biz_info
        self.update_by = update_by
        self.use_status = use_status

        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')

        try:
            tmp_query = tb_group_template.query.filter(tb_group_template.id==self.id).first()
            if tmp_query != None:
                print (tmp_query)
                if self.group_name != '':
                    tmp_query.group_name = self.group_name
                if self.group_code != '':
                    tmp_query.group_code = self.group_code
                if self.template != '':
                    tmp_query.template = self.template
                if self.document_type != '':
                    tmp_query.document_type = self.document_type
                if self.group_title != '':
                    tmp_query.group_title = self.group_title
                if self.step_group != '':
                    tmp_query.step_group = self.step_group
                tmp_query.update_date = str(st)
                if self.group_data != '':
                    tmp_query.group_data = self.group_data
                if self.biz_info != '':
                    tmp_query.biz_info = self.biz_info
                if self.update_by != '':   
                    tmp_query.update_by = self.update_by
                if self.use_status != '':   
                    tmp_query.use_status = self.use_status

                db.session.commit()
                return {'result':'OK'}
            
            else:                
                return {'result':'ER'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_template_group_v4(self,id_data,group_name=None,group_code=None,template=None,document_type=None,group_title=None,step_group=None,group_data=None,biz_info=None,update_by=None,use_status=None):
        self.id = id_data
        self.group_name = group_name
        self.group_code = group_code
        self.template = template
        self.document_type = document_type
        self.group_title = group_title
        self.step_group = step_group
        self.group_data = group_data
        self.biz_info = biz_info
        self.update_by = update_by
        self.use_status = use_status

        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        check_code = False
        check_type = False
        check_update = False
        check_biz = False
        check_biz_in = False
        check_have = False
        try:
            tmp_query = tb_group_template.query.filter(tb_group_template.id==self.id).first()
            # print ('tmp_query: ',tmp_query.group_code)

            group_code_db = tmp_query.group_code
            document_type_db = tmp_query.document_type
            eval_biz_db = eval(tmp_query.biz_info)
            
            if type(eval_biz_db) == list:
                id_card_num_db = (eval(tmp_query.biz_info))[0]['id_card_num']
            elif type(eval_biz_db) == dict:
                id_card_num_db = (eval(tmp_query.biz_info))['id_card_num']
            if self.biz_info != '' and self.biz_info != None:
                if 'id_card_num' in self.biz_info:
                    eval_biz_self = eval(self.biz_info)
                    if type(eval_biz_self) == dict:
                        biz_num_self = eval_biz_self['id_card_num']
                    elif type(eval_biz_self) == list:
                        biz_num_self = eval_biz_self[0]['id_card_num']
                else:
                    return {'result':'ER','messageText':'This data already exists'}
                
                print ('biz_num_self: ',biz_num_self)
                
                if group_code_db == self.group_code or document_type_db == document_type or id_card_num_db == biz_num_self:
                    check_have = True

                
                search_biz_result = db.session.query(tb_group_template).filter(tb_group_template.biz_info.contains(biz_num_self)).filter(tb_group_template.id != (self.id)).all()
                # print ('search_biz_result: ',search_biz_result)

                if search_biz_result != []:
                    check_biz = True
            
                if check_biz == False : # ไม่มี id_card_num
                    print ('ไม่มี id_card_num')
                    check_update = True

                elif check_biz == True : # มี id_card_num อยู่แล้ว
                    print ('มี id_card_num อยู่แล้ว')
                    for i in range(len(search_biz_result)):
                        tmp_query_dict = search_biz_result[i].__dict__
                        
                        # if '_sa_instance_state' in tmp_query_dict:
                        #     del tmp_query_dict['_sa_instance_state']
                        # print ('tmp_query_dict: ',tmp_query_dict)

                        if biz_num_self in tmp_query_dict['biz_info']:
                            check_biz_in = True
                        if tmp_query_dict['group_code'] == self.group_code :
                            check_code = True
                            
                            
                            if tmp_query_dict['document_type'] == self.document_type:
                                check_type = True

                                check_have = False

                    print ('check_have: ',check_have)

                    if check_code == True and check_type == True and check_biz_in == True: # มี group_code มี document_type อยู่แล้ว
                        print ('มี group_code มี document_type อยู่แล้ว')
                        return {'result':'ER','messageText':'This data already exists'}
                    elif check_code == False and check_type == True and check_biz_in == True and check_have == True: # ไม่มี group_code มี document_type อยู่แล้ว
                        check_update = True

                    elif check_code == True and check_type == False and check_biz_in == True and check_have == True: # มี group_code ไม่มี document_type 
                        check_update = True

                    elif check_code == False and check_type == False and check_biz_in == True and check_have == True: # ไม่มี group_code ไม่มี document_type 
                        check_update = True
                

                print ('check_update: ',check_update)
                if check_update == True:            
                    if tmp_query != None:
                        
                        tmp_query.group_name = self.group_name
                    
                        tmp_query.group_code = self.group_code
                    
                        tmp_query.template = self.template
                    
                        tmp_query.document_type = self.document_type
                    
                        tmp_query.group_title = self.group_title
                    
                        tmp_query.step_group = self.step_group
                        tmp_query.update_date = str(st)
                    
                        tmp_query.group_data = self.group_data
                    
                        tmp_query.biz_info = self.biz_info
                        
                        tmp_query.update_by = self.update_by
                    
                        tmp_query.use_status = self.use_status

                        db.session.commit()
                        return {'result':'OK'}
                    
                    else:                
                        return {'result':'ER'}

            elif self.biz_info == '' or self.biz_info == None:              
                
                print ('self.biz_info == '' or self.biz_info == None')
                search_biz_result = db.session.query(tb_group_template).filter(tb_group_template.biz_info == '').all()

                if search_biz_result != []:
                    check_biz = True
            
                if check_biz == False : # ไม่มี id_card_num
                    print ('ไม่มี id_card_num')
                    check_update = True

                elif check_biz == True : # มี id_card_num อยู่แล้ว
                    print ('มี id_card_num อยู่แล้ว')
                    for i in range(len(search_biz_result)):
                        tmp_query_dict = search_biz_result[i].__dict__
                    
                        # if '_sa_instance_state' in tmp_query_dict:
                        #     del tmp_query_dict['_sa_instance_state']

                        
                        if tmp_query_dict['group_code'] == self.group_code:
                            check_code = True

                           
                            if tmp_query_dict['document_type'] == self.document_type:
                                check_type = True


                    if check_code == True and check_type == True: # มี group_code มี document_type อยู่แล้ว
                        print ('มี group_code มี document_type อยู่แล้ว')
                        return {'result':'ER','messageText':'This data already exists'}

                    elif check_code == False and check_type == True and check_have == True: # ไม่มี group_code มี document_type อยู่แล้ว
                        print ('ไม่มี group_code มี document_type อยู่แล้ว')
                        check_update = True

                    elif check_code == True and check_type == False and check_have == True: # มี group_code ไม่มี document_type 
                        print ('มี group_code ไม่มี document_type ')
                        check_update = True

                    elif check_code == False and check_type == False and check_have == True: # ไม่มี group_code ไม่มี document_type 
                        print ('ไม่มี group_code ไม่มี document_type ')
                        check_update = True

            print ('check_update2: ',check_update)
            if check_update == True:            
                if tmp_query != None:
                    
                    tmp_query.group_name = self.group_name
                
                    tmp_query.group_code = self.group_code
                
                    tmp_query.template = self.template
                
                    tmp_query.document_type = self.document_type
                
                    tmp_query.group_title = self.group_title
                
                    tmp_query.step_group = self.step_group
                    tmp_query.update_date = str(st)
                
                    tmp_query.group_data = self.group_data
                
                    tmp_query.biz_info = self.biz_info
                    
                    tmp_query.update_by = self.update_by
                    
                    tmp_query.use_status = self.use_status

                    db.session.commit()
                    return {'result':'OK'}
                
                else:                
                    return {'result':'ER'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def update_template_group_v6(self,id_data,group_name=None,group_code=None,template=None,document_type=None,group_title=None,step_group=None,group_data=None,biz_info=None,update_by=None,use_status=None,cover_page=None,group_color=None,email_middle=None,timegroup=None,daygroup=None,webhook=None):
        self.id = id_data
        self.group_name = group_name
        self.group_code = group_code
        self.template = str(template)
        self.document_type = document_type
        self.group_title = group_title
        self.step_group = step_group
        self.group_data = group_data
        self.biz_info = biz_info
        self.update_by = update_by
        self.use_status = use_status
        self.cover_page = cover_page
        self.group_color = group_color
        self.timegroup = timegroup
        self.daygroup = daygroup
        self.email_middle = email_middle
        self.webhook = webhook
        if timegroup != None:
            self.timegroup = str(timegroup)
        if email_middle != None:
            self.email_middle = str(email_middle)
        if daygroup != None:
            self.daygroup = str(daygroup)
        if group_color != None:
            self.group_color = str(group_color).replace(' ','').lower()
            self.group_color = str([{'color':self.group_color}])

        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%d/%b/%Y %H:%M:%S')
        check_code = False
        check_type = False
        check_update = False
        check_biz = False
        check_biz_in = False
        check_have = False
        print('group template update')
        try:
            if self.biz_info != '' and self.biz_info != None:
                sql = '''SELECT ID,group_code,document_type,biz_info,create_date,create_by,tid FROM tb_group_template WHERE tid=:tid AND status='ACTIVE'; '''
                connection = engine.connect()
                result = connection.execute(text(sql),tid=self.id)
                resultQuery = [dict(row) for row in result]
                if len(resultQuery) != 0:
                    tmp_query = resultQuery[0]
                    tmpid = tmp_query['id']
                    tmpcreate_date = tmp_query['create_date']
                    tmpcreate_by = tmp_query['create_by']
                    tmptid = tmp_query['tid']
                    sql_update = '''UPDATE tb_group_template SET status='REEJCT' WHERE id=:id '''
                    connection.execute(text(sql_update),id=tmpid)
                    resultsql = connection.execute('INSERT INTO tb_group_template (group_name,group_code,template,document_type,group_title,step_group,status,create_date,update_date,group_data,biz_info,create_by,update_by,use_status,\
                    cover_page,tid,group_color,email_middle,timegroup_auto,daygroup_auto,webhook) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);',self.group_name,self.group_code,self.template,self.document_type\
                    ,self.group_title,self.step_group,'ACTIVE',tmpcreate_date,str(st),self.group_data,self.biz_info,tmpcreate_by,self.update_by,self.use_status,self.cover_page,tmptid,self.group_color,self.email_middle,self.timegroup,self.daygroup,self.webhook)
                    return {'result':'OK'}
            elif self.biz_info == '' or self.biz_info == None: 
                return {'result':'ER'}
            return {'result':'ER'}
            # tmp_query = tb_group_template.query.filter(tb_group_template.tid==self.id).filter(tb_group_template.status!='REJECT').first()
            # group_code_db = tmp_query.group_code
            # document_type_db = tmp_query.document_type
            # eval_biz_db = eval(tmp_query.biz_info)
            
            # if type(eval_biz_db) == list:
            #     id_card_num_db = (eval(tmp_query.biz_info))[0]['id_card_num']
            # elif type(eval_biz_db) == dict:
            #     id_card_num_db = (eval(tmp_query.biz_info))['id_card_num']
            # if self.biz_info != '' and self.biz_info != None:
            #     if 'id_card_num' in self.biz_info:
            #         eval_biz_self = eval(self.biz_info)
            #         if type(eval_biz_self) == dict:
            #             biz_num_self = eval_biz_self['id_card_num']
            #         elif type(eval_biz_self) == list:
            #             biz_num_self = eval_biz_self[0]['id_card_num']
            #     else:
            #         return {'result':'ER','messageText':'This data already exists'}
            #     if group_code_db == self.group_code or document_type_db == document_type or id_card_num_db == biz_num_self:
            #         check_have = True
            #     search_biz_result = db.session.query(tb_group_template).filter(tb_group_template.biz_info.contains(biz_num_self)).filter(tb_group_template.tid != (self.id)).filter(tb_group_template.status == 'ACTIVE').all()
            #     # print (search_biz_result)
            #     if search_biz_result != []:
            #         check_biz = True
            #     if check_biz == False : # ไม่มี id_card_num
            #         check_update = True
            #     elif check_biz == True : # มี id_card_num อยู่แล้ว
            #         for i in range(len(search_biz_result)):
            #             tmp_query_dict = search_biz_result[i].__dict__
            #             # if '_sa_instance_state' in tmp_query_dict:
            #             #     del tmp_query_dict['_sa_instance_state']
            #             if biz_num_self in tmp_query_dict['biz_info']:
            #                 check_biz_in = True
            #             # if self.group_code == tmp_query_dict['group_code']:
            #             #     self.group_code = tmp_query_dict['group_code']
            #             if tmp_query_dict['group_code'] == self.group_code :
            #                 check_code = True
            #                 if tmp_query_dict['document_type'] == self.document_type:
            #                     check_type = True
            #                     check_have = False
            #         if check_code == True and check_type == True and check_biz_in == True: # มี group_code มี document_type อยู่แล้ว
            #             check_update = True
            #         elif check_code == False and check_type == True and check_biz_in == True and check_have == True: # ไม่มี group_code มี document_type อยู่แล้ว
            #             check_update = True
            #         elif check_code == True and check_type == False and check_biz_in == True and check_have == True: # มี group_code ไม่มี document_type 
            #             check_update = True
            #         elif check_code == False and check_type == False and check_biz_in == True and check_have == True: # ไม่มี group_code ไม่มี document_type 
            #             check_update = True
            #     if check_update == True:            
            #         if tmp_query != None:
            #             tmp_query.status = 'REJECT'
            #             insert_result = tb_group_template(group_name=self.group_name,group_code=self.group_code,template=str(self.template),document_type=self.document_type,group_title=self.group_title,\
            #                 step_group=self.step_group,status='ACTIVE',create_date=tmp_query.create_date,update_date=str(st),group_data=self.group_data,biz_info=self.biz_info,create_by=tmp_query.create_by,\
            #                 update_by=self.update_by,use_status=self.use_status,cover_page=self.cover_page,tid=tmp_query.tid,group_color=self.group_color,email_middle=self.email_middle,\
            #                 timegroup_auto=self.timegroup,daygroup_auto=self.daygroup)
            #             db.session.add(insert_result)
            #             db.session.flush()
            #             db.session.commit()
            #             return {'result':'OK'}
            #         else:                
            #             return {'result':'ER'}
            # elif self.biz_info == '' or self.biz_info == None:              
            #     search_biz_result = db.session.query(tb_group_template).filter(tb_group_template.biz_info == '').all()
            #     if search_biz_result != []:
            #         check_biz = True
            #     if check_biz == False : # ไม่มี id_card_num
            #         check_update = True
            #     elif check_biz == True : # มี id_card_num อยู่แล้ว
            #         for i in range(len(search_biz_result)):
            #             tmp_query_dict = search_biz_result[i].__dict__
            #             # if '_sa_instance_state' in tmp_query_dict:
            #             #     del tmp_query_dict['_sa_instance_state']                        
            #             if tmp_query_dict['group_code'] == self.group_code:
            #                 check_code = True
            #                 if tmp_query_dict['document_type'] == self.document_type:
            #                     check_type = True
            #         if check_code == True and check_type == True: # มี group_code มี document_type อยู่แล้ว
            #             return {'result':'ER','messageText':'This data already exists'}
            #         elif check_code == False and check_type == True and check_have == True: # ไม่มี group_code มี document_type อยู่แล้ว
            #             check_update = True
            #         elif check_code == True and check_type == False and check_have == True: # มี group_code ไม่มี document_type 
            #             check_update = True
            #         elif check_code == False and check_type == False and check_have == True: # ไม่มี group_code ไม่มี document_type 
            #             check_update = True
            # if check_update == True:            
            #     if tmp_query != None:                   
            #         tmp_query.status = 'REJECT'
            #         insert_result = tb_group_template(group_name=self.group_name,group_code=self.group_code,template=str(self.template),document_type=self.document_type,group_title=self.group_title,step_group=self.step_group,status='ACTIVE',create_date=tmp_query.create_date,update_date=str(st),group_data=self.group_data,biz_info=self.biz_info,create_by=tmp_query.create_by,update_by=self.update_by,use_status=self.use_status,cover_page=self.cover_page,tid=tmp_query.tid,group_color=self.group_color,email_middle=self.email_middle,timegroup_auto=self.timegroup,daygroup_auto=self.daygroup)
            #         db.session.add(insert_result)
            #         db.session.flush()
            #         db.session.commit()
            #         return {'result':'OK'}
                
            #     else:                
            #         return {'result':'ER'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}
        finally:
            connection.close()
            db.session.close()


class select_2():
    def select_stepGroup(self,sid):
        self.sid = sid
        arr_StatusTmp = []
        sql = """ select
                    tsd.step_data_sid AS "step_data_sid",
                    tsd.step_code AS "step_code",
                    tb_group_template_2."id",
                    tb_group_template_2."group_name",
                    tb_group_template_2."template",
                    tb_group_template_2."email_step",
                    tb_step_data."sid",
                    tb_step_data."data_json"
                FROM
                    tb_send_detail AS tsd
                    INNER JOIN tb_group_template_2 ON tb_group_template_2.template LIKE '%' || tsd.step_code || '%' 
                    INNER JOIN tb_step_data ON tb_step_data.sid = tsd.step_data_sid
                WHERE
                    tsd.step_data_sid = '""" +self.sid +"""'
                    AND tb_group_template_2.status = 'ACTIVE' 
                """
        with engine.connect() as connection:
            result = connection.execute(text(sql),sid=self.sid,)
            connection.close()
            tmp_query = [dict(row) for row in result]
        for bb in range(len(tmp_query)):
            print('len',len(tmp_query))
            step_Data = tmp_query[bb]['data_json']
            stepGroup = eval(str(tmp_query[bb]['email_step']))
            print(tmp_query[bb]['email_step'])
            step_Data = eval(str(step_Data))
            # config ตัวแปรเเต่ละรอบ
            step_before = ''
            arr_step = []
            # config ตัวแปรเเต่ละรอบ
            s = False
            print('len',len(step_Data))
            for ii in range(len(step_Data)):
                step_num = eval(str(step_Data[ii]['step_num']))
                # print('step_num',step_num)
                tmp_step_detail = eval(str(step_Data[ii]['step_detail']))
                for kk in range(len(tmp_step_detail)):
                    oneMail = tmp_step_detail[kk]['one_email']
                    # print('oneMail',oneMail)
                    # print('stepGroup[0]',stepGroup[0])
                    if oneMail == stepGroup[0]:
                        # print('in 01')
                        stepNumNow =  (int(step_num) - 1)
                        s = True
                        step_before = oneMail
                        # arr_step.append(int(step_num))
                    
                    else:
                        # print('in 02')
                        for xy in range(len(stepGroup)):
                            if oneMail == stepGroup[xy]:
                                # print('in in 02 02')
                                print('step_before',step_before)
                                print('self.InputEmail[xy-1]',stepGroup[xy-1])
                                if stepGroup[xy-1] == step_before:
                                    stepNumNow =  (int(step_num) - 1)
                                    s = True
                                    step_before = oneMail
                                    # arr_step.append(int(step_num))
                    # print('s55',s)
                    if s == True:
                        for xy in range(len(stepGroup)):
                            if stepGroup[xy] ==  oneMail:
                                print('kiki')
                                arr_step.append(int(step_num))
        print('arr_step',arr_step)
        print('__________________________________')
        if len(arr_step) == len(stepGroup):
            return arr_step
        else:
            return []

    def select_infoGroup_v2(self,group_id):
        self.group_id = group_id
        with slave.connect() as connection:
            result = connection.execute(text('SELECT "sid_group","doctype_group","email_middle","bizinfo_group" FROM "tb_group_document_2" WHERE "id" =:group_id'),group_id=self.group_id)
            connection.close()
            tmp_query = [dict(row) for row in result]
        # print('tmp_query',tmp_query)
        for x in range(len(tmp_query)):
            tmp_query[x]['sid_group'] = eval(str(tmp_query[x]['sid_group']))
            tmp_query[x]['doctype_group'] = eval(str(tmp_query[x]['doctype_group']))
            tmp_query[x]['email_middle'] = eval(str(tmp_query[x]['email_middle']))
            tmp_query[x]['bizinfo_group'] = eval(str(tmp_query[x]['bizinfo_group']))
        return tmp_query
        
    def recursive_select_querydocGroupVersion2(self,email_one,group_id,tax_id,status,limit,offset,keyword,count_data):
        try:
            self.email_one = email_one
            # self.document_type = document_type
            self.group_id = group_id
            self.tax_id = tax_id
            self.status = status
            self.limit = limit
            self.offset = offset
            self.keyword = keyword
            count_data = count_data
            tmp_arrjson = []
            txtQuery = ''
            tmp_query = []
            count = 0
            queryString = '''"status" = 'ACTIVE' AND "sid_group" != '[]' '''
            if self.email_one != None :
                queryString += '''AND ("email_view_group" LIKE '%'''+ self.email_one +'''%' OR status_group LIKE '%'''+ self.email_one +'''%') '''
            if self.tax_id != None and self.tax_id != '' :
                queryString += '''AND bizinfo LIKE '%'''+ self.tax_id +'''%' '''
            else:
                queryString += '''AND (bizinfo = '' OR bizinfo IS NULL)'''
            # if self.document_type != None :
            #     queryString += "AND document_type = '"+ str(self.document_type) +"'"   
            if self.status == 'N' or self.status == 'W' :
                queryString += "AND group_status = 'N'"     
            if self.keyword == None:
                query_sql = '''SELECT * FROM "tb_group_document_2" WHERE '''+queryString+''' ORDER BY "updatetime" DESC limit(:limit) offset(:offset)'''
            else:
                try:      
                    dats = datetime.datetime.strptime(self.keyword, '%Y-%m-%d')
                    datetime1 = dats.strftime('%Y-%m-%d 00:00:00')
                    datetime2 = dats.strftime('%Y-%m-%d 23:59:59')       
                    query_sql = "SELECT * FROM tb_group_document_2 WHERE "+ queryString +" AND updatetime >= '"+datetime1+"' AND updatetime <= '"+datetime2+"' ORDER BY updatetime DESC limit(:limit) offset(:offset)"                      
                except ValueError:
                    print('key not datetime') 
                    if self.keyword == '':
                        query_sql = '''SELECT * FROM "tb_group_document_2" WHERE '''+queryString+''' ORDER BY "updatetime" DESC limit(:limit) offset(:offset)'''
                    else:   
                        query_sql = '''SELECT * FROM "tb_group_document_2" WHERE '''+queryString+''' AND (doctype_group LIKE '%'''+ self.keyword +'''%'  or group_name LIKE '%'''+ self.keyword +'''%') ORDER BY "updatetime" DESC limit(:limit) offset(:offset)'''         
            if self.group_id != None:
                with engine.connect() as connection:
                    result_select = connection.execute("SELECT * FROM tb_group_document_2 WHERE status = 'ACTIVE' AND id = '"+ str(self.group_id) +"'")
                    tmp_query = [dict(row) for row in result_select]
                    connection.close()
            else:                
                with engine.connect() as connection:
                    result_select = connection.execute(text(query_sql),limit=self.limit,offset=self.offset)
                    tmp_query = [dict(row) for row in result_select]
                    connection.close()

            if len(tmp_query) != 0:
                print(len(tmp_query))
                for n in range(len(tmp_query)):
                    step_beforeMe = []
                    step_now = 0
                    tmparr_stepnum = []
                    tmp_step_group_detail = None
                    tmp_pdf = None
                    jsonurl_info = None
                    tmp_group_title = None
                    tmp_cover_page = None
                    tmp_step_group = None
                    tmp_maxstep = None
                    list_file_name = []
                    tmp_arr_status_group = []
                    tmp_arr_status_email = []
                    tmp_arr_status_group_001 = []
                    tmparr_stepstatus = []
                    arr_email_list = []
                    json_tmp = {}
                    tmp_text_status = 'Y'
                    tmp_text_status_string = 'อนุมัติแล้ว'
                    tmp_arr_data_sum_01 = []
                    tmp_json = tmp_query[n]
                    if '_sa_instance_state' in tmp_json:
                        del tmp_json['_sa_instance_state']
                    # print(tmp_json)
                    tmp_processid =None
                    tmp_color = None
                    data_biz = None
                    tmp_groupid = tmp_json['id']
                    
                    tmp_sidgroup = tmp_json['sid_group']
                    tmp_updatetime = tmp_json['updatetime']
                    tmp_status = tmp_json['status']
                    tmp_group_other = tmp_json['group_other']
                    tmp_group_data_json = tmp_json['group_data_json']
                    tmp_status_group = tmp_json['status_group']
                    tmp_email_view_group = tmp_json['email_view_group']
                    tmp_group_status = tmp_json['group_status']
                    if tmp_group_status == None:
                        tmp_group_status = 'N'
                    tmp_calculate_fieds = tmp_json['calculate_fieds']
                    tmp_group_title = tmp_json['group_title']
                    tmp_tracking_group = tmp_json['tracking_group']
                    tmp_json_data = tmp_json['json_data']
                    tmp_average_data = None
                    try:
                        tmp_average_data = eval(tmp_json['average_data'])
                    except Exception as e:
                        tmp_average_data = None
                    query_document = None
                    if 'bizinfo' in tmp_json :
                        if tmp_json['bizinfo'] != None:
                            if tmp_json['bizinfo'] != '':
                                eval_biz = eval(tmp_json['bizinfo'])
                                if type(eval_biz) == dict:
                                    for x in range(len(tmp_json['bizinfo'])):
                                        tmp_biz = {}
                                        tmp_biz['id_card_num'] = eval_biz['id_card_num']
                                        tmp_biz['first_name_th'] = eval_biz['first_name_th']
                                        tmp_biz['first_name_eng'] = eval_biz['first_name_eng']
                                        tmp_biz['role_name'] = eval_biz['role_name']
                                        tmp_biz['dept_id'] = eval_biz['dept_id']
                                    data_biz = tmp_biz
                                elif type(eval_biz) == list:
                                    for x in range(len(tmp_query['bizinfo'])):
                                        tmp_biz = {}
                                        tmp_biz['id_card_num'] = eval_biz[0]['id_card_num']
                                        tmp_biz['first_name_th'] = eval_biz[0]['first_name_th']
                                        tmp_biz['first_name_eng'] = eval_biz[0]['first_name_eng']
                                        tmp_biz['role_name'] = eval_biz[0]['role_name']
                                        tmp_biz['dept_id'] = eval_biz[0]['dept_id']
                                    data_biz = tmp_biz
                            else:
                                data_biz =None
                    if 'bizinfo' in tmp_json :
                        if tmp_json['bizinfo'] != None:
                            if tmp_json['bizinfo'] != '':
                                query_document = db.session.query(paper_lessdocument_detail)\
                                    .filter(and_(paper_lessdocument_detail.documentStatus=='ACTIVE',paper_lessdocument_detail.biz_info.contains(data_biz['id_card_num'])))\
                                    .order_by(desc(paper_lessdocument_detail.documentUpdate)).first()
                            else:
                                query_document = db.session.query(paper_lessdocument_detail)\
                                    .filter(and_(paper_lessdocument_detail.documentStatus=='ACTIVE',paper_lessdocument_detail.biz_info.contains==''))\
                                    .order_by(desc(paper_lessdocument_detail.documentUpdate)).first()
                    tmpdocumentdetail = None
                    if query_document != None:
                        tmpdocumentdetail = query_document.documentJson
                        if tmpdocumentdetail != None:
                            tmpdocumentdetail = eval(tmpdocumentdetail)
                    if tmp_group_title != None:
                        tmp_group_title = eval(tmp_group_title)
                    tmpurl_html_data = None
                    tmp_html_data = None
                    if self.group_id != None and self.email_one != None:
                        tmp_maxstep = tmp_json['maxstep']
                        tmp_step_group = tmp_json['step_group']
                        tmp_step_group_detail = tmp_json['step_group_detail']
                        tmp_pdf_org = tmp_json['pdf_org']
                        tmp_pdf_sign = tmp_json['pdf_sign']
                        tmp_hashid = tmp_json['hash_id']
                        tmp_cover_page = tmp_json['cover_page']
                        tmp_html_data = tmp_json['html_data']
                        if tmp_html_data != None:
                            tmpurl_html_data = myUrl_domain + 'api/v1/html?group_id=' + str(tmp_groupid)
                        query_process = db.session.query(tb_process_request)\
                            .filter(and_(tb_process_request.group_id==str(tmp_groupid),tb_process_request.email==self.email_one))\
                            .order_by(desc(tb_process_request.datetime)).first()
                        if query_process != None:
                            tmp_json_process = query_process.__dict__
                            tmp_processid = tmp_json_process['id']
                        if tmp_maxstep != None:
                            try:                               
                                tmp_maxstep = eval(tmp_maxstep)                                
                            except Exception as e:                                
                                tmp_maxstep = str(tmp_maxstep)
                        # if tmp_step_group != None:
                        #     if tmp_step_group != '':
                        #         tmp_step_group = eval(tmp_step_group)
                        #         if len(tmp_step_group) != 0:
                        #             tmp_step_group = tmp_step_group[0]
                        #             print(tmp_step_group)
                        
                        if tmp_cover_page != None:
                            if tmp_cover_page != '':
                                tmp_cover_page = eval(tmp_cover_page)
                            else:
                                tmp_cover_page = None
                        if tmp_step_group_detail != None:
                            tmp_step_group_detail = eval(tmp_step_group_detail)
                        if tmp_pdf_sign != None:
                            tmp_pdf = tmp_pdf_sign
                        else:
                            tmp_pdf = tmp_pdf_org
                        jsonurl_info = None
                        if tmp_pdf != None:
                            url_downloadpdf = myUrl_domain + 'api/v1/download/group_pdf?groupid=' + tmp_hashid
                            url_viewpdf = myUrl_domain + 'api/v1/view/group_pdf?groupid=' + tmp_hashid
                            jsonurl_info = {'view_pdf':url_viewpdf,'download_pdf':url_downloadpdf}
                        list_file_name = []
                        # path_image = os.getcwd() + '/storage/image/' + self.group_id
                        path_image = path_global_1 + '/storage/image/' + self.group_id
                        try:
                            for the_file in os.listdir(path_image):
                                file_path = os.path.join(path_image, the_file)
                                # current_app.logger.info(file_path)
                                filename_only = str(file_path).split('/')[-1]
                                url_view_image = myUrl_domain + 'api/view2/pdf_image/' + self.group_id +'/' + filename_only
                                list_file_name.append({'image_Url': url_view_image})
                        except Exception as e:
                            list_file_name = []
                    if tmp_calculate_fieds != None:
                        tmp_calculate_fieds = eval(str(tmp_calculate_fieds))
                    status_viewGroup = False
                    if tmp_email_view_group != None:
                        tmp_email_view_group = eval(tmp_email_view_group)
                        if len(tmp_email_view_group) != 0:
                            for z in range(len(tmp_email_view_group)):
                                if self.email_one in tmp_email_view_group[z]['email_view_group']:
                                    status_viewGroup = True
                    if tmp_group_status == 'Y':
                        tmp_text_status = 'Y'
                        tmp_text_status_string = 'อนุมัติแล้ว'
                    elif tmp_group_status == 'R':
                        tmp_text_status = 'R'
                        tmp_text_status_string = 'ปฎิเสธอนุมัติ'
                    elif tmp_group_status == 'N':
                        if tmp_status_group != None:
                            tmp_status_group = eval(tmp_status_group)
                            for z in range(len(tmp_status_group)):
                                tmpstatusgroup = tmp_status_group[z]
                                tmp_arr_status_group.append(tmpstatusgroup['status'])
                                tmp_arr_status_email.append(tmpstatusgroup['email_one'])
                        # print(tmp_arr_status_group)
                        # print(tmp_arr_status_email)
                        count_email = tmp_arr_status_email.count(self.email_one)
                        for g in range(len(tmp_arr_status_group)):
                            tmpstatus = tmp_arr_status_group[g]
                            tmpemailone = tmp_arr_status_email[g]
                            if type(tmpemailone) is list:
                                for h in tmpemailone:
                                    if str(self.email_one).lower() == str(h).lower().replace(' ',''):
                                        my_status = tmpstatus
                                        tmpemailone = self.email_one
                            if tmpemailone == self.email_one:
                                my_status = tmpstatus
                            index_stepnum = g - 1
                            tmpbefore_status = tmp_arr_status_group[index_stepnum]
                            tmpbefore_emailone = tmp_arr_status_email[index_stepnum] 
                            if 'Reject' in tmp_arr_status_group:
                                step_now = g
                                tmparr_stepstatus.append('Reject')
                            elif tmpemailone == self.email_one and my_status == 'Incomplete_input':
                                step_now = g
                                tmparr_stepstatus.append('Wait_input')
                            elif tmpemailone == self.email_one and my_status == 'Incomplete_1':
                                step_now = g
                                tmparr_stepstatus.append('Incomplete')
                            elif tmpemailone == self.email_one and my_status == 'Incomplete':                                      
                                if self.email_one not in arr_email_list:
                                    index_step_me = g
                                    if index_step_me != 0:
                                        while index_step_me > 0:
                                            if len(tmparr_stepstatus) == 0:
                                                index_step_me = index_step_me - 1
                                                if tmp_arr_status_group[index_step_me] == 'Incomplete_1':
                                                    step_now = g
                                                    tmparr_stepstatus.append('Incomplete')
                                                elif tmp_arr_status_group[index_step_me] == 'Incomplete':
                                                    step_now = g
                                                    tmparr_stepstatus.append('Incomplete')
                                                    for kkk in range(len(tmp_arr_status_group)-1):
                                                        step_beforeMe.append(tmp_arr_status_group[kkk])
                                                else:
                                                    step_now = g
                                                    tmparr_stepstatus.append('Wait')
                                                arr_email_list.append(self.email_one)
                                            else:
                                                index_step_me = index_step_me - 1
                                                continue
                                    else:
                                        step_now = g
                                        tmparr_stepstatus.append('Wait')
                            elif tmpemailone == self.email_one and my_status == 'Complete':                                    
                                if self.email_one not in arr_email_list:
                                    if count_email == 1:
                                        for nz in range(g,len(tmp_arr_status_group),1):
                                            if self.email_one in tmp_arr_status_email[nz] and tmp_arr_status_group[nz] == 'Incomplete':
                                                step_now = g
                                                tmparr_stepstatus.append('Wait')
                                            elif self.email_one not in tmp_arr_status_email[nz] and tmp_arr_status_group[nz] == 'Incomplete':
                                                step_now = g
                                                tmparr_stepstatus.append('Progress')
                                        arr_email_list.append(self.email_one)
                                    else:                                                
                                        for nz in range(g,len(tmp_arr_status_group),1):
                                            if self.email_one not in arr_email_list:
                                                if self.email_one in tmp_arr_status_email[nz] and tmp_arr_status_group[nz] == 'Complete':
                                                    pass                                                    
                                                if self.email_one in tmp_arr_status_email[nz] and tmp_arr_status_group[nz] == 'Incomplete':
                                                    step_now = g
                                                    tmparr_stepstatus.append('Wait')
                                                    arr_email_list.append(self.email_one)
                                                if self.email_one not in tmp_arr_status_email[nz] and tmp_arr_status_group[nz] == 'Incomplete':
                                                    step_now = g
                                                    tmparr_stepstatus.append('Progress')
                                                    arr_email_list.append(self.email_one)
                            tmp_arr_status_group_001.append(tmpstatus)

                        if 'Reject' in tmparr_stepstatus:
                            tmp_text_status = 'R'
                            tmp_text_status_string = 'เอกสารที่ส่งคืนแก้ไข'
                        elif 'Wait_input' in tmparr_stepstatus:
                            tmp_text_status = 'WI'
                            tmp_text_status_string = 'รอคุณกรอกข้อมูล'
                        elif 'V' in tmparr_stepstatus:   
                            tmp_text_status = 'V'
                            tmp_text_status_string = 'ดูเอกสาร'
                        elif 'Progress' in tmparr_stepstatus and 'Wait' in tmparr_stepstatus:
                            # tmp_text_status = 'Z'
                            # tmp_text_status_string = 'อยู่ในช่วงดำเนินการ'
                            tmp_text_status = 'N'
                            tmp_text_status_string = 'กำลังดำเนินการ' 
                        elif 'Wait' in tmparr_stepstatus:
                            tmp_text_status = 'W'
                            tmp_text_status_string = 'รอคุณอนุมัติ'
                        elif 'Incomplete' in tmparr_stepstatus:
                            # tmp_text_status = 'Z'
                            # tmp_text_status_string = 'อยู่ในช่วงดำเนินการ'
                            tmp_text_status = 'N'
                            tmp_text_status_string = 'กำลังดำเนินการ'
                            if 'Complete' not in step_beforeMe:
                                tmp_text_status = 'Z'
                                tmp_text_status_string = 'อยู่ในช่วงดำเนินการ' 
                        elif 'Progress' in tmparr_stepstatus:
                            tmp_text_status = 'N'
                            tmp_text_status_string = 'กำลังดำเนินการ'                    
                        elif tmparr_stepstatus.count('Incomplete') >= 2:
                            # tmp_text_status = 'Z'
                            # tmp_text_status_string = 'อยู่ในช่วงดำเนินการ'
                            tmp_text_status = 'N'
                            tmp_text_status_string = 'กำลังดำเนินการ' 
                        elif 'Incomplete' in tmparr_stepstatus and 'Complete' in tmparr_stepstatus:
                            tmp_text_status = 'N'
                            tmp_text_status_string = 'กำลังดำเนินการ'
                        else:
                            tmp_text_status = 'N'
                            tmp_text_status_string = 'กำลังดำเนินการ'
                    
                    if tmp_sidgroup != None:
                        tmp_sidgroup = eval(tmp_sidgroup)
                    if tmp_updatetime != None:
                        tmp_updatetime = tmp_updatetime
                        tmp_datetimeString = str(tmp_updatetime).split('+')[0]
                    if tmp_group_other != None:
                        tmp_group_other = eval(tmp_group_other)
                        for i in range(len(tmp_group_other)):
                            if 'color' in tmp_group_other[i]:
                                tmp_color = tmp_group_other[i]['color']
                    if tmp_group_data_json != None:
                        tmp_group_data_json = eval(tmp_group_data_json)
                        for o in range(len(tmp_group_data_json)):
                            if 'data_sum' in tmp_group_data_json[o]:
                                tmp_data_sum = tmp_group_data_json[o]['data_sum']
                                for z in range(len(tmp_data_sum)):
                                    if 'name' in tmp_data_sum[z]:
                                        tmp_key = str(tmp_data_sum[z]['name']).replace(' ','')
                                        tmp_value = (tmp_data_sum[z]['value'])
                                        json_tmp[tmp_key] = tmp_value
                                        # arr_data_sum.append({tmp_key:tmp_value})
                                tmp_arr_data_sum_01.append(json_tmp)
                            else:
                                if len(tmp_group_data_json[o]) != 0:
                                    tmp_group_data_json[o][0]['No_keyno_ppl'] = (o + 1)
                                    tmp_arr_data_sum_01.append(tmp_group_data_json[o][0])
                    if tmp_json_data != None:
                        if tmp_json_data != 'None':
                            tmp_arr_data_sum_01 = eval(tmp_json_data)
                    dateTime_String = tmp_updatetime
                    th_dateTime_2 = convert_datetime_TH_2(int(dateTime_String.timestamp()))
                    ts = int(time.time())
                    date_time_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    year_today = datetime.datetime.fromtimestamp(ts).strftime('%Y')
                    datetime_display = int(dateTime_String.timestamp())
                    date_time_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y-%m-%d')
                    yar_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%Y')
                    time_show_db = datetime.datetime.fromtimestamp(datetime_display).strftime('%H:%M')
                    old_year = datetime.datetime.fromtimestamp(datetime_display).strftime('%d/%m/%Y')
                    if date_time_today == date_time_db:
                        date_display_show = time_show_db
                    else:
                        if year_today == yar_db:
                            date_display_show = convert_datetime_TH_2_display(datetime_display)
                        else:
                            date_display_show = old_year
                    if tmp_step_group != None:
                        if tmp_step_group != '':
                            tmp_step_group = eval(tmp_step_group)
                            if len(tmp_step_group) != 0:
                                for j in range(len(tmp_step_group)):
                                    if 'step_num' in tmp_step_group[j]: 
                                        if len(tmp_arr_status_email) != 0:
                                            for hy in range(len(tmp_arr_status_email[step_now])):
                                                if tmp_arr_status_email[step_now][hy] == self.email_one:                        
                                                    tmparr_stepnum.append(tmp_step_group[j]['step_num'][step_now])
                    result_sum = sum_doc_name_group_v2(eval(tmp_json['doctype_group']))
                    if result_sum['result'] == 'ER':
                        result_sum['messageText'] = []
                    result_sum_biz = sum_biz_info_group(eval(tmp_json['bizinfo_group']))
                    if self.status != None :
                        if tmp_text_status == self.status :      
                            if count_data < int(self.limit):           
                                tmp_arrjson.append({
                                    'status':tmp_status,
                                    'group_id':tmp_groupid,
                                    'sid_group':tmp_sidgroup,
                                    'color_group':tmp_color,
                                    'datetime':int(tmp_updatetime.timestamp()),
                                    'datetime_string':tmp_datetimeString,
                                    'datetime_display':date_display_show,
                                    'datetime_thai':th_dateTime_2,
                                    'document_count':len(tmp_sidgroup),
                                    'document_data':tmp_arr_data_sum_01,
                                    'status_group':tmp_text_status,
                                    'status_group_string':tmp_text_status_string,
                                    'viewgroup':status_viewGroup,
                                    'calculate_fieds':tmp_calculate_fieds,
                                    'image_display':list_file_name,
                                    'sign_position':tmp_step_group_detail,
                                    'pdf_info':tmp_pdf,
                                    'url_info':jsonurl_info,
                                    'group_title':tmp_group_title,
                                    'cover_page':tmp_cover_page,
                                    'biz_info':data_biz,
                                    'document_type_detail':tmpdocumentdetail,
                                    'step_group_document':tmparr_stepnum,
                                    'max_step':tmp_maxstep,
                                    'process_id':tmp_processid,
                                    'html_data':tmp_html_data,
                                    'html_url':tmpurl_html_data,
                                    'tracking_id':tmp_tracking_group,
                                    'average_data':tmp_average_data,
                                    'data_group': eval(tmp_json['data_group']),
                                    'doctype_group': eval(tmp_json['doctype_group']),
                                    'bizinfo_group': eval(tmp_json['bizinfo_group']),
                                    'total_document_type':result_sum['messageText'],
                                    'total_biz':result_sum_biz['messageText'],
                                    'group_name':tmp_json['group_name'],
                                    'sum_documentType': len(result_sum['messageText'])
                                })
                                count_data += 1
                            else:
                                break
                    else:
                        if tmp_text_status == 'Y' or tmp_text_status == 'N' or tmp_text_status == 'W' :      
                            if count_data < int(self.limit):           
                                tmp_arrjson.append({
                                    'status':tmp_status,
                                    'group_id':tmp_groupid,
                                    'sid_group':tmp_sidgroup,
                                    'color_group':tmp_color,
                                    'datetime':int(tmp_updatetime.timestamp()),
                                    'datetime_string':tmp_datetimeString,
                                    'datetime_display':date_display_show,
                                    'datetime_thai':th_dateTime_2,
                                    'document_count':len(tmp_sidgroup),
                                    'document_data':tmp_arr_data_sum_01,
                                    'status_group':tmp_text_status,
                                    'status_group_string':tmp_text_status_string,
                                    'viewgroup':status_viewGroup,
                                    'calculate_fieds':tmp_calculate_fieds,
                                    'image_display':list_file_name,
                                    'sign_position':tmp_step_group_detail,
                                    'pdf_info':tmp_pdf,
                                    'url_info':jsonurl_info,
                                    'group_title':tmp_group_title,
                                    'cover_page':tmp_cover_page,
                                    'biz_info':data_biz,
                                    'document_type_detail':tmpdocumentdetail,
                                    'step_group_document':tmparr_stepnum,
                                    'max_step':tmp_maxstep,
                                    'process_id':tmp_processid,
                                    'html_data':tmp_html_data,
                                    'html_url':tmpurl_html_data,
                                    'tracking_id':tmp_tracking_group,
                                    'average_data':tmp_average_data,
                                    'data_group': eval(tmp_json['data_group']),
                                    'doctype_group': eval(tmp_json['doctype_group']),
                                    'bizinfo_group': eval(tmp_json['bizinfo_group']),
                                    'total_document_type':result_sum['messageText'],
                                    'total_biz':result_sum_biz['messageText'],
                                    'group_name':tmp_json['group_name'],
                                    'sum_documentType': len(result_sum['messageText'])
                                })
                                count_data += 1
                            else:
                                break
                print(len(tmp_arrjson))
                print('*****************')
                return {'result':'OK','messageText':tmp_arrjson}
            else:
                return {'result':'ER','messageER':'data not found'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':'not found','status_Code':200,'messageER':str(e)}


    def select_offset_querydocGroupVersion2(self,email_one,document_type,tax_id,status,offset,keyword):
        self.email_one = email_one
        # self.document_type = document_type
        self.tax_id = tax_id
        self.status = status
        self.offset = offset
        self.keyword = keyword
        Complete_Approve = 0
        Incomplete_Pendding = 0
        Reject = 0
        Wait = 0
        status_Z = 0
        countOffset = 0
        tmp_arrjson = []
        txtQuery = ''
        tmp_query = []
        count = 0
        try:
            queryString = '''"status" = 'ACTIVE' AND "sid_group" != '[]' '''
            if self.email_one != None :
                queryString += '''AND ("email_view_group" LIKE '%'''+ self.email_one +'''%' OR status_group LIKE '%'''+ self.email_one +'''%') '''
            if self.tax_id != None and self.tax_id != '' :
                queryString += '''AND bizinfo LIKE '%'''+ self.tax_id +'''%' '''
            else:
                queryString += '''AND (bizinfo = '' OR bizinfo IS NULL)'''
            # if self.document_type != None :
            #     queryString += "AND document_type = '"+ str(self.document_type) +"'"   
            if self.status == 'N' or self.status == 'W' :
                queryString += "AND group_status = 'N'"       
            if self.keyword == None:
                query_sql = '''SELECT "status","status_group","group_status" FROM "tb_group_document_2" WHERE '''+queryString+''' ORDER BY "updatetime" DESC'''
            else:
                try:      
                    dats = datetime.datetime.strptime(self.keyword, '%Y-%m-%d')
                    datetime1 = dats.strftime('%Y-%m-%d 00:00:00')
                    datetime2 = dats.strftime('%Y-%m-%d 23:59:59')       
                    query_sql = "SELECT * FROM tb_group_document_2 WHERE "+ queryString +" AND updatetime >= '"+datetime1+"' AND updatetime <= '"+datetime2+"' ORDER BY updatetime DESC"                     
                except ValueError:
                    print('key not datetime') 
                    if self.keyword == '':
                        query_sql = '''SELECT status,status_group,group_status FROM "tb_group_document_2" WHERE '''+queryString+''' ORDER BY "updatetime" DESC'''
                    else:   
                        query_sql = '''SELECT status,status_group,group_status FROM "tb_group_document_2" WHERE '''+queryString+''' AND json_data LIKE '%'''+ self.keyword +'''%' ORDER BY "updatetime" DESC'''         
            
            with engine.connect() as connection:
                print(query_sql)
                result_select = connection.execute(text(query_sql))
                tmp_query = [dict(row) for row in result_select]
                connection.close()
            
            if len(tmp_query) != 0:
                print(len(tmp_query))
                for n in range(len(tmp_query)):
                    tmp_arr_status_group = []
                    tmp_arr_status_email = []
                    tmp_arr_status_group_001 = []
                    tmparr_stepstatus = []
                    arr_email_list = []
                    tmp_text_status = 'Y'
                    tmp_text_status_string = 'อนุมัติแล้ว'  
                    tmp_json = tmp_query[n]
                    tmp_status = tmp_json['status']
                    tmp_status_group = tmp_json['status_group']
                    tmp_group_status = tmp_json['group_status']
                    # tmp_group_status = tmp_json['group_status']
                    if tmp_group_status == None:
                        tmp_group_status = 'N'
                    # tmp_document_type = tmp_json['document_type']
                    if tmp_group_status == 'Y':
                        tmp_text_status = 'Y'
                        tmp_text_status_string = 'อนุมัติแล้ว'
                        Complete_Approve += 1
                    elif tmp_group_status == 'R':
                        tmp_text_status = 'R'
                        tmp_text_status_string = 'ปฎิเสธอนุมัติ'
                    elif tmp_group_status == 'N':
                        if tmp_status_group != None:
                            tmp_status_group = eval(tmp_status_group)
                            for z in range(len(tmp_status_group)):
                                tmpstatusgroup = tmp_status_group[z]
                                tmp_arr_status_group.append(tmpstatusgroup['status'])
                                tmp_arr_status_email.append(tmpstatusgroup['email_one'])
                        count_email = tmp_arr_status_email.count(self.email_one)
                        for g in range(len(tmp_arr_status_group)):
                            tmpstatus = tmp_arr_status_group[g]
                            tmpemailone = tmp_arr_status_email[g]
                            if type(tmpemailone) is list:
                                for h in tmpemailone:
                                    if str(self.email_one).lower() == str(h).lower().replace(' ',''):
                                        my_status = tmpstatus
                                        tmpemailone = self.email_one
                            if tmpemailone == self.email_one:
                                my_status = tmpstatus
                            index_stepnum = g - 1
                            tmpbefore_status = tmp_arr_status_group[index_stepnum]
                            tmpbefore_emailone = tmp_arr_status_email[index_stepnum] 
                            if 'Reject' in tmp_arr_status_group:
                                step_now = g
                                tmparr_stepstatus.append('Reject')
                            elif tmpemailone == self.email_one and my_status == 'Incomplete_input':
                                step_now = g
                                tmparr_stepstatus.append('Wait_input')
                            elif tmpemailone == self.email_one and my_status == 'Incomplete_1':
                                step_now = g
                                tmparr_stepstatus.append('Incomplete')
                            elif tmpemailone == self.email_one and my_status == 'Incomplete':                                      
                                if self.email_one not in arr_email_list:
                                    index_step_me = g
                                    if index_step_me != 0:
                                        while index_step_me > 0:
                                            if len(tmparr_stepstatus) == 0:
                                                index_step_me = index_step_me - 1
                                                if tmp_arr_status_group[index_step_me] == 'Incomplete_1':
                                                    step_now = g
                                                    tmparr_stepstatus.append('Incomplete')
                                                elif tmp_arr_status_group[index_step_me] == 'Incomplete':
                                                    step_now = g
                                                    tmparr_stepstatus.append('Incomplete')
                                                else:
                                                    step_now = g
                                                    tmparr_stepstatus.append('Wait')
                                                arr_email_list.append(self.email_one)
                                            else:
                                                index_step_me = index_step_me - 1
                                                continue
                                    else:
                                        step_now = g
                                        tmparr_stepstatus.append('Wait')
                            elif tmpemailone == self.email_one and my_status == 'Complete':                                    
                                if self.email_one not in arr_email_list:
                                    if count_email == 1:
                                        for nz in range(g,len(tmp_arr_status_group),1):
                                            if self.email_one in tmp_arr_status_email[nz] and tmp_arr_status_group[nz] == 'Incomplete':
                                                step_now = g
                                                tmparr_stepstatus.append('Wait')
                                            elif self.email_one not in tmp_arr_status_email[nz] and tmp_arr_status_group[nz] == 'Incomplete':
                                                step_now = g
                                                tmparr_stepstatus.append('Progress')
                                        arr_email_list.append(self.email_one)
                                    else:                                                
                                        for nz in range(g,len(tmp_arr_status_group),1):
                                            if self.email_one not in arr_email_list:
                                                if self.email_one in tmp_arr_status_email[nz] and tmp_arr_status_group[nz] == 'Complete':
                                                    pass                                                    
                                                if self.email_one in tmp_arr_status_email[nz] and tmp_arr_status_group[nz] == 'Incomplete':
                                                    step_now = g
                                                    tmparr_stepstatus.append('Wait')
                                                    arr_email_list.append(self.email_one)
                                                if self.email_one not in tmp_arr_status_email[nz] and tmp_arr_status_group[nz] == 'Incomplete':
                                                    step_now = g
                                                    tmparr_stepstatus.append('Progress')
                                                    arr_email_list.append(self.email_one)
                            tmp_arr_status_group_001.append(tmpstatus)

                        if 'Reject' in tmparr_stepstatus:
                            tmp_text_status = 'R'
                            tmp_text_status_string = 'เอกสารที่ส่งคืนแก้ไข'
                            Reject += 1
                        elif 'Wait_input' in tmparr_stepstatus:
                            tmp_text_status = 'WI'
                            tmp_text_status_string = 'รอคุณกรอกข้อมูล'
                        elif 'V' in tmparr_stepstatus:   
                            tmp_text_status = 'V'
                            tmp_text_status_string = 'ดูเอกสาร'
                        elif 'Progress' in tmparr_stepstatus and 'Wait' in tmparr_stepstatus:
                            tmp_text_status = 'Z'
                            tmp_text_status_string = 'อยู่ในช่วงดำเนินการ'
                            status_Z += 1
                            Incomplete_Pendding += 1
                        elif 'Wait' in tmparr_stepstatus:
                            tmp_text_status = 'W'
                            tmp_text_status_string = 'รอคุณอนุมัติ'
                            Wait += 1
                        elif 'Incomplete' in tmparr_stepstatus:
                            tmp_text_status = 'Z'
                            tmp_text_status_string = 'อยู่ในช่วงดำเนินการ'
                            status_Z += 1
                            Incomplete_Pendding += 1
                        elif 'Progress' in tmparr_stepstatus:
                            tmp_text_status = 'N'
                            tmp_text_status_string = 'กำลังดำเนินการ'   
                            Incomplete_Pendding += 1
                        elif tmparr_stepstatus.count('Incomplete') >= 2:
                            tmp_text_status = 'Z'
                            tmp_text_status_string = 'อยู่ในช่วงดำเนินการ'
                            status_Z += 1
                            Incomplete_Pendding += 1
                        elif 'Incomplete' in tmparr_stepstatus and 'Complete' in tmparr_stepstatus:
                            tmp_text_status = 'N'
                            tmp_text_status_string = 'กำลังดำเนินการ'
                            Incomplete_Pendding += 1
                        else:
                            tmp_text_status = 'N'
                            tmp_text_status_string = 'กำลังดำเนินการ'
                            Incomplete_Pendding += 1
                
                    sum_document_all = Complete_Approve + Incomplete_Pendding + Wait
                    offset = int(self.offset)                    
                    if self.status == None and offset == sum_document_all:
                        countOffset = n + 1
                        break
                    if self.status == 'Y' and offset == Complete_Approve:
                        countOffset = n + 1
                        break
                    if self.status == 'N' and offset == Incomplete_Pendding:
                        countOffset = n + 1
                        break
                    if self.status == 'W' and offset == Wait:
                        countOffset = n + 1
                        break
                print('countOffset',countOffset)
                return {'result':'OK','messageText': countOffset}  
            else:
                return {'result':'ER','messageER':'data not found'}          

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':'not found','status_Code':200,'messageER':str(e)}
 
    def select_offset_querydocGroupVersion2(self,email_one,document_type,tax_id,status,offset,keyword):
        self.email_one = email_one
        # self.document_type = document_type
        self.tax_id = tax_id
        self.status = status
        self.offset = offset
        self.keyword = keyword
        Complete_Approve = 0
        Incomplete_Pendding = 0
        Reject = 0
        Wait = 0
        status_Z = 0
        countOffset = 0
        tmp_arrjson = []
        txtQuery = ''
        tmp_query = []
        count = 0
        try:
            queryString = '''"status" = 'ACTIVE' AND "sid_group" != '[]' '''
            if self.email_one != None :
                queryString += '''AND ("email_view_group" LIKE '%'''+ self.email_one +'''%' OR status_group LIKE '%'''+ self.email_one +'''%') '''
            if self.tax_id != None and self.tax_id != '' :
                queryString += '''AND bizinfo LIKE '%'''+ self.tax_id +'''%' '''
            else:
                queryString += '''AND (bizinfo = '' OR bizinfo IS NULL)'''
            # if self.document_type != None :
            #     queryString += "AND document_type = '"+ str(self.document_type) +"'"   
            if self.status == 'N' or self.status == 'W' :
                queryString += "AND group_status = 'N'"       
            if self.keyword == None:
                query_sql = '''SELECT "status","status_group","group_status" FROM "tb_group_document_2" WHERE '''+queryString+''' ORDER BY "updatetime" DESC'''
            else:
                try:      
                    dats = datetime.datetime.strptime(self.keyword, '%Y-%m-%d')
                    datetime1 = dats.strftime('%Y-%m-%d 00:00:00')
                    datetime2 = dats.strftime('%Y-%m-%d 23:59:59')       
                    query_sql = "SELECT * FROM tb_group_document_2 WHERE "+ queryString +" AND updatetime >= '"+datetime1+"' AND updatetime <= '"+datetime2+"' ORDER BY updatetime DESC"                     
                except ValueError:
                    print('key not datetime') 
                    if self.keyword == '':
                        query_sql = '''SELECT status,status_group,group_status FROM "tb_group_document_2" WHERE '''+queryString+''' ORDER BY "updatetime" DESC'''
                    else:   
                        query_sql = '''SELECT * FROM "tb_group_document_2" WHERE '''+queryString+''' AND (doctype_group LIKE '%'''+ self.keyword +'''%'  or group_name LIKE '%'''+ self.keyword +'''%') ORDER BY "updatetime" DESC limit(:limit) offset(:offset)'''         
            
            with engine.connect() as connection:
                # print(query_sql)
                result_select = connection.execute(text(query_sql))
                tmp_query = [dict(row) for row in result_select]
                connection.close()
            
            if len(tmp_query) != 0:
                print(len(tmp_query))
                for n in range(len(tmp_query)):
                    tmp_arr_status_group = []
                    tmp_arr_status_email = []
                    tmp_arr_status_group_001 = []
                    tmparr_stepstatus = []
                    arr_email_list = []
                    tmp_text_status = 'Y'
                    tmp_text_status_string = 'อนุมัติแล้ว'  
                    tmp_json = tmp_query[n]
                    tmp_status = tmp_json['status']
                    tmp_status_group = tmp_json['status_group']
                    tmp_group_status = tmp_json['group_status']
                    # tmp_group_status = tmp_json['group_status']
                    if tmp_group_status == None:
                        tmp_group_status = 'N'
                    # tmp_document_type = tmp_json['document_type']
                    if tmp_group_status == 'Y':
                        tmp_text_status = 'Y'
                        tmp_text_status_string = 'อนุมัติแล้ว'
                        Complete_Approve += 1
                    elif tmp_group_status == 'R':
                        tmp_text_status = 'R'
                        tmp_text_status_string = 'ปฎิเสธอนุมัติ'
                    elif tmp_group_status == 'N':
                        if tmp_status_group != None:
                            tmp_status_group = eval(tmp_status_group)
                            for z in range(len(tmp_status_group)):
                                tmpstatusgroup = tmp_status_group[z]
                                tmp_arr_status_group.append(tmpstatusgroup['status'])
                                tmp_arr_status_email.append(tmpstatusgroup['email_one'])
                        count_email = tmp_arr_status_email.count(self.email_one)
                        for g in range(len(tmp_arr_status_group)):
                            tmpstatus = tmp_arr_status_group[g]
                            tmpemailone = tmp_arr_status_email[g]
                            if type(tmpemailone) is list:
                                for h in tmpemailone:
                                    if str(self.email_one).lower() == str(h).lower().replace(' ',''):
                                        my_status = tmpstatus
                                        tmpemailone = self.email_one
                            if tmpemailone == self.email_one:
                                my_status = tmpstatus
                            index_stepnum = g - 1
                            tmpbefore_status = tmp_arr_status_group[index_stepnum]
                            tmpbefore_emailone = tmp_arr_status_email[index_stepnum] 
                            if 'Reject' in tmp_arr_status_group:
                                step_now = g
                                tmparr_stepstatus.append('Reject')
                            elif tmpemailone == self.email_one and my_status == 'Incomplete_input':
                                step_now = g
                                tmparr_stepstatus.append('Wait_input')
                            elif tmpemailone == self.email_one and my_status == 'Incomplete_1':
                                step_now = g
                                tmparr_stepstatus.append('Incomplete')
                            elif tmpemailone == self.email_one and my_status == 'Incomplete':                                      
                                if self.email_one not in arr_email_list:
                                    index_step_me = g
                                    if index_step_me != 0:
                                        while index_step_me > 0:
                                            if len(tmparr_stepstatus) == 0:
                                                index_step_me = index_step_me - 1
                                                if tmp_arr_status_group[index_step_me] == 'Incomplete_1':
                                                    step_now = g
                                                    tmparr_stepstatus.append('Incomplete')
                                                elif tmp_arr_status_group[index_step_me] == 'Incomplete':
                                                    step_now = g
                                                    tmparr_stepstatus.append('Incomplete')
                                                else:
                                                    step_now = g
                                                    tmparr_stepstatus.append('Wait')
                                                arr_email_list.append(self.email_one)
                                            else:
                                                index_step_me = index_step_me - 1
                                                continue
                                    else:
                                        step_now = g
                                        tmparr_stepstatus.append('Wait')
                            elif tmpemailone == self.email_one and my_status == 'Complete':                                    
                                if self.email_one not in arr_email_list:
                                    if count_email == 1:
                                        for nz in range(g,len(tmp_arr_status_group),1):
                                            if self.email_one in tmp_arr_status_email[nz] and tmp_arr_status_group[nz] == 'Incomplete':
                                                step_now = g
                                                tmparr_stepstatus.append('Wait')
                                            elif self.email_one not in tmp_arr_status_email[nz] and tmp_arr_status_group[nz] == 'Incomplete':
                                                step_now = g
                                                tmparr_stepstatus.append('Progress')
                                        arr_email_list.append(self.email_one)
                                    else:                                                
                                        for nz in range(g,len(tmp_arr_status_group),1):
                                            if self.email_one not in arr_email_list:
                                                if self.email_one in tmp_arr_status_email[nz] and tmp_arr_status_group[nz] == 'Complete':
                                                    pass                                                    
                                                if self.email_one in tmp_arr_status_email[nz] and tmp_arr_status_group[nz] == 'Incomplete':
                                                    step_now = g
                                                    tmparr_stepstatus.append('Wait')
                                                    arr_email_list.append(self.email_one)
                                                if self.email_one not in tmp_arr_status_email[nz] and tmp_arr_status_group[nz] == 'Incomplete':
                                                    step_now = g
                                                    tmparr_stepstatus.append('Progress')
                                                    arr_email_list.append(self.email_one)
                            tmp_arr_status_group_001.append(tmpstatus)

                        if 'Reject' in tmparr_stepstatus:
                            tmp_text_status = 'R'
                            tmp_text_status_string = 'เอกสารที่ส่งคืนแก้ไข'
                            Reject += 1
                        elif 'Wait_input' in tmparr_stepstatus:
                            tmp_text_status = 'WI'
                            tmp_text_status_string = 'รอคุณกรอกข้อมูล'
                        elif 'V' in tmparr_stepstatus:   
                            tmp_text_status = 'V'
                            tmp_text_status_string = 'ดูเอกสาร'
                        elif 'Progress' in tmparr_stepstatus and 'Wait' in tmparr_stepstatus:
                            tmp_text_status = 'Z'
                            tmp_text_status_string = 'อยู่ในช่วงดำเนินการ'
                            status_Z += 1
                            Incomplete_Pendding += 1
                        elif 'Wait' in tmparr_stepstatus:
                            tmp_text_status = 'W'
                            tmp_text_status_string = 'รอคุณอนุมัติ'
                            Wait += 1
                        elif 'Incomplete' in tmparr_stepstatus:
                            tmp_text_status = 'Z'
                            tmp_text_status_string = 'อยู่ในช่วงดำเนินการ'
                            status_Z += 1
                            Incomplete_Pendding += 1
                        elif 'Progress' in tmparr_stepstatus:
                            tmp_text_status = 'N'
                            tmp_text_status_string = 'กำลังดำเนินการ'   
                            Incomplete_Pendding += 1
                        elif tmparr_stepstatus.count('Incomplete') >= 2:
                            tmp_text_status = 'Z'
                            tmp_text_status_string = 'อยู่ในช่วงดำเนินการ'
                            status_Z += 1
                            Incomplete_Pendding += 1
                        elif 'Incomplete' in tmparr_stepstatus and 'Complete' in tmparr_stepstatus:
                            tmp_text_status = 'N'
                            tmp_text_status_string = 'กำลังดำเนินการ'
                            Incomplete_Pendding += 1
                        else:
                            tmp_text_status = 'N'
                            tmp_text_status_string = 'กำลังดำเนินการ'
                            Incomplete_Pendding += 1
                
                    sum_document_all = Complete_Approve + Incomplete_Pendding + Wait
                    offset = int(self.offset)                    
                    if self.status == None and offset == sum_document_all:
                        countOffset = n + 1
                        break
                    if self.status == 'Y' and offset == Complete_Approve:
                        countOffset = n + 1
                        break
                    if self.status == 'N' and offset == Incomplete_Pendding:
                        countOffset = n + 1
                        break
                    if self.status == 'W' and offset == Wait:
                        countOffset = n + 1
                        break
                print('countOffset',countOffset)
                return {'result':'OK','messageText': countOffset}  
            else:
                return {'result':'ER','messageER':'data not found'}          

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':'not found','status_Code':200,'messageER':str(e)}
 
    def select_querydoc_group_version2(self,email_one,group_id,tax_id,status,limit,offset,keyword):
        try:
            self.email_one = email_one
            # self.document_type = document_type
            self.group_id = group_id
            self.tax_id = tax_id
            self.status = status
            self.limit = limit
            self.offset = offset
            self.keyword = keyword
            tmp_arrjson = []
            if self.group_id == None:
                limit = int(self.limit)
                offset = int(self.offset)
                if offset != 0:
                    result_offset = select_2().select_offset_querydocGroupVersion2(self.email_one,self.tax_id,self.status,self.limit,self.offset,keyword)
                    if result_offset['result'] == 'OK':                
                        offset = result_offset['messageText']
                        
                result = select_2().recursive_select_querydocGroupVersion2(self.email_one,self.group_id,self.tax_id,self.status,self.limit,offset,self.keyword,len(tmp_arrjson))
                if result['result'] == 'OK':                
                    tmp_arrjson = result['messageText']
                    offset += limit
                    while len(tmp_arrjson) < limit :                    
                        result2 = select_2().recursive_select_querydocGroupVersion2(self.email_one,self.group_id,self.tax_id,self.status,self.limit,offset,self.keyword,len(tmp_arrjson))
                        if result2['result'] == 'OK':
                            tmp_arrjson.extend(result2['messageText'])
                            offset += limit
                        else:
                            break
                    print(len(tmp_arrjson))
                    return {'result':'OK','messageText':tmp_arrjson}
                else:
                    return {'result':'ER','messageER':'data not found'}      
            else:
                self.limit = 1
                result = select_2().recursive_select_querydocGroupVersion2(self.email_one,self.group_id,self.tax_id,self.status,self.limit,offset,self.keyword,len(tmp_arrjson))
                return {'result':'OK','messageText': result['messageText']}

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':'not found','status_Code':200,'messageER':str(e)}
    
    


    def select_DocumentDetail(self,taxid,documentType):
        self.taxid = taxid
        self.documentType = documentType
        try:
            arr_data = []
            query_tmp = paper_lessdocument_detail.query.filter(paper_lessdocument_detail.biz_info.contains(self.taxid),paper_lessdocument_detail.documentStatus=='ACTIVE',\
            paper_lessdocument_detail.documentType==self.documentType).all()
            for u in range(len(query_tmp)):
                tmp_json = query_tmp[u].__dict__
                del tmp_json['_sa_instance_state']
                try:
                    tmp_business_json = eval(tmp_json['biz_info'])
                except Exception as e:
                    tmp_business_json = None
                if tmp_json['other_service_permission'] != None:
                    tmp_service_other = eval(tmp_json['other_service_permission'])
                else:
                    tmp_service_other = None
                if tmp_json['chat_bot'] != None:
                    tmp_chatbot = eval(tmp_json['chat_bot'])
                else:
                    tmp_chatbot = None
                jsondata = {
                    'documentJson':eval(tmp_json['documentJson']),
                    'documentUser':tmp_json['documentUser'],
                    'documentUpdate':tmp_json['documentUpdate'],
                    'documentUpdate_string':str(tmp_json['documentUpdate']),
                    'email':tmp_json['email'],
                    'documentType':tmp_json['documentType'],
                    'documentCode':tmp_json['documentCode'],
                    'status':tmp_json['documentStatus'],
                    'business_json':tmp_business_json,
                    'business_string':str(tmp_json['biz_info']),
                    'create_service':str(tmp_json['service_permission']),
                    'service_other':(tmp_service_other),
                    'chat_bot':tmp_chatbot
                }
                arr_data.append(jsondata)
            if len(arr_data) != 0:
                return {'result':'OK','messageText':arr_data}
            else:
                return {'result':'ER','messageText':'ไม่พบข้อมูล'}
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def rejectdoc_to_eform(self,sid,token_header):
        self.sid = sid
        self.token_header = token_header
        try:
            result_check_efprm = select_2().check_from_eform(self.sid)
            if result_check_efprm['result'] == 'OK' and result_check_efprm['messageText'] == 'eformppl':
                result_select_hash_sid = select_2().select_hash_sid(self.sid)
                if result_select_hash_sid['result'] == 'OK':
                    hash_sid = result_select_hash_sid['messageText']
                    result_call = callPost_eform_reject(self.token_header,hash_sid)
                    return {'result':'OK','status_Code':200,'messageText':result_call['messageText'],'messageER':None}
                else:
                    return {'result':'ER','status_Code':200,'messageText':None,'messageER':result_select_hash_sid['messageText']}
            else:
                return {'result':'ER','status_Code':200,'messageText':None,'messageER':result_check_efprm['messageText']}
        except Exception as e:
            print (str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','status_Code':200,'messageText':None,'messageER':'Fails!'}

    def check_from_eform(self,sid):
        try:
            self.sid = sid
            with slave.connect() as connection:
                result = connection.execute(text('SELECT "data_document" FROM "tb_doc_detail" WHERE "step_id" =:sid'),sid=self.sid)
                connection.close()
            tmp_query = [dict(row) for row in result]
            if tmp_query == []:
                return {'result':'ER','messageText':'Not found'}
            elif tmp_query != []:
                tmp_query = tmp_query[0]
            data_document = tmp_query['data_document']
            result_gen = data_doc(data_document)
            if result_gen['result'] == 'OK':
                if result_gen['messageText']['sub'] == 'eformppl':
                    return {'result':'OK','messageText':result_gen['messageText']['sub']}
                else:
                    return {'result':'ER','messageText':'Doc from sub '+result_gen['messageText']['sub']}
            else:
                return {'result':'ER','messageText':'Fails!'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def select_hash_sid(self,sid):
        try:
            self.sid = sid
            with slave.connect() as connection:
                result = connection.execute(text('SELECT "hash_sid_code" FROM "tb_track_paper" WHERE "step_data_sid" =:sid'),sid=self.sid)
                connection.close()
            tmp_query = [dict(row) for row in result]
            if tmp_query != []:
                return {'result':'OK','messageText':tmp_query[0]['hash_sid_code']}
            else:
                return {'result':'ER','messageText':'Not Found'}
        except Exception as e:
            print (str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}
    # ไม่มี document_type
    def select_tmpgroup_list_2(self,username=None,tax_id=None,id_data=None):
        try:
            self.username = username
            self.tax_id = tax_id
            self.id = id_data
            tax_id = '%{}%'.format(self.tax_id)
            query_result_select = None
            list_json = []
            tmp_query ={}
            stringQuery1 = ''' SELECT "group_name","group_code","template","group_title","step_group","status","create_date","update_date","group_data","biz_info","create_by","update_by",
                "use_status","cover_page","tid","group_color","email_middle","timegroup_auto","daygroup_auto" FROM "tb_group_template_2" '''
            print(self.username,self.tax_id,self.id)
            if self.id != None: # มี ID
                with engine.connect() as connection:
                    result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "tid" = :tid AND "status" = 'ACTIVE' ORDER BY "create_date" DESC  ''')\
                        ,tid=self.id)
                    connection.close()
                result_select = [dict(row) for row in result]
            elif self.tax_id != None and self.username == None and self.id == None : # มี TAX_ID ไม่มี username
                with engine.connect() as connection:
                    result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "biz_info" LIKE :tax_id AND "status" = 'ACTIVE' ORDER BY "create_date" DESC ''')\
                        ,tax_id=tax_id)
                    connection.close()    
                result_select = [dict(row) for row in result]             
            elif self.tax_id == None and self.username != None and self.id == None : # มี username ไม่มี TAX_ID 
                with engine.connect() as connection:
                    result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "create_by" = :username AND "biz_info" = '' AND "status" = 'ACTIVE' ORDER BY "create_date" DESC ''')\
                        ,username=self.username)
                    connection.close()  
                result_select = [dict(row) for row in result]    
            elif self.username == None and self.tax_id == None and self.id == None : # ไม่มี username ไม่มี tax_id 
                with engine.connect() as connection:
                    result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "status" = 'ACTIVE' ORDER BY "create_date" DESC ''')\
                        ,)
                    connection.close()
                result_select = [dict(row) for row in result]
            elif self.tax_id == None and self.username == None and self.id == None : # ไม่มีอะไรเลยยยย
                return {'result':'ER','messageText':None,'messageER':'Not have data','status_Code':404}
            else:
                return {'result':'ER','messageText':None,'messageER':'Parameter incorrect','status_Code':404} 

            if result_select == []:
                return {'result':'ER','messageText':None,'messageER':'data not found','status_Code':200}            
            print('lenQuery',len(result_select))
            for i in range(len(result_select)):
                tmp_query = result_select[i]
                if '_sa_instance_state' in tmp_query:
                    del tmp_query['_sa_instance_state']
                if tmp_query['tid'] != None:
                    tmp_query['id'] = tmp_query['tid']
                if 'tid' in tmp_query:
                    del tmp_query['tid']
                if 'biz_info' in tmp_query :
                    if tmp_query['biz_info'] != '':
                        # tmp_query['biz_info'] = eval(str(tmp_query['biz_info']))
                        eval_biz = eval(str(tmp_query['biz_info']))
                        if type(eval_biz) == dict:
                            for x in range(len(tmp_query['biz_info'])):
                                tmp_biz = {}
                                tmp_biz['id_card_num'] = eval_biz['id_card_num']
                                tmp_biz['first_name_th'] = eval_biz['first_name_th']
                                tmp_biz['first_name_eng'] = eval_biz['first_name_eng']
                                tmp_biz['role_name'] = eval_biz['role_name']
                                tmp_biz['dept_id'] = eval_biz['dept_id']
                            tmp_query['biz_info'] = tmp_biz
                        elif type(eval_biz) == list:
                            for x in range(len(tmp_query['biz_info'])):
                                tmp_biz = {}
                                tmp_biz['id_card_num'] = eval_biz[0]['id_card_num']
                                tmp_biz['first_name_th'] = eval_biz[0]['first_name_th']
                                tmp_biz['first_name_eng'] = eval_biz[0]['first_name_eng']
                                tmp_biz['role_name'] = eval_biz[0]['role_name']
                                tmp_biz['dept_id'] = eval_biz[0]['dept_id']
                            tmp_query['biz_info'] = tmp_biz
                    else:
                        tmp_query['biz_info'] =None

                if tmp_query['biz_info'] != None:
                    id_card = '%{}%'.format(tmp_biz['id_card_num'])
                    with engine.connect() as connection:
                        result = connection.execute(text(''' SELECT "documentJson" FROM "tb_document_detail" WHERE "documentStatus" = 'ACTIVE' AND "biz_info" LIKE :tax_id ORDER BY "documentUpdate" DESC ''')\
                            ,tax_id=id_card)
                        connection.close()
                    query_document = [dict(row) for row in result]
                else:
                    with engine.connect() as connection:
                        result = connection.execute(text(''' SELECT "documentJson" FROM "tb_document_detail" WHERE "documentStatus" = 'ACTIVE' AND ("biz_info" = '' OR "biz_info" = 'None') ORDER BY "documentUpdate" DESC '''))
                        connection.close()
                    query_document = [dict(row) for row in result]

                tmpdocumentdetail = None
                if query_document != []:
                    query_document = query_document[0]
                    tmpdocumentdetail = query_document['documentJson']
                    if tmpdocumentdetail != None:
                        tmpdocumentdetail = eval(tmpdocumentdetail)
                tmp_query['document_type_detail'] = tmpdocumentdetail
                if 'email_middle' in tmp_query:
                    if tmp_query['email_middle'] != '':
                        tmp_query['email_middle'] = eval(str(tmp_query['email_middle']))
                if 'timegroup_auto' in tmp_query:
                    if tmp_query['timegroup_auto'] != '':
                        tmp_query['timegroup'] = eval(str(tmp_query['timegroup_auto']))
                if 'daygroup_auto' in tmp_query:
                    if tmp_query['daygroup_auto'] != '':
                        tmp_query['daygroup'] = eval(str(tmp_query['daygroup_auto']))
                if 'group_data' in tmp_query:
                    if tmp_query['group_data'] != '':
                        tmp_query['group_data'] = eval(str(tmp_query['group_data']))
                if 'group_title' in tmp_query:
                    if tmp_query['group_title'] != '':
                        tmp_query['group_title'] = eval(str(tmp_query['group_title']))
                if 'step_group' in tmp_query:
                    if tmp_query['step_group'] != '':
                        try:
                            tmp_query['step_group'] = eval((tmp_query['step_group']))
                        except Exception as e:
                            tmp_query['step_group'] = None
                if 'template' in tmp_query:
                    if tmp_query['template'] != '':
                        tmp_query['template'] = eval(tmp_query['template'])
                if 'create_date' in tmp_query and 'update_date' in tmp_query:
                    tmp_query['create_date'] = str(tmp_query['create_date'])
                    tmp_query['update_date'] = str(tmp_query['update_date'])
                if 'cover_page' in tmp_query:
                    if tmp_query['cover_page'] != '':
                        tmp_query['cover_page'] = eval(str(tmp_query['cover_page']))
                if 'group_color' in tmp_query:
                    if tmp_query['group_color'] != None:
                        tmp_query['group_color'] = eval(tmp_query['group_color'])
                        if 'color' in tmp_query['group_color'][0]:
                            tmp_query['group_color'] = tmp_query['group_color'][0]['color']
                list_json.append(tmp_query)            
            return {'result':'OK','messageText':list_json,'status_Code':200,'messageER':None}    
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200
          
    def select_tax_id_onebox_attach_file(self,sidcode):
        self.sidcode = sidcode
        try:
            tq = db.session.query(\
                paper_lessdocument,
                paper_lessdatastep,
                paper_lesssender
            )\
            .join(paper_lesssender,paper_lesssender.step_data_sid==paper_lessdocument.step_id)\
            .join(paper_lessdatastep,paper_lessdatastep.sid==paper_lessdocument.step_id)\
            .filter(paper_lessdocument.step_id==self.sidcode)\
            .first()
            tmp_biz_info = None
            tmp_usersender = None
            # print(tq[1])
            for u in range(len(tq)):
                # print(u)
                tmpjson = tq[u].__dict__
                if '_sa_instance_state' in tmpjson:
                    del tmpjson['_sa_instance_state']
                if u == 0:
                    # print(tmpjson)
                    tmp_document_type = tmpjson['documentType']
                    documentJson = eval(str(tmpjson['documentJson']))
                    doc_name_type = str(documentJson['document_type']+'/'+documentJson['document_name'])
                if u == 1:
                    tmp_biz_info = tmpjson['biz_info']
                if u == 2:
                    tmp_usersender = tmpjson['send_user']
                if tmp_biz_info == 'None':
                    tmp_biz_info = None
            if tmp_biz_info != None:
                try:
                    tmp_biz_info = eval(tmp_biz_info)
                    tmp_id_card_num = tmp_biz_info['id_card_num']
                    print('id_card_num: ',tmp_id_card_num)
                    return {'result':'OK','messageText':str(tmp_id_card_num),'messageText2':doc_name_type}
                except Exception as e:
                    tax_id = None
                    tmp_id_card_num =None
            else:
                return {'result':'ER'}            
        except Exception as e:
            print(str(e))
            return {'result':'ER','messageText':str(e)}

    def select_attach_file_onebox(self,sid): 
        self.sid = sid
        try:
            with slave.connect() as connection:
                result = connection.execute(text('SELECT "document_id","attempted_folder","pathfolder","json_data" FROM "tb_doc_detail" JOIN "tb_transactionfile" ON "tb_transactionfile".folder_name = "tb_doc_detail".attempted_folder WHERE step_id=:sid'),sid=self.sid)
                connection.close()
            tmp_query = [dict(row) for row in result]
            return {'result':'OK','messageText':tmp_query}

        except Exception as e:
            print (str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    # ไม่มี document_type
    def select_list_template_group_sum_v5(self,username,tax_id,id_data):
        try:
            self.username = username
            self.tax_id = tax_id
            self.id = id_data
            # self.document_type = document_type
            tax_id = '%{}%'.format(self.tax_id)
            query_result_select = None
            list_json = []
            tmp_query ={}

            if self.id != None: # มี ID
                with slave.connect() as connection:
                    result = connection.execute(text(''' SELECT COUNT("id") FROM "tb_group_template_2" WHERE "tid" = :tid AND "status" = 'ACTIVE' '''),tid=self.id)
                    connection.close()
                result_select = [dict(row) for row in result]
            elif self.tax_id != None and self.username == None and self.id == None : # มี TAX_ID ไม่มี username
                with slave.connect() as connection:
                    result = connection.execute(text(''' SELECT COUNT("id") FROM "tb_group_template_2" WHERE "biz_info" LIKE :tax_id AND "status" = 'ACTIVE' '''),tax_id=tax_id)
                    connection.close()    
                result_select = [dict(row) for row in result]              
            elif self.tax_id == None and self.username != None and self.id == None : # มี username ไม่มี TAX_ID 
                print('username != None')
                with slave.connect() as connection:
                    result = connection.execute(text(''' SELECT COUNT("id") FROM "tb_group_template_2" WHERE "create_by" = :username AND "biz_info" = '' AND "status" = 'ACTIVE' '''),username=self.username)
                    connection.close()  
                result_select = [dict(row) for row in result]    
            elif self.username == None and self.tax_id == None and self.id == None : #  ไม่มี username ไม่มี tax_id 
                with slave.connect() as connection:
                    result = connection.execute(text(''' SELECT COUNT("id") FROM "tb_group_template_2" WHERE "status" = 'ACTIVE' '''))
                    connection.close()
                result_select = [dict(row) for row in result]
            elif self.tax_id == None and self.username == None and self.id == None : # ไม่มีอะไรเลยยยย
                return {'result':'ER','messageText':None,'messageER':'Not have data','status_Code':404}
            else:
                return {'result':'ER','messageText':None,'messageER':'Parameter incorrect','status_Code':404} 

            count = result_select[0]
            print('lenQuery', count['count']) 
            jsondata = {
                'sum_tamplate_group': count['count']
            }
            list_json.append(jsondata)
            return {'result':'OK','messageText':list_json,'status_Code':200,'messageER':None}    
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def select_list_template_group_v5(self,username,tax_id,id_data,limit,offset):
        try:
            self.username = username
            self.tax_id = tax_id
            self.id = id_data
            # self.document_type = document_type
            self.limit = limit
            self.offset = offset
            tax_id = '%{}%'.format(self.tax_id)
            query_result_select = None
            list_json = []
            tmp_query ={}
            stringQuery1 = ''' SELECT "group_name","group_code","template","group_title","step_group","status","create_date","update_date","group_data","biz_info","create_by","update_by",
                "use_status","cover_page","tid","group_color","email_middle","timegroup_auto","daygroup_auto","email_step","status_doing_auto" FROM "tb_group_template_2" '''
            print(self.username,self.tax_id,self.id)
            if self.id != None: # มี ID
                with engine.connect() as connection:
                    result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "tid" = :tid AND "status" = 'ACTIVE' ORDER BY "create_date" DESC limit(:limit) offset(:offset) ''')\
                        ,tid=self.id,limit=self.limit,offset=self.offset)
                    connection.close()
                result_select = [dict(row) for row in result]
            elif self.tax_id != None and self.username == None and self.id == None : # มี TAX_ID ไม่มี username
                with engine.connect() as connection:
                    result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "biz_info" LIKE :tax_id AND "status" = 'ACTIVE' ORDER BY "create_date" DESC limit(:limit) offset(:offset) ''')\
                        ,tax_id=tax_id,limit=self.limit,offset=self.offset)
                    connection.close()    
                result_select = [dict(row) for row in result]             
            elif self.tax_id == None and self.username != None and self.id == None : # มี username ไม่มี TAX_ID 
                with engine.connect() as connection:
                    result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "create_by" = :username AND "biz_info" = '' AND "status" = 'ACTIVE' ORDER BY "create_date" DESC limit(:limit) offset(:offset) ''')\
                        ,username=self.username,limit=self.limit,offset=self.offset)
                    connection.close()  
                result_select = [dict(row) for row in result]    
            elif self.username == None and self.tax_id == None and self.id == None : # ไม่มี username ไม่มี tax_id 
                with engine.connect() as connection:
                    result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "status" = 'ACTIVE' ORDER BY "create_date" DESC limit(:limit) offset(:offset) ''')\
                        ,limit=self.limit,offset=self.offset)
                    connection.close()
                result_select = [dict(row) for row in result]
            elif self.tax_id == None and self.username == None and self.id == None : # ไม่มีอะไรเลยยยย
                return {'result':'ER','messageText':None,'messageER':'Not have data','status_Code':404}
            else:
                return {'result':'ER','messageText':None,'messageER':'Parameter incorrect','status_Code':404} 

            if result_select == []:
                return {'result':'ER','messageText':None,'messageER':'data not found','status_Code':200}            
            print('lenQuery',len(result_select))
            for i in range(len(result_select)):
                tmp_query = result_select[i]
                if '_sa_instance_state' in tmp_query:
                    del tmp_query['_sa_instance_state']
                if tmp_query['tid'] != None:
                    tmp_query['id'] = tmp_query['tid']
                if 'tid' in tmp_query:
                    del tmp_query['tid']
                if 'biz_info' in tmp_query :
                    if tmp_query['biz_info'] != '':
                        # tmp_query['biz_info'] = eval(str(tmp_query['biz_info']))
                        eval_biz = eval(str(tmp_query['biz_info']))
                        if type(eval_biz) == dict:
                            for x in range(len(tmp_query['biz_info'])):
                                tmp_biz = {}
                                tmp_biz['id_card_num'] = eval_biz['id_card_num']
                                tmp_biz['first_name_th'] = eval_biz['first_name_th']
                                tmp_biz['first_name_eng'] = eval_biz['first_name_eng']
                                tmp_biz['role_name'] = eval_biz['role_name']
                                tmp_biz['dept_id'] = eval_biz['dept_id']
                            tmp_query['biz_info'] = tmp_biz
                        elif type(eval_biz) == list:
                            for x in range(len(tmp_query['biz_info'])):
                                tmp_biz = {}
                                tmp_biz['id_card_num'] = eval_biz[0]['id_card_num']
                                tmp_biz['first_name_th'] = eval_biz[0]['first_name_th']
                                tmp_biz['first_name_eng'] = eval_biz[0]['first_name_eng']
                                tmp_biz['role_name'] = eval_biz[0]['role_name']
                                tmp_biz['dept_id'] = eval_biz[0]['dept_id']
                            tmp_query['biz_info'] = tmp_biz
                    else:
                        tmp_query['biz_info'] =None

                if tmp_query['biz_info'] != None:
                    id_card = '%{}%'.format(tmp_biz['id_card_num'])
                    with engine.connect() as connection:
                        result = connection.execute(text(''' SELECT "documentJson" FROM "tb_document_detail" WHERE "documentStatus" = 'ACTIVE' AND "biz_info" LIKE :tax_id ORDER BY "documentUpdate" DESC ''')\
                            ,tax_id=id_card)
                        connection.close()
                    query_document = [dict(row) for row in result]
                else:
                    with engine.connect() as connection:
                        result = connection.execute(text(''' SELECT "documentJson" FROM "tb_document_detail" WHERE "documentStatus" = 'ACTIVE' AND ("biz_info" = '' OR "biz_info" = 'None') ORDER BY "documentUpdate" DESC '''))
                        connection.close()
                    query_document = [dict(row) for row in result]

                tmpdocumentdetail = None
                if query_document != []:
                    query_document = query_document[0]
                    tmpdocumentdetail = query_document['documentJson']
                    if tmpdocumentdetail != None:
                        tmpdocumentdetail = eval(tmpdocumentdetail)
                tmp_query['document_type_detail'] = tmpdocumentdetail
                if 'email_middle' in tmp_query:
                    if tmp_query['email_middle'] != '':
                        tmp_query['email_middle'] = eval(str(tmp_query['email_middle']))
                if 'timegroup_auto' in tmp_query:
                    if tmp_query['timegroup_auto'] != '':
                        tmp_query['timegroup'] = eval(str(tmp_query['timegroup_auto']))
                if 'daygroup_auto' in tmp_query:
                    if tmp_query['daygroup_auto'] != '':
                        tmp_query['daygroup'] = eval(str(tmp_query['daygroup_auto']))
                if 'group_data' in tmp_query:
                    if tmp_query['group_data'] != '':
                        tmp_query['group_data'] = eval(str(tmp_query['group_data']))
                if 'group_title' in tmp_query:
                    if tmp_query['group_title'] != '':
                        tmp_query['group_title'] = eval(str(tmp_query['group_title']))
                if 'step_group' in tmp_query:
                    if tmp_query['step_group'] != '':
                        try:
                            tmp_query['step_group'] = eval((tmp_query['step_group']))
                        except Exception as e:
                            tmp_query['step_group'] = None
                if 'template' in tmp_query:
                    if tmp_query['template'] != '':
                        tmp_query['template'] = eval(tmp_query['template'])
                if 'create_date' in tmp_query and 'update_date' in tmp_query:
                    tmp_query['create_date'] = str(tmp_query['create_date'])
                    tmp_query['update_date'] = str(tmp_query['update_date'])
                if 'cover_page' in tmp_query:
                    if tmp_query['cover_page'] != '':
                        tmp_query['cover_page'] = eval(str(tmp_query['cover_page']))
                if 'group_color' in tmp_query:
                    if tmp_query['group_color'] != None:
                        tmp_query['group_color'] = eval(tmp_query['group_color'])
                        if 'color' in tmp_query['group_color'][0]:
                            tmp_query['group_color'] = tmp_query['group_color'][0]['color']
                list_json.append(tmp_query)            
            return {'result':'OK','messageText':list_json,'status_Code':200,'messageER':None}    
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200
   

    def select_group_sid(self,id_group):
        try:
            self.id_group = id_group
            with slave.connect() as connection:
                result = connection.execute(text('SELECT "sid_group" FROM "tb_group_document" WHERE id =:id'),id=self.id_group)
                connection.close()
                if result != [] and result != None and result != '':
                    tmp_query = [dict(row) for row in result][0]
                # print ('tmp_query:',tmp_query)
            return {'result':'OK','messageText':tmp_query}
        except Exception as e:
            print (str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def select_json_file_attach_all(self):
        try:
            with slave.connect() as connection:
                result = connection.execute(text('SELECT "json_data","folder_name","storage" FROM "tb_transactionfile" WHERE "storage" IS NULL LIMIT 100'))
                connection.close()
                tmp_query = [dict(row) for row in result]
                # print ('tmp_query:',tmp_query)
            return {'result':'OK','messageText':tmp_query}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}


    def select_list_template_group_v4(self,username,tax_id,id_data,document_type,limit,offset):
        try:
            self.username = username
            self.tax_id = tax_id
            self.id = id_data
            self.document_type = document_type
            self.limit = limit
            self.offset = offset
            tax_id = '%{}%'.format(self.tax_id)
            query_result_select = None
            list_json = []
            tmp_query ={}
            stringQuery1 = ''' SELECT "group_name","group_code","template","document_type","group_title","step_group","status","create_date","update_date","group_data","biz_info","create_by","update_by",
                "use_status","cover_page","tid","group_color","email_middle","timegroup_auto","daygroup_auto","webhook" FROM "tb_group_template" '''

            if self.id != None: # มี ID
                with slave.connect() as connection:
                    result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "tid" = :tid AND "status" = 'ACTIVE' ORDER BY "create_date" DESC limit(:limit) offset(:offset) ''')\
                        ,tid=self.id,limit=self.limit,offset=self.offset)
                    connection.close()
                result_select = [dict(row) for row in result]
            elif self.tax_id != None and self.username == None and self.id == None and self.document_type == None: # มี TAX_ID ไม่มี username ไม่มี document_type 
                with slave.connect() as connection:
                    result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "biz_info" LIKE :tax_id AND "status" = 'ACTIVE' ORDER BY "create_date" DESC limit(:limit) offset(:offset) ''')\
                        ,tax_id=tax_id,limit=self.limit,offset=self.offset)
                    connection.close()    
                result_select = [dict(row) for row in result]              
            elif self.tax_id == None and self.username != None and self.id == None and self.document_type == None: # มี username ไม่มี document_type ไม่มี TAX_ID 
                with slave.connect() as connection:
                    result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "create_by" = :username AND "biz_info" = '' AND "status" = 'ACTIVE' ORDER BY "create_date" DESC limit(:limit) offset(:offset) ''')\
                        ,username=self.username,limit=self.limit,offset=self.offset)
                    connection.close()  
                result_select = [dict(row) for row in result]    
            elif self.username == None and self.tax_id == None and self.id == None and self.document_type != None: # มี document_type ไม่มี username ไม่มี tax_id 
                with slave.connect() as connection:
                    result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "document_type" = :doc_type AND "status" = 'ACTIVE' ORDER BY "create_date" DESC limit(:limit) offset(:offset) ''')\
                        ,doc_type=self.document_type,limit=self.limit,offset=self.offset)
                    connection.close()
                result_select = [dict(row) for row in result]
            elif self.tax_id == None and self.username == None and self.id == None and self.document_type != None: # ไม่มีอะไรเลยยยย
                return {'result':'ER','messageText':None,'messageER':'Not have data','status_Code':404}
            else:
                return {'result':'ER','messageText':None,'messageER':'Parameter incorrect','status_Code':404} 

            if result_select == []:
                return {'result':'ER','messageText':None,'messageER':'data not found','status_Code':200}            
            print('lenQuery',len(result_select))
            for i in range(len(result_select)):
                tmp_query = result_select[i]
                if '_sa_instance_state' in tmp_query:
                    del tmp_query['_sa_instance_state']
                if tmp_query['tid'] != None:
                    tmp_query['id'] = tmp_query['tid']
                if 'tid' in tmp_query:
                    del tmp_query['tid']
                if 'biz_info' in tmp_query :
                    if tmp_query['biz_info'] != '':
                        # tmp_query['biz_info'] = eval(str(tmp_query['biz_info']))
                        eval_biz = eval(str(tmp_query['biz_info']))
                        if type(eval_biz) == dict:
                            for x in range(len(tmp_query['biz_info'])):
                                tmp_biz = {}
                                tmp_biz['id_card_num'] = eval_biz['id_card_num']
                                tmp_biz['first_name_th'] = eval_biz['first_name_th']
                                tmp_biz['first_name_eng'] = eval_biz['first_name_eng']
                                tmp_biz['role_name'] = eval_biz['role_name']
                                tmp_biz['dept_id'] = eval_biz['dept_id']
                            tmp_query['biz_info'] = tmp_biz
                        elif type(eval_biz) == list:
                            for x in range(len(tmp_query['biz_info'])):
                                tmp_biz = {}
                                tmp_biz['id_card_num'] = eval_biz[0]['id_card_num']
                                tmp_biz['first_name_th'] = eval_biz[0]['first_name_th']
                                tmp_biz['first_name_eng'] = eval_biz[0]['first_name_eng']
                                tmp_biz['role_name'] = eval_biz[0]['role_name']
                                tmp_biz['dept_id'] = eval_biz[0]['dept_id']
                            tmp_query['biz_info'] = tmp_biz
                    else:
                        tmp_query['biz_info'] =None

                if tmp_query['biz_info'] != None:
                    id_card = '%{}%'.format(tmp_biz['id_card_num'])
                    with slave.connect() as connection:
                        result = connection.execute(text(''' SELECT "documentJson" FROM "tb_document_detail" WHERE "documentType" = :doc_type AND "documentStatus" = 'ACTIVE' AND "biz_info" LIKE :tax_id ORDER BY "documentUpdate" DESC ''')\
                            ,doc_type=tmp_query['document_type'],tax_id=id_card)
                        connection.close()
                    query_document = [dict(row) for row in result]
                else:
                    with slave.connect() as connection:
                        result = connection.execute(text(''' SELECT "documentJson" FROM "tb_document_detail" WHERE "documentType" = :doc_type AND "documentStatus" = 'ACTIVE' AND ("biz_info" = '' OR "biz_info" = 'None') ORDER BY "documentUpdate" DESC ''')\
                            ,doc_type=tmp_query['document_type'])
                        connection.close()
                    query_document = [dict(row) for row in result]

                tmpdocumentdetail = None
                if query_document != []:
                    query_document = query_document[0]
                    tmpdocumentdetail = query_document['documentJson']
                    if tmpdocumentdetail != None:
                        tmpdocumentdetail = eval(tmpdocumentdetail)
                tmp_query['document_type_detail'] = tmpdocumentdetail
                if 'email_middle' in tmp_query:
                    if tmp_query['email_middle'] != '':
                        tmp_query['email_middle'] = eval(str(tmp_query['email_middle']))
                if 'timegroup_auto' in tmp_query:
                    if tmp_query['timegroup_auto'] != '':
                        tmp_query['timegroup'] = eval(str(tmp_query['timegroup_auto']))
                if 'daygroup_auto' in tmp_query:
                    if tmp_query['daygroup_auto'] != '':
                        tmp_query['daygroup'] = eval(str(tmp_query['daygroup_auto']))
                if 'group_data' in tmp_query:
                    if tmp_query['group_data'] != '':
                        tmp_query['group_data'] = eval(str(tmp_query['group_data']))
                if 'group_title' in tmp_query:
                    if tmp_query['group_title'] != '':
                        tmp_query['group_title'] = eval(str(tmp_query['group_title']))
                if 'step_group' in tmp_query:
                    if tmp_query['step_group'] != '':
                        try:
                            tmp_query['step_group'] = eval((tmp_query['step_group']))
                        except Exception as e:
                            tmp_query['step_group'] = None
                if 'template' in tmp_query:
                    if tmp_query['template'] != '':
                        tmp_query['template'] = eval(tmp_query['template'])
                if 'create_date' in tmp_query and 'update_date' in tmp_query:
                    tmp_query['create_date'] = str(tmp_query['create_date'])
                    tmp_query['update_date'] = str(tmp_query['update_date'])
                if 'cover_page' in tmp_query:
                    if tmp_query['cover_page'] != '':
                        tmp_query['cover_page'] = eval(str(tmp_query['cover_page']))
                if 'group_color' in tmp_query:
                    if tmp_query['group_color'] != None:
                        tmp_query['group_color'] = eval(tmp_query['group_color'])
                        if 'color' in tmp_query['group_color'][0]:
                            tmp_query['group_color'] = tmp_query['group_color'][0]['color']
                list_json.append(tmp_query)            
            return {'result':'OK','messageText':list_json,'status_Code':200,'messageER':None}    
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def select_list_template_group_sum_v4(self,username,tax_id,id_data,document_type):
        try:
            self.username = username
            self.tax_id = tax_id
            self.id = id_data
            self.document_type = document_type
            tax_id = '%{}%'.format(self.tax_id)
            query_result_select = None
            list_json = []
            tmp_query ={}

            if self.id != None: # มี ID
                with slave.connect() as connection:
                    result = connection.execute(text(''' SELECT COUNT("id") FROM "tb_group_template" WHERE "tid" = :tid AND "status" = 'ACTIVE' '''),tid=self.id)
                    connection.close()
                result_select = [dict(row) for row in result]
            elif self.tax_id != None and self.username == None and self.id == None and self.document_type == None: # มี TAX_ID ไม่มี username ไม่มี document_type 
                with slave.connect() as connection:
                    result = connection.execute(text(''' SELECT COUNT("id") FROM "tb_group_template" WHERE "biz_info" LIKE :tax_id AND "status" = 'ACTIVE' '''),tax_id=tax_id)
                    connection.close()    
                result_select = [dict(row) for row in result]              
            elif self.tax_id == None and self.username != None and self.id == None and self.document_type == None: # มี username ไม่มี document_type ไม่มี TAX_ID 
                with slave.connect() as connection:
                    result = connection.execute(text(''' SELECT COUNT("id") FROM "tb_group_template" WHERE "create_by" = :username AND "biz_info" = '' AND "status" = 'ACTIVE' '''),username=self.username)
                    connection.close()  
                result_select = [dict(row) for row in result]    
            elif self.username == None and self.tax_id == None and self.id == None and self.document_type != None: # มี document_type ไม่มี username ไม่มี tax_id 
                with slave.connect() as connection:
                    result = connection.execute(text(''' SELECT COUNT("id") FROM "tb_group_template" WHERE "document_type" = :doc_type AND "status" = 'ACTIVE' '''),doc_type=self.document_type)
                    connection.close()
                result_select = [dict(row) for row in result]
            elif self.tax_id == None and self.username == None and self.id == None and self.document_type != None: # ไม่มีอะไรเลยยยย
                return {'result':'ER','messageText':None,'messageER':'Not have data','status_Code':404}
            else:
                return {'result':'ER','messageText':None,'messageER':'Parameter incorrect','status_Code':404} 

            count = result_select[0]
            print('lenQuery', count['count']) 
            jsondata = {
                'sum_tamplate_group': count['count']
            }
            list_json.append(jsondata)
            return {'result':'OK','messageText':list_json,'status_Code':200,'messageER':None}    
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def select_list_template_group_search_v4(self,username,tax_id,document_type,limit,offset,keyword):
        try:
            self.username = username
            self.tax_id = tax_id
            self.document_type = document_type
            self.limit = limit
            self.offset = offset
            self.keyword = keyword
            keyword1 = '%{}%'.format(self.keyword)
            keyword2 = '%ment_name":"%{}%"%'.format(self.keyword)
            tax_id = '%{}%'.format(self.tax_id)            
            query_result_select = None
            list_json = []
            tmp_query ={}
            stringQuery1 = ''' SELECT "group_name","group_code","template","document_type","group_title","step_group","status","create_date","update_date","group_data",TP."biz_info","create_by","update_by",
                "use_status","cover_page","tid","group_color","email_middle","timegroup_auto","daygroup_auto","documentJson" FROM "tb_group_template" TP JOIN "tb_document_detail" DT ON "documentType" = "document_type" '''
            stringQuery2 = ''' "status" = 'ACTIVE' AND "documentStatus" = 'ACTIVE' AND (lower("update_by") LIKE lower(:keyword1) OR lower("group_name") LIKE lower(:keyword1) OR lower("documentJson") LIKE lower(:keyword2))
                ORDER BY "create_date" DESC limit(:limit) offset(:offset) '''
            stringQuery3 = ''' "status" = 'ACTIVE' AND "documentStatus" = 'ACTIVE' AND "update_date" >= :datetime1 AND "update_date" <= :datetime2 ORDER BY "create_date" DESC limit(:limit) offset(:offset) '''
            
            try: 
                parse(self.keyword, fuzzy=False)
                print('key is datetime')
                dats = datetime.datetime.strptime(self.keyword, '%Y-%m-%d')
                datetime1 = dats.strftime('%Y-%m-%d 00:00:00')
                datetime2 = dats.strftime('%Y-%m-%d 23:59:59')
                if self.tax_id != None and self.username == None and self.document_type == None: # มี TAX_ID ไม่มี username ไม่มี document_type 
                    with slave.connect() as connection:
                        result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE TP."biz_info" LIKE :tax_id AND DT."biz_info" LIKE :tax_id AND ''' + stringQuery3 + '''  ''')\
                            ,tax_id=tax_id,datetime1=datetime1,datetime2=datetime2,limit=self.limit,offset=self.offset)
                        connection.close()     
                    result_select = [dict(row) for row in result]              
                elif self.tax_id == None and self.username != None and self.document_type == None: # มี username ไม่มี document_type ไม่มี TAX_ID 
                    with slave.connect() as connection:
                        result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "create_by" = :username AND TP."biz_info" = '' AND ''' + stringQuery3 + ''' ''')\
                            ,username=self.username,datetime1=datetime1,datetime2=datetime2,limit=self.limit,offset=self.offset)
                        connection.close() 
                    result_select = [dict(row) for row in result]    
                elif self.username == None and self.tax_id == None and self.document_type != None: # มี document_type ไม่มี username ไม่มี tax_id 
                    with slave.connect() as connection:
                        result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "document_type" = :doc_type AND ''' + stringQuery3 + ''' ''')\
                            ,doc_type=self.document_type,datetime1=datetime1,datetime2=datetime2,limit=self.limit,offset=self.offset)
                        connection.close()
                    result_select = [dict(row) for row in result]
                elif self.tax_id == None and self.username == None and self.document_type != None: # ไม่มีอะไรเลยยยย
                    return {'result':'ER','messageText':None,'messageER':'Not have data','status_Code':404}
                else:
                    return {'result':'ER','messageText':None,'messageER':'Parameter incorrect','status_Code':404} 

            except ValueError:
                print('key not datetime') 
                if self.tax_id != None and self.username == None and self.document_type == None: # มี TAX_ID ไม่มี username ไม่มี document_type 
                    with slave.connect() as connection:
                        result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE TP."biz_info" LIKE :tax_id AND DT."biz_info" LIKE :tax_id AND ''' + stringQuery2 + '''  ''')\
                            ,tax_id=tax_id,keyword1=keyword1,keyword2=keyword2,limit=self.limit,offset=self.offset)
                        connection.close()     
                    result_select = [dict(row) for row in result]              
                elif self.tax_id == None and self.username != None and self.document_type == None: # มี username ไม่มี document_type ไม่มี TAX_ID 
                    with slave.connect() as connection:
                        result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "create_by" = :username AND TP."biz_info" = '' AND ''' + stringQuery2 + ''' ''')\
                            ,username=self.username,keyword1=keyword1,keyword2=keyword2,limit=self.limit,offset=self.offset)
                        connection.close() 
                    result_select = [dict(row) for row in result]    
                elif self.username == None and self.tax_id == None and self.document_type != None: # มี document_type ไม่มี username ไม่มี tax_id 
                    with slave.connect() as connection:
                        result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "document_type" = :doc_type AND ''' + stringQuery2 + ''' ''')\
                            ,doc_type=self.document_type,keyword1=keyword1,keyword2=keyword2,limit=self.limit,offset=self.offset)
                        connection.close()
                    result_select = [dict(row) for row in result]
                elif self.tax_id == None and self.username == None and self.document_type != None: # ไม่มีอะไรเลยยยย
                    return {'result':'ER','messageText':None,'messageER':'Not have data','status_Code':404}
                else:
                    return {'result':'ER','messageText':None,'messageER':'Parameter incorrect','status_Code':404} 

            if result_select == []:
                return {'result':'ER','messageText':None,'messageER':'data not found','status_Code':200}            
            print('lenQuery',len(result_select))
            for i in range(len(result_select)):
                tmp_query = result_select[i]
                if '_sa_instance_state' in tmp_query:
                    del tmp_query['_sa_instance_state']
                if tmp_query['tid'] != None:
                    tmp_query['id'] = tmp_query['tid']
                if 'tid' in tmp_query:
                    del tmp_query['tid']
                if 'biz_info' in tmp_query :
                    if tmp_query['biz_info'] != '':
                        # tmp_query['biz_info'] = eval(str(tmp_query['biz_info']))
                        eval_biz = eval(str(tmp_query['biz_info']))
                        if type(eval_biz) == dict:
                            for x in range(len(tmp_query['biz_info'])):
                                tmp_biz = {}
                                tmp_biz['id_card_num'] = eval_biz['id_card_num']
                                tmp_biz['first_name_th'] = eval_biz['first_name_th']
                                tmp_biz['first_name_eng'] = eval_biz['first_name_eng']
                                tmp_biz['role_name'] = eval_biz['role_name']
                                tmp_biz['dept_id'] = eval_biz['dept_id']
                            tmp_query['biz_info'] = tmp_biz
                        elif type(eval_biz) == list:
                            for x in range(len(tmp_query['biz_info'])):
                                tmp_biz = {}
                                tmp_biz['id_card_num'] = eval_biz[0]['id_card_num']
                                tmp_biz['first_name_th'] = eval_biz[0]['first_name_th']
                                tmp_biz['first_name_eng'] = eval_biz[0]['first_name_eng']
                                tmp_biz['role_name'] = eval_biz[0]['role_name']
                                tmp_biz['dept_id'] = eval_biz[0]['dept_id']
                            tmp_query['biz_info'] = tmp_biz
                    else:
                        tmp_query['biz_info'] =None

                tmp_query['document_type_detail'] = eval(str(tmp_query['documentJson']))
                del tmp_query['documentJson']
                if 'email_middle' in tmp_query:
                    if tmp_query['email_middle'] != '':
                        tmp_query['email_middle'] = eval(str(tmp_query['email_middle']))
                if 'timegroup_auto' in tmp_query:
                    if tmp_query['timegroup_auto'] != '':
                        tmp_query['timegroup'] = eval(str(tmp_query['timegroup_auto']))
                if 'daygroup_auto' in tmp_query:
                    if tmp_query['daygroup_auto'] != '':
                        tmp_query['daygroup'] = eval(str(tmp_query['daygroup_auto']))
                if 'group_data' in tmp_query:
                    if tmp_query['group_data'] != '':
                        tmp_query['group_data'] = eval(str(tmp_query['group_data']))
                if 'group_title' in tmp_query:
                    if tmp_query['group_title'] != '':
                        tmp_query['group_title'] = eval(str(tmp_query['group_title']))
                if 'step_group' in tmp_query:
                    if tmp_query['step_group'] != '':
                        try:
                            tmp_query['step_group'] = eval((tmp_query['step_group']))
                        except Exception as e:
                            tmp_query['step_group'] = None
                if 'template' in tmp_query:
                    if tmp_query['template'] != '':
                        tmp_query['template'] = eval(tmp_query['template'])
                if 'create_date' in tmp_query and 'update_date' in tmp_query:
                    tmp_query['create_date'] = str(tmp_query['create_date'])
                    tmp_query['update_date'] = str(tmp_query['update_date'])
                if 'cover_page' in tmp_query:
                    if tmp_query['cover_page'] != '':
                        tmp_query['cover_page'] = eval(str(tmp_query['cover_page']))
                if 'group_color' in tmp_query:
                    if tmp_query['group_color'] != None:
                        tmp_query['group_color'] = eval(tmp_query['group_color'])
                        if 'color' in tmp_query['group_color'][0]:
                            tmp_query['group_color'] = tmp_query['group_color'][0]['color']
                list_json.append(tmp_query)            
            return {'result':'OK','messageText':list_json,'status_Code':200,'messageER':None}    
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200
    
    def select_list_template_group_search_sum_v4(self,username,tax_id,document_type,keyword):
        try:
            self.username = username
            self.tax_id = tax_id
            self.document_type = document_type
            self.keyword = keyword
            keyword1 = '%{}%'.format(self.keyword)
            keyword2 = '%ment_name":"%{}%"%'.format(self.keyword)
            tax_id = '%{}%'.format(self.tax_id)            
            query_result_select = None
            list_json = []
            tmp_query ={}
            stringQuery1 = ''' SELECT TP."id" FROM "tb_group_template" TP JOIN "tb_document_detail" DT ON "documentType" = "document_type" '''
            stringQuery2 = ''' "status" = 'ACTIVE' AND "documentStatus" = 'ACTIVE' AND (lower("update_by") LIKE lower(:keyword1) OR lower("group_name") LIKE lower(:keyword1) OR lower("documentJson") LIKE lower(:keyword2))
                ORDER BY "create_date" DESC '''
            stringQuery3 = ''' "status" = 'ACTIVE' AND "documentStatus" = 'ACTIVE' AND "update_date" >= :datetime1 AND "update_date" <= :datetime2 ORDER BY "create_date" DESC'''
            
            try: 
                parse(self.keyword, fuzzy=False)
                print('key is datetime')
                dats = datetime.datetime.strptime(self.keyword, '%Y-%m-%d')
                datetime1 = dats.strftime('%Y-%m-%d 00:00:00')
                datetime2 = dats.strftime('%Y-%m-%d 23:59:59')
                if self.tax_id != None and self.username == None and self.document_type == None: # มี TAX_ID ไม่มี username ไม่มี document_type 
                    with slave.connect() as connection:
                        result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE TP."biz_info" LIKE :tax_id AND DT."biz_info" LIKE :tax_id AND ''' + stringQuery3 + '''  ''')\
                            ,tax_id=tax_id,datetime1=datetime1,datetime2=datetime2)
                        connection.close()     
                    result_select = [dict(row) for row in result]              
                elif self.tax_id == None and self.username != None and self.document_type == None: # มี username ไม่มี document_type ไม่มี TAX_ID 
                    with slave.connect() as connection:
                        result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "create_by" = :username AND TP."biz_info" = '' AND ''' + stringQuery3 + ''' ''')\
                            ,username=self.username,datetime1=datetime1,datetime2=datetime2)
                        connection.close() 
                    result_select = [dict(row) for row in result]    
                elif self.username == None and self.tax_id == None and self.document_type != None: # มี document_type ไม่มี username ไม่มี tax_id 
                    with slave.connect() as connection:
                        result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "document_type" = :doc_type AND ''' + stringQuery3 + ''' ''')\
                            ,doc_type=self.document_type,datetime1=datetime1,datetime2=datetime2)
                        connection.close()
                    result_select = [dict(row) for row in result]
                elif self.tax_id == None and self.username == None and self.document_type != None: # ไม่มีอะไรเลยยยย
                    return {'result':'ER','messageText':None,'messageER':'Not have data','status_Code':404}
                else:
                    return {'result':'ER','messageText':None,'messageER':'Parameter incorrect','status_Code':404} 

            except ValueError:
                print('key not datetime') 
                if self.tax_id != None and self.username == None and self.document_type == None: # มี TAX_ID ไม่มี username ไม่มี document_type 
                    with slave.connect() as connection:
                        result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE TP."biz_info" LIKE :tax_id AND DT."biz_info" LIKE :tax_id AND ''' + stringQuery2 + '''  ''')\
                            ,tax_id=tax_id,keyword1=keyword1,keyword2=keyword2)
                        connection.close()     
                    result_select = [dict(row) for row in result]              
                elif self.tax_id == None and self.username != None and self.document_type == None: # มี username ไม่มี document_type ไม่มี TAX_ID 
                    with slave.connect() as connection:
                        result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "create_by" = :username AND TP."biz_info" = '' AND ''' + stringQuery2 + ''' ''')\
                            ,username=self.username,keyword1=keyword1,keyword2=keyword2)
                        connection.close() 
                    result_select = [dict(row) for row in result]    
                elif self.username == None and self.tax_id == None and self.document_type != None: # มี document_type ไม่มี username ไม่มี tax_id 
                    with slave.connect() as connection:
                        result = connection.execute(text(''' ''' + stringQuery1 + ''' WHERE "document_type" = :doc_type AND ''' + stringQuery2 + ''' ''')\
                            ,doc_type=self.document_type,keyword1=keyword1,keyword2=keyword2)
                        connection.close()
                    result_select = [dict(row) for row in result]
                elif self.tax_id == None and self.username == None and self.document_type != None: # ไม่มีอะไรเลยยยย
                    return {'result':'ER','messageText':None,'messageER':'Not have data','status_Code':404}
                else:
                    return {'result':'ER','messageText':None,'messageER':'Parameter incorrect','status_Code':404} 

            print('lenQuery', len(result_select)) 
            jsondata = {
                'sum_tamplate_group_search': len(result_select)
            }
            list_json.append(jsondata)            
            return {'result':'OK','messageText':list_json,'status_Code':200,'messageER':None}    
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200
    
    def select_data_document_other_business(self,email):
        self.email = email
        data_list = []
        txt_query = ''
        try:
            biz_list = email_data_business_v1(self.email)
            if biz_list['result'] == 'OK':
                for biz in biz_list['data']:
                    txt_query += ''' "biz_info" NOT LIKE '%{}%' AND '''.format(biz)
                print('txtquery :',txt_query)
            else:
                return {'result':'ER','messageText':None,'messageER': biz_list['messageER'],'status_Code':200}
            with slave.connect() as connection:
                result = connection.execute(text('''SELECT "documentJson" FROM "tb_doc_detail" JOIN "tb_step_data" ON "sid" = "step_id" JOIN "tb_send_detail" ON "step_data_sid" = "step_id"
                    WHERE '''+ txt_query +''' "biz_info" != 'None' AND "biz_info" != '' AND "documentType" != '' AND ("sender_email" = :email OR "recipient_email" LIKE '%':email'%') ORDER BY "update_time" DESC '''),email=self.email)
                connection.close()
            query_result = [dict(row) for row in result]
            print('len :',len(query_result))
            for i in range(len(query_result)):
                data_json = {
                    "documentJson": eval(query_result[i]['documentJson'])
                }
                if data_json not in data_list:
                    data_list.append(data_json)
            return ({'result':'OK','data':data_list})
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}

    def select_list_ref(self,doc_type):
        self.doc_type = doc_type
        list_resp = []
        dict_resp = {}
        try:
            with slave.connect() as connection:
                result = connection.execute(text('SELECT "id", "send_user", "send_time", "status", "sender_name", "sender_email", "sender_position", "file_id", "file_name", "tracking_id", "step_code",\
                    "step_data_sid", "doc_id", "sender_biz_info", "template_webhook", "email_center", "recipient_email", "status_details", "document_status", "group_id", "stepnow", "stepmax", "time_expire",\
                    "importance", "eform_id", "last_digitsign", "status_ref", "list_ref","status_service" FROM "tb_send_detail" WHERE status_ref=:status_ref AND document_status=:document_status'),status_ref=True,document_status='Y')
                connection.close()
            tmp_query = [dict(row) for row in result]
            if tmp_query != None and tmp_query != []:
                for x in range(len(tmp_query)):
                    doc_type_db = str(tmp_query[x]['doc_id']).split('-')[0]
                    if doc_type_db == self.doc_type:
                        dict_resp = {
                            'doc_id' : tmp_query[x]['doc_id'],
                            # 'sender_name' : tmp_query[x]['sender_name'],
                            # 'sender_email' : tmp_query[x]['sender_email'],
                            'sid' : tmp_query[x]['step_data_sid'],
                            'file_name' : tmp_query[x]['file_name'],
                            'tracking_id' : tmp_query[x]['tracking_id'],
                            'recipient_email' : eval(str(tmp_query[x]['recipient_email'])),
                            # 'status_details' : eval(str(tmp_query[x]['status_details'])),
                            'document_status' : tmp_query[x]['document_status']
                        }
                        list_resp.append(dict_resp)

                    # tmp_query[x]['status_details'] = eval(str(tmp_query[x]['status_details']))
                    # tmp_query[x]['list_ref'] = eval(str(tmp_query[x]['list_ref']))
                    # tmp_query[x]['recipient_email'] = eval(str(tmp_query[x]['recipient_email']))
                if list_resp == []:
                    return {'result':'OK','messageText':'Not found data','status_Code':200,'messageER':None}
                else:
                    return {'result':'OK','messageText':list_resp,'status_Code':200,'messageER':None}
            else:
                return {'result':'ER','messageText':None,'status_Code':200,'messageER':'Not have data'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def select_list_ref_v2(self,doc_type,email):
        self.doc_type = doc_type
        self.email = email
        list_resp = []
        dict_resp = {}
        try:
            with slave.connect() as connection:
                result = connection.execute(text('SELECT "doc_id","step_data_sid","file_name","tracking_id","recipient_email","document_status",\
                    "status_ref","sender_email","file_id","string_sign","string_pdf" FROM "tb_send_detail" JOIN "tb_pdf_storage" ON "tb_pdf_storage".fid = "tb_send_detail".file_id WHERE status_ref=:status_ref \
                    AND document_status=:document_status AND sender_email=:sender_email'),status_ref=True,document_status='Y',sender_email=self.email)
                connection.close()
            tmp_query = [dict(row) for row in result]
            # print (tmp_query)
            if tmp_query != None and tmp_query != []:
                for x in range(len(tmp_query)):
                    doc_type_db = str(tmp_query[x]['doc_id']).split('-')[0]
                    if doc_type_db == self.doc_type:
                        str_base64 = tmp_query[x]['string_sign']
                        if str_base64 == None or str_base64 == '':
                            str_base64 = tmp_query[x]['string_pdf']
                        dict_resp = {
                            'doc_id' : tmp_query[x]['doc_id'],
                            # 'sender_name' : tmp_query[x]['sender_name'],
                            # 'sender_email' : tmp_query[x]['sender_email'],
                            'sid' : tmp_query[x]['step_data_sid'],
                            'file_name' : tmp_query[x]['file_name'],
                            'tracking_id' : tmp_query[x]['tracking_id'],
                            'recipient_email' : eval(str(tmp_query[x]['recipient_email'])),
                            # 'status_details' : eval(str(tmp_query[x]['status_details'])),
                            'document_status' : tmp_query[x]['document_status'],
                            'file_id' : tmp_query[x]['file_id'],
                            'file_size' : (len(str_base64) * 3) / 4 - str_base64.count('=', -2)
                        }
                        list_resp.append(dict_resp)

                    # tmp_query[x]['status_details'] = eval(str(tmp_query[x]['status_details']))
                    # tmp_query[x]['list_ref'] = eval(str(tmp_query[x]['list_ref']))
                    # tmp_query[x]['recipient_email'] = eval(str(tmp_query[x]['recipient_email']))
                if list_resp == []:
                    return {'result':'OK','messageText':'Not found data','status_Code':200,'messageER':None}
                else:
                    return {'result':'OK','messageText':list_resp,'status_Code':200,'messageER':None}
            else:
                return {'result':'ER','messageText':None,'status_Code':200,'messageER':'Not have data'}
        except Exception as e:
            print (str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}


    def select_private_key(self,service_id):
        self.service_id = service_id
        dict_secret = {}
        try:
            with slave.connect() as connection:
                result = connection.execute(text('SELECT "serviceName","private","code" FROM "tb_connex" WHERE code=:code'),code=self.service_id)
                connection.close()
            # print(result)
            tmp_query = [dict(row) for row in result]
            
            if tmp_query != None and tmp_query != []:
                tmp_query = tmp_query[0]
                dict_secret = {
                    'serviceName' : tmp_query['serviceName'],
                    'private' : tmp_query['private'],
                    'code' : tmp_query['code']
                }
                return {'result':'OK','messageText':dict_secret,'status_Code':200,'messageER':None}
            else:
                return {'result':'ER','messageText':None,'status_Code':200,'messageER':'Not have data'}

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':str(e)}

    def count_all_draft(self,key,email):
        try:
            self.key = key
            self.email = email
            tmp_result = {}
            key2 = '%' + str(self.key) + '%'
            # mail = find_email(self.key)
            endTime = ''
            ch,startTime = checkDatetime(self.key)
            text_sql = 'SELECT COUNT("id") FROM "tb_draft_document"'
            where_sql =  ' WHERE "tb_draft_document"."sender_email"=:email AND "tb_draft_document"."status"=:status'
            ORDER_sql = ' ORDER BY "tb_draft_document"."update_time" DESC'
            if ch == True:
                endTime = startTime.replace(hour=23, minute=59, second=59, microsecond=0)
                where_sql += ' AND "tb_draft_document"."update_time" <=:endTime AND "tb_draft_document"."update_time" >=:startTime'
            else:
                where_sql += ' AND ("tb_draft_document"."documentType" LIKE :key2 OR "tb_draft_document"."recipient_email" LIKE :key2 OR "tb_draft_document"."documentJson" LIKE :key2)'
            text_sql += where_sql
            print('text_sql',text_sql)
            with slave.connect() as connection:
                query_result = connection.execute(text(text_sql),email=self.email,status='ACTIVE',endTime=str(endTime),startTime=str(startTime),key2=key2)
                connection.close()
                tmp_query = [dict(row) for row in query_result]
            return {'result':'OK','messageText':tmp_query,'status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def count_select_draft_document_v2_sql(self,email):
        try:
            self.email = email
            tmp_result = {}
            with slave.connect() as connection:
                query_result = connection.execute(text('SELECT COUNT("id") FROM "tb_draft_document" WHERE "tb_draft_document"."sender_email"=:email AND "tb_draft_document"."status"=:status'),email=self.email,status='ACTIVE')
                connection.close()
                tmp_query = [dict(row) for row in query_result]
            # query_result = db.session.query(paperless_draft).filter(paperless_draft.sender_email==self.email)\
            #     .filter(paperless_draft.status=='ACTIVE')\
            #     .count()
            # print (query_result)

            # tmp_result = {
            #     'count' : str(query_result)
            # }
            return {'result':'OK','messageText':tmp_query,'status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200
    
    def search_draft_document_v2_sql(self,key,limit,offset,email):
        try:
            self.key = key
            self.limit = limit
            self.offset = offset
            self.email = email
            list_tmp = []
            key2 = '%' + str(self.key) + '%'
            status = 'ACTIVE'
            # mail = find_email(self.key)
            endTime = ''
            ch,startTime = checkDatetime(self.key)
            text_sql = 'SELECT "id","data_json","data_json_Upload","biz_info","qrCode_position","recipient_email","string_pdf",\
                        "documentJson","options_page","documentType","status","sender_email","update_time","tid","template","type_file","folder_name",\
                        "email_center","step_code","attempted_name","attach_data","importance","last_digitsign","time_expire" FROM "tb_draft_document"'
            where_sql =  ' WHERE "tb_draft_document"."sender_email"=:email AND "tb_draft_document"."status"=:status'
            LIMIT_OFF = ' LIMIT :limit OFFSET :offset'
            ORDER_sql = ' ORDER BY "tb_draft_document"."update_time" DESC'
            if self.limit != '' and self.offset != '':
                if ch == True:
                    endTime = startTime.replace(hour=23, minute=59, second=59, microsecond=0)
                    where_sql += ' AND "tb_draft_document"."update_time" <=:endTime AND "tb_draft_document"."update_time" >=:startTime'
                    text_sql += where_sql + ORDER_sql + LIMIT_OFF
                else:
                    where_sql += ' AND ("tb_draft_document"."documentType" LIKE :key2 OR "tb_draft_document"."recipient_email" LIKE :key2 OR "tb_draft_document"."documentJson" LIKE :key2) '
                    text_sql += where_sql + ORDER_sql + LIMIT_OFF
            else:
                if ch == True:
                    endTime = startTime.replace(hour=23, minute=59, second=59, microsecond=0)
                    where_sql += ' AND "tb_draft_document"."update_time" <=:endTime AND "tb_draft_document"."update_time" >=:startTime'
                    text_sql += where_sql + ORDER_sql
                else:
                    where_sql += ' AND ("tb_draft_document"."documentType" LIKE :key2 OR "tb_draft_document"."recipient_email" LIKE :key2 OR "tb_draft_document"."documentJson" LIKE :key2) '
                    text_sql += where_sql + ORDER_sql
            with slave.connect() as connection:
                query_result = connection.execute(text(text_sql),email=self.email,status='ACTIVE',endTime=str(endTime),startTime=str(startTime),limit=self.limit,offset=self.offset,key2=key2)
                connection.close()
                tmp_query = [dict(row) for row in query_result]
            if tmp_query != None and tmp_query != []:
                for u in range(len(tmp_query)):
                    if tmp_query[u]['attach_data'] != 'None' and tmp_query[u]['attach_data'] != '' and tmp_query[u]['attach_data'] != None:
                        tmp_query[u]['attach_data'] = eval((tmp_query[u]['attach_data']))
                    else:
                        tmp_query[u]['attach_data'] = tmp_query[u]['attach_data']
                    if  tmp_query[u]['time_expire'] != None:
                        time = tmp_query[u]['time_expire']
                        timeDay = int(int(time) / 24 ) 
                        timeHour = int(int(time) % 24 )
                        arr_time = [timeDay,timeHour]
                        tmp_query[u]['time_expire'] = str(arr_time)
                    tmp_query[u]['data_json'] = eval(str(tmp_query[u]['data_json']))
                    tmp_query[u]['data_json_Upload'] = eval(str(tmp_query[u]['data_json_Upload']))
                    tmp_query[u]['documentJson'] = eval(str(tmp_query[u]['documentJson']))
                    tmp_query[u]['options_page'] = eval(str(tmp_query[u]['options_page']))
                    tmp_query[u]['qrCode_position'] = eval(str(tmp_query[u]['qrCode_position']))
                    tmp_query[u]['recipient_email'] = eval(str(tmp_query[u]['recipient_email']))
                    tmp_query[u]['sender_email'] = (tmp_query[u]['sender_email'])
                    tmp_query[u]['data_json'] = eval(str(tmp_query[u]['data_json']))
                    if tmp_query[u]['biz_info'] != 'None' or tmp_query[u]['biz_info'] != [] or tmp_query[u]['biz_info'] != ''or tmp_query[u]['biz_info'] != None:
                        tmp_query[u]['biz_info'] = eval(str(tmp_query[u]['biz_info']))
                    else:
                        tmp_query[u]['biz_info'] = tmp_query[u]['biz_info']
                
                return {'result':'OK','messageText':tmp_query,'status_Code':200,'messageER':None}
            else:
                return {'result':'ER','messageText':'Not found data','status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    # def select_draft_document_by_id_v2_sql(self,tid):
    #     try:
    #         self.tid = tid
    #         list_tmp = []
    #         with engine.connect() as connection:
    #             query_result = connection.execute(text('SELECT "id","data_json","data_json_Upload","biz_info","qrCode_position","recipient_email","string_pdf",\
    #                     "documentJson","options_page","documentType","status","sender_email","update_time","tid","template","type_file","folder_name",\
    #                     "email_center","step_code","attempted_name","attach_data","importance","last_digitsign","time_expire" FROM "tb_draft_document" WHERE "tb_draft_document"."tid"=:tid AND "tb_draft_document"."status"=:status'),tid=self.tid,status='ACTIVE')
    #             connection.close()
    #             tmp_query = [dict(row) for row in query_result]
    #         if tmp_query != None and tmp_query != []:
    #             for u in range(len(tmp_query)):
    #                 if tmp_query[u]['attach_data'] != 'None' and tmp_query[u]['attach_data'] != '' and tmp_query[u]['attach_data'] != None:
    #                     tmp_query[u]['attach_data'] = eval((tmp_query[u]['attach_data']))
    #                 else:
    #                     tmp_query[u]['attach_data'] = tmp_query[u]['attach_data']
    #                 if  tmp_query[u]['time_expire'] != None:
    #                     time = tmp_query[u]['time_expire']
    #                     timeDay = int(int(time) / 24 ) 
    #                     timeHour = int(int(time) % 24 )
    #                     arr_time = [timeDay,timeHour]
    #                     tmp_query[u]['time_expire'] = str(arr_time)
    #                 tmp_query[u]['data_json'] = eval(str(tmp_query[u]['data_json']))
    #                 tmp_query[u]['data_json_Upload'] = eval(str(tmp_query[u]['data_json_Upload']))
    #                 tmp_query[u]['documentJson'] = eval(str(tmp_query[u]['documentJson']))
    #                 tmp_query[u]['options_page'] = eval(str(tmp_query[u]['options_page']))
    #                 tmp_query[u]['qrCode_position'] = eval(str(tmp_query[u]['qrCode_position']))
    #                 tmp_query[u]['recipient_email'] = eval(str(tmp_query[u]['recipient_email']))
    #                 tmp_query[u]['sender_email'] = (tmp_query[u]['sender_email'])
    #                 tmp_query[u]['data_json'] = eval(str(tmp_query[u]['data_json']))
    #                 if tmp_query[u]['biz_info'] != 'None' or tmp_query[u]['biz_info'] != [] or tmp_query[u]['biz_info'] != ''or tmp_query[u]['biz_info'] != None:
    #                     tmp_query[u]['biz_info'] = eval(str(tmp_query[u]['biz_info']))
    #                 else:
    #                     tmp_query[u]['biz_info'] = tmp_query[u]['biz_info']
                
    #             return {'result':'OK','messageText':tmp_query,'status_Code':200,'messageER':None}
    #         else:
    #             return {'result':'OK','messageText':'Not have data','status_Code':200,'messageER':None}
    #     except Exception as e:
    #         exc_type, exc_obj, exc_tb = sys.exc_info()
    #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #         print(exc_type, fname, exc_tb.tb_lineno)
    #         return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def select_draft_document_by_id_v2_sql(self,tid):
        try:
            self.tid = tid
            list_tmp = []
            with slave.connect() as connection:
                query_result = connection.execute(text('SELECT "id","data_json","data_json_Upload","biz_info","qrCode_position","recipient_email","string_pdf",\
                        "documentJson","options_page","documentType","status","sender_email","update_time","tid","template","type_file","folder_name",\
                        "email_center","step_code","attempted_name","attach_data","importance","last_digitsign","time_expire","status_ref","list_ref" FROM "tb_draft_document" WHERE "tb_draft_document"."tid"=:tid AND "tb_draft_document"."status"=:status'),tid=self.tid,status='ACTIVE')
                connection.close()
                tmp_query = [dict(row) for row in query_result]
            if tmp_query != None and tmp_query != []:
                for u in range(len(tmp_query)):
                    if tmp_query[u]['attach_data'] != 'None' and tmp_query[u]['attach_data'] != '' and tmp_query[u]['attach_data'] != None:
                        tmp_query[u]['attach_data'] = eval((tmp_query[u]['attach_data']))
                    else:
                        tmp_query[u]['attach_data'] = tmp_query[u]['attach_data']
                    if  tmp_query[u]['time_expire'] != None:
                        time = tmp_query[u]['time_expire']
                        timeDay = int(int(time) / 24 ) 
                        timeHour = int(int(time) % 24 )
                        arr_time = [timeDay,timeHour]
                        tmp_query[u]['time_expire'] = str(arr_time)
                    tmp_query[u]['data_json'] = eval(str(tmp_query[u]['data_json']))
                    tmp_query[u]['data_json_Upload'] = eval(str(tmp_query[u]['data_json_Upload']))
                    tmp_query[u]['documentJson'] = eval(str(tmp_query[u]['documentJson']))
                    tmp_query[u]['options_page'] = eval(str(tmp_query[u]['options_page']))
                    tmp_query[u]['qrCode_position'] = eval(str(tmp_query[u]['qrCode_position']))
                    tmp_query[u]['recipient_email'] = eval(str(tmp_query[u]['recipient_email']))
                    tmp_query[u]['sender_email'] = (tmp_query[u]['sender_email'])
                    tmp_query[u]['data_json'] = eval(str(tmp_query[u]['data_json']))
                    if tmp_query[u]['biz_info'] != 'None' or tmp_query[u]['biz_info'] != [] or tmp_query[u]['biz_info'] != ''or tmp_query[u]['biz_info'] != None:
                        tmp_query[u]['biz_info'] = eval(str(tmp_query[u]['biz_info']))
                    else:
                        tmp_query[u]['biz_info'] = tmp_query[u]['biz_info']
                
                return {'result':'OK','messageText':tmp_query,'status_Code':200,'messageER':None}
            else:
                return {'result':'OK','messageText':'Not have data','status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    # def select_draft_document_v2_sql(self,email,limit,offset):
    #     try:
    #         self.email = email
    #         self.limit = limit
    #         self.offset = offset
    #         list_tmp = []
    #         if self.limit != '' and self.offset != '':
    #             with engine.connect() as connection:
    #                 query_result = connection.execute(text('SELECT "id","data_json","data_json_Upload","biz_info","qrCode_position","recipient_email","string_pdf",\
    #                 "documentJson","options_page","documentType","status","sender_email","update_time","tid","template",\
    #                 "type_file","folder_name","email_center","step_code","attempted_name","attach_data","importance","last_digitsign","time_expire" \
    #                 FROM "tb_draft_document" WHERE "tb_draft_document"."sender_email"=:email AND "tb_draft_document"."status"=:status\
    #                 LIMIT :limit OFFSET :offset'),email=self.email,status='ACTIVE',limit=int(self.limit),offset=int(self.offset))
    #                 connection.close()
    #                 tmp_query = [dict(row) for row in query_result]
    #         else:
    #             print('else')
    #             with engine.connect() as connection:
    #                 query_result = connection.execute(text('SELECT "id","data_json","data_json_Upload","biz_info","qrCode_position","recipient_email","string_pdf",\
    #                 "documentJson","options_page","documentType","status","sender_email","update_time","tid","template",\
    #                 "type_file","folder_name","email_center","step_code","attempted_name","attach_data","importance","last_digitsign","time_expire" \
    #                 FROM "tb_draft_document" WHERE "tb_draft_document"."sender_email"=:email AND "tb_draft_document"."status"=:status\
    #                 '),email=self.email,status='ACTIVE')
    #                 connection.close()
    #                 tmp_query = [dict(row) for row in query_result]
    #         print('len tmp_query',len(tmp_query))
    #         if tmp_query != None and tmp_query != []:
    #             for u in range(len(tmp_query)):
    #                 if tmp_query[u]['attach_data'] != 'None' and tmp_query[u]['attach_data'] != '' and tmp_query[u]['attach_data'] != None:
    #                     tmp_query[u]['attach_data'] = eval((tmp_query[u]['attach_data']))
    #                 else:
    #                     tmp_query[u]['attach_data'] = tmp_query[u]['attach_data']
    #                 if  tmp_query[u]['time_expire'] != None:
    #                     time = tmp_query[u]['time_expire']
    #                     timeDay = int(int(time) / 24 ) 
    #                     timeHour = int(int(time) % 24 )
    #                     arr_time = [timeDay,timeHour]
    #                     tmp_query[u]['time_expire'] = str(arr_time)
    #                 tmp_query[u]['data_json'] = eval(str(tmp_query[u]['data_json']))
    #                 tmp_query[u]['data_json_Upload'] = eval(str(tmp_query[u]['data_json_Upload']))
    #                 tmp_query[u]['documentJson'] = eval(str(tmp_query[u]['documentJson']))
    #                 tmp_query[u]['options_page'] = eval(str(tmp_query[u]['options_page']))
    #                 tmp_query[u]['qrCode_position'] = eval(str(tmp_query[u]['qrCode_position']))
    #                 tmp_query[u]['recipient_email'] = eval(str(tmp_query[u]['recipient_email']))
    #                 tmp_query[u]['sender_email'] = (tmp_query[u]['sender_email'])
    #                 tmp_query[u]['data_json'] = eval(str(tmp_query[u]['data_json']))
    #                 if tmp_query[u]['biz_info'] != 'None' or tmp_query[u]['biz_info'] != [] or tmp_query[u]['biz_info'] != ''or tmp_query[u]['biz_info'] != None:
    #                     tmp_query[u]['biz_info'] = eval(str(tmp_query[u]['biz_info']))
    #                 else:
    #                     tmp_query[u]['biz_info'] = tmp_query[u]['biz_info']
                
    #             return {'result':'OK','messageText':tmp_query,'status_Code':200,'messageER':None}
    #         else:
    #             return {'result':'OK','messageText':'Not have data','status_Code':200,'messageER':None}
    #     except Exception as e:
    #         exc_type, exc_obj, exc_tb = sys.exc_info()
    #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #         print(exc_type, fname, exc_tb.tb_lineno)
    #         return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def select_draft_document_v2_sql(self,email,limit,offset):
        try:
            self.email = email
            self.limit = limit
            self.offset = offset
            list_tmp = []
            if self.limit != '' and self.offset != '':
                with slave.connect() as connection:
                    query_result = connection.execute(text('SELECT "id","data_json","data_json_Upload","biz_info","qrCode_position","recipient_email","string_pdf",\
                    "documentJson","options_page","documentType","status","sender_email","update_time","tid","template",\
                    "type_file","folder_name","email_center","step_code","attempted_name","attach_data","importance","last_digitsign","time_expire","status_ref","list_ref" \
                    FROM "tb_draft_document" WHERE "tb_draft_document"."sender_email"=:email AND "tb_draft_document"."status"=:status\
                    LIMIT :limit OFFSET :offset'),email=self.email,status='ACTIVE',limit=int(self.limit),offset=int(self.offset))
                    connection.close()
                    tmp_query = [dict(row) for row in query_result]
            else:
                print('else')
                with slave.connect() as connection:
                    query_result = connection.execute(text('SELECT "id","data_json","data_json_Upload","biz_info","qrCode_position","recipient_email","string_pdf",\
                    "documentJson","options_page","documentType","status","sender_email","update_time","tid","template",\
                    "type_file","folder_name","email_center","step_code","attempted_name","attach_data","importance","last_digitsign","time_expire","status_ref","list_ref" \
                    FROM "tb_draft_document" WHERE "tb_draft_document"."sender_email"=:email AND "tb_draft_document"."status"=:status\
                    '),email=self.email,status='ACTIVE')
                    connection.close()
                    tmp_query = [dict(row) for row in query_result]
            print('len tmp_query',len(tmp_query))
            if tmp_query != None and tmp_query != []:
                for u in range(len(tmp_query)):
                    if tmp_query[u]['attach_data'] != 'None' and tmp_query[u]['attach_data'] != '' and tmp_query[u]['attach_data'] != None:
                        tmp_query[u]['attach_data'] = eval((tmp_query[u]['attach_data']))
                    else:
                        tmp_query[u]['attach_data'] = tmp_query[u]['attach_data']
                    if  tmp_query[u]['time_expire'] != None:
                        time = tmp_query[u]['time_expire']
                        timeDay = int(int(time) / 24 ) 
                        timeHour = int(int(time) % 24 )
                        arr_time = [timeDay,timeHour]
                        tmp_query[u]['time_expire'] = str(arr_time)
                    tmp_query[u]['data_json'] = eval(str(tmp_query[u]['data_json']))
                    tmp_query[u]['data_json_Upload'] = eval(str(tmp_query[u]['data_json_Upload']))
                    tmp_query[u]['documentJson'] = eval(str(tmp_query[u]['documentJson']))
                    tmp_query[u]['options_page'] = eval(str(tmp_query[u]['options_page']))
                    tmp_query[u]['qrCode_position'] = eval(str(tmp_query[u]['qrCode_position']))
                    tmp_query[u]['recipient_email'] = eval(str(tmp_query[u]['recipient_email']))
                    tmp_query[u]['sender_email'] = (tmp_query[u]['sender_email'])
                    tmp_query[u]['data_json'] = eval(str(tmp_query[u]['data_json']))
                    if tmp_query[u]['biz_info'] != 'None' or tmp_query[u]['biz_info'] != [] or tmp_query[u]['biz_info'] != ''or tmp_query[u]['biz_info'] != None:
                        tmp_query[u]['biz_info'] = eval(str(tmp_query[u]['biz_info']))
                    else:
                        tmp_query[u]['biz_info'] = tmp_query[u]['biz_info']
                
                return {'result':'OK','messageText':tmp_query,'status_Code':200,'messageER':None}
            else:
                return {'result':'OK','messageText':'Not have data','status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200
    
    def select_step_data_draft(self,sid):
        try:
            self.sid = sid
            list_json = []
            query_result_step_data = paper_lessdatastep.query.with_entities(paper_lessdatastep.data_json,paper_lessdatastep.data_json_Upload,paper_lessdatastep.biz_info,paper_lessdatastep.qrCode_position).filter(paper_lessdatastep.sid == self.sid).first()
            result_select = db.session.query(paper_lessdatastep).filter(paper_lessdatastep.sid == self.sid).all()
            for x in range(len(result_select)):
                tmp_json = {}
                tmp_json['sid'] = str(result_select[x].sid)
                tmp_json['data_json'] = eval(str(result_select[x].data_json))
                tmp_json['data_json_Upload'] = eval(str(result_select[x].data_json_Upload))
                if result_select[x].biz_info != None and result_select[x].biz_info != '':
                    tmp_json['biz_info'] = eval(str(result_select[x].biz_info))
                else:
                    tmp_json['biz_info'] = result_select[x].biz_info
                tmp_json['qrCode_position'] = eval(str(result_select[x].qrCode_position))
                list_json.append(tmp_json)
            return {'result':'OK','messageText':list_json,'status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def select_pdf_detail(self,sid):
        try:
            self.sid = sid
            tmp_query = {}
            list_query = []
            query_result = db.session.query(\
                paper_lesssender,
                paper_lesspdf,
                paper_lessdocument
                
            )\
            .join(paper_lesssender,paper_lesssender.file_id==paper_lesspdf.fid)\
            .join(paper_lessdocument,paper_lessdocument.step_id==paper_lesssender.step_data_sid)\
            .filter(paper_lesssender.step_data_sid==self.sid)\
            .first()
            # print (query_result)
            for u in range(len(query_result)):
                # print (u)
                tmpjson = query_result[u].__dict__
                
                if '_sa_instance_state' in tmpjson:
                    del tmpjson['_sa_instance_state']
                if u == 0 :
                    tmp_query['step_data_sid'] = tmpjson['step_data_sid']
                    tmp_query['sender_email'] = (str(tmpjson['sender_email']))
                    tmp_query['recipient_email'] = eval(str(tmpjson['recipient_email']))
                if u == 1:
                    tmp_query['string_pdf'] = tmpjson['string_pdf']
                if u == 2:
                    tmp_query['documentJson'] = eval(str(tmpjson['documentJson']))
                    tmp_query['options_page'] = eval(str(tmpjson['options_page']))
                    tmp_query['documentType'] = tmpjson['documentType']

            # print (tmp_query)
            return {'result':'OK','messageText':tmp_query,'status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def count_select_draft_document(self,email):
        try:
            self.email = email
            tmp_result = {}
            query_result = db.session.query(paperless_draft).filter(paperless_draft.sender_email==self.email)\
                .filter(paperless_draft.status=='ACTIVE')\
                .count()
            print (query_result)
            tmp_result = {
                'count' : str(query_result)
            }
            return {'result':'OK','messageText':tmp_result,'status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200


    def select_draft_document(self,email,limit,offset):
        try:
            self.email = email
            self.limit = limit
            self.offset = offset
            list_tmp = []
            if self.limit != '' and self.offset != '':
                query_result = db.session.query(paperless_draft).filter(paperless_draft.sender_email==self.email)\
                    .filter(paperless_draft.status=='ACTIVE')\
                    .limit(self.limit)\
                    .offset(self.offset)\
                    .all()
            else:
                query_result = db.session.query(paperless_draft).filter(paperless_draft.sender_email==self.email)\
                    .filter(paperless_draft.status=='ACTIVE')\
                    .all()
            if query_result != None and query_result != []:
                for u in range(len(query_result)):
                    tmpjson = query_result[u].__dict__
                    if '_sa_instance_state' in tmpjson:
                        del tmpjson['_sa_instance_state']
                    tmpjson['data_json'] = eval(str(tmpjson['data_json']))
                    tmpjson['data_json_Upload'] = eval(str(tmpjson['data_json_Upload']))
                    tmpjson['documentJson'] = eval(str(tmpjson['documentJson']))
                    tmpjson['options_page'] = eval(str(tmpjson['options_page']))
                    tmpjson['qrCode_position'] = eval(str(tmpjson['qrCode_position']))
                    tmpjson['recipient_email'] = eval(str(tmpjson['recipient_email']))
                    if tmpjson['biz_info'] != 'None' and tmpjson['biz_info'] != [] and tmpjson['biz_info'] != ''and tmpjson['biz_info'] != None:
                        tmpjson['biz_info'] = eval(str(tmpjson['biz_info']))
                    else:
                        tmpjson['biz_info'] = tmpjson['biz_info']
                        tmpjson['sender_email'] = (tmpjson['sender_email'])
                    list_tmp.append(tmpjson)
                return {'result':'OK','messageText':list_tmp,'status_Code':200,'messageER':None}
            else:
                return {'result':'OK','messageText':'Not have data','status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def select_draft_document_by_id(self,tid):
        try:
            self.tid = tid
            list_tmp = []
            query_result = db.session.query(paperless_draft).filter(paperless_draft.tid==self.tid).filter(paperless_draft.status=='ACTIVE').all()
            if query_result != None and query_result != []:
                for u in range(len(query_result)):
                    tmpjson = query_result[u].__dict__
                    if '_sa_instance_state' in tmpjson:
                        del tmpjson['_sa_instance_state']
                    tmpjson['data_json'] = eval(str(tmpjson['data_json']))
                    tmpjson['data_json_Upload'] = eval(str(tmpjson['data_json_Upload']))
                    tmpjson['documentJson'] = eval(str(tmpjson['documentJson']))
                    tmpjson['options_page'] = eval(str(tmpjson['options_page']))
                    tmpjson['qrCode_position'] = eval(str(tmpjson['qrCode_position']))
                    tmpjson['recipient_email'] = eval(str(tmpjson['recipient_email']))
                    if tmpjson['attach_data'] != None:
                        tmpjson['attach_data'] = eval(str(tmpjson['attach_data']))
                    if tmpjson['biz_info'] != 'None' and tmpjson['biz_info'] != [] and tmpjson['biz_info'] != ''and tmpjson['biz_info'] != None:
                        tmpjson['biz_info'] = eval(str(tmpjson['biz_info']))
                    else:
                        tmpjson['biz_info'] = tmpjson['biz_info']
                        tmpjson['sender_email'] = (tmpjson['sender_email'])
                    list_tmp.append(tmpjson)
                return {'result':'OK','messageText':list_tmp,'status_Code':200,'messageER':None}
            else:
                return {'result':'OK','messageText':'Not have data','status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def search_draft_document(self,key,limit,offset,email):
        try:
            self.key = key
            self.limit = limit
            self.offset = offset
            self.email = email
            list_tmp = []
            key2 = '%' + str(self.key) + '%'
            # mail = find_email(self.key)
            endTime = ''
            ch,startTime = checkDatetime(self.key)
            if self.limit != '' and self.offset != '':
                if ch == True:
                    endTime = startTime.replace(hour=23, minute=59, second=59, microsecond=0)
                    print ('startTime: ',startTime)
                    print ('endtime: ',endTime)
                    query_result = db.session.query(paperless_draft).filter(paperless_draft.sender_email==self.email)\
                        .filter(paperless_draft.status=='ACTIVE')\
                        .filter(paperless_draft.update_time <= str(endTime))\
                        .filter(paperless_draft.update_time >= str(startTime))\
                        .order_by(desc(paperless_draft.update_time))\
                        .limit(self.limit)\
                        .offset(self.offset)\
                        .all()
                else:
                    query_result = db.session.query(paperless_draft).filter(paperless_draft.sender_email==self.email)\
                        .filter(paperless_draft.status=='ACTIVE')\
                        .filter(or_(paperless_draft.documentType.ilike(key2),paperless_draft.recipient_email.ilike(key2),paperless_draft.documentJson.ilike(key2)))\
                        .limit(self.limit)\
                        .offset(self.offset)\
                        .all()
            else:
                if ch == True:
                    endTime = startTime.replace(hour=23, minute=59, second=59, microsecond=0)
                    print ('startTime: ',startTime)
                    print ('endtime: ',endTime)
                    query_result = db.session.query(paperless_draft).filter(paperless_draft.sender_email==self.email)\
                        .filter(paperless_draft.status=='ACTIVE')\
                        .filter(paperless_draft.update_time <= str(endTime))\
                        .filter(paperless_draft.update_time >= str(startTime))\
                        .order_by(desc(paperless_draft.update_time))\
                        .all()
                else:
                    query_result = db.session.query(paperless_draft).filter(paperless_draft.sender_email==self.email)\
                        .filter(paperless_draft.status=='ACTIVE')\
                        .filter(or_(paperless_draft.documentType.ilike(key2),paperless_draft.recipient_email.ilike(key2),paperless_draft.documentJson.ilike(key2)))\
                        .all()  
            if query_result != None and query_result != []:
                for u in range(len(query_result)):
                    tmpjson = query_result[u].__dict__
                    if '_sa_instance_state' in tmpjson:
                        del tmpjson['_sa_instance_state']
                    tmpjson['data_json'] = eval(str(tmpjson['data_json']))
                    tmpjson['data_json_Upload'] = eval(str(tmpjson['data_json_Upload']))
                    tmpjson['documentJson'] = eval(str(tmpjson['documentJson']))
                    tmpjson['options_page'] = eval(str(tmpjson['options_page']))
                    tmpjson['qrCode_position'] = eval(str(tmpjson['qrCode_position']))
                    tmpjson['recipient_email'] = eval(str(tmpjson['recipient_email']))
                    if tmpjson['biz_info'] != 'None' and tmpjson['biz_info'] != [] and tmpjson['biz_info'] != ''and tmpjson['biz_info'] != None:
                        tmpjson['biz_info'] = eval(str(tmpjson['biz_info']))
                    else:
                        tmpjson['biz_info'] = tmpjson['biz_info']
                        tmpjson['sender_email'] = (tmpjson['sender_email'])
                    list_tmp.append(tmpjson)
                return {'result':'OK','messageText':list_tmp,'status_Code':200,'messageER':None}
            else:
                return {'result':'ER','messageText':'Not found data','status_Code':200,'messageER':None}

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def select_service_other_log_v1(self,service_list,str_datetime,end_datetime):
        self.service_list = service_list
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        # int(time.mktime(datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S").timetuple()))
        # str_datetime = str(st).split(' ')[0] + ' ' + '00:00:00'
        # end_datetime = str(st).split(' ')[0] + ' ' + '23:59:59'
        # print(str_datetime,end_datetime)
        # str_datetime = '2020-05-25 00:00:00'
        # end_datetime = '2020-05-25 23:59:59'
        tmp_datetime = datetime.datetime.fromtimestamp(ts)
        arr_result = []
        try:
            # query_tmp = db.session.query(
            #     tb_transaction_servicelog,
            #     paper_lessdocument)\
            #     .join(paper_lessdocument,paper_lessdocument.step_id==tb_transaction_servicelog.sidcode)\
            #     .filter(and_(tb_transaction_servicelog.datetime>=str_datetime,tb_transaction_servicelog.datetime<=end_datetime))\
            #     .all()
            sql = '''select "tb_transaction_servicelog".sidcode,"tb_transaction_servicelog".status,"tb_transaction_servicelog".datetime,"tb_doc_detail".document_id,"tb_doc_detail"."documentType",
                    "tb_transactionSftp".ID AS "id",
                    "tb_transactionSftp".status AS "status",
                    "tb_transactionSftp".folder_path AS "folder_path",
                    "tb_transactionSftp".date_time AS "date_time",
                    "tb_transactionSftp".document_type AS "document_type" 
                    FROM "tb_transaction_servicelog" 
                    INNER JOIN tb_doc_detail ON tb_transaction_servicelog.sidcode = tb_doc_detail.step_id 
                    LEFT OUTER JOIN "tb_transactionSftp" ON "tb_transactionSftp".folder_path LIKE'%%' || tb_doc_detail.attempted_folder || '%%' 
                    where tb_transaction_servicelog.datetime >= :str_datetime AND tb_transaction_servicelog.datetime<=:end_datetime '''
            connection = slave.connect()
            result = connection.execute(text(sql),str_datetime=str_datetime,end_datetime=end_datetime)
            connection.close()
            resultQuery = [dict(row) for row in result]
            if len(resultQuery) != 0:
                for x in range(len(resultQuery)):
                    tmpdata = resultQuery[x]
                    json_result = {}
                    tmpsidcode = tmpdata['sidcode']
                    json_result['datetime'] = str(tmpdata['datetime']).split('+')[0]
                    json_result['status'] = tmpdata['status']
                    json_result['document_id'] = tmpdata['document_id']
                    json_result['documentType'] = tmpdata['documentType']
                    # sql = '''
                    #     SELECT
                    #         tb_doc_detail.ID AS "doc_detail_id",
                    #         "tb_transactionSftp".ID AS "id",
                    #         "tb_transactionSftp".status AS "status",
                    #         "tb_transactionSftp".folder_path AS "folder_path",
                    #         "tb_transactionSftp".date_time AS "date_time",
                    #         "tb_transactionSftp".document_type AS "document_type" 
                    #     FROM
                    #         tb_doc_detail
                    #         LEFT OUTER JOIN "tb_transactionSftp" ON "tb_transactionSftp".folder_path LIKE'%%' || tb_doc_detail.attempted_folder || '%%' 
                    #     WHERE tb_doc_detail.step_id = :sidcode
                    # '''
                    # connection = slave.connect()
                    # result_02 = connection.execute(text(sql),sidcode=tmpsidcode)
                    # resultQuery_02 = [dict(row) for row in result_02]
                    # connection.close()
                    # if len(resultQuery_02) != 0:
                        # tmpdatasftp = resultQuery_02[0]
                    if tmpdata['id'] != None:
                        tmpstatus_sftp = tmpdata['status']
                        if 'Errno' in tmpstatus_sftp:
                            json_result['status'] = 'ER'
                            json_result['message'] = tmpstatus_sftp
                        else:
                            json_result['status'] = 'OK'
                            json_result['message'] = tmpstatus_sftp
                    arr_result.append(json_result)
                    # tmp_query_status = db.session.query(
                    #     paper_lessdocument,
                    #     paper_lesstransactionSftp
                    #     )\
                    #     .outerjoin(paper_lesstransactionSftp,paper_lesstransactionSftp.folder_path.contains(paper_lessdocument.attempted_folder))\
                    #     .filter(paper_lessdocument.step_id==tmpsidcode)
                    # print(tmp_query_status)
            return {'result':'OK','messageText':arr_result}
            if len(query_tmp) != 0:
                for x in range(len(query_tmp)):
                    json_result = {}
                    tmpqueryjson = query_tmp[x]
                    for i in range(len(tmpqueryjson)):
                        if i == 0:
                            jsonserviceLog = tmpqueryjson[i].__dict__
                            tmpsidcode = jsonserviceLog['sidcode']
                            tmpstatus = jsonserviceLog['status']
                            tmpdatetime = str(jsonserviceLog['datetime']).split('+')[0]
                            json_result['datetime'] = tmpdatetime
                            json_result['status'] = tmpstatus
                        if i == 1:
                            jsonDocument = tmpqueryjson[i].__dict__
                            tmpdoc_id = jsonDocument['document_id']
                            tmp_document = jsonDocument['documentType']
                            json_result['document_id'] = tmpdoc_id
                            json_result['documentType'] = tmp_document
                    tmp_query_status = db.session.query(
                        paper_lessdocument,
                        paper_lesstransactionSftp
                        )\
                        .outerjoin(paper_lesstransactionSftp,paper_lesstransactionSftp.folder_path.contains(paper_lessdocument.attempted_folder))\
                        .filter(paper_lessdocument.step_id==tmpsidcode)\
                        .first()
                    if tmp_query_status != None:
                        tmpjson = tmp_query_status._asdict()
                        if 'paper_lesstransactionSftp' in tmpjson:
                            if tmpjson['paper_lesstransactionSftp'] != None:
                                tmpjson['paper_lesstransactionSftp'] = tmpjson['paper_lesstransactionSftp'].__dict__
                                if 'status' in tmpjson['paper_lesstransactionSftp']:
                                    tmpstatus_sftp = tmpjson['paper_lesstransactionSftp']['status']
                                    if 'Errno' in tmpstatus_sftp:
                                        json_result['status'] = 'ER'
                                        json_result['message'] = tmpstatus_sftp
                                    else:
                                        json_result['status'] = 'OK'
                                        json_result['message'] = tmpstatus_sftp
                    arr_result.append(json_result)
                return {'result':'OK','messageText':arr_result}
            else:
                return {'result':'ER','messageER':'data not found'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200})
        finally:
            connection.close()
            
    def select_bizname_by_taxid(self,tax_id):
        try:
            if tax_id == None:
                return {'result':'OK','messageText':None}
            elif tax_id != None:
                self.tax_id = tax_id
                result_query = db.session.query(paper_lessbizProfile).filter(paper_lessbizProfile.bizTax == self.tax_id).all()
                for i in range(len(result_query)):
                    tmp_query = result_query[i].__dict__
                    if '_sa_instance_state' in tmp_query:
                        del tmp_query['_sa_instance_state']
                    if 'bizInfoJson' in tmp_query :
                        if tmp_query['bizInfoJson'] != '':
                            # tmp_query['biz_info'] = eval(str(tmp_query['biz_info']))
                            eval_biz = eval(str(tmp_query['bizInfoJson']))
                            if type(eval_biz) == dict:
                                for x in range(len(tmp_query['bizInfoJson'])):
                                    tmp_biz = {}
                                    tmp_biz['first_name_th'] = eval_biz['first_name_th']
                                tmp_query['bizInfoJson'] = tmp_biz

                            elif type(eval_biz) == list:
                                for x in range(len(tmp_query['bizInfoJson'])):
                                    tmp_biz = {}
                                    tmp_biz['first_name_th'] = eval_biz[0]['first_name_th']
                                tmp_query['bizInfoJson'] = tmp_biz
                    biz_name = tmp_query['bizInfoJson']['first_name_th']
                return {'result':'OK','messageText':str(biz_name)}
        except Exception as e:
            return {'result':'ER','messageText':str(e)}

    def select_pdf_filename(self,sid):
        self.sid = sid
        try:
            result_query = db.session.query(paper_lesssender.file_name,paper_lesssender.doc_id).filter(paper_lesssender.step_data_sid == self.sid).first()
            print ('result_query2: ',(result_query[0]))
            file_name = str(result_query[0])
            doc_id = str(result_query[1])
            
            return {'result': 'OK', 'messageText': {'file_name':str(file_name),'doc_id':str(doc_id)}}

        except Exception as ex:
            return {'result': 'ER', 'messageText': str(ex)}

    def select_get_pdf(self,data_idfile):
        self.data_idfile = data_idfile
        try:
            file_json = {}
            for i in paper_lessdatastep.query.filter_by(sid=self.data_idfile).all():
                file_json['datetime'] = i.update_time
                file_json['datetime_string'] = str(i.update_time).split('+')[0]
                file_json['datetime_upload'] = i.upload_time
                file_json['datetime_upload_string'] = str(i.upload_time).split('+')[0]
            for u in paper_lesstrack.query.filter_by(step_data_sid=self.data_idfile).all():
                for a in paper_lesspdf.query.filter_by(fid=u.file_id).all():
                    if a.string_sign == None or len(a.string_sign) == 0:
                        file_json['file_base'] = a.string_pdf
                        return {'result': 'OK', 'messageText': file_json,'status_Code':200}
                    else:
                        file_json['file_base'] = a.string_sign
                        return {'result': 'OK', 'messageText': file_json,'status_Code':200}
            return {'result': 'ER', 'messageText': 'Not Found!'}
        except Exception as ex:
            return {'result': 'ER', 'messageText': str(ex)}

    def select_tax_id_to_onebox(self,sidcode,tax_id):
        self.sidcode = sidcode
        self.tax_id = tax_id
        try:
            tq = db.session.query(\
                paper_lessdocument,
                paper_lessdatastep,
                paper_lesssender
            )\
            .join(paper_lesssender,paper_lesssender.step_data_sid==paper_lessdocument.step_id)\
            .join(paper_lessdatastep,paper_lessdatastep.sid==paper_lessdocument.step_id)\
            .filter(paper_lessdocument.step_id==self.sidcode)\
            .first()
            tmp_biz_info = None
            tmp_usersender = None
            # print(tq[1])
            for u in range(len(tq)):
                # print(u)
                tmpjson = tq[u].__dict__
                if '_sa_instance_state' in tmpjson:
                    del tmpjson['_sa_instance_state']
                if u == 0:
                    # print(tmpjson)
                    tmp_document_type = tmpjson['documentType']
                if u == 1:
                    tmp_biz_info = tmpjson['biz_info']
                if u == 2:
                    tmp_usersender = tmpjson['send_user']
                if tmp_biz_info == 'None':
                    tmp_biz_info = None
            if tmp_biz_info != None:
                try:
                    tmp_biz_info = eval(tmp_biz_info)
                    tmp_id_card_num = tmp_biz_info['id_card_num']
                    return {'result':'OK','messageText':str(tmp_id_card_num)}
                except Exception as e:
                    tax_id = None
                    tmp_id_card_num =None
            else:
                return {'result':'ER'}
        except Exception as e:
            print(str(e))
            return {'result':'ER','messageText':str(e)}

    def select_template_forgroup(self,tax_id,username,document_type):
        self.tax_id = tax_id
        self.username = username
        self.document_type = document_type
        arr_tmp = []
        if self.tax_id != None and self.username == None and self.document_type == None:
            tempquery = db.session.query(
                paper_lessstep.step_Code,
                paper_lessstep.step_Name,
                paper_lessstep.status_use,
                paper_lessstep.documentDetails,
                paper_lessstep.condition_temp,
                paper_lessstep.options_page
                )\
                .filter(and_(paper_lessstep.template_biz.contains(self.tax_id),paper_lessstep.status=='ACTIVE')).all()
            if len(tempquery) != 0:
                for x in range(len(tempquery)):
                    tmp_status_group = False
                    if tempquery[x][5] != None:
                        tmp_optionpage = eval(tempquery[x][5])
                        if 'group_detail' in tmp_optionpage:
                            if 'group_status' in tmp_optionpage['group_detail']:
                                if tmp_optionpage['group_detail']['group_status'] == True:
                                    tmp_status_group = True
                                # print(tmp_optionpage)
                    if tmp_status_group == True:
                        tmp_template = {
                            'template_code':tempquery[x][0],
                            'template_name':tempquery[x][1],
                            'use_status':tempquery[x][2],
                            'document_type':tempquery[x][3],
                            'template_condition':tempquery[x][4]
                        }
                        arr_tmp.append(tmp_template)
            else:
                return {'result':'ER','messageER':'data not found'}
        elif self.tax_id != None and self.username == None and self.document_type != None:
            tempquery = db.session.query(
                paper_lessstep.step_Code,
                paper_lessstep.step_Name,
                paper_lessstep.status_use,
                paper_lessstep.documentDetails,
                paper_lessstep.condition_temp,
                paper_lessstep.options_page
                )\
                .filter(and_(paper_lessstep.template_biz.contains(self.tax_id),paper_lessstep.status=='ACTIVE',paper_lessstep.documentDetails==self.document_type)).all()
            if len(tempquery) != 0:
                for x in range(len(tempquery)):
                    tmp_status_group = False
                    if tempquery[x][5] != None:
                        tmp_optionpage = eval(tempquery[x][5])
                        if 'group_detail' in tmp_optionpage:
                            if 'group_status' in tmp_optionpage['group_detail']:
                                if tmp_optionpage['group_detail']['group_status'] == True:
                                    tmp_status_group = True
                                # print(tmp_optionpage)
                    if tmp_status_group == True:
                        tmp_template = {
                            'template_code':tempquery[x][0],
                            'template_name':tempquery[x][1],
                            'use_status':tempquery[x][2],
                            'document_type':tempquery[x][3],
                            'template_condition':tempquery[x][4]
                        }
                        arr_tmp.append(tmp_template)
            else:
                return {'result':'ER','messageER':'data not found'}
        elif self.username != None and self.tax_id == None and self.document_type == None:
            tempquery = db.session.query(
                paper_lessstep.step_Code,
                paper_lessstep.step_Name,
                paper_lessstep.status_use,
                paper_lessstep.documentDetails,
                paper_lessstep.condition_temp,
                paper_lessstep.options_page
                )\
                .filter(and_(paper_lessstep.username==self.username,paper_lessstep.status=='ACTIVE')).all()
            if len(tempquery) != 0:
                for x in range(len(tempquery)):
                    tmp_status_group = False
                    if tempquery[x][5] != None:
                        tmp_optionpage = eval(tempquery[x][5])
                        if 'group_detail' in tmp_optionpage:
                            if 'group_status' in tmp_optionpage['group_detail']:
                                if tmp_optionpage['group_detail']['group_status'] == True:
                                    tmp_status_group = True
                                # print(tmp_optionpage)
                    if tmp_status_group == True:
                        tmp_template = {
                            'template_code':tempquery[x][0],
                            'template_name':tempquery[x][1],
                            'use_status':tempquery[x][2],
                            'document_type':tempquery[x][3],
                            'template_condition':tempquery[x][4]
                        }
                        arr_tmp.append(tmp_template)
            else:
                return {'result':'ER','messageER':'data not found'}
        elif self.username != None and self.tax_id == None and self.document_type != None:
            tempquery = db.session.query(
                paper_lessstep.step_Code,
                paper_lessstep.step_Name,
                paper_lessstep.status_use,
                paper_lessstep.documentDetails,
                paper_lessstep.condition_temp,
                paper_lessstep.options_page
                )\
                .filter(and_(paper_lessstep.username==self.username,paper_lessstep.status=='ACTIVE',paper_lessstep.documentDetails==self.document_type)).all()
            if len(tempquery) != 0:
                for x in range(len(tempquery)):
                    tmp_status_group = False
                    if tempquery[x][5] != None:
                        tmp_optionpage = eval(tempquery[x][5])
                        if 'group_detail' in tmp_optionpage:
                            if 'group_status' in tmp_optionpage['group_detail']:
                                if tmp_optionpage['group_detail']['group_status'] == True:
                                    tmp_status_group = True
                                # print(tmp_optionpage)
                    if tmp_status_group == True:
                        tmp_template = {
                            'template_code':tempquery[x][0],
                            'template_name':tempquery[x][1],
                            'use_status':tempquery[x][2],
                            'document_type':tempquery[x][3],
                            'template_condition':tempquery[x][4]
                        }
                        arr_tmp.append(tmp_template)
            else:
                return {'result':'ER','messageER':'data not found'}
        return {'result':'OK','messageText':arr_tmp}

    def select_template_group_status(self,templatecode):
        self.templatecode = templatecode
        arr_tmp = []
        try:
            tempquery = db.session.query(
                paper_lessstep.step_Code,
                paper_lessstep.step_Name,
                paper_lessstep.status_use,
                paper_lessstep.documentDetails,
                paper_lessstep.condition_temp,
                paper_lessstep.options_page
                )\
                .filter(and_(paper_lessstep.step_Code==self.templatecode,paper_lessstep.status=='ACTIVE')).first()
            if tempquery != None:
                db.session.close()
                tmp_status_group = False
                tmpgroup_detail = tempquery[5]
                if tmpgroup_detail != None:
                    tmpgroup_detail = eval(tmpgroup_detail)
                if 'group_detail' in tmpgroup_detail:
                    if 'group_status' in tmpgroup_detail['group_detail']:
                        if tmpgroup_detail['group_detail']['group_status'] == True:
                            tmp_status_group = True
                            tmp_step_num_group = len(tmpgroup_detail['group_detail']['step_num'])
                            return tmp_step_num_group                
                # print(tmp_step_num_group)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageER':str(e)})

    def select_list_template_group(self,username,tax_id,id_data):
        try:
            self.username = username
            self.tax_id = tax_id
            self.id = id_data
            query_result_select = None
            list_json = []
            tmp_query ={}

            

            if self.id != None: # มี ID
               
                try:
                    result_select = db.session.query(tb_group_template).filter(tb_group_template.id == self.id).all()
                except Exception as e:
                    
                    return {'result':'ER','messageText':None,'messageER':'invalid id','status_Code':200}

            elif self.tax_id != None and self.username != None and self.id == None: # มี TAX_ID มี username
                if self.username != '' and self.tax_id != '': # ใส่หมด
                    
                    result_select = db.session.query(tb_group_template).filter(tb_group_template.create_by == self.username).filter(tb_group_template.biz_info.contains(self.tax_id)).filter(tb_group_template.status == 'ACTIVE').order_by(desc(tb_group_template.create_date)).all()
                    if result_select == []:
                        return {'result':'ER','messageText':None,'messageER':'invalid username and tax_id','status_Code':200}

                elif self.username == '' and self.tax_id != '' : # ไม่ใส่ username ใส่ tax_id
                    
                    result_select = db.session.query(tb_group_template).filter(tb_group_template.biz_info.contains(self.tax_id)).filter(tb_group_template.status == 'ACTIVE').order_by(desc(tb_group_template.create_date)).all()

                elif self.username != '' and self.tax_id == '': # ใส่ username ไม่ใส่ tax_id
                    
                    result_select = db.session.query(tb_group_template).filter(tb_group_template.create_by == self.username).filter(tb_group_template.status == 'ACTIVE').order_by(desc(tb_group_template.create_date)).all()
                    
                elif self.username == '' and self.tax_id == '': # ไม่ใส่อะไรเลย
                   
                    result_select = db.session.query(tb_group_template).filter(tb_group_template.status == 'ACTIVE').order_by(desc(tb_group_template.create_date)).all()

            elif self.tax_id == None and self.username != None and self.id == None: # ไม่มี TAX_ID
                if self.username != '': # ใส่ username ไม่ใส่ tax_id2
                    
                    result_select = db.session.query(tb_group_template).filter(tb_group_template.create_by == self.username).filter(tb_group_template.status == 'ACTIVE').order_by(desc(tb_group_template.create_date)).all()
                    if result_select == []:
                        return {'result':'ER','messageText':None,'messageER':'invalid username','status_Code':200}

                elif self.username == '' : # ไม่ใส่อะไรเลย2
                    
                    result_select = db.session.query(tb_group_template).filter(tb_group_template.status == 'ACTIVE').order_by(desc(tb_group_template.create_date)).all()

            elif self.username == None and self.tax_id != None and self.id == None: # ไม่มี username
                if self.tax_id != '' : #ไม่มี username ใส่ tax_id
                   
                    result_select = db.session.query(tb_group_template).filter(tb_group_template.biz_info.contains(self.tax_id)).filter(tb_group_template.status == 'ACTIVE').order_by(desc(tb_group_template.create_date)).all()
                    if result_select == []:
                        return {'result':'ER','messageText':None,'messageER':'invalid tax_id','status_Code':200}

                elif self.tax_id == '' : # ไม่ใส่อะไรเลย3
                    result_select = db.session.query(tb_group_template).filter(tb_group_template.status == 'ACTIVE').order_by(desc(tb_group_template.create_date)).all()
            elif self.tax_id == None and self.username == None and self.id == None: # ไม่มีอะไรเลยยยย
                result_select = db.session.query(tb_group_template).filter(tb_group_template.status == 'ACTIVE').order_by(desc(tb_group_template.create_date)).all()
            for i in range(len(result_select)):
                tmp_query = result_select[i].__dict__
                
                if '_sa_instance_state' in tmp_query:
                    del tmp_query['_sa_instance_state']

                if 'biz_info' in tmp_query :
                    if tmp_query['biz_info'] != '':
                        eval_biz = eval(str(tmp_query['biz_info']))
                        if type(eval_biz) == dict:
                            for x in range(len(tmp_query['biz_info'])):
                                tmp_biz = {}
                                tmp_biz['id_card_num'] = eval_biz['id_card_num']
                                tmp_biz['first_name_th'] = eval_biz['first_name_th']
                                tmp_biz['first_name_eng'] = eval_biz['first_name_eng']
                                tmp_biz['role_name'] = eval_biz['role_name']
                                tmp_biz['dept_id'] = eval_biz['dept_id']
                            tmp_query['biz_info'] = tmp_biz

                        elif type(eval_biz) == list:
                            for x in range(len(tmp_query['biz_info'])):
                                tmp_biz = {}
                                tmp_biz['id_card_num'] = eval_biz[0]['id_card_num']
                                tmp_biz['first_name_th'] = eval_biz[0]['first_name_th']
                                tmp_biz['first_name_eng'] = eval_biz[0]['first_name_eng']
                                tmp_biz['role_name'] = eval_biz[0]['role_name']
                                tmp_biz['dept_id'] = eval_biz[0]['dept_id']
                            tmp_query['biz_info'] = tmp_biz
                if 'group_data' in tmp_query:
                    if tmp_query['group_data'] != '':
                        tmp_query['group_data'] = eval(str(tmp_query['group_data']))

                if 'group_title' in tmp_query:
                    if tmp_query['group_title'] != '':
                        tmp_query['group_title'] = eval(str(tmp_query['group_title']))
                if 'step_group' in tmp_query:
                    if tmp_query['step_group'] != '':
                        tmp_query['step_group'] = eval(str(tmp_query['step_group']))
                if 'create_date' in tmp_query and 'update_date' in tmp_query:
                    tmp_query['create_date'] = str(tmp_query['create_date'])
                    tmp_query['update_date'] = str(tmp_query['update_date'])
                list_json.append(tmp_query)
           
            count = i+1
            return {'result':'OK','messageText':list_json,'count':count,'status_Code':200,'messageER':None}
        
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def select_list_template_group_v2(self,username,tax_id,id_data,document_type):
        try:
            self.username = username
            self.tax_id = tax_id
            self.id = id_data
            self.document_type = document_type
            query_result_select = None
            list_json = []
            tmp_query ={}
            if self.id != None: # มี ID
               
                try:
                    result_select = db.session.query(tb_group_template).filter(tb_group_template.id == self.id).all()
                except Exception as e:
                    
                    return {'result':'ER','messageText':None,'messageER':'invalid id','status_Code':200}

            elif self.tax_id != None and self.username != None and self.id == None and self.document_type != None: # มี TAX_ID มี username มี document_type 
                if self.username != '' and self.tax_id != '': # ใส่หมด
                    
                    result_select = db.session.query(tb_group_template).filter(tb_group_template.create_by == self.username).filter(tb_group_template.biz_info.contains(self.tax_id)).filter(tb_group_template.document_type == self.document_type).filter(tb_group_template.status == 'ACTIVE').order_by(desc(tb_group_template.create_date)).all()
                    if result_select == []:
                        return {'result':'ER','messageText':None,'messageER':'invalid variable','status_Code':200}

            elif self.tax_id != None and self.username != None and self.id == None and self.document_type == None: # มี TAX_ID มี username ไม่มี document_type 
                if self.username != '' and self.tax_id != '': # ใส่ TAX_ID ใส่ username
                    
                    result_select = db.session.query(tb_group_template).filter(tb_group_template.create_by == self.username).filter(tb_group_template.biz_info.contains(self.tax_id)).filter(tb_group_template.status == 'ACTIVE').order_by(desc(tb_group_template.create_date)).all()
                    if result_select == []:
                        return {'result':'ER','messageText':None,'messageER':'invalid variable','status_Code':200}

            elif self.tax_id != None and self.username == None and self.id == None and self.document_type == None: # มี TAX_ID ไม่มี username ไม่มี document_type 
                if self.username != '' and self.tax_id != '': # มี TAX_ID ไม่มี username ไม่มี document_type
                    
                    result_select = db.session.query(tb_group_template).filter(tb_group_template.biz_info.contains(self.tax_id)).filter(tb_group_template.status == 'ACTIVE').order_by(desc(tb_group_template.create_date)).all()
                    if result_select == []:
                        return {'result':'ER','messageText':None,'messageER':'invalid variable','status_Code':200}
            
            elif self.tax_id == None and self.username != None and self.id == None and self.document_type != None: # ไม่มี TAX_ID มี username มี document_type
                if self.username != '': # ใส่ username ไม่ใส่ tax_id2
                    
                    result_select = db.session.query(tb_group_template).filter(tb_group_template.create_by == self.username).filter(tb_group_template.document_type == self.document_type).filter(tb_group_template.status == 'ACTIVE').order_by(desc(tb_group_template.create_date)).all()
                    if result_select == []:
                        return {'result':'ER','messageText':None,'messageER':'invalid variable','status_Code':200}


            elif self.tax_id == None and self.username != None and self.id == None and self.document_type == None: # ไม่มี TAX_ID มี username ไม่มี document_type
                if self.username != '': # ใส่ username ไม่ใส่ tax_id2 ไม่ใส่ document_type
                    
                    result_select = db.session.query(tb_group_template).filter(tb_group_template.create_by == self.username).filter(tb_group_template.status == 'ACTIVE').order_by(desc(tb_group_template.create_date)).all()
                    if result_select == []:
                        return {'result':'ER','messageText':None,'messageER':'invalid variable','status_Code':200}


            elif self.username == None and self.tax_id != None and self.id == None and self.document_type != None: # ไม่มี username มี TAX_ID มี document_type
                if self.tax_id != '' and self.document_type != '': #ไม่มี username ใส่ tax_id ใส่ document_type
                   
                    result_select = db.session.query(tb_group_template).filter(tb_group_template.biz_info.contains(self.tax_id)).filter(tb_group_template.document_type == self.document_type).filter(tb_group_template.status == 'ACTIVE').order_by(desc(tb_group_template.create_date)).all()
                    if result_select == []:
                        return {'result':'ER','messageText':None,'messageER':'invalid variable','status_Code':200}


            elif self.username == None and self.tax_id == None and self.id == None and self.document_type != None: # ไม่มี username ไม่มี tax_id มี document_type
                if self.document_type != '' : #ไม่มี username ไม่มี tax_id ใส่ document_type
                   
                    result_select = db.session.query(tb_group_template).filter(tb_group_template.document_type == self.document_type).filter(tb_group_template.status == 'ACTIVE').order_by(desc(tb_group_template.create_date)).all()
                    if result_select == []:
                        return {'result':'ER','messageText':None,'messageER':'invalid variable','status_Code':200}

            elif self.tax_id == None and self.username == None and self.id == None: # ไม่มีอะไรเลยยยย
               
                result_select = db.session.query(tb_group_template).filter(tb_group_template.status == 'ACTIVE').order_by(desc(tb_group_template.create_date)).all()


            for i in range(len(result_select)):
                tmp_query = result_select[i].__dict__
                
                if '_sa_instance_state' in tmp_query:
                    del tmp_query['_sa_instance_state']

                if 'biz_info' in tmp_query :
                    if tmp_query['biz_info'] != '':
                        # tmp_query['biz_info'] = eval(str(tmp_query['biz_info']))
                        eval_biz = eval(str(tmp_query['biz_info']))
                        if type(eval_biz) == dict:
                            for x in range(len(tmp_query['biz_info'])):
                                tmp_biz = {}
                                tmp_biz['id_card_num'] = eval_biz['id_card_num']
                                tmp_biz['first_name_th'] = eval_biz['first_name_th']
                                tmp_biz['first_name_eng'] = eval_biz['first_name_eng']
                                tmp_biz['role_name'] = eval_biz['role_name']
                                tmp_biz['dept_id'] = eval_biz['dept_id']
                            tmp_query['biz_info'] = tmp_biz

                        elif type(eval_biz) == list:
                            for x in range(len(tmp_query['biz_info'])):
                                tmp_biz = {}
                                tmp_biz['id_card_num'] = eval_biz[0]['id_card_num']
                                tmp_biz['first_name_th'] = eval_biz[0]['first_name_th']
                                tmp_biz['first_name_eng'] = eval_biz[0]['first_name_eng']
                                tmp_biz['role_name'] = eval_biz[0]['role_name']
                                tmp_biz['dept_id'] = eval_biz[0]['dept_id']
                            tmp_query['biz_info'] = tmp_biz

                if 'group_data' in tmp_query:
                    if tmp_query['group_data'] != '':
                        tmp_query['group_data'] = eval(str(tmp_query['group_data']))

                if 'group_title' in tmp_query:
                    if tmp_query['group_title'] != '':
                        tmp_query['group_title'] = eval(str(tmp_query['group_title']))

                if 'step_group' in tmp_query:
                    if tmp_query['step_group'] != '':
                        tmp_query['step_group'] = eval(str(tmp_query['step_group']))



                if 'create_date' in tmp_query and 'update_date' in tmp_query:
                    tmp_query['create_date'] = str(tmp_query['create_date'])
                    tmp_query['update_date'] = str(tmp_query['update_date'])

                    
                list_json.append(tmp_query)
           
            count = i+1
           
            
            return {'result':'OK','messageText':list_json,'count':count,'status_Code':200,'messageER':None}
        
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200})


    def select_list_template_group_v3(self,username,tax_id,id_data,document_type):
        try:
            self.username = username
            self.tax_id = tax_id
            self.id = id_data
            self.document_type = document_type
            query_result_select = None
            list_json = []
            tmp_query ={}
            tax_idtmp = None
            if self.tax_id != None:
                tax_idtmp = '%' + self.tax_id +'%'
            status = 'ACTIVE'
            sql = ''' 
                SELECT
                    tb_group_template.group_name AS "group_name",
                    tb_group_template.group_code AS "group_code",
                    tb_group_template."template" AS "template",
                    tb_group_template.document_type AS "document_type",
                    tb_group_template.group_title AS "group_title",
                    tb_group_template.step_group AS "step_group",
                    tb_group_template.status AS "status",
                    tb_group_template.create_date AS "create_date",
                    tb_group_template.update_date AS "update_date",
                    tb_group_template.group_data AS "group_data",
                    tb_group_template.biz_info AS "biz_info",
                    tb_group_template.create_by AS "create_by",
                    tb_group_template.update_by AS "update_by",
                    tb_group_template.use_status AS "use_status",
                    tb_group_template.cover_page AS "cover_page",
                    tb_group_template.tid AS "id",
                    tb_group_template.group_color AS "group_color",
                    tb_group_template.timegroup_auto AS "timegroup",
                    tb_group_template.daygroup_auto AS "daygroup",
                    tb_document_detail."documentJson" AS "document_type_detail"
                FROM
                    tb_group_template 
                INNER JOIN tb_document_detail ON tb_document_detail."documentType" = tb_group_template.document_type
            '''
            where = ''' 
                WHERE
                    tb_group_template.status = :tmpstatus 
                    AND tb_document_detail."documentStatus" = :tmpstatus                    
                '''
            orderbytmp = ''' ORDER BY tb_group_template.create_date DESC  '''
            if self.id != None:
                where += ''' AND tb_group_template.tid=:tmptid '''
            elif self.tax_id != None and self.username == None and self.id == None and self.document_type == None:
                where += ''' AND tb_group_template.biz_info LIKE :tax_idtmp AND tb_document_detail.biz_info LIKE :tax_idtmp'''
            elif self.tax_id == None and self.username != None and self.id == None and self.document_type == None:
                where += ''' AND tb_group_template.create_by=:tmpusername AND tb_group_template.biz_info=:tmpbiz_info '''
            elif self.username == None and self.tax_id == None and self.id == None and self.document_type != None:
                where += ''' AND tb_group_template.document_type=:tmpdoctype  '''
            sql += where + orderbytmp
            with slave.connect() as connection:
                result = connection.execute(text(sql),tax_idtmp=tax_idtmp,tmpstatus=status,tmptid=self.id,tmpusername=self.username,tmpbiz_info='',tmpdoctype=self.document_type)
            connection.close()
            query_result = [dict(row) for row in result]
            for n in range(len(query_result)):
                tmp_query = query_result[n]
                if 'document_type_detail' in tmp_query:
                    if tmp_query['document_type_detail'] != '':
                        tmp_query['document_type_detail'] = eval(str(tmp_query['document_type_detail']))
                if 'biz_info' in tmp_query :
                    if tmp_query['biz_info'] != '':
                        # tmp_query['biz_info'] = eval(str(tmp_query['biz_info']))
                        eval_biz = eval(str(tmp_query['biz_info']))
                        if type(eval_biz) == dict:
                            for x in range(len(tmp_query['biz_info'])):
                                tmp_biz = {}
                                tmp_biz['id_card_num'] = eval_biz['id_card_num']
                                tmp_biz['first_name_th'] = eval_biz['first_name_th']
                                tmp_biz['first_name_eng'] = eval_biz['first_name_eng']
                                tmp_biz['role_name'] = eval_biz['role_name']
                                tmp_biz['dept_id'] = eval_biz['dept_id']
                            tmp_query['biz_info'] = tmp_biz
                        elif type(eval_biz) == list:
                            for x in range(len(tmp_query['biz_info'])):
                                tmp_biz = {}
                                tmp_biz['id_card_num'] = eval_biz[0]['id_card_num']
                                tmp_biz['first_name_th'] = eval_biz[0]['first_name_th']
                                tmp_biz['first_name_eng'] = eval_biz[0]['first_name_eng']
                                tmp_biz['role_name'] = eval_biz[0]['role_name']
                                tmp_biz['dept_id'] = eval_biz[0]['dept_id']
                            tmp_query['biz_info'] = tmp_biz
                    else:
                        tmp_query['biz_info'] =None
                if 'email_middle' in tmp_query:
                    if tmp_query['email_middle'] != '':
                        tmp_query['email_middle'] = eval(str(tmp_query['email_middle']))
                if 'timegroup_auto' in tmp_query:
                    if tmp_query['timegroup_auto'] != '':
                        tmp_query['timegroup'] = eval(str(tmp_query['timegroup_auto']))
                if 'daygroup_auto' in tmp_query:
                    if tmp_query['daygroup_auto'] != '':
                        tmp_query['daygroup'] = eval(str(tmp_query['daygroup_auto']))
                if 'group_data' in tmp_query:
                    if tmp_query['group_data'] != '':
                        tmp_query['group_data'] = eval(str(tmp_query['group_data']))
                if 'group_title' in tmp_query:
                    if tmp_query['group_title'] != '':
                        tmp_query['group_title'] = eval(str(tmp_query['group_title']))
                if 'step_group' in tmp_query:
                    if tmp_query['step_group'] != '':
                        try:
                            tmp_query['step_group'] = eval((tmp_query['step_group']))
                        except Exception as e:
                            tmp_query['step_group'] = None
                if 'template' in tmp_query:
                    if tmp_query['template'] != '':
                        tmp_query['template'] = eval(tmp_query['template'])
                if 'create_date' in tmp_query and 'update_date' in tmp_query:
                    tmp_query['create_date'] = str(tmp_query['create_date'])
                    tmp_query['update_date'] = str(tmp_query['update_date'])
                if 'cover_page' in tmp_query:
                    if tmp_query['cover_page'] != '':
                        tmp_query['cover_page'] = eval(str(tmp_query['cover_page']))
                if 'group_color' in tmp_query:
                    if tmp_query['group_color'] != None:
                        tmp_query['group_color'] = eval(tmp_query['group_color'])
                        if 'color' in tmp_query['group_color'][0]:
                            tmp_query['group_color'] = tmp_query['group_color'][0]['color']
                list_json.append(tmp_query)
            return {'result':'OK','messageText':list_json,'status_Code':200,'messageER':None}  
            if self.id != None: # มี ID
                try:
                    result_select = db.session.query(tb_group_template).filter(and_(tb_group_template.tid == self.id,tb_group_template.status == 'ACTIVE')).all()
                except Exception as e:
                    return {'result':'ER','messageText':None,'messageER':'data not found','status_Code':200}
            elif self.tax_id != None and self.username == None and self.id == None and self.document_type == None: # มี TAX_ID ไม่มี username ไม่มี document_type 
                result_select = db.session.query(tb_group_template).filter(and_(tb_group_template.biz_info.contains(self.tax_id),tb_group_template.status == 'ACTIVE')).order_by(desc(tb_group_template.create_date))
                # return ''
                if result_select == []:
                    return {'result':'ER','messageText':None,'messageER':'data not found','status_Code':200}
            
            elif self.tax_id == None and self.username != None and self.id == None and self.document_type == None: # มี username ไม่มี document_type ไม่มี TAX_ID 
                result_select = db.session.query(tb_group_template).filter(and_(tb_group_template.create_by == self.username,tb_group_template.status == 'ACTIVE',tb_group_template.biz_info == '')).order_by(desc(tb_group_template.create_date)).all()
                print ('result_select: ',result_select)
                if result_select == []:
                    return {'result':'ER','messageText':None,'messageER':'data not found','status_Code':200}
            elif self.username == None and self.tax_id == None and self.id == None and self.document_type != None: # มี document_type ไม่มี username ไม่มี tax_id 
                result_select = db.session.query(tb_group_template).filter(and_(tb_group_template.document_type == self.document_type,tb_group_template.status == 'ACTIVE')).order_by(desc(tb_group_template.create_date)).all()
                if result_select == []:
                    return {'result':'ER','messageText':None,'messageER':'data not found','status_Code':200}
            elif self.tax_id == None and self.username == None and self.id == None: # ไม่มีอะไรเลยยยย
                    return {'result':'ER','messageText':None,'messageER':'Not have data','status_Code':404}
            print(result_select)
            for i in range(len(result_select)):
                tmp_query = result_select[i].__dict__
                if '_sa_instance_state' in tmp_query:
                    del tmp_query['_sa_instance_state']
                if tmp_query['tid'] != None:
                    tmp_query['id'] = tmp_query['tid']
                if 'tid' in tmp_query:
                    del tmp_query['tid']
                if 'biz_info' in tmp_query :
                    if tmp_query['biz_info'] != '':
                        # tmp_query['biz_info'] = eval(str(tmp_query['biz_info']))
                        eval_biz = eval(str(tmp_query['biz_info']))
                        if type(eval_biz) == dict:
                            for x in range(len(tmp_query['biz_info'])):
                                tmp_biz = {}
                                tmp_biz['id_card_num'] = eval_biz['id_card_num']
                                tmp_biz['first_name_th'] = eval_biz['first_name_th']
                                tmp_biz['first_name_eng'] = eval_biz['first_name_eng']
                                tmp_biz['role_name'] = eval_biz['role_name']
                                tmp_biz['dept_id'] = eval_biz['dept_id']
                            tmp_query['biz_info'] = tmp_biz
                        elif type(eval_biz) == list:
                            for x in range(len(tmp_query['biz_info'])):
                                tmp_biz = {}
                                tmp_biz['id_card_num'] = eval_biz[0]['id_card_num']
                                tmp_biz['first_name_th'] = eval_biz[0]['first_name_th']
                                tmp_biz['first_name_eng'] = eval_biz[0]['first_name_eng']
                                tmp_biz['role_name'] = eval_biz[0]['role_name']
                                tmp_biz['dept_id'] = eval_biz[0]['dept_id']
                            tmp_query['biz_info'] = tmp_biz
                    else:
                        tmp_query['biz_info'] =None
                if tmp_query['biz_info'] != None:
                    query_document = db.session.query(paper_lessdocument_detail)\
                        .filter(and_(paper_lessdocument_detail.documentType==tmp_query['document_type'],paper_lessdocument_detail.documentStatus=='ACTIVE',paper_lessdocument_detail.biz_info.contains(tmp_biz['id_card_num'])))\
                        .order_by(desc(paper_lessdocument_detail.documentUpdate)).first()
                else:
                    query_document = db.session.query(paper_lessdocument_detail)\
                        .filter(and_(paper_lessdocument_detail.email==self.username,paper_lessdocument_detail.documentType==tmp_query['document_type'],paper_lessdocument_detail.documentStatus=='ACTIVE'),or_(paper_lessdocument_detail.biz_info=='',paper_lessdocument_detail.biz_info==None))\
                        .order_by(desc(paper_lessdocument_detail.documentUpdate)).first()
                tmpdocumentdetail = None
                if query_document != None:
                    tmpdocumentdetail = query_document.documentJson
                    if tmpdocumentdetail != None:
                        tmpdocumentdetail = eval(tmpdocumentdetail)
                tmp_query['document_type_detail'] = tmpdocumentdetail
                if 'email_middle' in tmp_query:
                    if tmp_query['email_middle'] != '':
                        tmp_query['email_middle'] = eval(str(tmp_query['email_middle']))
                if 'timegroup_auto' in tmp_query:
                    if tmp_query['timegroup_auto'] != '':
                        tmp_query['timegroup'] = eval(str(tmp_query['timegroup_auto']))
                if 'daygroup_auto' in tmp_query:
                    if tmp_query['daygroup_auto'] != '':
                        tmp_query['daygroup'] = eval(str(tmp_query['daygroup_auto']))
                if 'group_data' in tmp_query:
                    if tmp_query['group_data'] != '':
                        tmp_query['group_data'] = eval(str(tmp_query['group_data']))
                if 'group_title' in tmp_query:
                    if tmp_query['group_title'] != '':
                        tmp_query['group_title'] = eval(str(tmp_query['group_title']))
                if 'step_group' in tmp_query:
                    if tmp_query['step_group'] != '':
                        try:
                            tmp_query['step_group'] = eval((tmp_query['step_group']))
                        except Exception as e:
                            tmp_query['step_group'] = None
                if 'template' in tmp_query:
                    if tmp_query['template'] != '':
                        tmp_query['template'] = eval(tmp_query['template'])
                if 'create_date' in tmp_query and 'update_date' in tmp_query:
                    tmp_query['create_date'] = str(tmp_query['create_date'])
                    tmp_query['update_date'] = str(tmp_query['update_date'])
                if 'cover_page' in tmp_query:
                    if tmp_query['cover_page'] != '':
                        tmp_query['cover_page'] = eval(str(tmp_query['cover_page']))
                if 'group_color' in tmp_query:
                    if tmp_query['group_color'] != None:
                        tmp_query['group_color'] = eval(tmp_query['group_color'])
                        if 'color' in tmp_query['group_color'][0]:
                            tmp_query['group_color'] = tmp_query['group_color'][0]['color']
                list_json.append(tmp_query)
            
            return {'result':'OK','messageText':list_json,'status_Code':200,'messageER':None}    
            
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200
        finally:
            connection.close()
            # db.session.close()


    def count_file_storage_v2(self):
        dict_count = {}
        try:
            with slave.connect() as connection:
                result_string_pdf = connection.execute('''SELECT COUNT(string_pdf) FROM "tb_pdf_storage" WHERE "string_pdf" IS NOT NULL''')
                connection.close()
            count_string_pdf = [dict(row) for row in result_string_pdf][0]['count']
            with slave.connect() as connection:
                result_string_sign = connection.execute('''SELECT COUNT(string_sign) FROM "tb_pdf_storage" WHERE "string_sign" IS NOT NULL''')
                connection.close()
            count_string_sign = [dict(row) for row in result_string_sign][0]['count']
            with slave.connect() as connection:
                result_path_pdf = connection.execute('''SELECT COUNT(path_pdf) FROM "tb_pdf_storage" WHERE "path_pdf" IS NOT NULL''')
                connection.close()
            count_path_pdf = [dict(row) for row in result_path_pdf][0]['count']
            with slave.connect() as connection:
                result_path_sign = connection.execute('''SELECT COUNT(path_sign) FROM "tb_pdf_storage" WHERE "path_sign" IS NOT NULL''')
                connection.close()
            count_path_sign = [dict(row) for row in result_path_sign][0]['count']
            with slave.connect() as connection:
                result_all = connection.execute('''SELECT COUNT(fid) FROM "tb_pdf_storage" WHERE "fid" IS NOT NULL''')
                connection.close()
            count_all = [dict(row) for row in result_all][0]['count']
            with slave.connect() as connection:
                result_max_fid = connection.execute('''SELECT MAX(fid) FROM "tb_pdf_storage" WHERE "fid" IS NOT NULL''')
                connection.close()
            count_max_fid = [dict(row) for row in result_max_fid][0]['max']
            with slave.connect() as connection:
                result_min_fid = connection.execute('''SELECT MIN(fid) FROM "tb_pdf_storage" WHERE "fid" IS NOT NULL''')
                connection.close()
            count_min_fid = [dict(row) for row in result_min_fid][0]['min']
            print (count_min_fid)
            dict_count = {
                'string_pdf':count_string_pdf,
                'string_sign':count_string_sign,
                'path_pdf':count_path_pdf,
                'path_sign':count_path_sign,
                'all':count_all,
                'range_index_fid':{'MAX':count_max_fid,'MIN':count_min_fid}
                }
            return {'result':'OK','messageText':dict_count,'status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return ({'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}),200

    def path_to_base64(self,fid):
        dict_path64 = {}
        # path_me = 'C:/Storage/iNet/paperless/paperless-back_last_v2/paperless-back_last/storage'
        file_string_pdf_sign = None
        file_string_pdf = None
        try:
            self.fid = fid
            with slave.connect() as connection:
                result_path_pdf = connection.execute(text('''SELECT (path_pdf) FROM "tb_pdf_storage" WHERE "fid"=:fid'''),fid=self.fid)
                connection.close()
            path_pdf = [dict(row) for row in result_path_pdf][0]['path_pdf']
            if path_pdf != None:
                with open(path_pdf, "rb") as files:
                    file_string_pdf = str(files.read()).split('\'')[1]
            with slave.connect() as connection:
                result_path_sign = connection.execute(text('''SELECT (path_sign) FROM "tb_pdf_storage" WHERE "fid"=:fid'''),fid=self.fid)
                connection.close()
            path_sign = [dict(row) for row in result_path_sign][0]['path_sign']
            if path_sign != None:
                with open(path_sign, "rb") as files2:
                    file_string_pdf_sign = str(files2.read()).split('\'')[1]
            with slave.connect() as connection:
                result_string_pdf = connection.execute(text('''SELECT (string_pdf) FROM "tb_pdf_storage" WHERE "fid"=:fid'''),fid=self.fid)
                connection.close()
            string_pdf = [dict(row) for row in result_string_pdf][0]['string_pdf']
            with slave.connect() as connection:
                result_string_sign = connection.execute(text('''SELECT (string_sign) FROM "tb_pdf_storage" WHERE "fid"=:fid'''),fid=self.fid)
                connection.close()
            string_sign = [dict(row) for row in result_string_sign][0]['string_sign']
            dict_path64 = {
                'path_pdf_base64' : file_string_pdf,
                'path_sign_base64' : file_string_pdf_sign,
                'string_pdf' : str(string_pdf),
                'string_sign' : str(string_sign)
            }
            return {'result':'OK','messageText':dict_path64,'status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}

    def path_to_base64_v2(self,fid):
        dict_path64 = {}
        # path_me = 'C:/Storage/iNet/paperless/paperless-back_last_v3/paperless-back_last-master/storage/'
        file_string_pdf_sign = None
        file_string_pdf = None
        try:
            self.fid = fid
            with slave.connect() as connection:
                result_path_pdf = connection.execute(text('''SELECT "path_pdf","path_sign","string_pdf","string_sign" FROM "tb_pdf_storage" WHERE "fid"=:fid AND "path_pdf" IS NOT NULL'''),fid=self.fid)
                connection.close()
            path_pdf_all = [dict(row) for row in result_path_pdf][0]
            path_pdf = path_pdf_all['path_pdf']
            path_sign = path_pdf_all['path_sign']
            string_pdf = path_pdf_all['string_pdf']
            string_sign = path_pdf_all['string_sign']
            with open(path_pdf, "rb") as files:
                file_string_pdf = str(files.read()).split('\'')[1]
            with open(path_sign, "rb") as files2:
                file_string_pdf_sign = str(files2.read()).split('\'')[1]
            dict_path64 = {
                'path_pdf_base64' : file_string_pdf,
                'path_sign_base64' : file_string_pdf_sign,
                'string_pdf' : str(string_pdf),
                'string_sign' : str(string_sign)
            }
            return {'result':'OK','messageText':dict_path64,'status_Code':200,'messageER':None}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {'result':'ER','messageText':None,'messageER':str(e),'status_Code':200}
    
    