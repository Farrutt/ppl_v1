#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from method.publicqrcode import *
from method.document import *
from method.verify import *
from controller.mail_string import *
from controller.validate import *
from db.db_method import *
from db.db_method_1 import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from api.file import *



if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less

def CallAPI_POST_oneid(url,header_token,datajson):
    try:
        tmp_header_token = 'Bearer ' + header_token
        response = requests.request("POST",headers={'Authorization': tmp_header_token}, url=url, json=datajson, verify=False, stream=True)
        response = response.json()
        insert().insert_tran_log_v1(str(response),'OK',str(datajson),url,header_token)
        return {'result': 'OK','messageText': response}
    except requests.HTTPError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(datajson),url,header_token)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as err:
        insert().insert_tran_log_v1(str(err),'ER',str(datajson),url,header_token)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as err:
        insert().insert_tran_log_v1(str(err),'ER',str(datajson),url,header_token)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(datajson),url,header_token)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(ex)}

def CallAPI_GET_oneid(url,header_token):
    try:
        tmp_header_token = 'Bearer ' + header_token
        response = requests.request("GET",headers={'Authorization': tmp_header_token}, url=url, verify=False, stream=True)
        response = response.json()
        insert().insert_tran_log_v1(str(response),'OK',None,url,header_token)
        return {'result': 'OK','messageText': response}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',None,url,header_token)
        return {'result': 'ER','messageText': "HTTP error occurred."}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',None,url,header_token)
        return {'result': 'ER','messageText': 'Request timed out'}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',None,url,header_token)
        return {'result': 'ER','messageText': 'API Connection error occurred.'}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',None,url,header_token)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(ex)}

@status_methods.route('/api/v1/excel/get_document', methods=['POST'])
# @token_required
def get_document_type_lower_v1():
    if request.method == 'POST':
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
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)}),401
        dataJson = request.json
        if 'email_thai_list' in dataJson and 'document_type' in dataJson and 'start_datetime' in dataJson and 'end_datetime' in dataJson and  len(dataJson) == 4:
            email_thai_list = dataJson['email_thai_list']
            document_type = dataJson['document_type']
            start_datetime = dataJson['start_datetime']
            end_datetime = dataJson['end_datetime']
            tmp_tax_id = ''
            list_tax_id = []
            tmp_message = result_verify['messageText'].json()
            tmp_data_biz_detail = tmp_message['biz_detail']
            for u in range(len(tmp_data_biz_detail)):
                tmp_data_getbiz = tmp_data_biz_detail[u]['getbiz'][0]
                tmp_id_card_num = tmp_data_getbiz['id_card_num']
                list_tax_id.append(tmp_id_card_num)
            tmp_username = tmp_message['username']
            if str(tmp_tax_id).replace(' ','') != '':
                if tmp_tax_id not in list_tax_id:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'tax_id not match'})
            # tmp_username = result_verify['username']
            result_select = select().select_report_v1(email_thai_list,document_type,start_datetime,end_datetime,tmp_tax_id)
            # print(result_select)
            # return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':None}),200
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
                filename = 'report_paperless' + st_filename + unique_filename
                data_excel = result_select['messageText']['Document_Details']
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
                # worksheet.write('B1', 'ประเภทเอกสาร',cell_format)
                worksheet.write('B1', 'ประเภทเอกสาร',cell_format)
                worksheet.write('C1', 'เลขที่เอกสาร',cell_format)
                worksheet.write('D1', 'เลขที่ติดตามเอกสาร',cell_format)
                worksheet.write('E1', 'รายละเอียด',cell_format)
                worksheet.write('F1', 'สถานะเอกสาร',cell_format)
                worksheet.write('G1', 'ผู้ส่งเอกสาร',cell_format)
                worksheet.write('H1', 'วันที่ส่ง',cell_format)
                worksheet.write('I1', 'หมายเหตุ',cell_format)
                worksheet.write('J1', 'ระยะเวลาดำเนินการ',cell_format)
                worksheet.write('K1', 'ระยะเวลาทั้งหมดที่เอกสารถูกดำเนินการ',cell_format)
                worksheet.write('L1', 'ระยะเวลาตั้งแต่เอกสารถูกนำเข้าถึงลำดับล่าสุด',cell_format)
                worksheet.set_column(0,0,5)
                worksheet.set_column(1,1,15)
                worksheet.set_column(2,3,20)
                worksheet.set_column(4,4,25)
                worksheet.set_column(5,5,20)
                worksheet.set_column(6,15,25)
                count = len(data_excel)
                for num in range (0, count):
                    line = data_excel[num]
                    if line['data_options']['body_text'] == None:
                        line['data_options']['body_text'] = ''
                    if line['data_options']['subject_text'] == None:
                        line['data_options']['subject_text'] = ''
                    worksheet.write(row, 0, (num+1), format1)
                    worksheet.write(row, 1, line['document_name'],format1)
                    worksheet.write(row, 2, line['document_id'] ,format1)
                    worksheet.write(row, 3, '=HYPERLINK("https://paperless.one.th/tracking?id=' + line['tracking_id'] + '","' + line['tracking_id']  + '")' ,format1)
                    worksheet.write(row, 4, line['data_options']['subject_text'] + ' ' + line['data_options']['body_text'],format1)
                    worksheet.write(row, 5, line['status_file_string'],format1)
                    worksheet.write(row, 6, line['sender_name'],format1)
                    worksheet.write(row, 7, line['dateTime_String_TH_1'] + ' ' + line['time_String'],format1)
                    worksheet.write(row, 8, line['remark_description'],format3)
                    worksheet.write(row, 9, line['timeline'],format3)
                    worksheet.write(row, 10, line['string_details_avg_time'],format3)
                    worksheet.write(row, 11, line['timing'],format1)
                    row += 1
                worksheet.write("M2","เอกสารทั้งหมด" , cell_format)
                worksheet.write("M3",count,format1)
                worksheet.write("N2","เอกสารกำลังดำเนินการ" , cell_format)
                worksheet.write("N3",count_n,format1)
                worksheet.write("O2","เอกสารอนุมัติ" , cell_format)
                worksheet.write("O3",count_y,format1)
                worksheet.write("P2","เอกสารปฏิเสธอนุมัติ" , cell_format)
                worksheet.write("P3",count_r,format1)
                workbook.close()
                filename = filename + '.xlsx'
                sha512encode_unifile = hashlib.sha512(str(unique_filename).encode('utf-8')).hexdigest()
                insert().insert_tran_excel_file_download_v1(path_indb,filename,sha512encode_unifile,tmp_username,str(dataJson))
                web_download_file = myUrl_domain + 'api/v1/excel/download_file/' + sha512encode_unifile
                return jsonify({'result':'OK','messageText':[{'download_excel_file':web_download_file,'token_download':sha512encode_unifile,'data':result_select['messageText']}],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_select['messageER']}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrct'}),404

@status_methods.route('/report/cost', methods=['GET'])
# @token_required
def get_document_cs():
    ts = int(time.time())
    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    st_filename = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S-')
    path = path_global_1 +'/storage/excel_report_type/' + str(st) + '/'
    path_indb = path_global_1 + '/storage/excel_report_type/' + str(st) + '/'
    # path = './storage/excel_report/' + str(st) + '/'
    # path_indb = '/storage/excel_report/' + str(st) + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    unique_filename = str(uuid.uuid4())
    filename = 'report_paperless' + st_filename + unique_filename
    sql = ''' 
        SELECT
            tb_send_detail.send_time,
            tb_step_data.update_time,
            tb_doc_detail.document_id,
            tb_doc_detail.options_page,
            tb_send_detail.file_name,
            tb_step_data.data_json
        FROM
            tb_send_detail 
        LEFT JOIN tb_doc_detail ON tb_doc_detail.step_id = tb_send_detail.step_data_sid
        LEFT JOIN tb_step_data ON tb_send_detail.step_data_sid = tb_step_data.sid
        WHERE
            status = 'ACTIVE' 
            AND document_status = 'Y'
            AND (tb_doc_detail."documentType" = 'CS' OR tb_doc_detail."documentType" = 'SCS')
        ORDER BY tb_doc_detail.document_id ASC
        '''
    with slave.connect() as connection:
        result = connection.execute(text(sql))
    query_result = [dict(row) for row in result]
    connection.close()
    workbook = xlsxwriter.Workbook(path + filename + '.xlsx')
    worksheet = workbook.add_worksheet()
    format1 = workbook.add_format()
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
    worksheet.write('A1', 'ลำดับ',cell_format)
    worksheet.write('B1', 'เลขที่เอกสาร',cell_format)
    worksheet.write('C1', 'ชื่อไฟล์',cell_format)
    worksheet.write('D1', 'หัวข้อ',cell_format)
    worksheet.write('E1', 'เนื้อเรื่อง',cell_format)
    worksheet.write('F1', 'เวลาส่ง',cell_format)
    worksheet.write('G1', 'เวลาอนุมัติล่าสุด',cell_format)
    worksheet.set_column(0,0,6)
    worksheet.set_column(1,1,22)
    worksheet.set_column(2,3,18)
    worksheet.set_column(4,4,23)
    worksheet.set_column(5,6,20)
    worksheet.set_column(7,12,25)
    count = len(query_result)
    row = 1
    col = 0
    for num in range (0, count):
        line = query_result[num]
        try:
            line['data_json'] = eval(line['data_json'])
        except Exception as e:
            line['data_json'] = ''
        # print(line['options_page'])
        # if 'body_text' in line['options_page']:
            # if line['options_page']['body_text'] == None:
            #     line['options_page']['body_text'] = ''
            # if line['options_page']['subject_text'] == None:
            #     line['options_page']['subject_text'] = ''
        # else:
            # print(line['options_page'])
            # line['options_page']['body_text'] = ''
            # line['options_page']['subject_text'] = ''

        worksheet.write(row, 0, (num+1), format2)
        worksheet.write(row, 1, line['document_id'],format2)
        worksheet.write(row, 2, line['file_name'] ,format2)
        workbook.close()
    # for n in range(len(query_result)):
    #     print(query_result[n])  
    #     return ''
    return ''

@status_methods.route('/api/v2/excel/get_document', methods=['POST'])
# @token_required
def get_document_type_lower_v2():
    if request.method == 'POST':
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
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)}),401
        dataJson = request.json
        if 'email_thai_list' in dataJson and 'document_type' in dataJson and 'start_datetime' in dataJson and 'end_datetime' in dataJson and 'tax_id' in dataJson and len(dataJson) == 5:
            email_thai_list = dataJson['email_thai_list']
            document_type = dataJson['document_type']
            start_datetime = dataJson['start_datetime']
            end_datetime = dataJson['end_datetime']
            tmp_tax_id = dataJson['tax_id']
            list_tax_id = []
            tmp_message = result_verify['messageText'].json()
            tmp_data_biz_detail = tmp_message['biz_detail']
            for u in range(len(tmp_data_biz_detail)):
                tmp_data_getbiz = tmp_data_biz_detail[u]['getbiz'][0]
                tmp_id_card_num = tmp_data_getbiz['id_card_num']
                list_tax_id.append(tmp_id_card_num)
            tmp_username = tmp_message['username']
            if str(tmp_tax_id).replace(' ','') != '':
                if tmp_tax_id not in list_tax_id:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'tax_id not match'})
            # tmp_username = result_verify['username']
            result_select = select().select_report_v1(email_thai_list,document_type,start_datetime,end_datetime,tmp_tax_id)
            # print(result_select)
            # return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':None}),200
            if result_select['result'] == 'OK':
                ts = int(time.time())
                st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                st_filename = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S-')
                path = path_global_1 +'/storage/excel_report/' + str(st) + '/'
                path_indb = path_global_1 + '/storage/excel_report/' + str(st) + '/'
                # path = './storage/excel_report/' + str(st) + '/'
                # path_indb = '/storage/excel_report/' + str(st) + '/'
                if not os.path.exists(path):
                    os.makedirs(path)
                unique_filename = str(uuid.uuid4())
                filename = 'report_paperless' + st_filename + unique_filename
                data_excel = result_select['messageText']['Document_Details']
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
                tmpRP_no = ''
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
                worksheet.write('E12', 'รายละเอียด',cell_format)
                worksheet.write('F12', 'สถานะเอกสาร',cell_format)
                worksheet.write('G12', 'ผู้ส่งเอกสาร',cell_format)
                worksheet.write('H12', 'วันที่ส่ง',cell_format)
                worksheet.write('I12', 'หมายเหตุ',cell_format)
                worksheet.write('J12', 'ระยะเวลาดำเนินการ',cell_format)
                worksheet.write('K12', 'ระยะเวลาทั้งหมดที่เอกสารถูกดำเนินการ',cell_format)
                worksheet.write('L12', 'ระยะเวลาตั้งแต่เอกสารถูกนำเข้าถึงลำดับล่าสุด',cell_format)
                worksheet.set_column(0,0,6)
                worksheet.set_column(1,1,22)
                worksheet.set_column(2,3,18)
                worksheet.set_column(4,4,23)
                worksheet.set_column(5,6,20)
                worksheet.set_column(7,12,25)
                count = len(data_excel)
                for num in range (0, count):
                    line = data_excel[num]
                    if line['data_options']['body_text'] == None:
                        line['data_options']['body_text'] = ''
                    if line['data_options']['subject_text'] == None:
                        line['data_options']['subject_text'] = ''
                    if tmp_tax_id == '0107544000094' and document_type == 'SPR':
                        for u in range(len(line['data_options']['service_properties'])):
                            tmpData = line['data_options']['service_properties'][u]
                            name_service = tmpData['name_service']
                            if name_service == 'GROUP':
                                tmpother = tmpData['other'][0]
                                tmpproperties = tmpother['properties']
                                for g in range(len(tmpproperties)):
                                    if 'display' in tmpproperties[g]:
                                        if tmpproperties[g]['display'] == 'เลขที่ใบขอซื้อ':
                                            tmpRP_no = tmpproperties[g]['value']
                                            worksheet.write('M12', 'PR No.',cell_format)
                    worksheet.write(row, 0, (num+1), format2)
                    worksheet.write(row, 1, line['document_name'],format2)
                    worksheet.write(row, 2, line['document_id'] ,format2)
                    worksheet.write(row, 3, '=HYPERLINK("' + url_paperless + 'tracking?id=' + line['tracking_id'] + '","' + line['tracking_id']  + '")' ,format2)
                    worksheet.write(row, 4, line['data_options']['subject_text'] + line['data_options']['body_text'],format2)
                    worksheet.write(row, 5, line['status_file_string'],format2)
                    try:
                        sender_name = eval(line['sender_name'])['th']
                    except Exception as e:
                        sender_name = line['sender_name']
                    worksheet.write(row, 6, sender_name,format2)
                    worksheet.write(row, 7, line['dateTime_String_TH_1'] + ' ' + line['time_String'],format2)
                    worksheet.write(row, 8, line['remark_description'],format2)
                    worksheet.write(row, 9, line['timeline'],format1)
                    worksheet.write(row, 10, line['string_details_avg_time'],format2)
                    worksheet.write(row, 11, line['timing'],format2)
                    worksheet.write(row, 12, tmpRP_no,format2)
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
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_select['messageER']}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrct'}),404

@status_methods.route('/api/v3/excel/get_document', methods=['POST'])
# @token_required
def get_document_type_lower_v3():
    if request.method == 'POST':
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
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)}),401
        dataJson = request.json
        if 'email_thai_list' in dataJson and 'document_type' in dataJson and 'start_datetime' in dataJson and 'end_datetime' in dataJson and 'tax_id' in dataJson and len(dataJson) == 5:
            email_thai_list = dataJson['email_thai_list']
            document_type = dataJson['document_type']
            start_datetime = dataJson['start_datetime']
            end_datetime = dataJson['end_datetime']
            tmp_tax_id = dataJson['tax_id']
            list_tax_id = []
            tmp_message = result_verify['messageText'].json()
            tmp_data_biz_detail = tmp_message['biz_detail']
            for u in range(len(tmp_data_biz_detail)):
                tmp_data_getbiz = tmp_data_biz_detail[u]['getbiz'][0]
                tmp_id_card_num = tmp_data_getbiz['id_card_num']
                list_tax_id.append(tmp_id_card_num)
            tmp_username = tmp_message['username']
            print('v1')
            if str(tmp_tax_id).replace(' ','') != '':
                if tmp_tax_id not in list_tax_id:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'tax_id not match'})
            # tmp_username = result_verify['username']
            result_select = select_1().select_report_v3(email_thai_list,document_type,start_datetime,end_datetime,tmp_tax_id)
            print('v3')
            # print(result_select)
            # return jsonify({'result':'OK','messageText':result_select['messageText'],'status_Code':200,'messageER':None}),200
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
                filename = 'report_paperless' + st_filename + unique_filename
                data_excel = result_select['messageText']['Document_Details']
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
                # worksheet.write('B1', 'ประเภทเอกสาร',cell_format)
                worksheet.write('B1', 'ประเภทเอกสาร',cell_format)
                worksheet.write('C1', 'เลขที่เอกสาร',cell_format)
                worksheet.write('D1', 'เลขที่ติดตามเอกสาร',cell_format)
                worksheet.write('E1', 'รายละเอียด',cell_format)
                worksheet.write('F1', 'สถานะเอกสาร',cell_format)
                worksheet.write('G1', 'ผู้ส่งเอกสาร',cell_format)
                worksheet.write('H1', 'วันที่ส่ง',cell_format)
                worksheet.write('I1', 'หมายเหตุ',cell_format)
                worksheet.write('J1', 'ระยะเวลาดำเนินการ',cell_format)
                worksheet.write('K1', 'ระยะเวลาทั้งหมดที่เอกสารถูกดำเนินการ',cell_format)
                worksheet.write('L1', 'ระยะเวลาตั้งแต่เอกสารถูกนำเข้าถึงลำดับล่าสุด',cell_format)
                worksheet.set_column(0,0,5)
                worksheet.set_column(1,1,15)
                worksheet.set_column(2,3,20)
                worksheet.set_column(4,4,25)
                worksheet.set_column(5,5,20)
                worksheet.set_column(6,15,25)
                count = len(data_excel)
                for num in range (0, count):
                    line = data_excel[num]
                    if line['data_options']['body_text'] == None:
                        line['data_options']['body_text'] = ''
                    if line['data_options']['subject_text'] == None:
                        line['data_options']['subject_text'] = ''
                    worksheet.write(row, 0, (num+1), format1)
                    worksheet.write(row, 1, line['document_name'],format1)
                    worksheet.write(row, 2, line['document_id'] ,format1)
                    worksheet.write(row, 3, '=HYPERLINK("' + url_paperless + 'tracking?id=' + line['tracking_id'] + '","' + line['tracking_id']  + '")' ,format1)
                    worksheet.write(row, 4, line['data_options']['subject_text'] + line['data_options']['body_text'],format1)
                    worksheet.write(row, 5, line['status_file_string'],format1)
                    worksheet.write(row, 6, line['sender_name'],format1)
                    worksheet.write(row, 7, line['dateTime_String_TH_1'] + ' ' + line['time_String'],format1)
                    worksheet.write(row, 8, line['remark_description'],format3)
                    worksheet.write(row, 9, line['timeline'],format3)
                    worksheet.write(row, 10, line['string_details_avg_time'],format3)
                    worksheet.write(row, 11, line['timing'],format1)
                    row += 1
                worksheet.write("M2","เอกสารทั้งหมด" , cell_format)
                worksheet.write("M3",count,format1)
                worksheet.write("N2","เอกสารกำลังดำเนินการ" , cell_format)
                worksheet.write("N3",count_n,format1)
                worksheet.write("O2","เอกสารอนุมัติ" , cell_format)
                worksheet.write("O3",count_y,format1)
                worksheet.write("P2","เอกสารปฏิเสธอนุมัติ" , cell_format)
                worksheet.write("P3",count_r,format1)
                workbook.close()
                filename = filename + '.xlsx'
                sha512encode_unifile = hashlib.sha512(str(unique_filename).encode('utf-8')).hexdigest()
                insert().insert_tran_excel_file_download_v1(path_indb,filename,sha512encode_unifile,tmp_username,str(dataJson))
                web_download_file = myUrl_domain + 'api/v1/excel/download_file/' + sha512encode_unifile
                return jsonify({'result':'OK','messageText':[{'download_excel_file':web_download_file,'token_download':sha512encode_unifile,'data':result_select['messageText']}],'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':result_select['messageER']}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':'parameter incorrct'}),404

@status_methods.route('/api/v1/excel/get_document_service', methods=['POST'])
def get_excel_document_api_v1():
    if request.method == 'POST':
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
        except Exception as e:
            return jsonify({'result':'ER','messageText':None,'messageER':'token expire unauthorized ' + str(e)}),401
        dataJson = request.json
        if 'service' in dataJson and 'start_datetime' in dataJson and 'end_datetime' in dataJson and 'tax_id' in dataJson and len(dataJson) == 4:
            list_tax_id = []
            tmp_message = result_verify['messageText'].json()
            tmp_data_biz_detail = tmp_message['biz_detail']
            tmp_servicename = dataJson['service']
            tmp_st_datetime = dataJson['start_datetime']
            tmp_end_datetime = dataJson['end_datetime']
            tmp_tax_id = dataJson['tax_id']
            for u in range(len(tmp_data_biz_detail)):
                tmp_data_getbiz = tmp_data_biz_detail[u]['getbiz'][0]
                tmp_id_card_num = tmp_data_getbiz['id_card_num']
                list_tax_id.append(tmp_id_card_num)
            tmp_username = tmp_message['username']
            if str(tmp_tax_id).replace(' ','') != '':
                if tmp_tax_id not in list_tax_id:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'tax_id not match'})
            if type(tmp_st_datetime) is not int or type(tmp_end_datetime) is not int:
                return jsonify({'result':'ER','messageText':None,'messageER':'start datetime or end datetime with out int','status_Code':200}),200
            result_select = select().select_report_service_v1(tmp_st_datetime,tmp_end_datetime,tmp_servicename,tmp_tax_id)
            # return {'result':'OK','messageText':result_select}
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
                filename = 'reportservice_paperless' + st_filename + unique_filename
                data_excel = result_select['messageText']
                row = 1
                col = 0
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
                worksheet.write('B1', 'เลขที่เอกสาร',cell_format)
                worksheet.write('C1', 'วันที่ส่ง',cell_format)
                # worksheet.write('D1', 'ข้อความ',cell_format)
                worksheet.write('D1', 'สถานะ',cell_format)
                worksheet.write('E1', 'สาเหตุ',cell_format)
                worksheet.set_column(0,0,5)
                worksheet.set_column(1,4,15)
                count = len(data_excel)
                for num in range (0, count):
                    line = data_excel[num]
                    if line['status'] == 'OK':
                        line['status'] = 'สำเร็จ'
                    elif line['status'] == 'ER':
                        line['status'] = 'ไม่สำเร็จ'
                    elif line['status'] == 'NOT':
                        line['status'] = 'สำเร็จแต่ไม่มีเอกสารไฟล์แนบ'
                    worksheet.write(row, 0, (num+1), format1)
                    worksheet.write(row, 1, line['document_id'],format1)
                    worksheet.write(row, 2, line['datetime'] ,format1)
                    worksheet.write(row, 3, line['status'] ,format1)
                    if line['status'] == 'ไม่สำเร็จ':
                        worksheet.write(row, 4, line['message'] ,format1)
                    row += 1
                workbook.close()
                filename = filename + '.xlsx'
                sha512encode_unifile = hashlib.sha512(str(unique_filename).encode('utf-8')).hexdigest()
                insert().insert_tran_excel_file_download_v1(path_indb,filename,sha512encode_unifile,tmp_username,str(dataJson))
                web_download_file = myUrl_domain + 'api/v1/excel/download_file/' + sha512encode_unifile
                return jsonify({'result':'OK','messageText':[{'download_excel_file':web_download_file,'token_download':sha512encode_unifile,'data':result_select['messageText']}],'status_Code':200,'messageER':None}),200

@status_methods.route('/api/v1/excel/download_file/<string:key_token_download>', methods=['GET'])
def download_file_excel_v1(key_token_download):
    result = select().select_report_excel_download_v1(key_token_download)
    if result['result'] == 'OK':
        msg_result = result['messageText']
        path_downloadFile = msg_result['path_excel'] + msg_result['name_excel']
        return send_file(os.path.join(path_downloadFile), as_attachment=True, attachment_filename='%s' % msg_result['name_excel'])
    else:
        return redirect(url_paperless)
