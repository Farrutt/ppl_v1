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
from method.callserver import *
from controller.mail_string import *
from controller.validate import *
from db.db_method_2 import *
from db.db_method_1 import *
from db.db_method_3 import *
from db.db_method import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from api.file import *
from method.sftp_fucn import *
from method.callwebHook import *
from method.cal_BI import *



if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less


@status_methods.route('/api/v2/group_document/search_sum',methods=['GET'])
@token_required_v3
def document_group_api_search_sum_v2():
    if request.method == 'GET':
        email_one = request.args.get('email_one')
        document_type = request.args.get('document_type')
        tax_id = request.args.get('tax_id')
        timestamps = request.args.get('timestamp')
        keyword = request.args.get('keyword')
        if email_one == None and document_type == None and tax_id == None:
            abort(404)
        resul_data = select_1().select_querydocument_group_search_sum_v2(email_one,document_type,tax_id,keyword,timestamps)
        if resul_data['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'message':'succuess','data':resul_data['messageText']},'messageER':None,'status_Code':200})
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail','data':resul_data['messageER']},'status_Code':200})


@status_methods.route('/api/v2/group_document/search',methods=['GET'])
@token_required_v3
def document_group_api_search_v2():
    if request.method == 'GET':
        email_one = request.args.get('email_one')
        document_type = request.args.get('document_type')
        group_id = request.args.get('group_id')
        tax_id = request.args.get('tax_id')
        status = request.args.get('status')
        timestamps = request.args.get('timestamp')
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        keyword = request.args.get('keyword')
        if email_one == None and document_type == None and group_id == None and tax_id == None:
            abort(404)
        resul_data = select_1().select_querydocument_group_search_v2(email_one,document_type,group_id,tax_id,status,limit,offset,keyword,timestamps)
        if resul_data['result'] == 'OK':
            # tmptmp_stamp = None
            # if 'timestamp' in resul_data:
            #     tmptmp_stamp = resul_data['timestamp']
            return jsonify({'result':'OK','messageText':{'message':'succuess','data':resul_data['messageText']},'timestamp': resul_data['timestamp'],'messageER':None,'status_Code':200})
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail','data':resul_data['messageER']},'status_Code':200})


@status_methods.route('/api/v1/auto_group', methods=['POST'])
# @token_required_v2

def auto_group_api_v1():
    dataJson = request.json
    if 'step_code' in dataJson and 'key' in dataJson and 'color_group' in dataJson:
        tmp_step_code = dataJson['step_code']
        tmp_key = dataJson['key']
        tmp_color_group = dataJson['color_group']
        email_thai = 'auto'
        arr_stepCode_green = []
        arr_stepCode_yellow = []
        arr_stepCode_red = []
        if 'D6FEC1F7D792CC9947CFCCC313338' in tmp_key:
            for n in range(len(tmp_step_code)):
                if tmp_color_group[n] == 'green':
                    arr_stepCode_green.append(tmp_step_code[n])
                elif tmp_color_group[n] == 'yellow':
                    arr_stepCode_yellow.append(tmp_step_code[n])
                elif tmp_color_group[n] == 'red':
                    arr_stepCode_red.append(tmp_step_code[n])
            for z in range(3):
                arr_tmpsidcode_0001 = []
                if len(arr_stepCode_green) != 0:
                    result_select = select().select_step_code_togroup_v1(arr_stepCode_green)
                    # print(result_select)
                    result_select['messageText']['color'] = 'green'
                    arr_stepCode_green = []
                elif len(arr_stepCode_yellow) != 0:
                    result_select = select().select_step_code_togroup_v1(arr_stepCode_yellow)
                    result_select['messageText']['color'] = 'yellow'
                    arr_stepCode_yellow = []
                elif len(arr_stepCode_red) != 0:
                    result_select = select().select_step_code_togroup_v1(arr_stepCode_red)
                    result_select['messageText']['color'] = 'red'
                    arr_stepCode_red = []
                # print(result_select)
                # return ''
            # result_select = select().select_step_code_togroup_v1(arr_stepCode)
                if result_select['result'] == 'OK':
                    tmp_sidcode = result_select['messageText']['data']
                    tmp_step_code = result_select['messageText']['stepcode']
                    tmp_color = result_select['messageText']['color']
                    for u in range(len(tmp_sidcode)):
                        if len(tmp_sidcode[u]) != 0:
                            for y in range(len(tmp_sidcode[u])):
                                arr_tmpsidcode_0001.append(tmp_sidcode[u][y])
                    # print(result_select)
                    result_select['messageText']['data'] = [arr_tmpsidcode_0001]
                    tmp_sidcode = result_select['messageText']['data']
                    # print(tmp_sidcode,'arr_tmpsidcode_0001')
                    if len(tmp_sidcode) != 0:
                        for z in range(len(tmp_sidcode)):
                            tmpsigndata = []
                            tmp_statusgroup_email = []
                            arr_color = []
                            tmp_sidcode_new = tmp_sidcode[z]
                            tmp_stepcode_new = tmp_step_code[z]
                            tmp_color_group_new = tmp_color
                            
                            arr_color.append({'color':tmp_color})
                            result_select = select().select_filter_sidcode_to_group_v1(tmp_sidcode_new)
                            # print(result_select)
                            # return ''
                            
                            if result_select['result'] == 'OK':
                                if type_product == 'prod':
                                    if tmp_color_group_new == 'green':       
                                        # tmp_statusgroup_email.append({'email_one':'nawarat.kl@one.th','status':'Incomplete'})
                                        # tmpsigndata.append({'email_one':'nawarat.kl@one.th','sign_llx':'0.407','sign_lly':'0.548','sign_urx':'0.180','sign_ury':'0.110','sign_page':'1','status':'incomplete'})                            
                                        tmp_statusgroup_email.append({'email_one':'tivanon.ja@one.th','status':'Incomplete'})
                                        tmpsigndata.append({'email_one':'tivanon.ja@one.th','sign_llx':'0.407','sign_lly':'0.548','sign_urx':'0.180','sign_ury':'0.110','sign_page':'1','status':'incomplete'})
                                    elif tmp_color_group_new == 'yellow':
                                        # tmp_statusgroup_email.append({'email_one':'nawarat.kl@one.th','status':'Incomplete'})
                                        # tmp_statusgroup_email.append({'email_one':'jirayu.ko@one.th','status':'Incomplete'})                                  
                                        # tmp_statusgroup_email.append({'email_one':'methinee.tu@one.th','status':'Incomplete'})
                                        # tmpsigndata.append({'email_one':'nawarat.kl@one.th','sign_llx':'0.158','sign_lly':'0.467','sign_urx':'0.210','sign_ury':'0.140','sign_page':'1','status':'incomplete'})
                                        # tmpsigndata.append({'email_one':'jirayu.ko@one.th','sign_llx':'0.392','sign_lly':'0.467','sign_urx':'0.210','sign_ury':'0.140','sign_page':'1','status':'incomplete'})
                                        # tmpsigndata.append({'email_one':'methinee.tu@one.th','sign_llx':'0.626','sign_lly':'0.463','sign_urx':'0.210','sign_ury':'0.140','sign_page':'1','status':'incomplete'})
                                        tmp_statusgroup_email.append({'email_one':'phakinee@one.th','status':'Incomplete'})                                  
                                        tmp_statusgroup_email.append({'email_one':'tivanon.ja@one.th','status':'Incomplete'})
                                        tmp_statusgroup_email.append({'email_one':'wanchai.vach@one.th','status':'Incomplete'})
                                        tmpsigndata.append({'email_one':'phakinee@one.th','sign_llx':'0.158','sign_lly':'0.467','sign_urx':'0.210','sign_ury':'0.140','sign_page':'1','status':'incomplete'})
                                        tmpsigndata.append({'email_one':'tivanon.ja@one.th','sign_llx':'0.392','sign_lly':'0.467','sign_urx':'0.210','sign_ury':'0.140','sign_page':'1','status':'incomplete'})
                                        tmpsigndata.append({'email_one':'wanchai.vach@one.th','sign_llx':'0.626','sign_lly':'0.463','sign_urx':'0.210','sign_ury':'0.140','sign_page':'1','status':'incomplete'})
                                    elif tmp_color_group_new == 'red':
                                        # tmp_statusgroup_email.append({'email_one':'nawarat.kl@one.th','status':'Incomplete'})
                                        # tmp_statusgroup_email.append({'email_one':'jirayu.ko@one.th','status':'Incomplete'})                                  
                                        # tmp_statusgroup_email.append({'email_one':'methinee.tu@one.th','status':'Incomplete'})
                                        # tmp_statusgroup_email.append({'email_one':'pongsit.mu@one.th','status':'Incomplete'})
                                        # tmpsigndata.append({'email_one':'nawarat.kl@one.th','sign_llx':'0.078','sign_lly':'0.513','sign_urx':'0.200','sign_ury':'0.100','sign_page':'1','status':'incomplete'})
                                        # tmpsigndata.append({'email_one':'jirayu.ko@one.th','sign_llx':'0.294','sign_lly':'0.513','sign_urx':'0.200','sign_ury':'0.100','sign_page':'1','status':'incomplete'})
                                        # tmpsigndata.append({'email_one':'methinee.tu@one.th','sign_llx':'0.506','sign_lly':'0.513','sign_urx':'0.200','sign_ury':'0.100','sign_page':'1','status':'incomplete'})
                                        # tmpsigndata.append({'email_one':'pongsit.mu@one.th','sign_llx':'0.722','sign_lly':'0.513','sign_urx':'0.200','sign_ury':'0.100','sign_page':'1','status':'incomplete'})
                                        tmp_statusgroup_email.append({'email_one':'phakinee@one.th','status':'Incomplete'})
                                        tmp_statusgroup_email.append({'email_one':'tivanon.ja@one.th','status':'Incomplete'})                                    
                                        tmp_statusgroup_email.append({'email_one':'wanchai.vach@one.th','status':'Incomplete'})                                    
                                        tmp_statusgroup_email.append({'email_one':'morragot.ku@one.th','status':'Incomplete'})
                                        tmpsigndata.append({'email_one':'phakinee@one.th','sign_llx':'0.078','sign_lly':'0.513','sign_urx':'0.200','sign_ury':'0.100','sign_page':'1','status':'incomplete'})
                                        tmpsigndata.append({'email_one':'tivanon.ja@one.th','sign_llx':'0.294','sign_lly':'0.513','sign_urx':'0.200','sign_ury':'0.100','sign_page':'1','status':'incomplete'})
                                        tmpsigndata.append({'email_one':'wanchai.vach@one.th','sign_llx':'0.506','sign_lly':'0.513','sign_urx':'0.200','sign_ury':'0.100','sign_page':'1','status':'incomplete'})
                                        tmpsigndata.append({'email_one':'morragot.ku@one.th','sign_llx':'0.722','sign_lly':'0.513','sign_urx':'0.200','sign_ury':'0.100','sign_page':'1','status':'incomplete'})
                                elif type_product == 'uat':
                                    if tmp_color_group_new == 'green':       
                                        # tmp_statusgroup_email.append({'email_one':'nawarat.kl@one.th','status':'Incomplete'})
                                        # tmpsigndata.append({'email_one':'nawarat.kl@one.th','sign_llx':'0.407','sign_lly':'0.548','sign_urx':'0.180','sign_ury':'0.110','sign_page':'1','status':'incomplete'})                            
                                        tmp_statusgroup_email.append({'email_one':'nawarat.kl@thai.com','status':'Incomplete'})
                                        tmpsigndata.append({'email_one':'nawarat.kl@thai.com','sign_llx':'0.407','sign_lly':'0.548','sign_urx':'0.180','sign_ury':'0.110','sign_page':'1','status':'incomplete'})
                                    elif tmp_color_group_new == 'yellow':
                                        # tmp_statusgroup_email.append({'email_one':'nawarat.kl@one.th','status':'Incomplete'})
                                        # tmp_statusgroup_email.append({'email_one':'jirayu.ko@one.th','status':'Incomplete'})                                  
                                        # tmp_statusgroup_email.append({'email_one':'methinee.tu@one.th','status':'Incomplete'})
                                        # tmpsigndata.append({'email_one':'nawarat.kl@one.th','sign_llx':'0.158','sign_lly':'0.467','sign_urx':'0.210','sign_ury':'0.140','sign_page':'1','status':'incomplete'})
                                        # tmpsigndata.append({'email_one':'jirayu.ko@one.th','sign_llx':'0.392','sign_lly':'0.467','sign_urx':'0.210','sign_ury':'0.140','sign_page':'1','status':'incomplete'})
                                        # tmpsigndata.append({'email_one':'methinee.tu@one.th','sign_llx':'0.626','sign_lly':'0.463','sign_urx':'0.210','sign_ury':'0.140','sign_page':'1','status':'incomplete'})
                                        tmp_statusgroup_email.append({'email_one':'warud.mi@thai.com','status':'Incomplete'})                                  
                                        tmp_statusgroup_email.append({'email_one':'nawarat.kl@thai.com','status':'Incomplete'})
                                        tmp_statusgroup_email.append({'email_one':'kamonluk.mo@thai.com','status':'Incomplete'})
                                        tmpsigndata.append({'email_one':'warud.mi@thai.com','sign_llx':'0.158','sign_lly':'0.467','sign_urx':'0.210','sign_ury':'0.140','sign_page':'1','status':'incomplete'})
                                        tmpsigndata.append({'email_one':'nawarat.kl@thai.com','sign_llx':'0.392','sign_lly':'0.467','sign_urx':'0.210','sign_ury':'0.140','sign_page':'1','status':'incomplete'})
                                        tmpsigndata.append({'email_one':'kamonluk.mo@thai.com','sign_llx':'0.626','sign_lly':'0.463','sign_urx':'0.210','sign_ury':'0.140','sign_page':'1','status':'incomplete'})
                                    elif tmp_color_group_new == 'red':
                                        # tmp_statusgroup_email.append({'email_one':'nawarat.kl@one.th','status':'Incomplete'})
                                        # tmp_statusgroup_email.append({'email_one':'jirayu.ko@one.th','status':'Incomplete'})                                  
                                        # tmp_statusgroup_email.append({'email_one':'methinee.tu@one.th','status':'Incomplete'})
                                        # tmp_statusgroup_email.append({'email_one':'pongsit.mu@one.th','status':'Incomplete'})
                                        # tmpsigndata.append({'email_one':'nawarat.kl@one.th','sign_llx':'0.078','sign_lly':'0.513','sign_urx':'0.200','sign_ury':'0.100','sign_page':'1','status':'incomplete'})
                                        # tmpsigndata.append({'email_one':'jirayu.ko@one.th','sign_llx':'0.294','sign_lly':'0.513','sign_urx':'0.200','sign_ury':'0.100','sign_page':'1','status':'incomplete'})
                                        # tmpsigndata.append({'email_one':'methinee.tu@one.th','sign_llx':'0.506','sign_lly':'0.513','sign_urx':'0.200','sign_ury':'0.100','sign_page':'1','status':'incomplete'})
                                        # tmpsigndata.append({'email_one':'pongsit.mu@one.th','sign_llx':'0.722','sign_lly':'0.513','sign_urx':'0.200','sign_ury':'0.100','sign_page':'1','status':'incomplete'})
                                        tmp_statusgroup_email.append({'email_one':'warud.mi@thai.com','status':'Incomplete'})
                                        tmp_statusgroup_email.append({'email_one':'nawarat.kl@thai.com','status':'Incomplete'})                                    
                                        tmp_statusgroup_email.append({'email_one':'kamonluk.mo@thai.com','status':'Incomplete'})                                    
                                        tmp_statusgroup_email.append({'email_one':'pongsit.mu@thai.com','status':'Incomplete'})
                                        tmpsigndata.append({'email_one':'warud.mi@thai.com','sign_llx':'0.078','sign_lly':'0.513','sign_urx':'0.200','sign_ury':'0.100','sign_page':'1','status':'incomplete'})
                                        tmpsigndata.append({'email_one':'nawarat.kl@thai.com','sign_llx':'0.294','sign_lly':'0.513','sign_urx':'0.200','sign_ury':'0.100','sign_page':'1','status':'incomplete'})
                                        tmpsigndata.append({'email_one':'kamonluk.mo@thai.com','sign_llx':'0.506','sign_lly':'0.513','sign_urx':'0.200','sign_ury':'0.100','sign_page':'1','status':'incomplete'})
                                        tmpsigndata.append({'email_one':'pongsit.mu@thai.com','sign_llx':'0.722','sign_lly':'0.513','sign_urx':'0.200','sign_ury':'0.100','sign_page':'1','status':'incomplete'})
                                tmp_sidcode_03 = result_select['messageText']
            # return ''
                                
                                result_select_email = select().select_datajson_toemail(tmp_sidcode_03)
                                result_insert = insert().insert_group_v1(tmp_sidcode_03,result_select_email['messageText'],email_thai,result_select_email['step_num_sum'],result_select_email['data_sum'],arr_color,result_select_email['email_view_group'],tmpsigndata,tmp_statusgroup_email)  
                                if 'result' in result_insert:
                                    if result_insert['result'] == 'OK':
                                        tmpgroup_id = str(result_insert['messageText']['group_id'])
                                        tmptracking_group = str(result_insert['messageText']['tracking_group'])
                                        tmpgroup_color = str(result_insert['messageText']['group_color'])
                                        str_hash_id = hash_512_v2(str(result_insert['messageText']['group_id']))
                                        update().update_hashid_ingroup_v1(str(result_insert['messageText']['group_id']),str_hash_id)                              
                                        result_update = update().update_group_v1(tmp_sidcode_03,str(result_insert['messageText']['group_id'])) 
                                        chat_sender_group_v1(str(result_insert['messageText']['group_id']),None)
                                        unique_folderFilename = tmpgroup_id
                                        # path = path_global_1 + '/storage/html/' + unique_folderFilename +'/'
                                        # path_indb = path_global_1 + '/storage/html/' + unique_folderFilename +'/'
                                        # path = './storage/html/' + unique_folderFilename +'/'
                                        # path_indb = '/storage/html/' + unique_folderFilename +'/'
                                        # if not os.path.exists(path):
                                        #     os.makedirs(path)
                                        # dataBi = result_select_email['data_bi']
                                        # info = {
                                        #     "group_tracking":tmptracking_group,
                                        #     "group_color":tmpgroup_color,
                                        #     "group_detail":dataBi
                                        # }
                                        # if type_product == 'prod':
                                        #     url_BI_logic = url_bi_2 + '/calculate'
                                        # else:
                                        #     url_BI_logic = url_bi_cs + '/api/v1/calculate'
                                        # resultDataBI = callPost_v3(url_BI_logic,info)
                                        # if resultDataBI['result'] == 'OK':
                                        #     tmpmessage = resultDataBI['messageText'].json()
                                        #     if tmpmessage['message'] == 'Success':
                                        #         tmpdata = tmpmessage['data']
                                        #         if 'Warning_Detail' in tmpdata:
                                        #             pathfile = path + unique_folderFilename + '.html'
                                        #             try:
                                        #                 with open(pathfile, 'a') as the_file:
                                        #                     the_file.write(tmpdata['Warning_Detail'])
                                        #                 update_3().update_HtmlData_Bi_v1(tmpgroup_id,tmpdata['Warning_Detail'])
                                        #             except Exception as e:
                                        #                 pass
                                        # url_BI_logic = url_bi_2 + '/calculateTest'
                                        # resultDataBI = callPost_v3(url_BI_logic,info)
                                        # if resultDataBI['result'] == 'OK':
                                        #     tmpmessage = resultDataBI['messageText'].json()
                                        #     if tmpmessage['message'] == 'success':
                                        #         tmpdata = tmpmessage['data']
                                        #         pathfile = path + unique_folderFilename + '.html'
                                        #         with open(pathfile, 'a') as the_file:
                                        #             the_file.write(tmpdata)
                                        #         update_3().update_HtmlData_Bi_v1(tmpgroup_id,tmpdata)
            return jsonify({'result':'OK','messageText':{'message':'success','data':None},'status_Code':200,'messageER':None}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'key incorrect','data':None,'code':'ERCG999'}}),404    
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':None,'code':'ERCG999'}}),404

@status_methods.route('/api/v1/create_group', methods=['POST'])
@token_required_v2
def create_group_api_v1(username,email_thai,token_Code):
    dataJson = request.json
    if 'sidcode' in dataJson and 'key' in dataJson and len(dataJson) == 2:
        tmp_sidcode = dataJson['sidcode']
        tmp_key = dataJson['key']
        if '5B479B3936F2CE4FCEDA37555ADB5' in tmp_key:
            result_select_email = select().select_datajson_toemail(tmp_sidcode)
            if result_select_email['result'] == 'OK':
                result_insert = insert().insert_group_v1(tmp_sidcode,result_select_email['messageText'],email_thai,result_select_email['step_num_sum'])
                if result_insert['result'] == 'OK':
                    result_update = update().update_group_v1(tmp_sidcode,str(result_insert['messageText']['group_id']))
                    if result_update['result'] == 'OK':
                        return jsonify({'result':'OK','messageText':{'message':'success','data':None},'status_Code':200,'messageER':None}),200
                    else:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'fail','data':None,'code':'ERCG001'}}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'fail','data':None,'code':'ERCG002'}}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'fail','data':None,'code':'ERCG003'}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'key incorrect','data':None,'code':'ERCG999'}}),404
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':None,'code':'ERCG999'}}),404

@status_methods.route('/api/v1/update_step_group', methods=['PUT'])
@token_required_v2
def update_step_group(username,email_thai,token_Code):
    dataJson = request.json
    if 'status' in dataJson and 'step_num' in dataJson and 'group_id' in dataJson and len(dataJson) == 3:
        tmp_status = dataJson['status']
        tmp_step_num = dataJson['step_num']
        tmp_groupid = dataJson['group_id']
        
        return jsonify({'result':'OK','messageText':{'data':None,'message':'success'},'messageER':None,'status_Code':200}),200

@status_methods.route('/api/v1/save_pdf_group', methods=['POST'])
@token_required_v2
def save_pdf_group_api_v1(username,email_thai,token_Code):
    dataJson = request.json
    if 'pdf_data' in dataJson and 'group_id' in dataJson and len(dataJson) == 2:
        tmp_pdfdata = dataJson['pdf_data']
        tmp_groupid = dataJson['group_id']
        result_insert = insert().insert_pdf_togroup_v1(tmp_groupid,tmp_pdfdata)
        if result_insert['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'data':None,'message':'success'},'messageER':None,'status_Code':200}),200
        else:            
            return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'fail'},'status_Code':200}),200
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':None,'code':'ERCG999'}}),404

@status_methods.route('/api/v1/update_pdf_group', methods=['PUT'])
@token_required_v2
def update_pdf_group_api_v1(username,email_thai,token_Code):
    dataJson = request.json
    if 'pdf_data' in dataJson and 'group_id' in dataJson and len(dataJson) == 2:
        tmp_pdfdata = dataJson['pdf_data']
        tmp_groupid = dataJson['group_id']
        # tmp_data = dataJson['data']
        result_update = update().update_pdf_ingroup_v1(tmp_groupid,tmp_pdfdata,email_thai)
        if result_update['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'data':None,'message':'success'},'messageER':None,'status_Code':200}),200
        else:            
            return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'fail'},'status_Code':200}),200    
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':None,'code':'ERCG999'}}),404

@status_methods.route('/api/v2/update_pdf_group', methods=['PUT'])
@token_required_v2
def update_pdf_group_api_v2(username,email_thai,token_Code):
    dataJson = request.json
    if 'pdf_data' in dataJson and 'group_id' in dataJson and len(dataJson) == 2:
        tmp_pdfdata = dataJson['pdf_data']
        tmp_groupid = dataJson['group_id']
        # tmp_data = dataJson['data']
        result_update = update().update_pdf_ingroup_v2(tmp_groupid,tmp_pdfdata,email_thai)
        if result_update['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'data':None,'message':'success'},'messageER':None,'status_Code':200}),200
        else:            
            return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'fail'},'status_Code':200}),200    
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':None,'code':'ERCG999'}}),404

@status_methods.route('/api/v1/remove_group', methods=['POST'])
@token_required_v2
def remove_group_api_v1(username,email_thai,token_Code):
    dataJson = request.json
    if 'group_id' in dataJson and 'key' in dataJson and len(dataJson) == 2:
        tmp_groupid = dataJson['group_id']
        tmp_key = dataJson['key']
        if '572AC34B99BDCFEFEC963431D352C' in tmp_key:
            result_update = update().update_toremove_group_v1(tmp_groupid,email_thai)
            if result_update['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'fail','data':None,'code':'ERRG001'}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'key incorrect','data':None,'code':'ERRG999'}}),404
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':None,'code':'ERRG999'}}),404

@status_methods.route('/api/v1/remove_document_ingroup', methods=['POST'])
@token_required_v2
def remove_document_ingroup_api_v1(username,email_thai,token_Code):
    dataJson = request.json
    if 'sidcode' in dataJson and 'group_id' in dataJson and 'key' in dataJson and len(dataJson) == 3:
        tmp_sidcode = dataJson['sidcode']
        tmp_groupid = dataJson['group_id']
        tmp_key = dataJson['key']
        tmp_averagdata = None
        if '161F21E75B232BA9C5ED834A426E9' in tmp_key:
            result_update = update().update_toremove_document_ingroup_v1(tmp_sidcode,tmp_groupid,email_thai)
            for z in range(len(tmp_sidcode)):
                check_update = update().update_step_v4_group(tmp_sidcode[z],email_thai,'A03','Reject',0.0,0.0,'')
            if result_update['result'] == 'OK':
                result_select_email = select().select_datajson_toemail(result_update['tmpsid'])
                unique_folderFilename = tmp_groupid
                path = path_global_1 + '/storage/html/' + unique_folderFilename +'/'
                path_indb = path_global_1 + '/storage/html/' + unique_folderFilename +'/'
                if not os.path.exists(path):
                    os.makedirs(path)
                resultTracking = select_3().select_trackinggroup_v1(dataJson['group_id'])
                dataBi = result_select_email['data_bi']
                info = {
                    "group_tracking":resultTracking['tracking_group'],
                    "group_color":resultTracking['group_color'],
                    "group_detail":dataBi
                }
                if type_product == 'prod':
                    url_BI_logic = url_bi_2 + '/calculate'
                else:
                    url_BI_logic = url_bi_cs + '/api/v1/calculate'
                resultDataBI = callPost_v3(url_BI_logic,info)
                if resultDataBI['result'] == 'OK':
                    tmpmessage = resultDataBI['messageText'].json()
                    if tmpmessage['message'] == 'Success':
                        tmpdata = tmpmessage['data']
                        if 'Warning_Detail' in tmpdata:
                            pathfile = path + unique_folderFilename + '.html'
                            tmp_jsondata = tmpdata['Warning_json']
                            if 'averag' in tmpdata:
                                tmp_averagdata = tmpdata['averag']
                            try:
                                with open(pathfile, 'a') as the_file:
                                    the_file.write(tmpdata['Warning_Detail'])
                                update_3().update_HtmlData_Bi_v1(tmp_groupid,tmpdata['Warning_Detail'],tmp_jsondata,tmp_averagdata)
                            except Exception as e:
                                pass
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'status_Code':200,'messageER':None}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'fail','data':None,'code':'ERRIG001'}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'key incorrect','data':None,'code':'ERRIG999'}}),404
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':None,'code':'ERRIG999'}}),404

@status_methods.route('/api/v2/remove_document_ingroup', methods=['POST'])
def remove_document_ingroup_api_v2():    
    try:
        if 'Authorization' not in request.headers:
            abort(401)
        token_header = request.headers['Authorization']
        token_header = str(token_header).split(' ')[1]
    except Exception as ex:
        abort(401)
    try:
        result_data = token_required_func(token_header)
        if result_data['result'] == 'ER':
            abort(401)
    except Exception as e:
        abort(401)
    dataJson = request.json
    if 'sidcode' in dataJson and 'group_id' in dataJson and 'category_type' in dataJson and 'key' in dataJson and len(dataJson) == 4:
        if result_data['result'] == 'OK':
            tmpemail = result_data['email']
            tmpusername = result_data['username']
            tmpemail = result_data['email']
            tmpuser_id = result_data['user_id']
            tmpcitizen = result_data['citizen_data']
        # return ''
        tmp_sidcode = dataJson['sidcode']
        tmp_groupid = dataJson['group_id']
        tmpcategory_type = str(dataJson['category_type']).lower()
        tmpcatype_string = ''
        if tmpcategory_type == 'reject' or tmpcategory_type == 'pending' or tmpcategory_type == 'remove':
            pass
        else:            
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'category_type incorrect','data':None,'code':'ERRIG02'}}),200
        if tmpcategory_type == 'reject':
            tmpcatype_string = 'Reject'
        elif tmpcategory_type== 'pending':
            tmpcatype_string = 'Pending'
        elif tmpcategory_type== 'remove':
            tmpcatype_string = 'remove'
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'category_type incorrect','data':None,'code':'ERRIG02'}}),200
        tmp_key = dataJson['key']
        if '161F21E75B232BA9C5ED834A426E9' in tmp_key:
            if tmpcatype_string != 'remove':
                result_update = update().update_toremove_document_ingroup_v1(tmp_sidcode,tmp_groupid,tmpemail)
                for z in range(len(tmp_sidcode)):
                    check_update = update().update_step_v4_group(tmp_sidcode[z],tmpemail,'A03',tmpcatype_string,0.0,0.0,'')
                if result_update['result'] == 'OK':
                    result_select_email = select().select_datajson_toemail(result_update['tmpsid'])
                    unique_folderFilename = tmp_groupid
                    path = path_global_1 + '/storage/html/' + unique_folderFilename +'/'
                    path_indb = path_global_1 + '/storage/html/' + unique_folderFilename +'/'
                    if not os.path.exists(path):
                        os.makedirs(path)
                    resultTracking = select_3().select_trackinggroup_v1(dataJson['group_id'])
                    dataBi = result_select_email['data_bi']
                    info = {
                        "group_tracking":resultTracking['tracking_group'],
                        "group_color":resultTracking['group_color'],
                        "group_detail":dataBi
                    }
                    if type_product == 'prod':
                        url_BI_logic = url_bi_2 + '/calculate'
                    else:
                        url_BI_logic = url_bi_cs + '/api/v1/calculate'
                    resultDataBI = callPost_v3(url_BI_logic,info)
                    if resultDataBI['result'] == 'OK':
                        tmpmessage = resultDataBI['messageText'].json()
                        if tmpmessage['message'] == 'Success':
                            tmpdata = tmpmessage['data']
                            if 'Warning_Detail' in tmpdata:
                                pathfile = path + unique_folderFilename + '.html'
                                tmp_jsondata = tmpdata['Warning_json']
                                try:
                                    with open(pathfile, 'a') as the_file:
                                        the_file.write(tmpdata['Warning_Detail'])
                                    update_3().update_HtmlData_Bi_v1(tmp_groupid,tmpdata['Warning_Detail'])
                                except Exception as e:
                                    pass
                    return jsonify({'result':'OK','messageText':{'message':'success','data':None},'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'fail','data':None,'code':'ERRIG001'}}),200
            else:
                result_update = update().update_changestatusgroup_v1(tmp_sidcode)
                result_update = update().update_toremove_document_ingroup_v1(tmp_sidcode,tmp_groupid,tmpemail)
                print(result_update)
                if result_update['result'] == 'OK':
                    result_select_email = select().select_datajson_toemail(result_update['tmpsid'])
                    unique_folderFilename = tmp_groupid
                    path = path_global_1 + '/storage/html/' + unique_folderFilename +'/'
                    path_indb = path_global_1 + '/storage/html/' + unique_folderFilename +'/'
                    if not os.path.exists(path):
                        os.makedirs(path)
                    resultTracking = select_3().select_trackinggroup_v1(dataJson['group_id'])
                    dataBi = result_select_email['data_bi']                    
                    call_service_BI(dataJson['group_id'],'','','','','','')
                    return jsonify({'result':'OK','messageText':{'message':'success','data':None},'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'fail','data':None,'code':'ERRIG002'}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'key incorrect','data':None,'code':'ERRIG999'}}),404
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':None,'code':'ERRIG999'}}),404

@status_methods.route('/api/v1/add_documentto_group', methods=['POST'])
@token_required_v2
def add_documentto_group_api_v1(username,email_thai,token_Code):
    dataJson = request.json
    if 'sidcode' in dataJson and 'group_id' in dataJson and 'key' in dataJson and len(dataJson) == 3:
        tmp_sidcode = dataJson['sidcode']
        tmp_groupid = dataJson['group_id']
        tmp_key = dataJson['key']
        if '378D7A482DF135771C685434E6A5F' in tmp_key:
            result_select_email = select().select_datajson_toemail(tmp_sidcode)
            if result_select_email['result'] == 'OK':
                result_update = update().update_toadd_document_ingroup_v1(tmp_sidcode,tmp_groupid,result_select_email['messageText'],email_thai)
                if result_update['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':{'message':'success','data':None},'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'fail','data':[result_update['data']],'code':'ERADG001'}}),200
            else:
                return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'fail','data':None,'code':'ERADG002'}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'key incorrect','data':None,'code':'ERADG999'}}),404
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':None,'code':'ERADG999'}}),404

@status_methods.route('/api/v1/group_document', methods=['POST'])
@token_required_v2
def group_document_api_v1(username,email_thai,token_Code):
    dataJson = request.json
    if 'email_one' in dataJson and len(dataJson) == 1:
        tmp_email = dataJson['email_one']
        result_select = select().select_group_list_email_new_v2(tmp_email)
        if result_select['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'message':'success','data':result_select['messageText']},'status_Code':200,'messageER':None}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'fail' + result_select['messageER'],'data':None,'code':'ERADG001'}}),200

@status_methods.route('/api/v2/group_document', methods=['POST'])
@token_required_v2
def group_document_api_v2(username,email_thai,token_Code):
    dataJson = request.json
    if 'email_one' in dataJson and 'group_status' in dataJson and 'datetime' in dataJson and len(dataJson) == 3:
        tmp_email = dataJson['email_one']
        tmp_group_status = dataJson['group_status']
        tmp_datetime = dataJson['datetime']
        date_start_tmp = datetime.datetime.fromtimestamp(tmp_datetime)
        datetime_end_tmp = datetime.datetime.fromtimestamp(time.time())
        result_select = select().select_group_list_email_v2(tmp_email,tmp_group_status,date_start_tmp,datetime_end_tmp)
        if result_select['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'message':'success','data':result_select['messageText']},'status_Code':200,'messageER':None}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'fail ' + result_select['messageER'],'data':None,'code':'ERADG001'}}),200

@status_methods.route('/api/v1/update_signature_group', methods=['POST'])
@token_required_v2
def update_signature_group_api_v1(username,email_thai,token_Code):
    dataJson = request.json
    if 'group_id' in dataJson and 'email_one' in dataJson and 'sign_base' in dataJson:
        tmpgroup_id = dataJson['group_id']
        tmpemail_one = dataJson['email_one']
        tmpsign_base = dataJson['sign_base']
        result_update = update().update_signature_group_v1(tmpgroup_id,tmpemail_one,tmpsign_base)
        if result_update['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'message':'success','data':None},'status_Code':200,'messageER':None}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'fail ' + result_update['messageText'],'data':None,'code':'ERUSG001'}}),200

@status_methods.route('/api/v1/one/chat/group_document', methods=['POST'])
@token_required_v2
def group_document_one_chat_api_v2(username,email_thai,token_Code):
    dataJson = request.json
    if 'hashgroup_id' in dataJson and 'email_one' in dataJson:
        tmp_group_id = dataJson['hashgroup_id']
        tmpemail_one = dataJson['email_one']
        result_select = select().select_group_one_email_v1_groupchat(tmp_group_id,tmpemail_one)
        if result_select['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'message':'success','data':result_select['messageText']},'status_Code':200,'messageER':None}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'fail ' + result_select['messageER'],'data':None,'code':'ERADG001'}}),200

@status_methods.route('/api/v2/one/group_document', methods=['POST'])
@token_required_v2
def group_document_one_api_v2(username,email_thai,token_Code):
    dataJson = request.json
    if 'group_id' in dataJson and 'email_one' in dataJson:
        tmp_group_id = dataJson['group_id']
        tmpemail_one = dataJson['email_one']
        result_select = select().select_group_one_email_v3(tmp_group_id,tmpemail_one)
        if result_select['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'message':'success','data':result_select['messageText']},'status_Code':200,'messageER':None}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'fail ' + result_select['messageER'],'data':None,'code':'ERADG001'}}),200

@status_methods.route('/api/v1/one/group_document',methods=['POST'])
@token_required
def one_collect_api_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'group_id' in dataJson and 'email_one' in dataJson:
            tmp_group_id = dataJson['group_id']
            tmpemail_one = dataJson['email_one']
            result_select = select().select_dashboard_collect_one_v1(tmp_group_id,tmpemail_one)
            if result_select['result'] == 'OK':
                return jsonify({'result':'OK','mesageText':{'document_detail':result_select['messageText'],'group_info':result_select['data']}})
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':result_select['messageText']},'status_Code':200}),200

@status_methods.route('/api/v1/view/group_pdf',methods=['GET'])
def view_group_pdf_api_v1():
    if request.method == 'GET':
        if (request.args.get('groupid')) != None:
            tmpgroupid = (request.args.get('groupid'))
            result_select = select().select_pdf_group_v1(tmpgroupid)
            if result_select['result'] == 'OK':
                base64_pdfFile = result_select['messageText']
                unique_filename = str(uuid.uuid4())
                return send_file(
                io.BytesIO(base64.b64decode(base64_pdfFile)),
                mimetype='application/pdf',
                as_attachment=False,
                attachment_filename='%s.pdf' % unique_filename)

@status_methods.route('/api/v1/download/group_pdf',methods=['GET'])
def download_group_pdf_api_v1():
    if request.method == 'GET':
        if (request.args.get('groupid')) != None:
            tmpgroupid = (request.args.get('groupid'))
            result_select = select().select_pdf_group_v1(tmpgroupid)
            if result_select['result'] == 'OK':
                base64_pdfFile = result_select['messageText']
                unique_filename = str(uuid.uuid4())
                return send_file(
                io.BytesIO(base64.b64decode(base64_pdfFile)),
                mimetype='application/pdf',
                as_attachment=True,
                attachment_filename='%s.pdf' % unique_filename)

@status_methods.route('/api/v1/template/template_group',methods=['PUT','POST','GET'])
@token_required_v3
def template_group_v1():
    if request.method == 'POST':
        token_header = request.headers['Authorization']
        resCheck = (str(token_header).split(' ')[1])       
        token_required = token_required_func(resCheck)
        username = token_required['username']
        thai_email = token_required['email']
        dataJson = request.json
        '''------ INSERT ------'''
        if 'group_name' in dataJson and 'group_code' in dataJson and 'template' in dataJson and 'document_type' in dataJson and 'group_title' in dataJson and 'step_group' in dataJson and 'group_data' in dataJson and 'business_info' in dataJson and 'use_status' in dataJson and 'cover_page' in dataJson and 'group_color' in dataJson:
            group_name = dataJson['group_name']
            group_code = dataJson['group_code']
            template = dataJson['template']
            document_type = dataJson['document_type']
            group_title = dataJson['group_title']
            step_group = dataJson['step_group']
            group_data = dataJson['group_data']
            business_info = dataJson['business_info']
            use_status = dataJson['use_status']
            cover_page = dataJson['cover_page']
            group_color = dataJson['group_color']
            tmp_email_middle = None
            tmp_timegroup = None
            tmp_daygroup = None
            webhook = None
            if 'email_middle' in dataJson:
                tmp_email_middle = dataJson['email_middle']
            if 'timegroup' in dataJson:
                tmp_timegroup = dataJson['timegroup']
            if 'daygroup' in dataJson:
                tmp_daygroup = dataJson['daygroup']
            if 'webhook' in dataJson:                
                webhook = dataJson['webhook']
            insert_result = insert_2().insert_template_group_v3(group_name,group_code,template,document_type,group_title,step_group,group_data,business_info,thai_email,thai_email,use_status,cover_page,group_color,tmp_email_middle,tmp_timegroup,tmp_daygroup,webhook)
            if insert_result['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':insert_result['messageText'],'data':None},'status_Code':200}),200
        # ------ DELETE ------
        elif 'id' in dataJson and len(dataJson) == 1:
            id_data = dataJson['id']
            delete_result = update_2().delete_template_group_v2(id_data,username)
            if delete_result['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'OK','messageText':None,'messageER':{'message':'data not found','data':None},'status_Code':200}),200
        else:
            abort(404)
    elif request.method == 'PUT':
         # ------ UPDATE ------
        try:
            token_header = request.headers['Authorization']
            resCheck = (str(token_header).split(' ')[1])       
            token_required = token_required_func(resCheck)
            # print ('token_required: ',token_required)
            username = token_required['username']
            thai_email = token_required['email']
            dataJson = request.json
            if 'id' in dataJson and 'group_name' in dataJson and 'group_code' in dataJson and 'template' in dataJson and 'document_type' in dataJson and 'group_title' in dataJson and 'step_group' in dataJson and 'group_data' in dataJson and 'business_info' in dataJson and 'use_status' in dataJson and 'cover_page' in dataJson and 'group_color' in dataJson:
                id_data = dataJson['id']
                group_name = dataJson['group_name']
                group_code = dataJson['group_code']
                template = dataJson['template']
                document_type = dataJson['document_type']
                group_title = dataJson['group_title']
                step_group = dataJson['step_group']
                group_data = dataJson['group_data']
                business_info = dataJson['business_info']
                use_status = dataJson['use_status']
                cover_page = dataJson['cover_page']
                group_color = dataJson['group_color']
                tmp_email_middle = None
                tmp_timegroup = None
                tmp_daygroup = None
                webhook = None
                if 'email_middle' in dataJson:
                    tmp_email_middle = dataJson['email_middle']
                if 'timegroup' in dataJson:
                    tmp_timegroup = dataJson['timegroup']
                if 'daygroup' in dataJson:
                    tmp_daygroup = dataJson['daygroup']
                if 'webhook' in dataJson:                
                    webhook = dataJson['webhook']
                update_result = update_2().update_template_group_v6(id_data,group_name,group_code,template,document_type,group_title,step_group,group_data,business_info,thai_email,use_status,cover_page,group_color,tmp_email_middle,tmp_timegroup,tmp_daygroup,webhook)
                # print(update_result)
                if update_result['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':{'message':'success','data':None},'messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail ' + update_result['messageText'],'data':None},'status_Code':200}),200
            #------ UPDATE USE_STATUS ------
            elif 'id' in dataJson and 'use_status' in dataJson and len(dataJson) == 2:
                id_data = dataJson['id']
                use_status = dataJson['use_status']
                use_status_result = update_2().use_status_template_group_v2(id_data,use_status,username)

                if use_status_result['result'] == 'OK':
                    return jsonify({'result':'OK','messageText':'success','messageER':None,'status_Code':200}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'messageER':'invalid id','status_Code':200}),200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'Fail','responseCode':500,'data':None,'errorMessage':str(e)})


    # ----- GET_LIST -----
    elif request.method == 'GET':
        try:
            username = request.args.get('username')
            tax_id = request.args.get('tax_id')
            id_data = request.args.get('id')
            document_type = request.args.get('document_type')
            list_json = []
            result_group_template = select_2().select_list_template_group_v3(username,tax_id,id_data,document_type)
            if result_group_template['result'] == 'OK':
                return jsonify({'result':'OK','messageText':{'message':'success','data':result_group_template['messageText']} ,'messageER':None,'status_Code':200}),200
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail ' + result_group_template['messageER'],'data':None},'status_Code':result_group_template['status_Code']}),result_group_template['status_Code']
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':{'data':None,'message':str(e)}}),200

@status_methods.route('/api/v1/template/template_document_forgorup',methods=['GET'])
@token_required_v3
def template_document_forgroup_v1():
    if request.method == 'GET':
        tmp_taxid = request.args.get('tax_id')
        tmp_username = request.args.get('username')
        tmp_documenttype = request.args.get('document_type')
        result_data = select_2().select_template_forgroup(tmp_taxid,tmp_username,tmp_documenttype)
        if result_data['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'data':result_data['messageText'],'message':'succuess'},'messageER':None,'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':result_data['messageER'],'data':None},'status_Code':200}),200

def most_frequent(List): 
    counter = 0
    num = List[0]
    for i in List: 
        curr_frequency = List.count(i) 
        if(curr_frequency> counter): 
            counter = curr_frequency 
            num = i 
  
    return num 

@status_methods.route('/api/v1/template/template_to_group',methods=['POST'])
@token_required_v3
def template_to_group_v1():
    if request.method == 'POST':
        dataJson = request.json
        arr_tmp = []
        arr_templatecode = []
        infojson = {}
        if 'template_code' in dataJson and len(dataJson) == 1:
            tmp_template_code = dataJson['template_code']
            for x in range(len(tmp_template_code)):
                tmp_templatecode_one = tmp_template_code[x]
                result_data = select_2().select_template_group_status(tmp_templatecode_one)
                arr_tmp.append(result_data)
            result = most_frequent(arr_tmp)
            for z in range(len(arr_tmp)):
                if result == arr_tmp[z]:
                    arr_templatecode.append(tmp_template_code[z])
            infojson['template_code'] = arr_templatecode
            resultchecktemplate = select_1().select_check_template_stepforgroup_v1(arr_templatecode)
            return jsonify({'result':'OK','messageText':{'message':'succuess','data':resultchecktemplate}})
        else:
            abort(404)

def fuc_manual_group(dataJson,tmpemail=None):
    if tmpemail == None:
        username = 'auto'
        thai_email = 'auto'
    else:
        username = tmpemail
        thai_email = tmpemail
    arr_group_succuess = []
    arr_group_color = []
    arr_group_name = []
    tmp_template_group_code = dataJson['template_group_code']
    for x in range(len(tmp_template_group_code)):
        arr_tmp = []
        arr_tmpsidcode_0001 = []
        tmp_tgcode = tmp_template_group_code[x]
        result_data = select_1().select_query_templategroup_v1(tmp_tgcode)
        if result_data['result'] == 'OK':
            arr_tmp.append(result_data['messageText'])
        result_step_code = fucn_filter_documentgroup(arr_tmp)
        # print(result_step_code)
        if result_step_code['result'] == 'OK':
            tmp_msg = result_step_code['messageText']
            tmp_group_data = tmp_msg['group_data']
            tmp_group_step = tmp_msg['group_step']
            tmp_group_title = tmp_msg['group_title']
            tmp_email_middle = tmp_msg['email_middle']
            tmp_webhook = tmp_msg['webhook']
            tmp_color = tmp_msg['color']
            arr_color = []
            arr_color.append({'color':tmp_color})
            tmp_stepCode = tmp_msg['template_code']
            tmpcover_name = tmp_msg['group_name']
            tmpdocument_type = tmp_msg['document_type']
            tmpbizinfo = tmp_msg['bizinfo']
            tmpstatus_group = 'N'
            tmpcover_page = tmp_msg['cover_page']
            result_select = select().select_step_code_togroup_v1(tmp_stepCode)
            if result_select['result'] == 'OK':
                tmp_sidcode = result_select['messageText']['data']
                tmp_step_code = result_select['messageText']['stepcode']
                for u in range(len(tmp_sidcode)):
                    if len(tmp_sidcode[u]) != 0:
                        for y in range(len(tmp_sidcode[u])):
                            arr_tmpsidcode_0001.append(tmp_sidcode[u][y])
            if len(arr_tmpsidcode_0001) != 0:
                result_siddata = select().select_filter_sidcode_to_group_v1(arr_tmpsidcode_0001)
                if result_siddata['result'] == 'OK':
                    tmpmessge = result_siddata['messageText']
                    if tmpmessge != None:
                        arr_group_succuess.append(tmp_tgcode)
                        arr_group_color.append(tmp_color)
                        arr_group_name.append(tmpcover_name)
                        result_select_email = select().select_datajson_toemail(tmpmessge)
                        # print(result_select_email)
                        # return ''
                        result_insert = insert().insert_group_v1(tmpmessge,result_select_email['messageText'],thai_email,result_select_email['step_num_sum'],result_select_email['data_sum'],arr_color,result_select_email['email_view_group'],tmp_group_step,tmp_group_data,tmp_group_title,tmpcover_name,tmpdocument_type,tmpbizinfo,tmpstatus_group,tmpcover_page,result_select_email['calculated_fields'],result_select_email['maxstep'],tmp_email_middle,None,None,tmp_webhook)  
                        if 'result' in result_insert:
                            if result_insert['result'] == 'OK':
                                tmpgroup_id = str(result_insert['messageText']['group_id'])
                                tmpdocument_type = str(result_insert['messageText']['document_type'])
                                tmptracking_group = str(result_insert['messageText']['tracking_group'])
                                tmpgroup_color = str(result_insert['messageText']['group_color'])
                                str_hash_id = hash_512_v2(str(result_insert['messageText']['group_id']))
                                update().update_hashid_ingroup_v1(str(result_insert['messageText']['group_id']),str_hash_id)      
                                executor.submit(call_webhookService_group,tmpgroup_id)                        
                                result_update = update_4().update_group_v3(tmpmessge,tmpgroup_id)
                                r_chat = chat_sender_group_v1(str(tmpgroup_id),None)
                                if 'CS' in tmpdocument_type:
                                    call_service_BI(tmpgroup_id,'','','','','','')
                                if tmpdocument_type == 'SCS' or tmpdocument_type == 'SCST' or tmpdocument_type == 'CS' or tmpdocument_type == 'JVCS':
                                    call_service_BI(tmpgroup_id,'','','','','','')
    info_result = {
        'template_group_code':arr_group_succuess,
        'color':arr_group_color,
        'name':arr_group_name
    }
    if len(arr_group_succuess) != 0:
        return {'result':'OK','messageText':{'message':'succuess','data':info_result}}
    else:
        return {'result':'ER','messageText':{'message':'fail','data':info_result}}

@status_methods.route('/api/v1/template/manual_group',methods=['POST'])
@token_required_v3
def manual_group_v1():
    if request.method == 'POST':
        if 'Authorization' not in request.headers:
            abort(401)
        token_header = request.headers['Authorization']
        try:
            resCheck = (str(token_header).split(' ')[1])  
        except:
            abort(401)     
        token_required = token_required_func(resCheck)
        if token_required['result'] != 'OK':
            abort(401)
        username = token_required['username']
        thai_email = token_required['email']
        dataJson = request.json
        if 'template_group_code' in dataJson and len(dataJson) == 1:
            r_statusGroup = fuc_manual_group(dataJson,thai_email)
            return jsonify(r_statusGroup)
            arr_group_succuess = []
            arr_group_color = []
            arr_group_name = []
            tmp_template_group_code = dataJson['template_group_code']
            for x in range(len(tmp_template_group_code)):
                arr_tmp = []
                arr_tmpsidcode_0001 = []
                tmp_tgcode = tmp_template_group_code[x]
                result_data = select_1().select_query_templategroup_v1(tmp_tgcode)
                if result_data['result'] == 'OK':
                    arr_tmp.append(result_data['messageText'])
                result_step_code = fucn_filter_documentgroup(arr_tmp)
                if result_step_code['result'] == 'OK':
                    tmp_msg = result_step_code['messageText']
                    tmp_group_data = tmp_msg['group_data']
                    tmp_group_step = tmp_msg['group_step']
                    tmp_group_title = tmp_msg['group_title']
                    tmp_email_middle = tmp_msg['email_middle']
                    tmp_color = tmp_msg['color']
                    arr_color = []
                    arr_color.append({'color':tmp_color})
                    tmp_stepCode = tmp_msg['template_code']
                    tmpcover_name = tmp_msg['group_name']
                    tmpdocument_type = tmp_msg['document_type']
                    tmpbizinfo = tmp_msg['bizinfo']
                    tmpstatus_group = 'N'
                    tmpcover_page = tmp_msg['cover_page']
                    result_select = select().select_step_code_togroup_v1(tmp_stepCode)
                    if result_select['result'] == 'OK':
                        tmp_sidcode = result_select['messageText']['data']
                        tmp_step_code = result_select['messageText']['stepcode']
                        for u in range(len(tmp_sidcode)):
                            if len(tmp_sidcode[u]) != 0:
                                for y in range(len(tmp_sidcode[u])):
                                    arr_tmpsidcode_0001.append(tmp_sidcode[u][y])
                    # print(arr_tmpsidcode_0001)
                    if len(arr_tmpsidcode_0001) != 0:
                        result_siddata = select().select_filter_sidcode_to_group_v1(arr_tmpsidcode_0001)
                        if result_siddata['result'] == 'OK':
                            tmpmessge = result_siddata['messageText']
                            if tmpmessge != None:
                                arr_group_succuess.append(tmp_tgcode)
                                arr_group_color.append(tmp_color)
                                arr_group_name.append(tmpcover_name)
                                result_select_email = select().select_datajson_toemail(tmpmessge)
                                # return ''
                                result_insert = insert().insert_group_v1(tmpmessge,result_select_email['messageText'],thai_email,result_select_email['step_num_sum'],result_select_email['data_sum'],arr_color,result_select_email['email_view_group'],tmp_group_step,tmp_group_data,tmp_group_title,tmpcover_name,tmpdocument_type,tmpbizinfo,tmpstatus_group,tmpcover_page,result_select_email['calculated_fields'],result_select_email['maxstep'],tmp_email_middle)  
                                if 'result' in result_insert:
                                    if result_insert['result'] == 'OK':
                                        tmpgroup_id = str(result_insert['messageText']['group_id'])
                                        tmptracking_group = str(result_insert['messageText']['tracking_group'])
                                        tmpgroup_color = str(result_insert['messageText']['group_color'])
                                        str_hash_id = hash_512_v2(str(result_insert['messageText']['group_id']))
                                        update().update_hashid_ingroup_v1(str(result_insert['messageText']['group_id']),str_hash_id)                              
                                        result_update = update().update_group_v1(tmpmessge,tmpgroup_id)
                                        unique_folderFilename = tmpgroup_id
                                        path = path_global_1 + '/storage/html/' + unique_folderFilename +'/'
                                        path_indb = path_global_1 + '/storage/html/' + unique_folderFilename +'/'
                                        # path = './storage/html/' + unique_folderFilename +'/'
                                        # path_indb = '/storage/html/' + unique_folderFilename +'/'
                                        if not os.path.exists(path):
                                            os.makedirs(path)
                                        dataBi = result_select_email['data_bi']
            info_result = {
                'template_group_code':arr_group_succuess,
                'color':arr_group_color,
                'name':arr_group_name
            }
            if len(arr_group_succuess) != 0:
                return jsonify({'result':'OK','messageText':{'message':'succuess','data':info_result},'messageER':None})
            else:
                return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail','data':info_result}})
        else:
            abort(404)

@status_methods.route('/api/v1/group_document',methods=['GET'])
@token_required_v3
def document_group_api_v1():
    if request.method == 'GET':
        email_one = request.args.get('email_one')
        document_type = request.args.get('document_type')
        group_id = request.args.get('group_id')
        if email_one == None and document_type == None and group_id == None:
            abort(404)
        resul_data = select_1().select_querydocument_group_v1(email_one,document_type,group_id)
        if resul_data['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'message':'succuess','data':resul_data['messageText']},'messageER':None,'status_Code':200})
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail','data':resul_data['messageER']},'status_Code':200})

@status_methods.route('/api/v1/options/cal_gethtml',methods=['GET'])
@token_required_v3
def cal_gethtml_api_v1():
    if request.method == 'GET':
        tmpgroup_id = request.args.get('group_id')
        tmptracking_group = request.args.get('tracking_group')
        sidcode = request.args.get('sidcode')
        group_color = request.args.get('group_color')
        if group_color == None:
            group_color = ''
        infodata = {}
        if sidcode == None and group_id == None and sidcode == None:
            abort(404)
        sidcode = eval(sidcode)
        r,req = call_service_BI(tmpgroup_id,'',tmptracking_group,group_color,'','',sidcode)
        return jsonify({'status':'success','message':None,'data':r})
        result_select_email = select().select_datajson_toemail(sidcode)
        unique_folderFilename = str(uuid.uuid4())
        path = path_global_1 + '/storage/html/' + tmpgroup_id +'/'
        path_indb = path_global_1 + '/storage/html/' + tmpgroup_id +'/'
        # path = './storage/html/' + tmpgroup_id +'/'
        # path_indb = '/storage/html/' + tmpgroup_id +'/'
        if not os.path.exists(path):
            os.makedirs(path)
        dataBi = result_select_email['data_bi']
        info = {
            "group_tracking":tmptracking_group,
            "group_color":group_color,
            "group_detail":dataBi
        }
        if type_product == 'prod':
            url_BI_logic = url_bi_2 + '/calculate'
        else:
            url_BI_logic = url_bi_2 + '/calculateTest'
        resultDataBI = callPost_v3(url_BI_logic,info)
        if resultDataBI['result'] == 'OK':
            tmpmessage = resultDataBI['messageText'].json()
            if tmpmessage['message'] == 'Success':
                tmpdata = tmpmessage['data']
                if 'Warning_Detail' in tmpdata:
                    pathfile = path + unique_folderFilename + '.html'
                    with open(pathfile, 'a') as the_file:
                        the_file.write(tmpdata['Warning_Detail'])
                    infodata = {
                        'html_data':tmpdata['Warning_Detail'],
                        'html_url': myUrl_domain + 'api/v1/html?group_id=' + str(tmpgroup_id) + '&name_id=' + unique_folderFilename
                    }
        return jsonify({'status':'success','message':None,'data':infodata})

@status_methods.route('/api/v1/options/calUpload',methods=['POST'])
@token_required_v3
def calUpload_api_v1():
    if request.method == 'POST':
        dataJson = request.json
        if 'CustomerName' in dataJson and 'Status' in dataJson and 'ActualCost' in dataJson and 'Eng.Cost/Month' in dataJson and 'Revenue/Month' in dataJson and 'SaleFactors' in dataJson and 'InternalCost' in dataJson and\
            'InternalFactor' in dataJson and 'ExternalCost' in dataJson and 'ExternalFactor' in dataJson and 'SalesName' in dataJson:
            info = {
                    "group_tracking": "",
                    "group_detail": [
                    {
                        "dateTime_String": "",
                        "document_id": "",
                        "document_name": "",
                        "document_type": "",
                        "file_name": "",
                        "sender_email": "",
                        "sender_name": "",
                        "tracking_id": "",
                        "detail": dataJson
                    }
                ]
            }
            injson = {
                'status':'fail',
                'data':None,
                'message':'fail get data'
            }
            if type_product == 'prod':
                url_BI_logic = url_bi_2 + '/RecheckCal'
            else:
                url_BI_logic = url_bi_2 + '/RecheckCalTest'
            resultDataBI = callPost_v3(url_BI_logic,info)
            if resultDataBI['result'] == 'OK':
                tmp_data = resultDataBI['messageText']
                tmp_data = tmp_data.json()
                print(tmp_data)
                if 'data' in tmp_data:
                    if 'Average' in tmp_data['data']:
                        tmpdata2 = tmp_data['data']
                        tmpAverage = tmpdata2['Average']
                        tmpgroupdetail = tmpdata2['group_detail']
                        injson['data'] = tmpgroupdetail[0]['massager']
                        injson['message'] = 'success get data'
                        injson['status'] = 'success'
            return jsonify(injson)
        else:
            abort(404)


        
        
