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

@status_methods.route('/api/v3/group_doc_v2',methods=['GET'])
@token_required_v3
def document_group_api_group_doc_v2():
    if request.method == 'GET':
        email_one = request.args.get('email_one')
        # document_type = request.args.get('document_type')
        group_id = request.args.get('group_id')
        tax_id = request.args.get('tax_id')
        status = request.args.get('status')
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        keyword = request.args.get('keyword')
        if email_one == None and group_id == None and tax_id == None:
            abort(404)
        resul_data = select_2().select_querydoc_group_version2(email_one,group_id,tax_id,status,limit,offset,keyword)
        if resul_data['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'message':'succuess','data':resul_data['messageText']},'messageER':None,'status_Code':200})
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail','data':resul_data['messageER']},'status_Code':200})



def fuc_manual_group_v2(dataJson,tmpemail=None):
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
    # วนเลข template group ตามค่า api ที่รับเข้ามา
    for x in range(len(tmp_template_group_code)):
        arr_tmp = []
        arr_tmpsidcode_0001 = []
        tmp_tgcode = tmp_template_group_code[x]
        result_data = select_1().select_query_templategroup_v2(tmp_tgcode)
        if result_data['result'] == 'OK':
            arr_tmp.append(result_data['messageText'])
        print('arr_tmp',arr_tmp)
        result_step_code = fucn_filter_documentgroup_v2(arr_tmp)
        # print(result_step_code)
        # return result_step_code
        if result_step_code['result'] == 'OK':
            tmp_msg = result_step_code['messageText']
            # tmp_group_data = tmp_msg['group_data']
            tmp_group_data = None
            tmp_group_step = tmp_msg['group_step']
            tmp_group_title = tmp_msg['group_title']
            tmp_email_middle = tmp_msg['email_middle']
            tmp_color = tmp_msg['color']
            arr_color = []
            arr_color.append({'color':tmp_color})
            tmp_stepCode = tmp_msg['template_code']
            tmpcover_name = tmp_msg['group_name']
            tmpbizinfo = tmp_msg['bizinfo']
            tmpstatus_group = 'N'
            tmp_emailStep = []
            if 'email_step' in tmp_msg:
                tmp_emailStep = tmp_msg['email_step']
            print('tmp_emailStep',tmp_emailStep)
            # tmpcover_page = tmp_msg['cover_page']
            tmpcover_page = ''
            # ส่ง step_code เข้าไปหา
            result_select = select_1().select_step_code_togroup_v2(tmp_stepCode)
            if result_select['result'] == 'OK':
                # หมายเลขเอกสาร
                tmp_sidcode = result_select['messageText']['data']
                # หมายเลข template
                tmp_step_code = result_select['messageText']['stepcode']
                for u in range(len(tmp_sidcode)):
                    if len(tmp_sidcode[u]) != 0:
                        for y in range(len(tmp_sidcode[u])):
                            arr_tmpsidcode_0001.append(tmp_sidcode[u][y])
            if len(arr_tmpsidcode_0001) != 0:
                result_siddata = select_1().select_filter_sidcode_to_group_v2(arr_tmpsidcode_0001,tmp_emailStep)
                if result_siddata['result'] == 'OK':
                    tmpmessge = result_siddata['messageText']
                    tmpstep_arr = result_siddata['tmp_step']
                    tmp_OneMail_Now = result_siddata['tmp_OneMail_Now']
                    # tmp_group_data = result_siddata['tmp_statusGroup']
                    tmp_doctypeGroup = result_siddata['tmp_doctypeGroup']
                    tmp_bizinfo = result_siddata['tmp_bizinfo']
                    tmp_maxstep = result_siddata['tmp_maxstep']
                    arr_string_options_page = result_siddata['arr_string_options_page']
                    arr_emailCenter = result_siddata['arr_emailCenter']
                    result_sum = sum_doc_name_group_v2(tmp_doctypeGroup)
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
                    tmp_email_middle = str(arr_emailCenter)
                    if tmpmessge != None:
                        arr_group_succuess.append(tmp_tgcode)
                        arr_group_color.append(tmp_color)
                        arr_group_name.append(tmpcover_name)
                        # print('tmpmessge',tmpmessge)
                        result_select_email = select_1().select_datajson_toemail_v2(tmpmessge)
                        tmp_statusGroup = []
                        tmp_emailStep = eval(tmp_emailStep)
                        for q in range(len(tmp_emailStep)):
                            name_one = fine_name_surename(tmp_emailStep[q])
                            emailOneStep = tmp_emailStep[q]
                            statusOneStep = 'Incomplete'
                            nameOneStep = name_one
                            dict_statusGroup = {
                                'email_one' : [emailOneStep],
                                'name_one': [nameOneStep],
                                'status': 'Incomplete'
                            }
                            tmp_statusGroup.append(dict_statusGroup)
                        tmp_group_data = str(tmp_statusGroup)
                        # print('result_select_email',result_select_email)
                        result_insert = insert_1().insert_group_v2(tmpmessge,tmp_OneMail_Now,thai_email,tmpstep_arr,result_select_email['data_sum'],arr_color,result_select_email['email_view_group'],tmp_group_step,tmp_group_data,tmp_group_title,tmpcover_name,tmpbizinfo,tmpstatus_group,tmpcover_page,result_select_email['calculated_fields'],tmp_maxstep,tmp_email_middle,tmp_doctypeGroup,tmp_bizinfo,arr_string_options_page)  
                        if 'result' in result_insert:
                            if result_insert['result'] == 'OK':
                                tmpgroup_id = str(result_insert['messageText']['group_id'])
                                tmptracking_group = str(result_insert['messageText']['tracking_group'])
                                tmpgroup_color = str(result_insert['messageText']['group_color'])
                                str_hash_id = hash_512_v2(str(result_insert['messageText']['group_id']))
                                update_1().update_docdetail_optionpage(tmpmessge,tmpstep_arr)
                                update_1().update_hashid_ingroup_v2(str(result_insert['messageText']['group_id']),str_hash_id)                              
                                result_update = update_1().update_group_v2(tmpmessge,tmpgroup_id)
                                r_chat = chat_sender_group_v2(str(tmpgroup_id),None)
                                # if tmpdocument_type == 'SCS' or tmpdocument_type == 'SCST' or tmpdocument_type == 'CS':
                                #     call_service_BI(tmpgroup_id,'','','','','','')
                                
                                    # tmpservice_id = None                  
                                    # if r['result'] =='OK':
                                    #     tmpservice_id = r['data'][0]['code']
                                    
                                    # info = {
                                    #     "group_tracking":tmptracking_group,
                                    #     "group_color":tmpgroup_color,
                                    #     "process_tracking":"Summary_Costsheet",
                                    #     "data":data_document
                                    # }
                                    
                                    # resultDataBI = callPost_v3(url_BI_logic,info)
                                    # if resultDataBI['result'] == 'OK':
                                    #     tmpmessage = resultDataBI['messageText'].json()
                                        
                                
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
                                #         if 'Warning_Detail' in tmpdata and 'Warning_json' in tmpdata:
                                #             pathfile = path + unique_folderFilename + '.html'
                                #             tmp_jsondata = tmpdata['Warning_json']
                                #             try:
                                #                 with open(pathfile, 'a') as the_file:
                                #                     the_file.write(tmpdata['Warning_Detail'])
                                #                 update_3().update_HtmlData_Bi_v1(tmpgroup_id,tmpdata['Warning_Detail'],tmp_jsondata)
                                #             except Exception as e:
                                #                 pass
    info_result = {
        'template_group_code':arr_group_succuess,
        'color':arr_group_color,
        'name':arr_group_name
    }
    print('info_result',info_result)
    if len(arr_group_succuess) != 0:
        return {'result':'OK','messageText':{'message':'succuess','data':info_result}}
    else:
        return {'result':'ER','messageText':{'message':'fail','data':info_result}}


@status_methods.route('/api/v1/find_name',methods=['POST'])
def find_name():
    if request.method == 'POST':
        dataJson = request.json
        if 'email_one' in dataJson and len(dataJson) == 1:
            email_one = dataJson['email_one']
            result_select = fine_name_surename_list(email_one)
            return jsonify({'result': 'OK', 'messageText': result_select, 'status_Code': 200}), 200
        else:
            abort(404)

@status_methods.route('/api/update_signature_group_v2', methods=['POST'])
@token_required_v2
def update_signature_group_api_version2(username,email_thai,token_Code):
    dataJson = request.json
    if 'group_id' in dataJson and 'email_one' in dataJson and 'sign_base' in dataJson:
        tmpgroup_id = dataJson['group_id']
        tmpemail_one = dataJson['email_one']
        tmpsign_base = dataJson['sign_base']
        result_update = update_2().update_signature_group_version2(tmpgroup_id,tmpemail_one,tmpsign_base)
        if result_update['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'message':'success','data':None},'status_Code':200,'messageER':None}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'fail ' + result_update['messageText'],'data':None,'code':'ERUSG001'}}),200


@status_methods.route('/api/update_pdf_group_v2', methods=['PUT'])
@token_required_v2
def update_pdf_group_api_version2(username,email_thai,token_Code):
    dataJson = request.json
    if 'pdf_data' in dataJson and 'group_id' in dataJson and len(dataJson) == 2:
        tmp_pdfdata = dataJson['pdf_data']
        tmp_groupid = dataJson['group_id']
        # tmp_data = dataJson['data']
        result_update = update_2().update_pdf_ingroup_verson2(tmp_groupid,tmp_pdfdata,email_thai)
        if result_update['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'data':None,'message':'success'},'messageER':None,'status_Code':200}),200
        else:            
            return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'fail'},'status_Code':200}),200    
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':None,'code':'ERCG999'}}),404



@status_methods.route('/api/save_pdf_group_v2', methods=['POST'])
@token_required_v2
def save_pdf_group_api_version2(username,email_thai,token_Code):
    dataJson = request.json
    if 'pdf_data' in dataJson and 'group_id' in dataJson and len(dataJson) == 2:
        tmp_pdfdata = dataJson['pdf_data']
        tmp_groupid = dataJson['group_id']
        result_insert = insert_2().insert_pdf_togroup_version2(tmp_groupid,tmp_pdfdata)
        if result_insert['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'data':None,'message':'success'},'messageER':None,'status_Code':200}),200
        else:            
            return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'fail'},'status_Code':200}),200
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':None,'code':'ERCG999'}}),404

# reject
@status_methods.route('/api/remove_document_ingroup_v2', methods=['POST'])
def remove_document_ingroup_api_forVersion2():    
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
    if 'sidcode' in dataJson and 'group_id' in dataJson and 'category_type' in dataJson and 'key' in dataJson and 'step_num' in dataJson:
        if result_data['result'] == 'OK':
            tmpemail = result_data['email']
            tmpusername = result_data['username']
            tmpemail = result_data['email']
            tmpuser_id = result_data['user_id']
            tmpcitizen = result_data['citizen_data']
        tmp_sidcode = dataJson['sidcode']
        tmp_groupid = dataJson['group_id']
        tmpcategory_type = str(dataJson['category_type']).lower()
        tmp_step_num = dataJson['step_num']
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
                result_update = update_2().update_toremove_document_ingroup_version2(tmp_sidcode,tmp_groupid,tmpemail)
                for z in range(len(tmp_sidcode)):
                    check_update = update().update_step_v4_group(tmp_sidcode[z],tmpemail,'A03',tmpcatype_string,0.0,0.0,tmp_step_num[z])
                if result_update['result'] == 'OK':
                    result_select_email = select().select_datajson_toemail(result_update['tmpsid'])
                    unique_folderFilename = tmp_groupid
                    path = path_global_1 + '/storage/html/' + unique_folderFilename +'/'
                    path_indb = path_global_1 + '/storage/html/' + unique_folderFilename +'/'
                    if not os.path.exists(path):
                        os.makedirs(path)
                    resultTracking = select_3().select_trackinggroup_v1(dataJson['group_id'])
                    dataBi = result_select_email['data_bi']
                    # info = {
                    #     "group_tracking":resultTracking['tracking_group'],
                    #     "group_color":resultTracking['group_color'],
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
                    #             tmp_jsondata = tmpdata['Warning_json']
                    #             try:
                    #                 with open(pathfile, 'a') as the_file:
                    #                     the_file.write(tmpdata['Warning_Detail'])
                    #                 update_3().update_HtmlData_Bi_v1(tmp_groupid,tmpdata['Warning_Detail'])
                    #             except Exception as e:
                    #                 pass
                    return jsonify({'result':'OK','messageText':{'message':'success','data':None},'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'fail','data':None,'code':'ERRIG001'}}),200
            else:
                result_update = update().update_changestatusgroup_v1(tmp_sidcode)
                result_update = update_2().update_toremove_document_ingroup_version2(tmp_sidcode,tmp_groupid,tmpemail)
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
                    # info = {
                    #     "group_tracking":resultTracking['tracking_group'],
                    #     "group_color":resultTracking['group_color'],
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
                    #             tmp_jsondata = tmpdata['Warning_json']
                    #             try:
                    #                 with open(pathfile, 'a') as the_file:
                    #                     the_file.write(tmpdata['Warning_Detail'])
                    #                 update_3().update_HtmlData_Bi_v1(tmp_groupid,tmpdata['Warning_Detail'])
                    #             except Exception as e:
                    #                 pass
                    return jsonify({'result':'OK','messageText':{'message':'success','data':None},'status_Code':200,'messageER':None}),200
                else:
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':{'message':'fail','data':None,'code':'ERRIG002'}}),200
        else:
            return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'key incorrect','data':None,'code':'ERRIG999'}}),404
    else:
        return jsonify({'result':'ER','messageText':None,'status_Code':404,'messageER':{'message':'parameter incorrect','data':None,'code':'ERRIG999'}}),404




@status_methods.route('/api/get/group2',methods=['GET'])
def getlist_group2():
    try:
        username = request.args.get('username')
        tax_id = request.args.get('tax_id')
        id_data = request.args.get('id')
        result_group_template = select_2().select_tmpgroup_list_2(username,tax_id,id_data)
        if result_group_template['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'message':'success','data':result_group_template['messageText']} ,'messageER':None,'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail ' + result_group_template['messageER'],'data':None},'status_Code':200})
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'result':'ER','status_Code':200,'messageText':None,'messageER':{'data':None,'message':str(e)}}),200

@status_methods.route('/api/get_tmpgroup2',methods=['GET'])
def checkout():
    result = select_1().select_tmpAllBiz()
    return jsonify({'result':'OK','messageText':result}),200

# insert group document version2 ไม่มี document_type
@status_methods.route('/api/v2/template/manual_group',methods=['POST'])
@token_required_v3
def manual_group_v2():
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
            r_statusGroup = fuc_manual_group_v2(dataJson,thai_email)
            return jsonify(r_statusGroup)
        else:
            abort(404)


# group_documet version2 แบบไม่มี document_type
@status_methods.route('/api/v3/group_document/sum',methods=['GET'])
@token_required_v3
def document_group_api_sum_nodocumenttype():
    if request.method == 'GET':
        email_one = request.args.get('email_one')
        tax_id = request.args.get('tax_id')
        keyword = request.args.get('keyword')
        if email_one == None and tax_id == None:
            abort(404)
        resul_data = select_1().select_querydocument_group_sum_v2(email_one,tax_id,keyword)
        if resul_data['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'message':'succuess','data':resul_data['messageText']},'messageER':None,'status_Code':200})
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail','data':resul_data['messageER']},'status_Code':200})

@status_methods.route('/api/v3/group_document',methods=['GET'])
@token_required_v3
def document_group_api_nodocumenttype():
    if request.method == 'GET':
        email_one = request.args.get('email_one')
        # document_type = request.args.get('document_type')
        group_id = request.args.get('group_id')
        tax_id = request.args.get('tax_id')
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        keyword = request.args.get('keyword')
        if email_one == None and group_id == None and tax_id == None:
            abort(404)
        resul_data = select_1().selectGroupDocument_version2(email_one,group_id,tax_id,limit,offset,keyword)
        if resul_data['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'message':'succuess','data':resul_data['messageText']},'messageER':None,'status_Code':200})
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':{'message':'fail','data':resul_data['messageER']},'status_Code':200})

