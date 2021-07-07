#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from method.verify import *
from method.publicqrcode import *
from controller.mail_string import *
from controller.validate import *
from method.callserver import *
from db.db_method import *
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *
from db.db_method_4 import *
from db.db_method_5 import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *


if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less

# new version
# excel สามารถเลือก report เป็น วัน เดือน ปี ชั่วโมง เช็คจากการ upload และ เซ็นเอกสาร
@status_methods.route('/api/v1/dashboard_admin/viewpaper/back/count/report',methods=['POST'])
def dashboard_admin_select_paper_back(): 
    if  request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None        
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)

        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        print('uername',username)
        print('email',email)
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        if 'tax_id' in dataJson and 'document_type' in dataJson and 'type' in dataJson and len(dataJson) == 3 :
            tax_id = dataJson['tax_id']
            document_type = str(dataJson['document_type']).upper()
            type_show = dataJson['type']
            print('result_level_eval',result_level_eval)
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                print(level_admin)
                if level_admin == None :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found','data':[]}}),200

                elif int(level_admin) == 0 :
                    list_result, tmp_2 = [], {}
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        if type_show == 'month':  
                            type_variable = type_show 
                            type_thai = 'รายเดือน'                         
                            data = executor.submit(select_1().select_admin_count_viewdoc_month_v2, tax_id,document_type,level_admin)
                        elif type_show == 'week':
                            type_variable = type_show  
                            type_thai = 'รายสัปดาห์'
                            data = executor.submit(select_1().select_admin_count_viewdoc_week_v2, tax_id,document_type,level_admin)
                        elif type_show == 'day':
                            type_variable = type_show 
                            type_thai = 'รายวัน' 
                            data = executor.submit(select_1().select_admin_count_viewdoc_day_v2, tax_id,document_type,level_admin)
                        elif type_show == 'hour':
                            type_variable = type_show  
                            type_thai = 'รายชั่วโมง'
                            data = executor.submit(select_1().select_admin_count_viewdoc_hour_v2, tax_id,document_type,level_admin)
                        return_data = data.result()                        
                    tmp_2[type_variable] = return_data['messageText']      
                    list_result.append(tmp_2)
                
                elif int(level_admin) == 1 :
                    tmp_json, list_result, tmp_2 = {}, [], {}
                    if tax_id == None or tax_id == "" :
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the biz_tax was not filled out.','data':[]}}),200
                    elif tax_id not in list_id_card_num:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the user is not in the business.','data':[]}}),200
                    else :
                        if len(tax_id) != 13:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because tax_id incorret','data':[]}}),200
                        elif len(tax_id) == 13:
                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                if type_show == 'month':  
                                    type_variable = type_show 
                                    type_thai = 'รายเดือน'                         
                                    data = executor.submit(select_1().select_admin_count_viewdoc_month_v2, tax_id,document_type,level_admin)
                                elif type_show == 'week':
                                    type_variable = type_show  
                                    type_thai = 'รายสัปดาห์'
                                    data = executor.submit(select_1().select_admin_count_viewdoc_week_v2, tax_id,document_type,level_admin)
                                elif type_show == 'day':
                                    type_variable = type_show 
                                    type_thai = 'รายวัน' 
                                    data = executor.submit(select_1().select_admin_count_viewdoc_day_v2, tax_id,document_type,level_admin)
                                elif type_show == 'hour':
                                    type_variable = type_show  
                                    type_thai = 'รายชั่วโมง'
                                    data = executor.submit(select_1().select_admin_count_viewdoc_hour_v2, tax_id,document_type,level_admin)
                                return_data = data.result()
                    tmp_2[type_variable] = return_data['messageText']      
                    list_result.append(tmp_2)
                    # print(list_result)
                print(return_data['result'])
                if return_data['result'] == 'OK':   
                    data_excel = list_result[0][type_variable]
                    data_excel1 = data_excel['documents_all_' + type_variable][0]
                    data_excel2 = data_excel['documents_past_' + type_variable]
                    ts = int(time.time())
                    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    st_filename = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S-')
                    path = path_global_1 + '/storage/excel_report/' + str(st) + '/'
                    path_indb = path_global_1 + '/storage/excel_report/' + str(st) + '/'
                    # path = './storage/excel_report/' + str(st) + '/'
                    # path_indb = '/storage/excel_report/' + str(st) + '/'
                    if not os.path.exists(path):
                        os.makedirs(path)
                    unique_filename = str(uuid.uuid4())
                    filename = 'report_paperless(' + type_variable + ')' + st_filename + unique_filename
                    row = 4
                    title = 'รายงานสรุปจำนวนเอกสารย้อนหลังจากการส่งเอกสารและการเซ็นเอกสาร (' + type_thai + ')'
                    workbook = xlsxwriter.Workbook(path + filename + '.xlsx')
                    worksheet = workbook.add_worksheet()
                    format1 = workbook.add_format()
                    format1.set_align('center')
                    format1.set_align('vcenter')
                    format1.set_text_wrap()
                    format2 = workbook.add_format({'bold': True})
                    format2.set_align('left')
                    format2.set_text_wrap()
                    cell_format = workbook.add_format({'bold': True})
                    cell_format.set_align('center')
                    cell_format.set_align('vcenter')
                    cell_format.set_text_wrap()
                    cell_format.font_size = 12
                    if document_type == "":
                        worksheet.write('C3', 'ทั้งหมด',format1)
                    else:
                        worksheet.write('C3', document_type,format1)
                    if tax_id == "":
                        worksheet.write('E3', 'ทั้งหมด',format1)
                    else:
                        worksheet.write('E3', tax_id,format1)
                    worksheet.write('B3', 'ประเภทเอกสาร',cell_format)                    
                    worksheet.write('D3', 'หมายเลขเอกสาร',cell_format)                  
                    worksheet.write('A4', 'ลำดับ',cell_format)
                    worksheet.write('B4', 'วันที่',cell_format)
                    worksheet.write('C4', 'จำนวนผู้ส่งเอกสาร',cell_format)
                    worksheet.write('D4', 'จำนวนเอกสารทั้งหมด',cell_format)
                    worksheet.write('E4', 'จำนวนเอกสารที่อยู่ในระบบ',cell_format)
                    worksheet.write('F4', 'จำนวนเอกสารที่ถูกยกเลิก',cell_format)
                    worksheet.write('G4', 'จำนวนเอกสารที่ถูกลบ',cell_format)
                    worksheet.merge_range('C2:G2', title,cell_format)
                    worksheet.merge_range('H4:I4', 'สรุปเอกสารทั้งหมด',cell_format)
                    worksheet.write('H5', 'จำนวนผู้ส่งเอกสารทั้งหมด',format2)
                    worksheet.write('H6', 'จำนวนเอกสารทั้งหมด',format2)
                    worksheet.write('H7', 'จำนวนเอกสารที่อยู่ในระบบ',format2)
                    worksheet.write('H8', 'จำนวนเอกสารที่ถูกยกเลิก',format2)
                    worksheet.write('H9', 'จำนวนเอกสารที่ถูกลบ',format2)
                    worksheet.write('I5', data_excel1['countUser_of_' + type_variable],format1)
                    worksheet.write('I6', data_excel1['documents_all'],format1)
                    worksheet.write('I7', data_excel1['documents_all_active'],format1)
                    worksheet.write('I8', data_excel1['documents_all_reject'],format1)
                    worksheet.write('I9', data_excel1['documents_all_delete'],format1)
                    worksheet.set_column(0,0,7)
                    worksheet.set_column(1,3,20)
                    worksheet.set_column(4,6,24)
                    worksheet.set_column(7,7,26)
                    for num in range (len(data_excel2)):
                        line = data_excel2[num]
                        dateStart = datetime.datetime.strptime(line['datetime_start'], '%Y-%m-%d %H:%M:%S')
                        dateEnd = datetime.datetime.strptime(line['datetime_end'], '%Y-%m-%d %H:%M:%S') 
                        if type_show == 'month':       
                            datetimes = dateStart.strftime('%Y-%m')
                        elif type_show == 'week':   
                            datetimes1 = dateEnd.strftime('%d')    
                            datetimes = dateStart.strftime('%Y-%m-(%d,' + datetimes1 + ')')                            
                        elif type_show == 'day':       
                            datetimes = dateStart.strftime('%Y-%m-%d')
                        elif type_show == 'hour':       
                            datetimes = dateStart.strftime('%Y-%m-%d %H:%M:%S')
                        worksheet.write(row, 0, (num+1), format1)
                        worksheet.write(row, 1, datetimes,format1)
                        worksheet.write(row, 2, line['count_user'],format1)
                        worksheet.write(row, 3, line['all_documents'],format1)
                        worksheet.write(row, 4, line['documents_active'],format1)
                        worksheet.write(row, 5, line['documents_reject'],format1)
                        worksheet.write(row, 6, line['documents_delete'],format1)
                        row += 1
                    workbook.close()
                    filename = filename + '.xlsx'
                    sha512encode_unifile = hashlib.sha512(str(unique_filename).encode('utf-8')).hexdigest()
                    web_download_file = myUrl_domain + 'api/v1/excel/download_file/' + sha512encode_unifile
                    return jsonify({'result':'OK','messageText':list_result,'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':list_result,'status_Code':200,'messageER':'error fetching data'}),200               
            else:
                return jsonify({'result':'OK','messageText':None,'status_Code':404,'messageER':'level admin incorret'}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorret'}),404

# excel สามารถเลือก report เป็น วัน เดือน ปี ชั่วโมง เช็คจากการ upload
@status_methods.route('/api/v1/dashboard_admin/viewpaper/back/count/report_upload',methods=['POST'])
def dashboard_adminSelect_sendtime(): 
    if  request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None        
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)

        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        print('uername',username)
        print('email',email)
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        if 'tax_id' in dataJson and 'document_type' in dataJson and 'type' in dataJson and len(dataJson) == 3 :
            tax_id = dataJson['tax_id']
            document_type = str(dataJson['document_type']).upper()
            type_show = dataJson['type']
            print('result_level_eval',result_level_eval)
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                print(level_admin)
                if level_admin == None :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found','data':[]}}),200

                elif int(level_admin) == 0 :
                    list_result, tmp_2 = [], {}
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        if type_show == 'month':  
                            type_variable = type_show 
                            type_thai = 'รายเดือน'                         
                            data = executor.submit(select().select_admin_count_viewdoc_month, tax_id,document_type,level_admin)
                        elif type_show == 'week':
                            type_variable = type_show  
                            type_thai = 'รายสัปดาห์'
                            data = executor.submit(select().select_admin_count_viewdoc_week_v2, tax_id,document_type,level_admin)
                        elif type_show == 'day':
                            type_variable = type_show 
                            type_thai = 'รายวัน' 
                            data = executor.submit(select().select_admin_count_viewdoc_day_v2, tax_id,document_type,level_admin)
                        elif type_show == 'hour':
                            type_variable = type_show  
                            type_thai = 'รายชั่วโมง'
                            data = executor.submit(select().select_admin_count_viewdoc_hour_v2, tax_id,document_type,level_admin)
                        return_data = data.result()                        
                    tmp_2[type_variable] = return_data['messageText']      
                    list_result.append(tmp_2)
                
                elif int(level_admin) == 1 :
                    tmp_json, list_result, tmp_2 = {}, [], {}
                    if tax_id == None or tax_id == "" :
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the biz_tax was not filled out.','data':[]}}),200
                    elif tax_id not in list_id_card_num:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the user is not in the business.','data':[]}}),200
                    else :
                        if len(tax_id) != 13:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because tax_id incorret','data':[]}}),200
                        elif len(tax_id) == 13:
                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                if type_show == 'month':  
                                    type_variable = type_show 
                                    type_thai = 'รายเดือน'                         
                                    data = executor.submit(select().select_admin_count_viewdoc_month_v2, tax_id,document_type,level_admin)
                                elif type_show == 'week':
                                    type_variable = type_show  
                                    type_thai = 'รายสัปดาห์'
                                    data = executor.submit(select().select_admin_count_viewdoc_week_v2, tax_id,document_type,level_admin)
                                elif type_show == 'day':
                                    type_variable = type_show 
                                    type_thai = 'รายวัน' 
                                    data = executor.submit(select().select_admin_count_viewdoc_day_v2, tax_id,document_type,level_admin)
                                elif type_show == 'hour':
                                    type_variable = type_show  
                                    type_thai = 'รายชั่วโมง'
                                    data = executor.submit(select().select_admin_count_viewdoc_hour_v2, tax_id,document_type,level_admin)
                                return_data = data.result()
                    tmp_2[type_variable] = return_data['messageText']      
                    list_result.append(tmp_2)
                    print(list_result)
                
                if return_data['result'] == 'OK':   
                    data_excel = list_result[0][type_variable]
                    data_excel1 = data_excel['documents_all_' + type_variable][0]
                    data_excel2 = data_excel['documents_past_' + type_variable]
                    ts = int(time.time())
                    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    st_filename = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S-')
                    path = './storage/excel_report/' + str(st) + '/'
                    path_indb = '/storage/excel_report/' + str(st) + '/'
                    if not os.path.exists(path):
                        os.makedirs(path)
                    unique_filename = str(uuid.uuid4())
                    filename = 'report_paperless(' + type_variable + ')' + st_filename + unique_filename
                    row = 4
                    title = 'รายงานสรุปจำนวนเอกสารย้อนหลังจากการอัพโหลด (' + type_thai + ')'
                    workbook = xlsxwriter.Workbook(path + filename + '.xlsx')
                    worksheet = workbook.add_worksheet()
                    format1 = workbook.add_format()
                    format1.set_align('center')
                    format1.set_align('vcenter')
                    format1.set_text_wrap()
                    format2 = workbook.add_format({'bold': True})
                    format2.set_align('left')
                    format2.set_text_wrap()
                    cell_format = workbook.add_format({'bold': True})
                    cell_format.set_align('center')
                    cell_format.set_align('vcenter')
                    cell_format.set_text_wrap()
                    cell_format.font_size = 12
                    if document_type == "":
                        worksheet.write('C3', 'ทั้งหมด',format1)
                    else:
                        worksheet.write('C3', document_type,format1)
                    if tax_id == "":
                        worksheet.write('E3', 'ทั้งหมด',format1)
                    else:
                        worksheet.write('E3', tax_id,format1)
                    worksheet.write('B3', 'ประเภทเอกสาร',cell_format)                    
                    worksheet.write('D3', 'หมายเลขเอกสาร',cell_format)                  
                    worksheet.write('A4', 'ลำดับ',cell_format)
                    worksheet.write('B4', 'วันที่',cell_format)
                    worksheet.write('C4', 'จำนวนผู้ส่งเอกสาร',cell_format)
                    worksheet.write('D4', 'จำนวนเอกสารทั้งหมด',cell_format)
                    worksheet.write('E4', 'จำนวนเอกสารที่อยู่ในระบบ',cell_format)
                    worksheet.write('F4', 'จำนวนเอกสารที่ถูกยกเลิก',cell_format)
                    worksheet.write('G4', 'จำนวนเอกสารที่ถูกลบ',cell_format)
                    worksheet.merge_range('C2:E2', title,cell_format)
                    worksheet.merge_range('H4:I4', 'สรุปเอกสารทั้งหมด',cell_format)
                    worksheet.write('H5', 'จำนวนผู้ส่งเอกสารทั้งหมด',format2)
                    worksheet.write('H6', 'จำนวนเอกสารทั้งหมด',format2)
                    worksheet.write('H7', 'จำนวนเอกสารที่อยู่ในระบบ',format2)
                    worksheet.write('H8', 'จำนวนเอกสารที่ถูกยกเลิก',format2)
                    worksheet.write('H9', 'จำนวนเอกสารที่ถูกลบ',format2)
                    worksheet.write('I5', data_excel1['countUser_of_' + type_variable],format1)
                    worksheet.write('I6', data_excel1['documents_all'],format1)
                    worksheet.write('I7', data_excel1['documents_all_active'],format1)
                    worksheet.write('I8', data_excel1['documents_all_reject'],format1)
                    worksheet.write('I9', data_excel1['documents_all_delete'],format1)
                    worksheet.set_column(0,0,7)
                    worksheet.set_column(1,3,20)
                    worksheet.set_column(4,5,24)
                    worksheet.set_column(7,7,26)
                    for num in range (len(data_excel2)):
                        line = data_excel2[num]
                        dateStart = datetime.datetime.strptime(line['datetime_start'], '%Y-%m-%d %H:%M:%S')
                        dateEnd = datetime.datetime.strptime(line['datetime_end'], '%Y-%m-%d %H:%M:%S') 
                        if type_show == 'month':       
                            datetimes = dateStart.strftime('%Y-%m')
                        elif type_show == 'week':   
                            datetimes1 = dateEnd.strftime('%d')    
                            datetimes = dateStart.strftime('%Y-%m-(%d,' + datetimes1 + ')')                            
                        elif type_show == 'day':       
                            datetimes = dateStart.strftime('%Y-%m-%d')
                        elif type_show == 'hour':       
                            datetimes = dateStart.strftime('%Y-%m-%d %H:%M:%S')
                        worksheet.write(row, 0, (num+1), format1)
                        worksheet.write(row, 1, datetimes,format1)
                        worksheet.write(row, 2, line['count_user'],format1)
                        worksheet.write(row, 3, line['all_documents'],format1)
                        worksheet.write(row, 4, line['documents_active'],format1)
                        worksheet.write(row, 5, line['documents_reject'],format1)
                        worksheet.write(row, 6, line['documents_delete'],format1)
                        row += 1
                    workbook.close()
                    filename = filename + '.xlsx'
                    sha512encode_unifile = hashlib.sha512(str(unique_filename).encode('utf-8')).hexdigest()
                    web_download_file = myUrl_domain + 'api/v1/excel/download_file/' + sha512encode_unifile
                    return jsonify({'result':'OK','messageText':list_result,'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':list_result,'status_Code':200,'messageER':'error fetching data'}),200               
            else:
                return jsonify({'result':'OK','messageText':None,'status_Code':404,'messageER':'level admin incorret'}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorret'}),404

# excel สามารถเลือก report เป็น วัน เดือน ปี ชั่วโมง เช็คจากการ sign
@status_methods.route('/api/v1/dashboard_admin/viewpaper/back/count/report_sign',methods=['POST'])
def dashboard_admin_select_paper_back_sign(): 
    if  request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None        
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)

        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        print('uername',username)
        print('email',email)
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        if 'tax_id' in dataJson and 'document_type' in dataJson and 'type' in dataJson and len(dataJson) == 3 :
            tax_id = dataJson['tax_id']
            document_type = str(dataJson['document_type']).upper()
            type_show = dataJson['type']
            print('result_level_eval',result_level_eval)
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                print(level_admin)
                if level_admin == None :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found','data':[]}}),200

                elif int(level_admin) == 0 :
                    list_result, tmp_2 = [], {}
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        if type_show == 'month':  
                            type_variable = type_show 
                            type_thai = 'รายเดือน'                         
                        elif type_show == 'week':
                            type_variable = type_show  
                            type_thai = 'รายสัปดาห์'
                        elif type_show == 'day':
                            type_variable = type_show 
                            type_thai = 'รายวัน' 
                        elif type_show == 'hour':
                            type_variable = type_show  
                            type_thai = 'รายชั่วโมง'
                        data = executor.submit(select_1().select_admin_count_viewdoc_v2, tax_id,document_type,level_admin,type_show)
                        return_data = data.result()                        
                    tmp_2[type_variable] = return_data['messageText']      
                    list_result.append(tmp_2)
                
                elif int(level_admin) == 1 :
                    tmp_json, list_result, tmp_2 = {}, [], {}
                    if tax_id == None or tax_id == "" :
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the biz_tax was not filled out.','data':[]}}),200
                    elif tax_id not in list_id_card_num:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the user is not in the business.','data':[]}}),200
                    else :
                        if len(tax_id) != 13:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because tax_id incorret','data':[]}}),200
                        elif len(tax_id) == 13:
                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                if type_show == 'month':  
                                    type_variable = type_show 
                                    type_thai = 'รายเดือน'                         
                                elif type_show == 'week':
                                    type_variable = type_show  
                                    type_thai = 'รายสัปดาห์'
                                elif type_show == 'day':
                                    type_variable = type_show 
                                    type_thai = 'รายวัน' 
                                elif type_show == 'hour':
                                    type_variable = type_show  
                                    type_thai = 'รายชั่วโมง'
                                data = executor.submit(select_1().select_admin_count_viewdoc_v2, tax_id,document_type,level_admin,type_show)
                                return_data = data.result()
                    tmp_2[type_variable] = return_data['messageText']      
                    list_result.append(tmp_2)
                    # print(list_result)
                print(return_data['result'])
                if return_data['result'] == 'OK':   
                    data_excel = list_result[0][type_variable]
                    data_excel1 = data_excel['documents_all_' + type_variable][0]
                    data_excel2 = data_excel['documents_past_' + type_variable]
                    ts = int(time.time())
                    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    st_filename = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S-')
                    path = path_global_1 + '/storage/excel_report/' + str(st) + '/'
                    path_indb = path_global_1 + '/storage/excel_report/' + str(st) + '/'
                    # path = './storage/excel_report/' + str(st) + '/'
                    # path_indb = '/storage/excel_report/' + str(st) + '/'
                    if not os.path.exists(path):
                        os.makedirs(path)
                    unique_filename = str(uuid.uuid4())
                    filename = 'report_paperless(' + type_variable + ')' + st_filename + unique_filename
                    row = 4
                    title = 'รายงานสรุปจำนวนเอกสารย้อนหลังจากการเซ็นเอกสาร (' + type_thai + ')'
                    workbook = xlsxwriter.Workbook(path + filename + '.xlsx')
                    worksheet = workbook.add_worksheet()
                    format1 = workbook.add_format()
                    format1.set_align('center')
                    format1.set_align('vcenter')
                    format1.set_text_wrap()
                    format2 = workbook.add_format({'bold': True})
                    format2.set_align('left')
                    format2.set_text_wrap()
                    cell_format = workbook.add_format({'bold': True})
                    cell_format.set_align('center')
                    cell_format.set_align('vcenter')
                    cell_format.set_text_wrap()
                    cell_format.font_size = 12
                    if document_type == "":
                        worksheet.write('C3', 'ทั้งหมด',format1)
                    else:
                        worksheet.write('C3', document_type,format1)
                    if tax_id == "":
                        worksheet.write('E3', 'ทั้งหมด',format1)
                    else:
                        worksheet.write('E3', tax_id,format1)
                    worksheet.write('B3', 'ประเภทเอกสาร',cell_format)                    
                    worksheet.write('D3', 'หมายเลขเอกสาร',cell_format)                  
                    worksheet.write('A4', 'ลำดับ',cell_format)
                    worksheet.write('B4', 'วันที่',cell_format)
                    worksheet.write('C4', 'จำนวนผู้ส่งเอกสาร',cell_format)
                    worksheet.write('D4', 'จำนวนเอกสารทั้งหมด',cell_format)
                    worksheet.write('E4', 'จำนวนเอกสารที่อยู่ในระบบ',cell_format)
                    worksheet.write('F4', 'จำนวนเอกสารที่ถูกยกเลิก',cell_format)
                    worksheet.write('G4', 'จำนวนเอกสารที่ถูกลบ',cell_format)
                    worksheet.merge_range('C2:G2', title,cell_format)
                    worksheet.merge_range('H4:I4', 'สรุปเอกสารทั้งหมด',cell_format)
                    worksheet.write('H5', 'จำนวนผู้ส่งเอกสารทั้งหมด',format2)
                    worksheet.write('H6', 'จำนวนเอกสารทั้งหมด',format2)
                    worksheet.write('H7', 'จำนวนเอกสารที่อยู่ในระบบ',format2)
                    worksheet.write('H8', 'จำนวนเอกสารที่ถูกยกเลิก',format2)
                    worksheet.write('H9', 'จำนวนเอกสารที่ถูกลบ',format2)
                    worksheet.write('I5', data_excel1['countUser_of_' + type_variable],format1)
                    worksheet.write('I6', data_excel1['documents_all'],format1)
                    worksheet.write('I7', data_excel1['documents_all_active'],format1)
                    worksheet.write('I8', data_excel1['documents_all_reject'],format1)
                    worksheet.write('I9', data_excel1['documents_all_delete'],format1)
                    worksheet.set_column(0,0,7)
                    worksheet.set_column(1,3,20)
                    worksheet.set_column(4,6,24)
                    worksheet.set_column(7,7,26)
                    for num in range (len(data_excel2)):
                        line = data_excel2[num]
                        dateStart = datetime.datetime.strptime(line['datetime_start'], '%Y-%m-%d %H:%M:%S')
                        dateEnd = datetime.datetime.strptime(line['datetime_end'], '%Y-%m-%d %H:%M:%S') 
                        if type_show == 'month':       
                            datetimes = dateStart.strftime('%Y-%m')
                        elif type_show == 'week':   
                            datetimes1 = dateEnd.strftime('%d')    
                            datetimes = dateStart.strftime('%Y-%m-(%d,' + datetimes1 + ')')                            
                        elif type_show == 'day':       
                            datetimes = dateStart.strftime('%Y-%m-%d')
                        elif type_show == 'hour':       
                            datetimes = dateStart.strftime('%Y-%m-%d %H:%M:%S')
                        worksheet.write(row, 0, (num+1), format1)
                        worksheet.write(row, 1, datetimes,format1)
                        worksheet.write(row, 2, line['count_user'],format1)
                        worksheet.write(row, 3, line['all_documents'],format1)
                        worksheet.write(row, 4, line['documents_active'],format1)
                        worksheet.write(row, 5, line['documents_reject'],format1)
                        worksheet.write(row, 6, line['documents_delete'],format1)
                        row += 1
                    workbook.close()
                    filename = filename + '.xlsx'
                    sha512encode_unifile = hashlib.sha512(str(unique_filename).encode('utf-8')).hexdigest()
                    web_download_file = myUrl_domain + 'api/v1/excel/download_file/' + sha512encode_unifile
                    return jsonify({'result':'OK','messageText':list_result,'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':list_result,'status_Code':200,'messageER':'error fetching data'}),200               
            else:
                return jsonify({'result':'OK','messageText':None,'status_Code':404,'messageER':'level admin incorret'}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorret'}),404


# ข้อมูลการ Login ย้อนหลังรายเดือน สามารถ Export เป็น  Excel ได้
@status_methods.route('/api/v1/dashboard_admin/transaction/login',methods=['POST'])
def dashboardAdmin_selectCount_TranlogLogin():
    if  request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        if 'typeShow' in dataJson: 
            typeShow = dataJson['typeShow']
        if result_level_eval['result'] == 'OK':
            with concurrent.futures.ThreadPoolExecutor() as executor:
                LoginMonth = executor.submit(select_1().selectCountLogin,typeShow)
                returnLogin = LoginMonth.result()
            
            if returnLogin['result'] == 'OK':
                dataCountLogin = returnLogin['messageText']
                dataCountLoginAll = dataCountLogin[0]['All_Historical_Login']
                dataCountLoginMonth = dataCountLogin[0]['Sub_Historical_Login']
                listDataMonth = dataCountLoginMonth['message']

                ts = int(time.time())
                st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                st_filename = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S-')
                path = path_global_1 + '/storage/excel_report/' + str(st) + '/'
                path_indb = path_global_1 + '/storage/excel_report/' + str(st) + '/'
                # path = './storage/excel_report/' + str(st) + '/'
                # path_indb = '/storage/excel_report/' + str(st) + '/'
                if not os.path.exists(path):
                    os.makedirs(path)                
                if typeShow == 'month':
                    titel_type = 'รายเดือน'
                    title = 'จำนวนการเข้าสู่ระบบ 12 เดือนย้อนหลัง'
                elif typeShow == 'hour':
                    titel_type = 'รายชั่วโมง'
                    hour_count = len(listDataMonth)                
                    title = 'จำนวนการเข้าสู่ระบบ '+str(hour_count)+' ชั่วโมงย้อนหลัง'
                unique_filename = str(uuid.uuid4())
                filename = 'รายงานสรุปการเข้าสู่ระบบ_Paperless_'+ titel_type +'_'+ st_filename + unique_filename
                workbook = xlsxwriter.Workbook(path + filename + '.xlsx')
                worksheet = workbook.add_worksheet()
                format1 = workbook.add_format({'bold': True})
                format1.set_align('center')
                format1.set_align('vcenter')                            
                format2 = workbook.add_format({'bold': True})
                format2.set_align('left')        
                format3 = workbook.add_format()
                format3.set_align('right')
                format4 = workbook.add_format()
                format4.set_align('left')
                format5 = workbook.add_format()
                format5.set_align('center')
                cell_format = workbook.add_format({'bold': True})
                cell_format.set_align('center')
                cell_format.set_align('vcenter')
                cell_format.font_size = 12
                worksheet.merge_range('A2:N2', title,cell_format)
                worksheet.merge_range('B4:C4', 'จำนวนการเข้าสู่ระบบทั้งหมด',format1)
                worksheet.write('C5', dataCountLoginAll['CountLoginAll'],format3)
                i = 3
                for x in range(len(listDataMonth)):
                    nameMonth = datetime.datetime.strptime(listDataMonth[x]['datetime_start'], '%Y-%m-%d %H:%M:%S')  
                    if typeShow == 'month':
                        worksheet.write(3,i, nameMonth.strftime("%B %Y"),format1)
                    elif typeShow == 'hour':                 
                        worksheet.write(3,i, nameMonth.strftime("%H:%M - %H:59"),format1)
                    worksheet.write(4,i+1, listDataMonth[x]['CountOfLogin'],format3)
                    i += 2
                    x +=1

                worksheet.write('A6', 'ลำดับ',format1)
                col_last = int(len(listDataMonth) * 2 + 3)
                for i in range(1,col_last,2):
                    worksheet.write(4,i, 'จำนวนการเข้าสู่ระบบ',format2)
                    worksheet.write(5,i, 'E-mail',format2)
                for i in range(2,col_last,2):                    
                    worksheet.write(5,i, 'จำนวน',format1)
                for i in range(col_last):
                    if i % 2 == 0:
                        worksheet.set_column(i,i,10)   
                    else:
                        worksheet.set_column(i,i,20) 
                col = 3
                rowAll = 6          
                for dataAll in dataCountLoginAll['CountUserLoginAll']:
                    worksheet.write(rowAll, 0, rowAll-5,format5)
                    worksheet.write(rowAll, 1, dataAll['email'],format4)
                    worksheet.write(rowAll, 2, dataAll['count'],format5)
                    rowAll += 1
                for dataMonth in listDataMonth:
                    row = 6
                    for line in dataMonth['CountUserLogin']:
                        worksheet.write(row, col, line['email'],format4)
                        worksheet.write(row, col + 1, line['count'],format5)
                        row += 1
                    col += 2
                workbook.close()
                filename = filename + '.xlsx'
                sha512encode_unifile = hashlib.sha512(str(unique_filename).encode('utf-8')).hexdigest()
                web_download_file = myUrl_domain + 'api/v1/excel/download_file/' + sha512encode_unifile
                return jsonify({'result':'OK','messageText':returnLogin['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'OK','messageText':returnLogin['messageText'],'status_Code':200,'messageER':{'message':'some data is error','data':[]}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorret'}),404


@status_methods.route('/api/v1/dashboard_admin/user', methods=['POST','GET'])
def dashboard_admin_v1():
    if request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            # print ('username',username)
            # print ('email',email)
            biz_detail = data_from_result_eval['biz_detail']
            # print ('len',len(biz_detail))
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
            # print ('list_id_card_num',list_id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        if 'biz_tax' in dataJson and 'secret_code' in dataJson and 'public_code' in dataJson and len(dataJson) == 3:
            tax_id = dataJson['biz_tax']
            tmp_secret_code = dataJson['secret_code']
            tmp_public_code = dataJson['public_code']
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                if level_admin == None :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found','data':[]}}),200
                elif int(level_admin) == 0 :
                    print('biz_tax เป็นค่าว่างได้')
                    if tmp_secret_code == 'yKCLoRmsBO' and tmp_public_code == 'lqDbIkI9u1ANCwWqL7KzbVDwSO960ETy':
                        result_select = select().select_for_admin_data_user_v2(tax_id)
                        if result_select['result'] == 'OK':
                            return jsonify({'result':'OK','messageText':{'message':'success','data':result_select['messageText']},'status_Code':200,'messageER':None}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'data not found','data':[]}}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'secret_code or public_code incorrect','data':[]}}),200
                elif int(level_admin) == 1 :
                    print ('biz_tax ห้ามเป็นนค่าว่าง !!!')
                    if tax_id == None or tax_id == "" :
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the biz_tax was not filled out.','data':[]}}),200
                    elif tax_id not in list_id_card_num:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the user is not in the business.','data':[]}}),200
                    else :
                        if len(tax_id) != 13:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'data not found','data':[]}}),200
                        else:
                            if tmp_secret_code == 'yKCLoRmsBO' and tmp_public_code == 'lqDbIkI9u1ANCwWqL7KzbVDwSO960ETy':
                                result_select = select().select_for_admin_data_user(tax_id)
                                if result_select['result'] == 'OK':
                                    return jsonify({'result':'OK','messageText':{'message':'success','data':result_select['messageText']},'status_Code':200,'messageER':None}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'data not found','data':[]}}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'secret_code or public_code incorrect','data':[]}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'parameter incorrect','data':[]}}),200

        # dataJson = request.json
        # if 'biz_tax' in dataJson and 'secret_code' in dataJson and 'public_code' in dataJson and len(dataJson) == 3:
        #     tax_id = dataJson['biz_tax']
        #     tmp_secret_code = dataJson['secret_code']
        #     tmp_public_code = dataJson['public_code']
        #     if tmp_secret_code == 'yKCLoRmsBO' and tmp_public_code == 'lqDbIkI9u1ANCwWqL7KzbVDwSO960ETy':
        #         result_select = select().select_for_admin_data_user(tax_id)
        #         if result_select['result'] == 'OK':
        #             return jsonify({'result':'OK','messageText':{'message':'success','data':result_select['messageText']},'status_Code':200,'messageER':None}),200
        #         else:
        #             return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'data not found','data':[]}}),200
        #     else:
        #         return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'secret_code or public_code incorrect','data':[]}}),200
        # else:
        #     return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'parameter incorrect','data':[]}}),200
    elif request.method == 'GET':
        user_id = request.args.get('userid')
        result_select = select().select_citizenlogin_to_onechatlogin_addbottofrdAUto(user_id)
        forward = result_select['forward']
        userid = None
        one_access_token = None
        access_token = None
        credentials_list = None
        email_addbot = None
        list_email = []
        json_data = []
        tmp_json = {}
        str_access_token = 'Bearer '
        username = None
        email = None
        level_admin = None
        for x in range(len(forward)):
            userid = result_select['forward'][x]['user_id']
            one_access_token = result_select['forward'][x]['one_access_token']
            access_token = result_select['forward'][x]['access_token']
            email_addbot = result_select['forward'][x]['email_addbot']
        list_email.append(email_addbot)
        tmp_json['data_onechat_add_bot'] = []
        tmp_json['data_oneauth_ca'] = []
        result_addbot = addbot_tofrdAUto(list_email)
        if result_addbot['status'] == 'success':
            tmp_list_friend = result_addbot['list_friend']
            for i in range(len(tmp_list_friend)):
                tmp_list = tmp_list_friend[i]
                print(tmp_list)
                tmp_status = tmp_list_friend[i]['status']
                if tmp_status == 'success':
                    tmp_json['data_onechat_add_bot'].append({'result':'OK','messageER':{'message':None,'data':[]},'status_Code':200,'messageText':tmp_list['message']})
                else:
                    tmp_json['data_onechat_add_bot'].append({'result':'ER','messageER':{'message':tmp_list['message'],'data':[]},'status_Code':200,'messageText':None})
        else:
            tmp_json['data_onechat_add_bot'].append({'result':'ER','messageER':{'message':result_addbot['msg'],'data':[]},'status_Code':200,'messageText':None})
        str_access_token += one_access_token
        credentials_list = credentials_list_v2('','','','','',str_access_token)
        if credentials_list['result'] == 'OK':
            tmp_msg = credentials_list['msg']
            if tmp_msg['totalResult'] == 0:
                tmp_json['data_oneauth_ca'].append({'result':'ER','messageText':None,'messageER':{'message':credentials_list['msg'],'data':[]},'status_Code':200})
            else:
                tmp_json['data_oneauth_ca'].append({'result':'OK','messageText':credentials_list['msg'],'messageER':None,'status_Code':200})
        else:
            tmp_json['data_oneauth_ca'].append({'result':'ER','messageText':None,'messageER':{'message':credentials_list['msg'],'data':[]},'status_Code':200})

        one_chat = login_OneChat(user_id,one_access_token)

        tmp_json['login_onechat'] = one_chat
        result_select['messageText'].append(tmp_json)
        if result_select['result'] == 'OK':
            return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':None}),200
        else:
            return jsonify({'result':'ER','messageText':[],'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200

@status_methods.route('/api/v1/dashboard_admin/transactionlog',methods=['POST','GET'])
def transactionlog_api_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'datetimeStart' in dataJson and 'datetimeEnd' in dataJson and 'limit' in dataJson and 'email_thai' in dataJson and len(dataJson) == 4:
            datetime_start = dataJson['datetimeStart']
            datetime_end = dataJson['datetimeEnd']
            limit = dataJson['limit']
            tmp_email_thai = dataJson['email_thai']
            result_select = select().select_table_transactionlog(datetime_start,datetime_end,limit,tmp_email_thai)
            if result_select['result'] == 'OK':
                return (jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':None})),200
            elif result_select['result'] == 'ER':
                return (jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}})),200
        else:
            return (jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':[]}})),404
    elif request.method == 'GET':
        tmp_tid = request.args.get('id')
        if tmp_tid != None:
            result_select = select().select_getone_transactionlog(tmp_tid)
            if result_select['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':[]}}),404

@status_methods.route('/api/v1/dashboard_admin/service_log',methods=['POST','GET'])
def service_log_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'datetimeStart' in dataJson and 'datetimeEnd' in dataJson and 'limit' in dataJson and 'email_thai' in dataJson and len(dataJson) == 4:
            datetime_start = dataJson['datetimeStart']
            datetime_end = dataJson['datetimeEnd']
            limit = dataJson['limit']
            tmp_email_thai = dataJson['email_thai']
            result_select = select().select_table_service_log(datetime_start,datetime_end,limit,tmp_email_thai)
            if result_select['result'] == 'OK':
                return (jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':None})),200
            elif result_select['result'] == 'ER':
                return (jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':None}})),200
        else:
            return (jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':[]}})),404
    elif request.method == 'GET':
        tmp_tid = request.args.get('id')
        if tmp_tid != None:
            result_select = select().select_getone_transactionlog(tmp_tid)
            if result_select['result'] == 'OK':
                return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':[]}}),404

@status_methods.route('/api/v2/dashboard_admin/bizpaper',methods=['GET'])
# @token_required
def get_bizpaperAndbizprofile_api_v2():
    if request.method == 'GET':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            print('result_verify',result_verify)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'token expire','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            print ('username',username)
            print ('email',email)
            biz_detail = data_from_result_eval['biz_detail']
            print ('len',len(biz_detail))
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
            print ('list_id_card_num',list_id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]} + str(e),'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))

        list_result_return = []
        if result_verify['result'] == 'OK':
            level_admin = result_level_eval['messageText']['level_admin']
            # print('level_admin',level_admin)
            if level_admin == None :
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found','data':[]}}),200
            elif int(level_admin) == 0 :
                messageText_result = result_verify['messageText'].json()
                result_select = select_1().select_tb_bizpaperAndbizprofile_v2()
                if result_select['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':[],'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200
            elif int(level_admin) == 1 :
                messageText_result = result_verify['messageText'].json()
                result_select = select_1().select_tb_bizpaperAndbizprofile_v2()
                if result_select['result'] == 'OK':
                    tmp_result_message = result_select['messageText']
                    tmp_biz_detail = messageText_result['biz_detail']
                    for n in range(len(tmp_biz_detail)):
                        tmp_biz_id = tmp_biz_detail[n]['biz_id']
                        for i in range(len(tmp_result_message)):
                            tmp_id = tmp_result_message[i]['id']
                            if tmp_id == tmp_biz_id:
                                list_result_return.append(tmp_result_message[i])
                    return jsonify({'result':'OK','messageText':list_result_return,'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':[],'status_Code':200,'messageER':{'message':'error','data':[]}}),200

        else:
            return jsonify({'result':'ER','messageText':[],'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401

@status_methods.route('/api/v1/dashboard_admin/bizpaper',methods=['GET'])
# @token_required
def get_bizpaperAndbizprofile_api_v1():
    if request.method == 'GET':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'token expire','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    if id_card_num not in list_id_card_num:
                        list_id_card_num.append(id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]} + str(e),'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))

        list_result_return = []
        if result_verify['result'] == 'OK':
            level_admin = result_level_eval['messageText']['level_admin']
            if level_admin == None :
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found','data':[]}}),200
            elif int(level_admin) == 0 :
                messageText_result = result_verify['messageText'].json()
                result_select = select().select_tb_bizpaperAndbizprofile()
                if result_select['result'] == 'OK':
                    # tmp_result_message = result_select['messageText']
                    # tmp_biz_detail = messageText_result['biz_detail']
                    # for n in range(len(tmp_biz_detail)):
                    #     tmp_biz_id = tmp_biz_detail[n]['biz_id']
                    #     for i in range(len(tmp_result_message)):
                    #         tmp_id = tmp_result_message[i]['id']
                    #         if tmp_id == tmp_biz_id:
                    #             list_result_return.append(tmp_result_message[i])
                    return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':[],'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200
            elif int(level_admin) == 1 :
                messageText_result = result_verify['messageText'].json()
                result_select = select().select_tb_bizpaperAndbizprofile()
                print(result_select)
                if result_select['result'] == 'OK':
                    tmp_result_message = result_select['messageText']
                    tmp_biz_detail = messageText_result['biz_detail']
                    for n in range(len(tmp_biz_detail)):
                        tmp_biz_id = tmp_biz_detail[n]['biz_id']
                        for i in range(len(tmp_result_message)):
                            tmp_id = tmp_result_message[i]['id']
                            if tmp_id == tmp_biz_id:
                                list_result_return.append(tmp_result_message[i])
                    return jsonify({'result':'OK','messageText':list_result_return,'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':[],'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200

        else:
            return jsonify({'result':'ER','messageText':[],'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401

@status_methods.route('/api/v1/dashboard_admin/document',methods=['POST'])
def dashboard_admin_document_v1():
    if request.method == 'POST':
        username = None
        email = None
        level_admin = None
        id_user = None
        getbiz = None
        id_card_num = None
        list_id_card_num = []
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            # print('result_verify : ',result_verify['messageText'].text)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            # print ('result_verify',data_from_result_eval)
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            id_user = data_from_result_eval['id']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        tax = None
        if 'datetimeStart' in dataJson and 'datetimeEnd' in dataJson and 'document_id' in dataJson and 'sender_email' in dataJson and 'recipient_email' in dataJson and 'tax_id' in dataJson and 'documentType' in dataJson and  'limit' in dataJson:
            tax = dataJson['tax_id']
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                try:
                    if level_admin == None:
                        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'level_admin not found'}),200
                    elif int(level_admin) == 0 :
                        datetime_start = dataJson['datetimeStart']
                        datetime_end = dataJson['datetimeEnd']
                        document_id = dataJson['document_id']
                        sender_email = dataJson['sender_email']
                        recipient_email = dataJson['recipient_email']
                        tax_id = dataJson['tax_id']
                        documentType = dataJson['documentType']
                        limit = dataJson['limit']
                        if 'text' in dataJson:
                            tmp_text = dataJson['text']
                        else:
                            tmp_text = ''
                        result_select = select_3().select_document_v2(datetime_start,datetime_end,document_id,sender_email,recipient_email,tax_id,documentType,limit,tmp_text)
                        if result_select['result'] == 'OK':
                            return jsonify({'result':'OK','result_lasttime' : result_select['last_time'] ,'messageText':result_select['messageText'],'status_Code':200,'messageER':None}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200
                    elif int(level_admin) == 1 :
                        if tax == None or tax == "":
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the tax_id was not filled out.','data':[]}}),200
                        elif tax not in list_id_card_num:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the user is not in the business.','data':[]}}),200
                        else:
                            if len(tax) != 13:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'data not found','data':[]}}),200
                            else:
                                datetime_start = dataJson['datetimeStart']
                                datetime_end = dataJson['datetimeEnd']
                                document_id = dataJson['document_id']
                                sender_email = dataJson['sender_email']
                                recipient_email = dataJson['recipient_email']
                                tax_id = dataJson['tax_id']
                                documentType = dataJson['documentType']
                                limit = dataJson['limit']
                                if 'text' in dataJson:
                                    tmp_text = dataJson['text']
                                else:
                                    tmp_text = ''
                                result_select = select_3().select_document_v2(datetime_start,datetime_end,document_id,sender_email,recipient_email,tax_id,documentType,limit,tmp_text)
                                if result_select['result'] == 'OK':
                                    return jsonify({'result':'OK','result_lasttime' : result_select['last_time'] ,'messageText':result_select['messageText'],'status_Code':200,'messageER':None}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200
                except Exception as e:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':str(e),'data':[]}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':[]}}),404

@status_methods.route('/api/v1/dashboard_admin/pdf/<string:type_pdf>',methods=['GET'])
def dashboard_admin_pdf_api_v1(type_pdf):
    if type_pdf == 'original_pdf':
        if request.method == 'GET':
            tmp_sidCode = request.args.get('sidCode')
            if tmp_sidCode != None:
                result_select = select().select_admin_dashboard_pdf_v1(tmp_sidCode)
                if result_select['result'] == 'OK':
                    try:
                        filename = result_select['messageText'][0]['file_name'].encode('latin-1')
                    except UnicodeEncodeError:
                        filenames = {
                            'filename': unicodedata.normalize('NFKD', result_select['messageText'][0]['file_name']).encode('latin-1', 'ignore'),
                            'filename*': "UTF-8''{}".format(result_select['messageText'][0]['file_name']),
                        }
                        filenames['filename'] = filenames['filename'].decode('utf8')
                    else:
                        filenames = {'filename': result_select['messageText'][0]['file_name']}
                    return send_file(io.BytesIO(base64.b64decode(str(result_select['messageText'][0]['string_pdf']))),mimetype='application/pdf',as_attachment=True,attachment_filename='%s' % str(filenames['filename']))
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}})
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':tmp_sidCode['messageText'],'data':[]}})
    elif type_pdf == 'sign_pdf':
        if request.method == 'GET':
            tmp_sidCode = request.args.get('sidCode')
            if tmp_sidCode != None:
                result_select = select().select_admin_dashboard_pdf_v1(tmp_sidCode)
                if result_select['result'] == 'OK':
                    try:
                        filename = result_select['messageText'][0]['file_name'].encode('latin-1')
                    except UnicodeEncodeError:
                        filenames = {
                            'filename': unicodedata.normalize('NFKD', result_select['messageText'][0]['file_name']).encode('latin-1', 'ignore'),
                            'filename*': "UTF-8''{}".format(result_select['messageText'][0]['file_name']),
                        }
                        filenames['filename'] = filenames['filename'].decode('utf8')
                    else:
                        filenames = {'filename': result_select['messageText'][0]['file_name']}
                    return send_file(io.BytesIO(base64.b64decode(str(result_select['messageText'][0]['string_sign']))),mimetype='application/pdf',as_attachment=True,attachment_filename='%s' % str(filenames['filename']))
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}})
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':tmp_sidCode['messageText'],'data':[]}})
    else:
        abort(404)

@status_methods.route('/api/v1/dashboard_admin/documentone',methods=['POST'])
def dashboard_admin_sidCode_api_v1():
    if request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        biz_detail = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            print ('username',username)
            print ('email',email)
            biz_detail = data_from_result_eval['biz_detail']
            print ('len',len(biz_detail))
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
            print ('list_id_card_num',list_id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]} + str(e),'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        if 'sidCode' in dataJson and 'tax_id' in dataJson and len(dataJson) == 2:
            sidCode = dataJson['sidCode']
            tax_id = dataJson['tax_id']
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                try:
                    if level_admin == None:
                        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'level_admin not found'}),200
                    elif int(level_admin) == 0 :
                        print('biz_tax เป็นค่าว่างได้')
                        result_select = select().select_admin_document_one_v1(sidCode,tax_id)
                        if result_select['result'] == 'OK':
                            return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':None}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200
                    elif int(level_admin) == 1 :
                        print ('biz_tax ห้ามเป็นนค่าว่าง !!!')
                        print ('tax id ',tax_id )
                        if tax_id == None or tax_id == "":
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the tax_id was not filled out.','data':[]}}),200
                        elif tax_id not in list_id_card_num:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the user is not in the business.','data':[]}}),200
                        else:
                            result_select = select().select_admin_document_one_v2(sidCode,tax_id)
                            if result_select['result'] == 'OK':
                                return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':None}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200
                except Exception as e:
                    return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':str(e),'data':[]}}),404
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':[]}}),404

@status_methods.route('/api/v1/dashboard_admin/login_admin',methods=['POST'])
def dashboard_admin_login():
    if request.method == 'POST':
        dataJson = request.json
        if 'username' in dataJson and 'password' in dataJson and len(dataJson) == 2:
            username = dataJson['username']
            password = dataJson['password']
            result_select = select().select_admin_username_login_v1(username,password)

            check = result_select['check']
            level_admin = result_select['level_admin']
            print ('level_admin: ',level_admin)
            data_result = {}
            if check == True :
                try:
                    tmp_json = {
                        "grant_type":  "password",
                        "username":     username,
                        "password":     password,
                        "client_id":    clientId,
                        "client_secret":secretKey
                    }
                    response = callPost_v2(one_url+"/api/oauth/getpwd",tmp_json)
                    if response['result'] == 'OK':
                        response_messageText = response['messageText']
                        response_messageText = response_messageText.json()
                        print(response_messageText)
                        tmp_one_access_token = response_messageText['token_type'] + ' ' +response_messageText['access_token']
                        result_update_status = update().update_login_user_admin_v1(username,password)
                        if result_update_status['result'] == 'OK':
                            getBuz = callGET_v2(one_url+"/api/account_and_biz_detail",tmp_one_access_token)
                            if getBuz['result'] == 'OK':
                                tmp_message = getBuz['messageText'].json()
                                data_result['one_access_token'] = response_messageText['access_token']
                                data_result['one_result_data'] = tmp_message
                                data_result['username'] = response_messageText['username']
                                data_result['level_admin'] = level_admin[0]['level_admin']

                            return jsonify({'result':'OK','messageText':{'message':'login success','data':data_result},'status_Code':200,'messageER':None}),200
                        else:
                            return jsonify({'result':'OK','messageText':{'message':'login success non update','data':data_result},'status_Code':200,'messageER':None}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':{'message':'username or password incorrect Unauthorized','data':[]}}),401
                except Exception as e:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':str(e),'data':[]}}),200
            elif check == False:
                return jsonify({'result':'ER','messageText':None,'status_Code':401,'messageER':{'message':'user non admin Unauthorized','data':[]}}),401
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':[]}}),404

@status_methods.route('/api/v1/dashboard_admin/delete_useradmin',methods=['PUT'])
def dashboard_admin_delete_useradmin():
    if request.method == 'PUT':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        if result_level_eval['result'] == 'OK':
            level_admin = result_level_eval['messageText']['level_admin']
            if level_admin == None :
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found','data':[]}}),200
            elif int(level_admin) == 0 :
                dataJson = request.json
                if 'username' in dataJson and 'email' in dataJson and len(dataJson) == 2:
                    username = dataJson['username']
                    email = dataJson['email']
                    result_update = update().update_username_admin(username,email)
                    if result_update['result'] == 'OK' :
                        return jsonify({'result':'OK','messageText':'remove user \''+ username+ '\' successful','status_Code':200,'messageER':None})
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_update['messageText'],'data':[]}})
                else:
                    return jsonify({'result':'ER','messageText':'parameter incorret','status_Code':200,'messageER':{'message':None,'data':[]}})
            elif int(level_admin) == 1 :
                return jsonify({'result':'OK','messageText':'This user cannot delete admin.','status_Code':200,'messageER':None})
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':None,'data':[]}})

@status_methods.route('/api/v1/excel/report_document_admin', methods=['POST'])
@token_required
def get_admin_document():
    if request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        biz_detail = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'token expire unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'token expire unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'token expire unauthorized ' + str(e),'data':[]}}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        try:
            if 'datetimeStart' in dataJson and 'datetimeEnd' in dataJson and 'document_id' in dataJson and 'sender_email' in dataJson and 'recipient_email' in dataJson and 'documentType' in dataJson and 'tax_id' in dataJson  and len(dataJson) == 7:
                start_datetime = dataJson['datetimeStart']
                end_datetime = dataJson['datetimeEnd']
                document_id = dataJson['document_id']
                sender_email = dataJson['sender_email']
                recipient_email = dataJson['recipient_email']
                document_type = dataJson['documentType']
                tmp_tax_id = dataJson['tax_id']
                if result_level_eval['result'] == 'OK':
                    level_admin = result_level_eval['messageText']['level_admin']
                    try:
                        if level_admin == None :
                            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'level_admin not found','data':[]}}),404
                        elif int(level_admin) == 0 :
                            if start_datetime == '' and end_datetime == '' and document_id == '' and sender_email == '' and recipient_email == '' and document_type == '' and  tmp_tax_id == '':
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'value not found'}}),200
                            list_tax_id = []
                            tmp_message = result_verify['messageText'].json()
                            tmp_data_biz_detail = tmp_message['biz_detail']
                            for u in range(len(tmp_data_biz_detail)):
                                tmp_data_getbiz = tmp_data_biz_detail[u]['getbiz'][0]
                                tmp_id_card_num = tmp_data_getbiz['id_card_num']
                                list_tax_id.append(tmp_id_card_num)
                            tmp_username = tmp_message['username']
                            result_select = select().select_document_for_report_admin_v2(start_datetime,end_datetime,document_id,sender_email,recipient_email,tmp_tax_id,document_type)
                            if result_select['result'] == 'OK':
                                ts = int(time.time())
                                st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                                st_filename = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S-')
                                path = path_global_1 + '/storage/excel_report/' + str(st) + '/'
                                path_indb = path_global_1 + '/storage/excel_report/' + str(st) + '/'
                                # path = './storage/excel_report/' + str(st) + '/'
                                # path_indb = '/storage/excel_report/' + str(st) + '/'
                                if not os.path.exists(path):
                                    os.makedirs(path)
                                unique_filename = str(uuid.uuid4())
                                filename = str(tmp_tax_id) + '_report_paperless' + st_filename + unique_filename
                                data_excel = result_select['messageText'][0]['data']
                                count_n = 0
                                count_r = 0
                                count_y = 0
                                count_c = 0
                                count_d = 0
                                for uu in range(len(data_excel)):
                                    if data_excel[uu]['status_file_code'] == 'N':
                                        count_n += 1
                                    if data_excel[uu]['status_file_code'] == 'R':
                                        count_r += 1
                                    if data_excel[uu]['status_file_code'] == 'Y':
                                        count_y += 1
                                    if data_excel[uu]['status_file_code'] == 'C':
                                        count_c += 1
                                    if data_excel[uu]['status_file_code'] == 'D':
                                        count_d += 1
                                row = 12
                                col = 0                                
                                workbook = xlsxwriter.Workbook(path + filename + '.xlsx')
                                worksheet = workbook.add_worksheet()
                                format1 = workbook.add_format()
                                format1.set_align('left')
                                format1.set_align('vcenter')
                                format1.font_size = 10
                                format1.set_text_wrap()
                                format2 = workbook.add_format()
                                format2.set_align('center')
                                format2.set_align('vcenter')
                                format2.font_size = 10
                                format2.set_text_wrap()
                                cell_format = workbook.add_format({'bold': True})
                                cell_format.set_align('center')
                                cell_format.set_align('vcenter')
                                cell_format.set_text_wrap()
                                cell_format.font_size = 11
                                cell_format2 = workbook.add_format({'bold': True})
                                cell_format2.set_align('left')
                                cell_format2.set_align('vcenter')
                                cell_format2.font_size = 11
                                worksheet.merge_range('D2:H2', 'รายงานสรุปรายละเอียดการดำเนินการเอกสาร paperless',cell_format)
                                worksheet.merge_range('B4:C4', 'จำนวนสถานะเอกสาร',cell_format)
                                worksheet.write('A12', 'ลำดับ',cell_format)
                                worksheet.write('B12', 'ประเภทเอกสาร',cell_format)
                                worksheet.write('C12', 'เลขที่เอกสาร',cell_format)
                                worksheet.write('D12', 'เลขที่ติดตามเอกสาร',cell_format)
                                worksheet.write('E12', 'สถานะเอกสาร',cell_format)
                                worksheet.write('F12', 'ผู้ส่งเอกสาร',cell_format)
                                worksheet.write('G12', 'วันที่ส่ง',cell_format)
                                worksheet.write('H12', 'หมายเหตุ',cell_format)
                                worksheet.write('I12', 'ระยะเวลาดำเนินการ',cell_format)
                                worksheet.write('J12', 'ระยะเวลาทั้งหมดที่เอกสารถูกดำเนินการ',cell_format)
                                worksheet.write('K12', 'ระยะเวลาตั้งแต่เอกสารถูกนำเข้าถึงลำดับล่าสุด',cell_format)
                                worksheet.set_column(0,0,6)
                                worksheet.set_column(1,1,22)
                                worksheet.set_column(2,4,16)
                                worksheet.set_column(5,5,20)
                                worksheet.set_column(6,10,25)
                                count = len(data_excel)
                                count2 = 0

                                for num in range (0, count):
                                    line = data_excel[num]
                                    worksheet.write(row, 0, (num+1), format2)
                                    worksheet.write(row, 1, line['document_name'],format2)
                                    worksheet.write(row, 2, line['document_id'] ,format2)
                                    worksheet.write(row, 3, '=HYPERLINK("' + url_paperless + 'tracking?id=' + line['tracking_id'] + '","' + line['tracking_id']  + '")' ,format2)
                                    worksheet.write(row, 4, line['status_file_string'],format2)
                                    worksheet.write(row, 5, line['sender_name'],format2)
                                    worksheet.write(row, 6, line['dateTime_String_TH_1'] + ' ' + line['time_String'],format2)
                                    worksheet.write(row, 7, line['remark_description'],format2)
                                    worksheet.write(row, 8, line['timeline'],format1)
                                    worksheet.write(row, 9, line['string_details_avg_time'],format2)
                                    worksheet.write(row, 10, line['timing'],format2)
                                    if line['remark_description'] == '' and 'ลำดับที่ 2' not in line['timeline']:
                                        worksheet.set_row(row, 29)
                                    row += 1
                                txt_filter = 'A12:K'+ str(row-1)
                                worksheet.autofilter(txt_filter)

                                worksheet.write("B5","เอกสารทั้งหมด" , cell_format2)
                                worksheet.write("C5",count,format2)
                                worksheet.write("B6","เอกสารกำลังดำเนินการ" , cell_format2)
                                worksheet.write("C6",count_n,format2)
                                worksheet.write("B7","เอกสารอนุมัติ" , cell_format2)
                                worksheet.write("C7",count_y,format2)
                                worksheet.write("B8","เอกสารปฏิเสธอนุมัติ" , cell_format2)
                                worksheet.write("C8",count_r,format2)
                                worksheet.write("B9","เอกสารถูกยกเลิก" , cell_format2)
                                worksheet.write("C9",count_c,format2)
                                worksheet.write("B10","เอกสารถูกลบ" , cell_format2)
                                worksheet.write("C10",count_d,format2)
                                
                                list_doc_type = []
                                list_doc_type2 = []
                                list_count = []
                                for num2 in range (0, count):
                                    line = data_excel[num2]
                                    list_doc_type.append(line['document_type'])
                                    if list_doc_type[num2] not in list_doc_type2:
                                        list_doc_type2.append(list_doc_type[num2])
                                    else:
                                        continue
                                L = 4
                                for num3 in range(len(list_doc_type2)):
                                    if num3 < 6:
                                        worksheet.write(L, 3, list_doc_type2[num3],format2)
                                        worksheet.write(L, 4, list_doc_type.count(list_doc_type2[num3]),format2)
                                    elif num3 < 12:
                                        worksheet.write(L-6, 5, list_doc_type2[num3],format2)
                                        worksheet.write(L-6, 6, list_doc_type.count(list_doc_type2[num3]),format2)
                                    elif num3 < 18:
                                        worksheet.write(L-12, 7, list_doc_type2[num3],format2)
                                        worksheet.write(L-12, 8, list_doc_type.count(list_doc_type2[num3]),format2)
                                    elif num3 < 24:
                                        worksheet.write(L-18, 7, list_doc_type2[num3],format2)
                                        worksheet.write(L-18, 8, list_doc_type.count(list_doc_type2[num3]),format2)
                                    L += 1
                                 
                                worksheet.write("D4","ประเภทเอกสาร" , cell_format)
                                worksheet.write("E4","จำนวน" , cell_format)
                                if num3 >= 6:
                                    worksheet.write("F4","ประเภทเอกสาร" , cell_format)
                                    worksheet.write("G4","จำนวน" , cell_format)
                                if num3 >= 12:
                                    worksheet.write("H4","ประเภทเอกสาร" , cell_format)
                                    worksheet.write("I4","จำนวน" , cell_format)
                                if num3 >= 18:
                                    worksheet.write("J4","ประเภทเอกสาร" , cell_format)
                                    worksheet.write("K4","จำนวน" , cell_format)
                                workbook.close()
                                filename = filename + '.xlsx'
                                sha512encode_unifile = hashlib.sha512(str(unique_filename).encode('utf-8')).hexdigest()
                                insert().insert_tran_excel_file_download_v1(path_indb,filename,sha512encode_unifile,tmp_username,str(dataJson))
                                web_download_file = myUrl_domain + 'api/v1/excel/download_file/' + sha512encode_unifile
                                return jsonify({'result':'OK','messageText':[{'download_excel_file':web_download_file,'token_download':sha512encode_unifile,'data':result_select['messageText']}],'status_Code':200,'messageER':None}),200
                            else:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200
                        elif int(level_admin) == 1 :
                            print ('biz_tax ห้ามเป็นค่าว่าง !!!')
                            if tmp_tax_id == None or tmp_tax_id == "" :
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the biz_tax was not filled out.','data':[]}}),200
                            elif tmp_tax_id not in list_id_card_num:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the user is not in the business.','data':[]}}),200

                            else :
                                if len(tmp_tax_id) != 13:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'data not found','data':[]}}),200
                                else:
                                    if start_datetime == '' and end_datetime == '' and document_id == '' and sender_email == '' and recipient_email == '' and document_type == '' and  tmp_tax_id == '':
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'data':None,'message':'value not found'}}),200
                                    list_tax_id = []
                                    tmp_message = result_verify['messageText'].json()
                                    tmp_data_biz_detail = tmp_message['biz_detail']
                                    for u in range(len(tmp_data_biz_detail)):
                                        tmp_data_getbiz = tmp_data_biz_detail[u]['getbiz'][0]
                                        tmp_id_card_num = tmp_data_getbiz['id_card_num']
                                        list_tax_id.append(tmp_id_card_num)
                                    tmp_username = tmp_message['username']
                                    result_select = select().select_document_for_report_admin_v2(start_datetime,end_datetime,document_id,sender_email,recipient_email,tmp_tax_id,document_type)
                                    if result_select['result'] == 'OK':
                                        ts = int(time.time())
                                        st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                                        st_filename = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S-')
                                        # path = './storage/excel_report/' + str(st) + '/'
                                        # path_indb = '/storage/excel_report/' + str(st) + '/'
                                        path = path_global_1 +'/storage/excel_report/' + str(st) + '/'
                                        path_indb = path_global_1 + '/storage/excel_report/' + str(st) + '/'
                                        if not os.path.exists(path):
                                            os.makedirs(path)
                                        unique_filename = str(uuid.uuid4())
                                        filename = 'admin_report_paperless' + st_filename + unique_filename
                                        data_excel = result_select['messageText'][0]['data']
                                        count_n = 0
                                        count_r = 0
                                        count_y = 0
                                        for uu in range(len(data_excel)):
                                            if data_excel[uu]['status_file_code'] == 'N':
                                                count_n += 1
                                            if data_excel[uu]['status_file_code'] == 'R':
                                                count_r += 1
                                            if data_excel[uu]['status_file_code'] == 'Y':
                                                count_y += 1
                                        row = 1
                                        col = 0
                                        L = 4
                                        M = 11
                                        workbook = xlsxwriter.Workbook(path + filename + '.xlsx')
                                        worksheet = workbook.add_worksheet()
                                        format1 = workbook.add_format()
                                        format1.set_align('center')
                                        format1.set_align('vcenter')
                                        format1.set_text_wrap()
                                        format2 = workbook.add_format()
                                        format2.set_text_wrap()
                                        format3 = workbook.add_format()
                                        format3.set_align('top')
                                        format3.set_text_wrap()
                                        cell_format = workbook.add_format({'bold': True})
                                        cell_format.set_align('center')
                                        cell_format.set_align('vcenter')
                                        cell_format.set_text_wrap()
                                        cell_format.font_size = 12
                                        worksheet.write('A1', 'ลำดับ',cell_format)
                                        worksheet.write('B1', 'ประเภทเอกสาร',cell_format)
                                        worksheet.write('C1', 'เลขที่เอกสาร',cell_format)
                                        worksheet.write('D1', 'เลขที่ติดตามเอกสาร',cell_format)
                                        worksheet.write('E1', 'สถานะเอกสาร',cell_format)
                                        worksheet.write('F1', 'ผู้ส่งเอกสาร',cell_format)
                                        worksheet.write('G1', 'วันที่ส่ง',cell_format)
                                        worksheet.write('H1', 'หมายเหตุ',cell_format)
                                        worksheet.write('I1', 'ระยะเวลาดำเนินการ',cell_format)
                                        worksheet.write('J1', 'ระยะเวลาทั้งหมดที่เอกสารถูกดำเนินการ',cell_format)
                                        worksheet.write('K1', 'ระยะเวลาตั้งแต่เอกสารถูกนำเข้าถึงลำดับล่าสุด',cell_format)
                                        worksheet.set_column(0,0,5)
                                        worksheet.set_column(1,1,15)
                                        worksheet.set_column(2,5,20)
                                        worksheet.set_column(6,13,25)
                                        count = len(data_excel)
                                        count2 = 0

                                        for num in range (0, count):
                                            line = data_excel[num]
                                            worksheet.write(row, 0, (num+1), format1)
                                            worksheet.write(row, 1, line['document_name'],format1)
                                            worksheet.write(row, 2, line['document_id'] ,format1)
                                            worksheet.write(row, 3, '=HYPERLINK("' + url_paperless + 'tracking?id=' + line['tracking_id'] + '","' + line['tracking_id']  + '")' ,format1)
                                            worksheet.write(row, 4, line['status_file_string'],format1)
                                            worksheet.write(row, 5, line['sender_name'],format1)
                                            worksheet.write(row, 6, line['dateTime_String_TH_1'] + ' ' + line['time_String'],format1)
                                            worksheet.write(row, 7, line['remark_description'],format3)
                                            worksheet.write(row, 8, line['timeline'],format3)
                                            worksheet.write(row, 9, line['string_details_avg_time'],format3)
                                            worksheet.write(row, 10, line['timing'],format1)
                                            row += 1
                                        worksheet.write("L2","เอกสารทั้งหมด" , cell_format)
                                        worksheet.write("L3",count,format1)
                                        worksheet.write("M2","เอกสารกำลังดำเนินการ" , cell_format)
                                        worksheet.write("M3",count_n,format1)
                                        worksheet.write("N2","เอกสารอนุมัติ" , cell_format)
                                        worksheet.write("N3",count_y,format1)
                                        worksheet.write("O2","เอกสารปฏิเสธอนุมัติ" , cell_format)
                                        worksheet.write("O3",count_r,format1)

                                        worksheet.write("L4","ประเภทเอกสาร" , cell_format)
                                        worksheet.write("M4","จำนวน" , cell_format)
                                        list_doc_type = []
                                        list_doc_type2 = []
                                        list_count = []
                                        for num2 in range (0, count):
                                            line = data_excel[num2]
                                            list_doc_type.append(line['document_type'])
                                            if list_doc_type[num2] not in list_doc_type2:
                                                list_doc_type2.append(list_doc_type[num2])
                                            else:
                                                continue
                                        for num3 in range(len(list_doc_type2)):
                                            worksheet.write(L, M, list_doc_type2[num3],format1)
                                            worksheet.write(L, 12, list_doc_type.count(list_doc_type2[num3]),format1)
                                            L += 1
                                        workbook.close()
                                        filename = filename + '.xlsx'
                                        sha512encode_unifile = hashlib.sha512(str(unique_filename).encode('utf-8')).hexdigest()
                                        insert().insert_tran_excel_file_download_v1(path_indb,filename,sha512encode_unifile,tmp_username,str(dataJson))
                                        web_download_file = myUrl_domain + 'api/v1/excel/download_file/' + sha512encode_unifile
                                        return jsonify({'result':'OK','messageText':[{'download_excel_file':web_download_file,'token_download':sha512encode_unifile,'data':result_select['messageText']}],'status_Code':200,'messageER':None}),200
                                    else:
                                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200

                            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'level_admin not found','data':[]}}),404
                    except Exception as e:
                        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':str(e),'data':[]}}),404
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrct','data':[]}}),404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

@status_methods.route('/api/v1/dashboard_admin/useradmin',methods=['POST','GET'])
def dashboard_admin_userAdmin_api_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            id_user = data_from_result_eval['id']

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401

        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        level_admin = result_level_eval['messageText']['level_admin']
        try:
            if level_admin == '0':
                dataJson = request.json
                if 'username' in dataJson and 'email_user' in dataJson and 'level_admin' in dataJson and len(dataJson) == 3:
                    username = dataJson['username']
                    email_user = dataJson['email_user']
                    level_admin = dataJson['level_admin']
                    result_insert = insert().insert_admin_username_v1(username,email_user,level_admin)
                    if result_insert['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':result_insert['messageText'],'status_Code':200,'messageER':{'message':None,'data':[]}})
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_insert['messageText'],'data':[]}})
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':[]}}),404

            else :
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'level_admin incorrect','data':[]}}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]} + str(e),'status_Code':200}),200
    elif request.method == 'GET':                    
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        list_test = []
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)

        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        
        try:
            result_level = select().select_level_admin_v1(username,email)
            result_level_eval = eval(str(result_level))
            dataJson = request.args.get('tax_id')
            tax_id = dataJson
            list_json = []
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                if level_admin == None or level_admin == "" :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found','data':[]}}),200
                elif int(level_admin) == 0 :
                    result_select = select().select_list_user_admin()
                    return jsonify({'result':'OK','messageText':result_select['messageText'],'messageER':None,'count': result_select['count'],'status_Code':200}),200
                elif int(level_admin) == 1 :
                    if tax_id == None or tax_id == "" :
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the biz_tax was not filled out.','data':[]}}),200                    
                    elif tax_id not in list_id_card_num:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the user is not in the business.','data':[]}}),200                    
                    else:
                        if len(tax_id) != 13:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'data not found','data':[]}}),200
                        else:
                            result_select = select().select_list_user_admin()
                            return jsonify({'result':'OK','messageText':result_select['messageText'],'messageER':None,'count': result_select['count'],'status_Code':200}),200
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':str(e),'status_Code':401}),401

@status_methods.route('/api/v1/dashboard_admin/document_type',methods=['POST'])
def dashboard_document_detail():
    if request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        if 'tax_id' in dataJson and 'documentStatus' in dataJson and len(dataJson) == 2:
            tax_id = dataJson['tax_id']
            documentStatus = dataJson['documentStatus']
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                if level_admin == None or level_admin == "" :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found','data':[]}}),200
                elif int(level_admin) == 0 :
                    # print('biz_tax เป็นค่าว่างได้')
                    if documentStatus == None or documentStatus == '':
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'documentStatus not null','data':[]}}),200
                    else:
                        result_select = select().select_document_detail(tax_id,documentStatus)
                        return jsonify({'result':'OK','messageText':{'data':result_select['messageText']},'count' : result_select['count'],'status_Code':200,'messageER':{'message':None,'data':[]}}),200
                elif int(level_admin) == 1 :
                    # print ('biz_tax ห้ามเป็นนค่าว่าง !!!')
                    if tax_id == None or tax_id == "" :
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the biz_tax was not filled out.','data':[]}}),200
                    elif tax_id not in list_id_card_num:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the user is not in the business.','data':[]}}),200
                    else :
                        if len(tax_id) != 13:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'data not found','data':[]}}),200
                        else:
                            if documentStatus == None or documentStatus == '':
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'documentStatus not null','data':None}}),200
                            else:
                                result_select = select().select_document_detail(tax_id,documentStatus)
                                return jsonify({'result':'OK','messageText':{'data':result_select['messageText']},'count' : result_select['count'],'status_Code':200,'messageER':None}),200

@status_methods.route('/api/v1/dashboard_admin/document_template',methods=['POST'])
def dashboard_step_template():
    if request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            # print ('username',username)
            # print ('email',email)
            biz_detail = data_from_result_eval['biz_detail']
            # print ('len',len(biz_detail))
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
            # print ('list_id_card_num',list_id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        if 'tax_id' in dataJson and 'documentStatus' in dataJson and len(dataJson) == 2:
            tax_id = dataJson['tax_id']
            documentStatus = dataJson['documentStatus']
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                if level_admin == None or level_admin == "" :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found','data':[]}}),200
                elif int(level_admin) == 0 :
                    print('biz_tax เป็นค่าว่างได้')
                    if documentStatus == None or documentStatus == '':
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'documentStatus not null'}),200
                    else:
                        result_select = select().select_step_template(tax_id,documentStatus)
                        return jsonify({'result':'OK','messageText':{'data':result_select['messageText']},'count' : result_select['count'],'status_Code':200,'messageER':None}),200
                elif int(level_admin) == 1 :
                    print ('biz_tax ห้ามเป็นนค่าว่าง !!!')
                    if tax_id == None or tax_id == "" :
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the biz_tax was not filled out.','data':[]}}),200
                    elif tax_id not in list_id_card_num:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the user is not in the business.','data':[]}}),200
                    else :
                        if len(tax_id) != 13:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'data not found','data':[]}}),200
                        else:
                            if documentStatus == None or documentStatus == '':
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'documentStatus not null'}),200
                            else:
                                result_select = select().select_step_template(tax_id,documentStatus)
                                return jsonify({'result':'OK','messageText':{'data':result_select['messageText']},'count' : result_select['count'],'status_Code':200,'messageER':None}),200

@status_methods.route('/api/v1/dashboard_admin/register_business',methods=['POST'])
def dashboard_admin_register_business_api_v1():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                abort(401)
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                abort(401)
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            id_user = data_from_result_eval['id']
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401

        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        level_admin = result_level_eval['messageText']['level_admin']
        try:
            if level_admin == '0':
                dataJson = request.json
                if 'tax_id' in dataJson and len(dataJson) == 1:
                    tmp_tax_id = dataJson['tax_id']
                    if len(tmp_tax_id) == 13:
                        result_insert = insert().insert_register_business_ppl_v2(tmp_tax_id)
                        url = str(url_ip_eform) + '/api/v1/add_tax_id'
                        data_info = {
                            "tax_id":tmp_tax_id
                        }
                        result_add_tax = callAuth_post_v2(url,data_info,token_header)
                        tmp_text = 'fail'
                        if result_add_tax['result'] == 'OK':
                            if result_add_tax['messageText'].json()['result'] == 'OK':
                                tmp_text = 'success'
                        if result_insert['result'] == 'OK':
                            return jsonify({'result':'OK','messageText':{'message':{'ppl':'success','eform':tmp_text},'data':[]},'status_Code':200,'messageER':None}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':tmp_tax_id +' already in business','data':[]}}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error tax_id incorrect','data':[]}}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':[]}}),404
            else :
                return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'error level_admin incorrect','data':[]}}),200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]} + str(e),'status_Code':200}),200

@status_methods.route('/api/v1/dashboard_admin/business_tax',methods=['GET'])
def dashboard_admin_register_business():
    if request.method == 'GET':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'token expire','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]} + str(e),'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        list_result_return = []
        if result_verify['result'] == 'OK':
            level_admin = result_level_eval['messageText']['level_admin']
            if level_admin == None :
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found','data':[]}}),200
            elif int(level_admin) == 0 :
                messageText_result = result_verify['messageText'].json()
                result_select = select_4().select_taxId_Admin()
                # print(result_select)
                if result_select['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':result_select['messageText'],'count':result_select['count'],'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':[],'status_Code':200,'count':result_select['count'],'messageER':{'message':result_select['messageText'],'data':[]}}),200
            elif int(level_admin) == 1 :
                messageText_result = result_verify['messageText'].json()
                result_select = select_4().select_taxId_Admin()
                if result_select['result'] == 'OK':
                    tmp_result_message = result_select['messageText']
                    tmp_biz_detail = messageText_result['biz_detail']
                    for n in range(len(tmp_biz_detail)):
                        tmp_biz_id = tmp_biz_detail[n]['biz_id']
                        for i in range(len(tmp_result_message)):
                            tmp_id = tmp_result_message[i]['id']
                            if tmp_id == tmp_biz_id:
                                list_result_return.append(tmp_result_message[i])
                    return jsonify({'result':'OK','messageText':list_result_return,'status_Code':200,'count':result_select['count'],'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':[],'status_Code':200,'count':result_select['count'],'messageER':{'message':result_select['messageText'],'data':[]}}),200

        else:
            return jsonify({'result':'ER','messageText':[],'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401

@status_methods.route('/api/v1/dashboard_admin/viewpaper_count',methods=['POST'])
def dashboard_admin_select_count():
    if  request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        if 'tax_id' in dataJson and 'document_type' in dataJson and len(dataJson) == 2 :
            tax_id = dataJson['tax_id']
            document_type = str(dataJson['document_type']).upper()
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                if level_admin == None :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found','data':[]}}),200
                elif int(level_admin) == 0 :
                    list_result = []
                    tmp_json = {}
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        month = executor.submit(select().select_admin_count_viewdoc_month, tax_id,document_type,level_admin)
                        day = executor.submit(select().select_admin_count_viewdoc_day_v2, tax_id,document_type,level_admin)
                        week = executor.submit(select().select_admin_count_viewdoc_week_v2, tax_id,document_type,level_admin)
                        hour = executor.submit(select().select_admin_count_viewdoc_hour_v2, tax_id,document_type,level_admin)
                        all_doc = executor.submit(select().select_admin_count_all, tax_id,document_type,level_admin)
                        return_month= month.result()
                        return_day = day.result()
                        return_week = week.result()
                        return_hour = hour.result()
                        return_all = all_doc.result()
                    tmp_2 = {}
                    tmp_2['message'] = return_all['messageText']
                    tmp_2['status'] = return_all['result']
                    tmp_json['all'] = tmp_2
                    tmp_2 = {}

                    tmp_2['message'] = return_month['messageText']
                    tmp_2['status'] = return_month['result']
                    tmp_json['month']= tmp_2
                    tmp_2 = {}

                    tmp_2['message'] = return_day['messageText']
                    tmp_2['status'] = return_day['result']
                    tmp_json['day'] = tmp_2
                    tmp_2 = {}

                    tmp_2['message'] = return_week['messageText']
                    tmp_2['status'] = return_week['result']
                    tmp_json['week'] = tmp_2
                    tmp_2 = {}

                    tmp_2['message'] = return_hour['messageText']
                    tmp_2['status'] = return_hour['result']
                    tmp_json['hour'] = tmp_2
                    tmp_2 = {}

                    list_result.append(tmp_json)
                    # if return_month['result'] == 'OK'  and return_week['result'] == 'OK' and return_hour['result'] == 'OK' and return_all['result'] == 'OK' and return_day['result'] == 'OK':
                    #     return jsonify({'result':'OK','messageText':list_result,'status_Code':200,'messageER':None}),200

                    if return_all['result'] == 'OK'  :
                        return jsonify({'result':'OK','messageText':list_result,'status_Code':200,'messageER':None}),200
                   
                    elif return_month['result'] == 'ER'  and return_week['result'] == 'ER' and return_hour['result'] == 'ER' and return_all['result'] == 'ER' and return_day['result'] == 'ER':
                        return jsonify({'result':'ER','messageText':list_result,'status_Code':200,'messageER':'error fetching data'}),200

                    else:
                        return jsonify({'result':'OK','messageText':list_result,'status_Code':200,'messageER':{'message':'some data is error','data':[]}}),200
                
                elif int(level_admin) == 1 :
                    tmp_json = {}
                    list_result = []
                    if tax_id == None or tax_id == "" :
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the biz_tax was not filled out.','data':[]}}),200
                    elif tax_id not in list_id_card_num:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the user is not in the business.','data':[]}}),200
                    else :
                        if len(tax_id) != 13:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because tax_id incorret','data':[]}}),200
                        elif len(tax_id) == 13:
                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                month = executor.submit(select().select_admin_count_viewdoc_month_v2, tax_id,document_type,level_admin)
                                day = executor.submit(select().select_admin_count_viewdoc_day_v2, tax_id,document_type,level_admin)
                                week = executor.submit(select().select_admin_count_viewdoc_week_v2, tax_id,document_type,level_admin)
                                hour = executor.submit(select().select_admin_count_viewdoc_hour_v2, tax_id,document_type,level_admin)
                                all_doc = executor.submit(select().select_admin_count_all, tax_id,document_type,level_admin)
                                return_month= month.result()
                                return_day = day.result()
                                return_week = week.result()
                                return_hour = hour.result()
                                return_all = all_doc.result()
                            tmp_2 = {}
                            tmp_2['message'] = return_all['messageText'][0]
                            tmp_2['status'] = return_all['result']
                            tmp_json['all'] = tmp_2
                            tmp_2 = {}

                            tmp_2['message'] = return_month['messageText']
                            tmp_2['status'] = return_month['result']
                            tmp_json['month']= tmp_2
                            tmp_2 = {}

                            tmp_2['message'] = return_day['messageText']
                            tmp_2['status'] = return_day['result']
                            tmp_json['day'] = tmp_2
                            tmp_2 = {}

                            tmp_2['message'] = return_week['messageText']
                            tmp_2['status'] = return_week['result']
                            tmp_json['week'] = tmp_2
                            tmp_2 = {}

                            tmp_2['message'] = return_hour['messageText']
                            tmp_2['status'] = return_hour['result']
                            tmp_json['hour'] = tmp_2
                            tmp_2 = {}

                            list_result.append(tmp_json)
                            if return_all['result'] == 'OK'  :
                                return jsonify({'result':'OK','messageText':list_result,'status_Code':200,'messageER':None}),200
                        
                            elif return_month['result'] == 'ER'  and return_week['result'] == 'ER' and return_hour['result'] == 'ER' and return_all['result'] == 'ER' and return_day['result'] == 'ER':
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error fetching data'}),200

                            else:
                                return jsonify({'result':'OK','messageText':list_result,'status_Code':200,'messageER':{'message':'some data is error','data':[]}}),200
                        
            else:
                return jsonify({'result':'OK','messageText':None,'status_Code':404,'messageER':'level admin incorret'}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorret'}),404

@status_methods.route('/api/v1/dashboard_admin/viewpaper',methods=['POST'])
def dashboard_admin_select_paper():
    if  request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            print ('username',username)
            print ('email',email)
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
            print ('list_id_card_num',list_id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        if 'datetimeStart' in dataJson and 'datetimeEnd' in dataJson and'tax_id' in dataJson and 'document_type' in dataJson and len(dataJson) == 4 :
            tax_id = dataJson['tax_id']
            document_type = str(dataJson['document_type']).upper()
            datetimeStart = dataJson['datetimeStart']
            datetimeEnd = dataJson['datetimeEnd']
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                if level_admin == None :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found','data':[]}}),200
                elif int(level_admin) == 0 :
                    print('biz_tax เป็นค่าว่างได้')
                    list_result = []
                    tmp_json = {}
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        result_paper = executor.submit(select().select_countpaper_datetime,tax_id,document_type,level_admin,datetimeStart,datetimeEnd)
                        return_result= result_paper.result()

                    if return_result['result'] == 'OK'  :
                        return jsonify({'result':'OK','messageText':return_result['messageText'],'status_Code':200,'messageER':None}),200

                    else:
                        return jsonify({'result':'ER','messageText':return_result['messageText'],'status_Code':200,'messageER':{'message':'some data is error','data':[]}}),200
                
                elif int(level_admin) == 1 :
                    print ('biz_tax ห้ามเป็นนค่าว่าง !!!')
                    tmp_json = {}
                    list_result = []
                    if tax_id == None or tax_id == "" :
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the biz_tax was not filled out.','data':[]}}),200
                    elif tax_id not in list_id_card_num:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the user is not in the business.','data':[]}}),200
                    else :
                        if len(tax_id) != 13:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because tax_id incorret','data':[]}}),200
                        elif len(tax_id) == 13:
                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                result_paper = executor.submit(select().select_countpaper_datetime,tax_id,document_type,level_admin,datetimeStart,datetimeEnd)
                                return_result= result_paper.result()
                           
                            if return_result['result'] == 'OK'  :
                                return jsonify({'result':'OK','messageText':return_result['messageText'],'status_Code':200,'messageER':None}),200

                            else:
                                return jsonify({'result':'ER','messageText':return_result['messageText'],'status_Code':200,'messageER':{'message':'some data is error','data':[]}}),200
                         
            else:
                return jsonify({'result':'OK','messageText':None,'status_Code':404,'messageER':'level admin incorret'}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorret'}),404

@status_methods.route('/api/v1/serv_temp/search',methods=['POST'])
def serv_temp_search_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'doc_id' in dataJson and len(dataJson) == 1:
            tmp_docid = dataJson['doc_id']
            result_select = select_1().select_doc_id_serviceother(tmp_docid)
            if result_select['result'] == 'OK':            
                return jsonify({'result':'OK','messageText':{'message':'succuess','data':result_select['messageText']},'status_Code':200,'messageER':None})
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':None}})

@status_methods.route('/api/v2/timeApprove_avg',methods=['POST'])
def timeApprove_avg_api_v2():
    if request.method == 'POST' :
        try:
            dataJson = request.json
            if 'doc_type' in dataJson and 'text_id' in dataJson and 'start_datetime' in dataJson and 'end_datetime' in dataJson and 'limit' in dataJson and dataJson['doc_type'] != "" and len(dataJson) == 5:
                doc_type =  dataJson['doc_type']
                text_id = dataJson['text_id']
                start_datetime = dataJson['start_datetime']
                end_datetime = dataJson['end_datetime']
                row_limit =  dataJson['limit']
                if row_limit == "":
                    row_limit = 1000
                result = select_1().select_report_avg_v2(doc_type, text_id, start_datetime, end_datetime, row_limit)                
                if result['result'] == 'OK':
                    ts = int(time.time())
                    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    st_filename = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S-')
                    path = path_global_1 + '/storage/excel_report/' + str(st) + '/'
                    path_indb = path_global_1 + '/storage/excel_report/' + str(st) + '/'
                    # path = './storage/excel_report/' + str(st) + '/'
                    # path_indb = '/storage/excel_report/' + str(st) + '/'
                    if not os.path.exists(path):
                        os.makedirs(path)
                    unique_filename = str(uuid.uuid4())
                    filename = 'report_paperless' + st_filename + unique_filename
                    data_excel = result['messageText']
                    row = 1
                    workbook = xlsxwriter.Workbook(path + filename + '.xlsx')
                    worksheet = workbook.add_worksheet()
                    format1 = workbook.add_format()
                    format1.set_align('center')
                    format1.set_align('vcenter')
                    format1.set_text_wrap()
                    format2 = workbook.add_format()
                    format2.set_align('left')
                    format2.set_text_wrap()
                    cell_format = workbook.add_format({'bold': True})
                    cell_format.set_align('center')
                    cell_format.set_align('vcenter')
                    cell_format.set_text_wrap()
                    cell_format.font_size = 12
                    worksheet.write('A1', 'ลำดับ',cell_format)
                    worksheet.write('B1', 'ประเภทเอกสาร',cell_format)
                    worksheet.write('C1', 'เลขประจำตัวผู้เสียภาษี',cell_format)
                    worksheet.write('D1', 'ชื่อผู้เซ็นเอกสาร',cell_format)
                    worksheet.write('E1', 'อีเมล์ผู้เซ็นเอกสาร',cell_format)
                    worksheet.write('F1', 'จำนวนการเซ็นเอกสาร',cell_format)
                    worksheet.write('G1', 'เวลาเฉลี่ยในการเซ็นเอกสาร',cell_format)
                    worksheet.write('H1', 'เวลาสูงสุดในการเซ็นเอกสาร',cell_format)
                    worksheet.write('I1', 'เวลาต่ำสุดในการเซ็นเอกสาร',cell_format)
                    worksheet.write('J1', 'หมายเหตุ',cell_format)
                    worksheet.set_column(0,0,7)
                    worksheet.set_column(1,2,14)
                    worksheet.set_column(3,4,20)
                    worksheet.set_column(5,5,13)
                    worksheet.set_column(6,8,26)
                    worksheet.set_column(9,9,15) 
                    if text_id == "":
                        text_id = 'None'                   
                    count = len(data_excel)
                    for num in range (0, count):
                        line = data_excel[num]
                        worksheet.write(row, 0, (num+1), format1)
                        worksheet.write(row, 1, doc_type,format1)
                        worksheet.write(row, 2, text_id,format1)
                        worksheet.write(row, 3, line['name'],format2)
                        worksheet.write(row, 4, line['onemail'],format2)
                        worksheet.write(row, 5, line['count_approve'],format1)
                        worksheet.write(row, 6, line['time_average'],format2)
                        worksheet.write(row, 7, line['time_max'],format2) 
                        worksheet.write(row, 8, line['time_min'],format2)
                        row += 1
                    workbook.close()
                    filename = filename + '.xlsx'
                    sha512encode_unifile = hashlib.sha512(str(unique_filename).encode('utf-8')).hexdigest()
                    # insert().insert_tran_excel_file_download_v1(path_indb,filename,sha512encode_unifile,tmp_username,str(dataJson))
                    web_download_file = myUrl_domain + 'api/v1/excel/download_file/' + sha512encode_unifile
                    return jsonify({'result':'OK','messageText':[{'download_excel_file':web_download_file,'token_download':sha512encode_unifile,'data':result['messageText']}],'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result['messageER']}),200          
            else:
                abort(404)
        except Exception as ex:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':str(ex)}),404
    else:
        abort(404)

@status_methods.route('/api/v1/today_transaction',methods=['GET'])
def today_transaction_api_v1():
    if request.method == 'GET':
        try:
            if 'Authorization' not in request.headers:
                abort(401)
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                abort(401)
        except KeyError as ex:
            return redirect(url_paperless)
        result_verify = token_required_func(token_header)
        if result_verify['result'] != 'OK':
            abort(401)
        try:
            resultjson = []
            list_id_card_num = []
            arr_list_taxid_sum = []
            username = result_verify['username']
            email = result_verify['email']
            citizen_data = eval(result_verify['citizen_data'])
            biz_detail = citizen_data['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
            result_level = select().select_level_admin_v1(username,email)
            result_level_eval = eval(str(result_level))
            if result_level_eval['result'] == 'OK':
                tmpdataleveladmin = result_level_eval['messageText']['level_admin']
                if tmpdataleveladmin == '0':
                    result_taxid = select_admin_3().select_taxid_admin_v1()
                    if result_taxid['result'] == 'OK':
                        tmpmessagedata = result_taxid['messageText']
                        data_tax = select_admin_3().select_data_admin_bizpaperless_v1()
                        if data_tax['result'] == 'OK':
                            datatax = data_tax['messageText'] 
                        for g in range(len(tmpmessagedata)):
                            tmptaxidall = tmpmessagedata[g]['bizTax']
                            countalltax = select_admin_3().select_stepdata_admin_all_v1(tmptaxidall)
                            if countalltax['result'] == 'OK':
                                arr_list_taxid_sum.append(countalltax['messageText'][0])
                        result_data = select_admin_3().select_stepdata_admin_v1(tmptaxidall)
                        # result_data['result'] = 'ER'                        
                        if result_data['result'] == 'OK':
                            tmpdata_tocount = result_data['messageText']
                            for i in range(len(tmpmessagedata)):
                                tmpdata = tmpmessagedata[i]
                                biztax = tmpmessagedata[i]['bizTax']
                                transactionMax = 0
                                transactionNow = 0
                                storageNow = 0
                                storageMax = 0
                                test = 0
                                tmpjson = {
                                    'tax_id':'',
                                    'count_today':0
                                }
                                if tmpdata != None:
                                    tmpdata = (tmpdata)
                                tempbizInfoJson = eval(tmpdata['bizInfoJson'])
                                tmpfirst_name_eng = tempbizInfoJson['first_name_eng']
                                tmpfirst_name_th = tempbizInfoJson['first_name_th']
                                for x in range(len(arr_list_taxid_sum)):
                                    if 'tax_id' in arr_list_taxid_sum[x]:
                                        if tmpmessagedata[i]['bizTax'] == arr_list_taxid_sum[x]['tax_id']:
                                            tmpjson['count_all'] = arr_list_taxid_sum[x]['count']
                                for x in range(len(datatax)):
                                    if tmpmessagedata[i]['bizTax'] == datatax[x]['tax_id']:
                                        if datatax[x]['transactionMax'] != null and datatax[x]['transactionMax'] != '':
                                            transactionMax = datatax[x]['transactionMax']  
                                        if datatax[x]['transactionNow'] != null and datatax[x]['transactionNow'] != '':
                                            transactionNow = datatax[x]['transactionNow']                                               
                                        if datatax[x]['storageNow'] != null and datatax[x]['storageNow'] != '':
                                            storageNow = datatax[x]['storageNow']                                                
                                        if datatax[x]['storageMax'] != null and datatax[x]['storageMax'] != '':
                                            storageMax = datatax[x]['storageMax']                                                 
                                for y in range(len(tmpdata_tocount)):                                                                       
                                    if tmpmessagedata[i]['bizTax'] in tmpdata_tocount[y]['biz_info']:
                                        tmpjson['count_today'] += 1
                                tmpjson['business_data'] = {
                                    'first_name_eng':tmpfirst_name_eng,
                                    'first_name_th':tmpfirst_name_th
                                }
                                tmpjson['tax_id'] = biztax
                                tmpjson['transactionMax'] = transactionMax
                                tmpjson['transactionNow'] = transactionNow
                                tmpjson['storageNow'] = storageNow
                                tmpjson['storageMax'] = storageMax
                                resultjson.append(tmpjson)
                            list_arr = sorted(resultjson, key=lambda k: k['count_today'], reverse=True)
                            print(len(list_arr))
                            return jsonify({'result':'OK','messageText':{'data':list_arr,'message':'success'},'messageER':None,'status_Code':200}),200
                        else:     
                            for i in range(len(tmpmessagedata)):
                                tmpdata = tmpmessagedata[i]
                                biztax = tmpmessagedata[i]['bizTax']   
                                transactionMax = 0
                                transactionNow = 0
                                storageNow = 0
                                storageMax = 0        
                                tmpjson = {
                                    'tax_id':'',
                                    'count_today':0
                                }
                                if tmpdata != None:
                                    tmpdata = (tmpdata)
                                for x in range(len(arr_list_taxid_sum)):
                                    if 'tax_id' in arr_list_taxid_sum[x]:
                                        if tmpmessagedata[i]['bizTax'] == arr_list_taxid_sum[x]['tax_id']:
                                            tmpjson['count_all'] = arr_list_taxid_sum[x]['count']
                                for x in range(len(datatax)):
                                    if tmpmessagedata[i]['bizTax'] == datatax[x]['tax_id']:
                                        if datatax[x]['transactionMax'] != null and datatax[x]['transactionMax'] != '':
                                            transactionMax = datatax[x]['transactionMax']  
                                        if datatax[x]['transactionNow'] != null and datatax[x]['transactionNow'] != '':
                                            transactionNow = datatax[x]['transactionNow']                                               
                                        if datatax[x]['storageNow'] != null and datatax[x]['storageNow'] != '':
                                            storageNow = datatax[x]['storageNow']                                                
                                        if datatax[x]['storageMax'] != null and datatax[x]['storageMax'] != '':
                                            storageMax = datatax[x]['storageMax']   
                                tempbizInfoJson = eval(tmpdata['bizInfoJson'])
                                tmpfirst_name_eng = tempbizInfoJson['first_name_eng']
                                tmpfirst_name_th = tempbizInfoJson['first_name_th']
                                tmpjson['business_data'] = {
                                    'first_name_eng':tmpfirst_name_eng,
                                    'first_name_th':tmpfirst_name_th
                                }
                                tmpjson['tax_id'] = biztax
                                tmpjson['count_today'] = 0
                                tmpjson['transactionMax'] = transactionMax
                                tmpjson['transactionNow'] = transactionNow
                                tmpjson['storageNow'] = storageNow
                                tmpjson['storageMax'] = storageMax
                                resultjson.append(tmpjson)
                            list_arr = sorted(resultjson, key=lambda k: k['count_today'], reverse=True)
                            return jsonify({'result':'OK','messageText':{'data':list_arr,'message':'success'},'messageER':None,'status_Code':200}),200
                        return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'data not found'},'status_Code':200}),200
                else:
                    abort(401)
        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':{'data':str(e),'message':'error'},'status_Code':200}),200

@status_methods.route('/api/v1/register/setting/theme',methods=['POST'])
def setting_theme():
    list_id_card_num = []
    if request.method == 'POST':
        dataForm = request.form
        dataFile = request.files
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized','status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
            print('list_id_card_num',list_id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)}),401
        if 'tax_id' in dataForm and 'color' in dataForm:
            tmp_tax_id = dataForm['tax_id']
            color = dataForm['color']
            img_logo = dataFile['img_logo']
            if tmp_tax_id in list_id_card_num :
                result_update = update_1().update_setting(tmp_tax_id,color,img_logo)
                if result_update['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':result_update['messageText'],'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':tmp_tax_id +' update fail ' + result_update['messageText']}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'user not in business'+str(tmp_tax_id)}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrect'}),404

@status_methods.route('/api/v1/business/setting_config',methods=['POST','GET'])
def business_setting_api_v1():
    list_id_card_num = []
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                abort(401)
        except KeyError as ex:
            abort(404)
        # token_header = 'Bearer ' + token_header
        result_verify = token_required_func(token_header)
        if result_verify['result'] != 'OK':
            abort(401)
        data_from_result_eval = result_verify
        username = data_from_result_eval['username']
        email = data_from_result_eval['email']
        biz_detail = eval(data_from_result_eval['biz_info'])
        biz_detail = biz_detail['biz_detail']
        for x in range(len(biz_detail)):
            getbiz = biz_detail[x]['getbiz']
            for i in range (len(getbiz)):
                id_card_num = getbiz[i]['id_card_num']
                list_id_card_num.append(id_card_num)
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        list_result_return = []
        if result_verify['result'] == 'OK':
            level_admin = result_level_eval['messageText']['level_admin']
            level_admin = int(level_admin)
            if level_admin == None :
                abort(401)
            elif int(level_admin) == 0:
                dataForm = request.form
                dataFile = request.files
                if 'tax_id' in dataForm and 'color' in dataForm and 'transactionMax' in dataForm and 'storageMax' in dataForm and 'status' in dataForm:
                    tmp_tax_id = dataForm['tax_id']
                    color = dataForm['color']
                    img_logo = dataFile['img_logo']
                    transactionMax = int(dataForm['transactionMax'])
                    storageMax = int(dataForm['storageMax'])
                    status = True
                    if dataForm['status'] == 'false':
                        status = False
                    if tmp_tax_id in list_id_card_num :
                        result_update = update_1().update_business_setting_v2(level_admin,tmp_tax_id,color,img_logo,status,transactionMax,storageMax)
                        if result_update['result'] == 'OK':
                            return jsonify({'result':'OK','messageText':result_update['messageText'],'status_Code':200,'messageER':None}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':tmp_tax_id +' update fail ' + result_update['messageText']}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'user not in business '+str(tmp_tax_id)}),200
                else:
                    abort(404)
            elif int(level_admin) == 1:
                dataForm = request.form
                dataFile = request.files
                if 'tax_id' in dataForm and 'color' in dataForm:
                    tmp_tax_id = dataForm['tax_id']
                    color = dataForm['color']
                    img_logo = dataFile['img_logo']
                    if tmp_tax_id in list_id_card_num :
                        result_update = update_1().update_business_setting_v2(level_admin,tmp_tax_id,color,img_logo,None,None,None)
                        if result_update['result'] == 'OK':
                            return jsonify({'result':'OK','messageText':result_update['messageText'],'status_Code':200,'messageER':None}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':tmp_tax_id +' update fail ' + result_update['messageText']}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'user not in business '+str(tmp_tax_id)}),200
                else:
                    abort(404)
    elif request.method == 'GET':
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                abort(401)
        except KeyError as ex:
            abort(404)
        # token_header = 'Bearer ' + token_header
        result_verify = token_required_func(token_header)
        if result_verify['result'] != 'OK':
            abort(401)
        data_from_result_eval = result_verify
        username = data_from_result_eval['username']
        email = data_from_result_eval['email']
        biz_detail = eval(data_from_result_eval['biz_info'])
        biz_detail = biz_detail['biz_detail']
        for x in range(len(biz_detail)):
            getbiz = biz_detail[x]['getbiz']
            for i in range (len(getbiz)):
                id_card_num = getbiz[i]['id_card_num']
                list_id_card_num.append(id_card_num)
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        list_result_return = []
        tmptax_id = None
        if result_verify['result'] == 'OK':
            level_admin = result_level_eval['messageText']['level_admin']
            level_admin = int(level_admin)
            tax_id = request.args.get('tax_id')
            if tax_id == None:
                abort(404)
            if level_admin == None:
                abort(401)
            elif level_admin == 0:
                tmptax_id = tax_id
            elif level_admin == 1:
                if tax_id in list_id_card_num:
                    tmptax_id = tax_id
        else:
            abort(401)
        if tax_id != None:
            result_select = select_admin_3().select_show_businessConfig_v1(level_admin,tax_id)
            if result_select['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'data':result_select['messageText'],'message':'success'},'messageER':None,'status_Code':200})
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'fail'},'status_Code':200})
        else:
            abort(401)

@status_methods.route('/api/v2/dashboard_admin/document',methods=['POST'])
def dashboard_admin_document_v2():
    if request.method == 'POST':
        username = None
        email = None
        level_admin = None
        id_user = None
        getbiz = None
        id_card_num = None
        list_id_card_num = []
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            # print('result_verify : ',result_verify['messageText'].text)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            # print ('result_verify',data_from_result_eval)
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            id_user = data_from_result_eval['id']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        tax = None
        if 'datetimeStart' in dataJson and 'datetimeEnd' in dataJson and 'document_id' in dataJson and 'sender_email' in dataJson and 'recipient_email' in dataJson and 'tax_id' in dataJson and 'documentType' in dataJson and  'limit' in dataJson and 'offset' in dataJson:
            tax = dataJson['tax_id']
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                try:
                    if level_admin == None:
                        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'level_admin not found'}),200
                    elif int(level_admin) == 0 :
                        datetime_start = dataJson['datetimeStart']
                        datetime_end = dataJson['datetimeEnd']
                        document_id = dataJson['document_id']
                        sender_email = dataJson['sender_email']
                        recipient_email = dataJson['recipient_email']
                        tax_id = dataJson['tax_id']
                        documentType = dataJson['documentType']
                        limit = dataJson['limit']
                        offset = dataJson['offset']
                        if 'text' in dataJson:
                            tmp_text = dataJson['text']
                        else:
                            tmp_text = ''
                        result_select = select_1().select_document_v3(datetime_start,datetime_end,document_id,sender_email,recipient_email,tax_id,documentType,limit,offset,tmp_text)
                        if result_select['result'] == 'OK':
                            return jsonify({'result':'OK','result_lasttime' : result_select['last_time'] ,'messageText':result_select['messageText'],'status_Code':200,'messageER':None}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200
                    elif int(level_admin) == 1 :
                        if tax == None or tax == "":
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the tax_id was not filled out.','data':[]}}),200
                        elif tax not in list_id_card_num:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the user is not in the business.','data':[]}}),200
                        else:
                            if len(tax) != 13:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'data not found','data':[]}}),200
                            else:
                                datetime_start = dataJson['datetimeStart']
                                datetime_end = dataJson['datetimeEnd']
                                document_id = dataJson['document_id']
                                sender_email = dataJson['sender_email']
                                recipient_email = dataJson['recipient_email']
                                tax_id = dataJson['tax_id']
                                documentType = dataJson['documentType']
                                limit = dataJson['limit']
                                offset = dataJson['offset']
                                if 'text' in dataJson:
                                    tmp_text = dataJson['text']
                                else:
                                    tmp_text = ''
                                result_select = select_1().select_document_v3(datetime_start,datetime_end,document_id,sender_email,recipient_email,tax_id,documentType,limit,offset,tmp_text)
                                if result_select['result'] == 'OK':
                                    return jsonify({'result':'OK','result_lasttime' : result_select['last_time'] ,'messageText':result_select['messageText'],'status_Code':200,'messageER':None}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200
                except Exception as e:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':str(e),'data':[]}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':[]}}),404

@status_methods.route('/api/v2/dashboard_admin/count_search_document',methods=['POST'])
def count_search_document_v2():
    if request.method == 'POST':
        username = None
        email = None
        level_admin = None
        id_user = None
        getbiz = None
        id_card_num = None
        list_id_card_num = []
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            # print('result_verify : ',result_verify['messageText'].text)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            # print ('result_verify',data_from_result_eval)
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            id_user = data_from_result_eval['id']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        tax = None
        if 'datetimeStart' in dataJson and 'datetimeEnd' in dataJson and 'document_id' in dataJson and 'sender_email' in dataJson and 'recipient_email' in dataJson and 'tax_id' in dataJson and 'documentType' in dataJson:
            tax = dataJson['tax_id']
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                try:
                    if level_admin == None:
                        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'level_admin not found'}),200
                    elif int(level_admin) == 0 :
                        datetime_start = dataJson['datetimeStart']
                        datetime_end = dataJson['datetimeEnd']
                        document_id = dataJson['document_id']
                        sender_email = dataJson['sender_email']
                        recipient_email = dataJson['recipient_email']
                        tax_id = dataJson['tax_id']
                        documentType = dataJson['documentType']
                        if 'text' in dataJson:
                            tmp_text = dataJson['text']
                        else:
                            tmp_text = ''
                        result_select = select().count_search_admin_document_v2(datetime_start,datetime_end,document_id,sender_email,recipient_email,tax_id,documentType,tmp_text)
                        if result_select['result'] == 'OK':
                            return jsonify({'result':'OK','messageText':{'count':result_select['messageText']},'status_Code':200,'messageER':None}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200
                    elif int(level_admin) == 1 :
                        if tax == None or tax == "":
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the tax_id was not filled out.','data':[]}}),200
                        elif tax not in list_id_card_num:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the user is not in the business.','data':[]}}),200
                        else:
                            if len(tax) != 13:
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'data not found','data':[]}}),200
                            else:
                                datetime_start = dataJson['datetimeStart']
                                datetime_end = dataJson['datetimeEnd']
                                document_id = dataJson['document_id']
                                sender_email = dataJson['sender_email']
                                recipient_email = dataJson['recipient_email']
                                tax_id = dataJson['tax_id']
                                documentType = dataJson['documentType']
                                if 'text' in dataJson:
                                    tmp_text = dataJson['text']
                                else:
                                    tmp_text = ''
                                result_select = select().count_search_admin_document_v2(datetime_start,datetime_end,document_id,sender_email,recipient_email,tax_id,documentType,tmp_text)
                                if result_select['result'] == 'OK':
                                    return jsonify({'result':'OK','messageText':{'count':result_select['messageText']},'status_Code':200,'messageER':None}),200
                                else:
                                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200
                except Exception as e:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':str(e),'data':[]}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':[]}}),404

@status_methods.route('/api/v1/dashboard_admin/search_document',methods=['POST'])
def search_document_v1():
    if request.method == 'POST':
        username = None
        email = None
        level_admin = None
        id_user = None
        getbiz = None
        id_card_num = None
        list_id_card_num = []
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            # print('result_verify : ',result_verify['messageText'].text)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            # print ('result_verify',data_from_result_eval)
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            id_user = data_from_result_eval['id']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        tax = None
        if 'key' in dataJson and 'email' in dataJson and 'limit' in dataJson and 'offset' in dataJson and len(dataJson) == 4: 
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                try:
                    if level_admin == None:
                        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'level_admin not found'}),200
                    elif int(level_admin) == 0 :
                        key = dataJson['key']
                        email = dataJson['email']
                        limit = dataJson['limit']
                        offset = dataJson['offset']
                        result_select = select_1().search_admin_document(key,email,limit,offset)

                        if result_select['result'] == 'OK':
                            return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':None}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200
                        
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':str(e),'data':[]}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':[]}}),404

@status_methods.route('/api/v1/dashboard_admin/count_search_document',methods=['POST'])
def count_search_document_v1():
    if request.method == 'POST':
        username = None
        email = None
        level_admin = None
        id_user = None
        getbiz = None
        id_card_num = None
        list_id_card_num = []
        try:
            token_header = request.headers['Authorization']
            try:
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            # print('result_verify : ',result_verify['messageText'].text)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            # print ('result_verify',data_from_result_eval)
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            id_user = data_from_result_eval['id']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        tax = None
        if 'key' in dataJson and 'email' in dataJson and len(dataJson) == 2: 
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                try:
                    if level_admin == None:
                        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'level_admin not found'}),200
                    elif int(level_admin) == 0 :
                        key = dataJson['key']
                        email = dataJson['email']
                        result_select = select_1().count_search_admin_document(key,email)
                        print (result_select)
                        if result_select['result'] == 'OK':
                            return jsonify({'result':'OK','messageText':{'count':result_select['messageText']},'status_Code':200,'messageER':None}),200
                        else:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':result_select['messageText'],'data':[]}}),200
                        
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':str(e),'data':[]}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':[]}}),404

@status_methods.route('/api/v1/dashboard_admin/viewpaper/datetime',methods=['POST'])
def dashboard_admin_select_count_datetime_2():
    if  request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            print ('username',username)
            print ('email',email)
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
            print ('list_id_card_num',list_id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        if 'datetimeStart' in dataJson and 'datetimeEnd' in dataJson and'tax_id' in dataJson and 'document_type' in dataJson and len(dataJson) == 4 :
            tax_id = dataJson['tax_id']
            document_type = str(dataJson['document_type']).upper()
            datetimeStart = dataJson['datetimeStart']
            datetimeEnd = dataJson['datetimeEnd']
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                if level_admin == None :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found','data':[]}}),200
                elif int(level_admin) == 0 :
                    print('biz_tax เป็นค่าว่างได้')
                    list_result = []
                    tmp_json = {}
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        result_paper = executor.submit(select_1().select_countpaper_datetime,tax_id,document_type,level_admin,datetimeStart,datetimeEnd)
                        return_result= result_paper.result()

                    if return_result['result'] == 'OK'  :
                        return jsonify({'result':'OK','messageText':return_result['messageText'],'status_Code':200,'messageER':None}),200

                    else:
                        return jsonify({'result':'ER','messageText':return_result['messageText'],'status_Code':200,'messageER':{'message':'some data is error','data':[]}}),200
                
                elif int(level_admin) == 1 :
                    print ('biz_tax ห้ามเป็นนค่าว่าง !!!')
                    tmp_json = {}
                    list_result = []
                    if tax_id == None or tax_id == "" :
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the biz_tax was not filled out.','data':[]}}),200
                    elif tax_id not in list_id_card_num:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the user is not in the business.','data':[]}}),200
                    else :
                        if len(tax_id) != 13:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because tax_id incorret','data':[]}}),200
                        elif len(tax_id) == 13:
                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                result_paper = executor.submit(select().select_countpaper_datetime,tax_id,document_type,level_admin,datetimeStart,datetimeEnd)
                                return_result= result_paper.result()
                           
                            if return_result['result'] == 'OK'  :
                                return jsonify({'result':'OK','messageText':return_result['messageText'],'status_Code':200,'messageER':None}),200

                            else:
                                return jsonify({'result':'ER','messageText':return_result['messageText'],'status_Code':200,'messageER':{'message':'some data is error','data':[]}}),200
                         
            else:
                return jsonify({'result':'OK','messageText':None,'status_Code':404,'messageER':'level admin incorret'}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorret'}),404

@status_methods.route('/api/v1/dashboard_admin/viewpaper/datetime/report',methods=['POST'])
def dashboard_admin_select_paper_back_datetime():
    if  request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            print ('username',username)
            print ('email',email)
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
            print ('list_id_card_num',list_id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        print(result_level_eval)
        dataJson = request.json
        if 'datetimeStart' in dataJson and 'datetimeEnd' in dataJson and'tax_id' in dataJson and 'document_type' in dataJson and len(dataJson) == 4 :
            tax_id = dataJson['tax_id']
            document_type = str(dataJson['document_type']).upper()
            datetimeStart = dataJson['datetimeStart']
            datetimeEnd = dataJson['datetimeEnd']
            if result_level_eval['result'] == 'OK':
                list_result, tmp_json = [], {}
                level_admin = result_level_eval['messageText']['level_admin']
                print(level_admin)
                if level_admin == None :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found','data':[]}}),200
                elif int(level_admin) == 0 :
                    print('biz_tax เป็นค่าว่างได้')
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        result_paper = executor.submit(select_1().select_countpaper_datetime,tax_id,document_type,level_admin,datetimeStart,datetimeEnd)
                        return_result= result_paper.result()
                
                elif int(level_admin) == 1 :
                    print ('biz_tax ห้ามเป็นนค่าว่าง !!!')
                    if tax_id == None or tax_id == "" :
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the biz_tax was not filled out.','data':[]}}),200
                    elif tax_id not in list_id_card_num:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the user is not in the business.','data':[]}}),200
                    else :
                        if len(tax_id) != 13:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because tax_id incorret','data':[]}}),200
                        elif len(tax_id) == 13:
                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                result_paper = executor.submit(select().select_countpaper_datetime,tax_id,document_type,level_admin,datetimeStart,datetimeEnd)
                                return_result= result_paper.result()
                           
                if return_result['result'] == 'OK'  :  
                    data_excel = return_result['messageText']
                    data_excel = data_excel['documents'][0]  
                    list_user = data_excel['list_user'] 

                    ts = int(time.time())
                    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    st_filename = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S-')
                    path = path_global_1 + '/storage/excel_report/' + str(st) + '/'
                    path_indb = path_global_1 + '/storage/excel_report/' + str(st) + '/'
                    # path = './storage/excel_report/' + str(st) + '/'
                    # path_indb = '/storage/excel_report/' + str(st) + '/'
                    if not os.path.exists(path):
                        os.makedirs(path)
                    unique_filename = str(uuid.uuid4())
                    filename = 'report_paperless' + st_filename + unique_filename
                    row = 7
                    workbook = xlsxwriter.Workbook(path + filename + '.xlsx')
                    worksheet = workbook.add_worksheet()
                    format1 = workbook.add_format()
                    format1.set_align('center')
                    format1.set_align('vcenter')
                    format1.set_text_wrap()
                    format2 = workbook.add_format()
                    format2.set_align('left')
                    format2.set_text_wrap()
                    cell_format = workbook.add_format({'bold': True})
                    cell_format.set_align('center')
                    cell_format.set_align('vcenter')
                    cell_format.set_text_wrap()
                    cell_format.font_size = 12
                    if document_type == "":
                        worksheet.write('B3', 'ทั้งหมด',format1)
                    else:
                        worksheet.write('B3', document_type,format1)
                    if tax_id == "":
                        worksheet.write('D3', 'ทั้งหมด',format1)
                    else:
                        worksheet.write('D3', tax_id,format1)
                    worksheet.write('A3', 'ประเภทเอกสาร',cell_format)                    
                    worksheet.write('C3', 'หมายเลขเอกสาร',cell_format)                  
                    worksheet.write('A4', 'เอกสารที่อยู่ในระบบ',cell_format)
                    worksheet.write('B4', 'เอกสารที่ถูกยกเลิก',cell_format)
                    worksheet.write('C4', 'ผู้ส่งเอกสาร',cell_format)
                    worksheet.write('D4', 'เอกสารกำลังดำเนินการ',cell_format)
                    worksheet.write('E4', 'เอกสารรอดำเนินการ',cell_format)
                    worksheet.write('F4', 'เอกสารอนุมัติแล้ว',cell_format)
                    worksheet.write('G4', 'เอกสารรออนุมัติ',cell_format)
                    worksheet.write('H4', 'เอกสารปฎิเสธอนุมัติ',cell_format)
                    worksheet.write('A5', data_excel['documents_active'],format1)
                    worksheet.write('B5', data_excel['documents_reject'],format1)
                    worksheet.write('C5', data_excel['count_user'],format1)
                    worksheet.write('D5', data_excel['doc_N'],format1)
                    worksheet.write('E5', data_excel['doc_none'],format1)
                    worksheet.write('F5', data_excel['doc_Y'],format1)
                    worksheet.write('G5', data_excel['doc_W'],format1)
                    worksheet.write('H5', data_excel['doc_R'],format1)
                    worksheet.merge_range('C2:E2', 'รายงานสรุปสถานะเอกสารทั้งหมด',cell_format)
                    worksheet.merge_range('A6:C6', 'อีเมล์ผู้ส่งเอกสาร',cell_format)
                    worksheet.write('A7', 'ลำดับ',cell_format)
                    worksheet.write('B7', 'อีเมล์',cell_format)
                    worksheet.write('C7', 'จำนวนเอกสาร',cell_format)                    
                    worksheet.set_column(0,2,18)
                    worksheet.set_column(1,1,24)
                    worksheet.set_column(3,3,22)
                    worksheet.set_column(4,7,19)
                    for num in range (len(list_user)):
                        line = list_user[num]
                        worksheet.write(row, 0, (num+1), format1)
                        worksheet.write(row, 1, line['email'],format2)
                        worksheet.write(row, 2, line['count'],format1)
                        row += 1
                    workbook.close()
                    filename = filename + '.xlsx'
                    sha512encode_unifile = hashlib.sha512(str(unique_filename).encode('utf-8')).hexdigest()
                    web_download_file = myUrl_domain + 'api/v1/excel/download_file/' + sha512encode_unifile                   
                    return jsonify({'result':'OK','messageText':return_result['messageText'],'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':return_result['messageText'],'status_Code':200,'messageER':{'message':'some data is error','data':[]}}),200                         
            else:
                return jsonify({'result':'OK','messageText':None,'status_Code':404,'messageER':'level admin incorret'}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorret'}),404

@status_methods.route('/api/v1/dashboard_admin/viewpaper/back/count',methods=['POST'])
def dashboard_admin_select_count_back_2():
    if  request.method == 'POST':
        username = None
        email = None
        level_admin = None
        list_id_card_num = []
        getbiz = None
        id_card_num = None
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        if 'tax_id' in dataJson and 'document_type' in dataJson and len(dataJson) == 2 :
            tax_id = dataJson['tax_id']
            document_type = str(dataJson['document_type']).upper()
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
                if level_admin == None :
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found','data':[]}}),200
                elif int(level_admin) == 0 :
                    list_result = []
                    tmp_json = {}
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        month = executor.submit(select_1().select_admin_count_viewdoc_month_v2, tax_id,document_type,level_admin)
                        day = executor.submit(select_1().select_admin_count_viewdoc_day_v2, tax_id,document_type,level_admin)
                        week = executor.submit(select_1().select_admin_count_viewdoc_week_v2, tax_id,document_type,level_admin)
                        hour = executor.submit(select_1().select_admin_count_viewdoc_hour_v2, tax_id,document_type,level_admin)
                        all_doc = executor.submit(select_1().select_admin_count_all, tax_id,document_type,level_admin)
                        return_month= month.result()
                        return_day = day.result()
                        return_week = week.result()
                        return_hour = hour.result()
                        return_all = all_doc.result()
                    tmp_2 = {}
                    tmp_2['message'] = return_all['messageText']
                    tmp_2['status'] = return_all['result']
                    tmp_json['all'] = tmp_2
                    tmp_2 = {}

                    tmp_2['message'] = return_month['messageText']
                    tmp_2['status'] = return_month['result']
                    tmp_json['month']= tmp_2
                    tmp_2 = {}

                    tmp_2['message'] = return_day['messageText']
                    tmp_2['status'] = return_day['result']
                    tmp_json['day'] = tmp_2
                    tmp_2 = {}

                    tmp_2['message'] = return_week['messageText']
                    tmp_2['status'] = return_week['result']
                    tmp_json['week'] = tmp_2
                    tmp_2 = {}

                    tmp_2['message'] = return_hour['messageText']
                    tmp_2['status'] = return_hour['result']
                    tmp_json['hour'] = tmp_2
                    tmp_2 = {}

                    list_result.append(tmp_json)
                    # if return_month['result'] == 'OK'  and return_week['result'] == 'OK' and return_hour['result'] == 'OK' and return_all['result'] == 'OK' and return_day['result'] == 'OK':
                    #     return jsonify({'result':'OK','messageText':list_result,'status_Code':200,'messageER':None}),200

                    if return_all['result'] == 'OK'  :
                        return jsonify({'result':'OK','messageText':list_result,'status_Code':200,'messageER':None}),200
                   
                    elif return_month['result'] == 'ER'  and return_week['result'] == 'ER' and return_hour['result'] == 'ER' and return_all['result'] == 'ER' and return_day['result'] == 'ER':
                        return jsonify({'result':'ER','messageText':list_result,'status_Code':200,'messageER':'error fetching data'}),200

                    else:
                        return jsonify({'result':'OK','messageText':list_result,'status_Code':200,'messageER':{'message':'some data is error','data':[]}}),200
                
                elif int(level_admin) == 1 :
                    tmp_json = {}
                    list_result = []
                    if tax_id == None or tax_id == "" :
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the biz_tax was not filled out.','data':[]}}),200
                    elif tax_id not in list_id_card_num:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because the user is not in the business.','data':[]}}),200
                    else :
                        if len(tax_id) != 13:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'error because tax_id incorret','data':[]}}),200
                        elif len(tax_id) == 13:
                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                month = executor.submit(select_1().select_admin_count_viewdoc_month_v2, tax_id,document_type,level_admin)
                                day = executor.submit(select_1().select_admin_count_viewdoc_day_v2, tax_id,document_type,level_admin)
                                week = executor.submit(select_1().select_admin_count_viewdoc_week_v2, tax_id,document_type,level_admin)
                                hour = executor.submit(select_1().select_admin_count_viewdoc_hour_v2, tax_id,document_type,level_admin)
                                all_doc = executor.submit(select_1().select_admin_count_all, tax_id,document_type,level_admin)
                                return_month= month.result()
                                return_day = day.result()
                                return_week = week.result()
                                return_hour = hour.result()
                                return_all = all_doc.result()
                            tmp_2 = {}
                            tmp_2['message'] = return_all['messageText'][0]
                            tmp_2['status'] = return_all['result']
                            tmp_json['all'] = tmp_2
                            tmp_2 = {}

                            tmp_2['message'] = return_month['messageText']
                            tmp_2['status'] = return_month['result']
                            tmp_json['month']= tmp_2
                            tmp_2 = {}

                            tmp_2['message'] = return_day['messageText']
                            tmp_2['status'] = return_day['result']
                            tmp_json['day'] = tmp_2
                            tmp_2 = {}

                            tmp_2['message'] = return_week['messageText']
                            tmp_2['status'] = return_week['result']
                            tmp_json['week'] = tmp_2
                            tmp_2 = {}

                            tmp_2['message'] = return_hour['messageText']
                            tmp_2['status'] = return_hour['result']
                            tmp_json['hour'] = tmp_2
                            tmp_2 = {}

                            list_result.append(tmp_json)
                            if return_all['result'] == 'OK'  :
                                return jsonify({'result':'OK','messageText':list_result,'status_Code':200,'messageER':None}),200
                        
                            elif return_month['result'] == 'ER'  and return_week['result'] == 'ER' and return_hour['result'] == 'ER' and return_all['result'] == 'ER' and return_day['result'] == 'ER':
                                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'error fetching data'}),200

                            else:
                                return jsonify({'result':'OK','messageText':list_result,'status_Code':200,'messageER':{'message':'some data is error','data':[]}}),200
                        
            else:
                return jsonify({'result':'OK','messageText':None,'status_Code':404,'messageER':'level admin incorret'}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorret'}),404

@status_methods.route('/api/v1/dashboard_admin/edit_config',methods=['PUT'])
def dashboard_amdin_edit_config_api_v1():
    if  request.method == 'PUT':
        list_id_card_num = []
        try:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')[1]
            except Exception as ex:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
        except KeyError as ex:
            return redirect(url_paperless)
        try:
            token_header = 'Bearer ' + token_header
            result_verify = verify().verify_one_id(token_header)
            if result_verify['result'] != 'OK':
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized','data':[]},'status_Code':401}),401
            data_from_result = result_verify['messageText'].text
            data_from_result_eval = eval(str(result_verify['messageText'].text))
            username = data_from_result_eval['username']
            email = data_from_result_eval['thai_email']
            biz_detail = data_from_result_eval['biz_detail']
            for x in range(len(biz_detail)):
                getbiz = biz_detail[x]['getbiz']
                for i in range (len(getbiz)):
                    id_card_num = getbiz[i]['id_card_num']
                    list_id_card_num.append(id_card_num)
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'Unauthorized' + str(e),'data':[]},'status_Code':401}),401
        result_level = select().select_level_admin_v1(username,email)
        result_level_eval = eval(str(result_level))
        dataJson = request.json
        if 'tax_id' in dataJson and 'json_config' in dataJson:
            tmptax_id = dataJson['tax_id']
            tmp_json_config = dataJson['json_config']
            if result_level_eval['result'] == 'OK':
                level_admin = result_level_eval['messageText']['level_admin']
            if level_admin == None :
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'level_admin not found','data':[]}}),200
            elif int(level_admin) == 0 :
                r = update_5().update_Configservice_business(tmp_json_config,tmptax_id)
                return jsonify(r)
# @status_methods.route('/api/v1/secret/genarate',methods=['POST'])
# def genarate_secret_v1():
#     if request.method == 'POST':
#         dataJson = request.json
#         if 'serviceName' not in dataJson:
#             abort(404)
#         keyPair = RSA.generate(3072)
#         tmpserviceName = dataJson['serviceName']
#         resultKey = genarate_secretkey(tmpserviceName)
#         # tmpkey = resultKey['key_process']
#         # print(tmpkey)
#         # decryptor = PKCS1_OAEP.new(keyPair)
#         # decrypted = decryptor.decrypt(tmpkey)
#         # print('Decrypted:', decrypted)
#         return jsonify({'status':'success','message':'success','data':resultKey})

@status_methods.route('/public/api/v1/taxid', methods=['GET'])
def filterbytaxid_api_v1():
    if request.method == 'GET':
        if 'Authorization' in request.headers:
            token_header = request.headers['Authorization']
            try:                
                token_header = str(token_header).split(' ')
                if token_header[0] != 'Bearer':
                    abort(401)
                else:
                    tmp_token = token_header[1]
            except Exception as ex:
                abort(401)
        else:
            abort(401)
        r = select_4().select_PaperlessToken_v1(tmp_token)
        if r['result'] == 'OK':
            tmp_tax_id = request.args.get('tax_id')
            if tmp_tax_id == None:
                return jsonify({'result':'ER','status_Code':200,'messageText':{'data':None,'message':'fail query string : tax_id'},'messageER':None}),200
            result = select_1().select_sum_document_bytaxid(tmp_tax_id)
            if result['result'] == 'OK' :
                return jsonify({'result':'OK','status_Code':200,'messageText':{'data':None,'message':result['messageText']},'messageER':None}),200
            else:
                return jsonify({'result':'ER','status_Code':200,'messageText':{'data':None,'message':'fail'},'messageER':None}),200
        else:
            abort(401)