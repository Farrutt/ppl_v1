# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from db.db_method import *
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *
from db.db_method_4 import *
from config.lib import *
from method.hashpy import *
from method.callserver import *
from method.access import *

# tmpsid_group = ['c758cb30-8fcf-49ea-b609-89b35134cfb6', '2e8d9d7d-9a92-45dc-b00a-ad03df4bfb3f', '7fe23a2c-7e77-4262-9930-f5855c76861a']
# tmp_jsondata = 
# r_update_DATA = update_3().update_DataSc_Bi_v1(tmpsid_group,tmp_jsondata)
def call_service_BI(tmpgroup_id,tmpservice_id,tmptracking_group,tmpgroup_color,process_tracking,data_document,tmpsid_group):
    sid_group = False
    messageData = None
    tmp_averagdata = None
    tmptax_type = None
    if tmpsid_group != '':
        r = select_4().select_service_id('BI')
        tmpservice_id = r['data'][0]['code']
        sid_group = True
        result_data = select().select_datajson_toemail(tmpsid_group)
        result_group = select_3().select_trackinggroup_v1(tmpgroup_id)
        if result_group['result'] == 'OK':
            tmptracking_group = result_group['tracking_group']
            tmpgroup_color = result_group['group_color']
            tmpsid_group = result_group['sid_group']
            # if 'tax_type' in result_group:
            tmptax_type = result_group['tax_type']
            result_data = select().select_datajson_toemail(tmpsid_group)
            dataBi = result_data['data_bi']
            data_document = result_data['data_document']
        # print(result_data)
        dataBi = result_data['data_bi']
        data_document = result_data['data_document']
    if tmpgroup_id != '' and tmpsid_group == '':        
        r = select_4().select_service_id('BI')
        tmpservice_id = r['data'][0]['code']
        result_group = select_3().select_trackinggroup_v1(tmpgroup_id)
        # print(result_group)
        if result_group['result'] == 'OK':
            tmptracking_group = result_group['tracking_group']
            tmpgroup_color = result_group['group_color']
            tmpsid_group = result_group['sid_group']
            tmptax_type = result_group['tax_type']
            result_data = select().select_datajson_toemail(tmpsid_group)
            dataBi = result_data['data_bi']
            data_document = result_data['data_document']
    if process_tracking == '':
        process_tracking = 'Summary_Costsheet'
    info = {
        "group_tracking":tmptracking_group,
        "group_color":tmpgroup_color,
        "process_tracking":process_tracking,
        "data":data_document
    }
    tmpDataBi = encode_secret_key(tmpservice_id,info)
    if tmpDataBi['result'] == 'OK':
        tmpmessageText = tmpDataBi['messageText']
    info_bi = {
        'service_id':tmpservice_id,
        'data_encode':tmpmessageText
    }    
    unique_folderFilename = tmpgroup_id
    path = path_global_1 +'/storage/html/' + unique_folderFilename +'/'
    path_indb = path_global_1 + '/storage/html/' + unique_folderFilename +'/'
    path = './storage/html/' + unique_folderFilename +'/'
    path_indb = '/storage/html/' + unique_folderFilename +'/'
    if not os.path.exists(path):
        os.makedirs(path)
    if 'INET' in tmptax_type:
        url_BI_logic = url_bi_cs + '/api/v4000/calculate'
    elif 'JV' in tmptax_type:        
        url_BI_logic = url_bi_cs_jv + '/api/vjv/calculate'
    resultDataBI = callPost_v3(url_BI_logic,info_bi)
    if resultDataBI['result'] == 'OK' and sid_group == False:
        messageData = resultDataBI['messageText'].json()
        if messageData['message'] == 'success':
            tmpdata = messageData['data']
            if tmpdata != None:
                if 'HTML' in tmpdata and 'JSON' in tmpdata:
                    pathfile = path + unique_folderFilename + '.html'
                    tmp_jsondata = tmpdata['JSON']
                    tmp_htmldata = tmpdata['HTML']
                    if 'averag' in tmpdata:
                        tmp_averagdata = tmpdata['averag']
                    try:
                        with open(pathfile, 'a') as the_file:
                            the_file.write(tmpdata['HTML'])
                        r_update_HTML = update_3().update_HtmlData_Bi_v1(tmpgroup_id,tmp_htmldata,tmp_jsondata,tmp_averagdata)
                        r_update_DATA = update_3().update_DataSc_Bi_v1(tmpsid_group,tmp_jsondata)
                    except Exception as e:
                        pass
        res = {'result':'OK','data':messageData}
    elif resultDataBI['result'] == 'OK' and sid_group == True:
        datamessage = resultDataBI['messageText'].json()
        if datamessage['message'] == 'success':
            tmpdata = datamessage['data']
            if tmpdata != None:
                if 'HTML' in tmpdata and 'JSON' in tmpdata:
                    pathfile = path + unique_folderFilename + '.html'
                    tmp_jsondata = tmpdata['JSON']
                    tmp_htmldata = tmpdata['HTML']
        messageData = {
            'html_data':tmp_htmldata,
            'html_url': myUrl_domain + 'api/v1/html?group_id=' + str(tmpgroup_id) + '&name_id=' + unique_folderFilename
        }
        res = {'result':'OK','data':messageData}
    else:
        messageData = resultDataBI['messageText'].json()
        res = {'result':'ER','data':messageData}
    return messageData,info_bi


def call_service_QT_BI(sid):
    if type_product == 'prod':
        url = 'http://203.154.135.51:5006/quatation_th'
    elif type_product == 'uat':
        url = 'http://uatservicereport.one.th:5002/quatation_th'
    resp_data = select_1().select_info_document(sid)
    if resp_data['result'] == 'OK':
        tmp_query = resp_data['messageText']
        for x in range(len(tmp_query)):
            tmp_query[x]['update_time'] = str(tmp_query[x]['update_time']).split('+')[0]
            result = data_doc(tmp_query[x]['data_document'])
            if result['result'] == 'OK':
                if result['messageText']['sub'] == 'eformppl':
                    tmp_query[x]['data_document'] = result
                    tmp_query[x]['data_document'] = tmp_query[x]['data_document']['messageText']['formdata_eform']['data_json_key']
                    for y in range(len(tmp_query[x]['data_document'])):
                        tmp_query[x]['data_document'][y]['ppl_document_id'] = tmp_query[x]['doc_id']
                        tmp_query[x]['data_document'][y]['datetime_approve'] = tmp_query[x]['update_time']
                    data_json = tmp_query[x]['data_document']
                    if data_json != None:
                        r_call = callPost_Test(url,data_json)
                        if r_call['result'] == 'OK':
                            tmpmessageText = r_call['messageText'].json()
                            print(tmpmessageText)
                            if tmpmessageText['message'] == 'success':
                                return {'result':'OK'}
                        return {'result':'ER'}
                    else:
                        return {'result':'ER','messageText':'data fail'}
                else:
                    return {'result':'ER','messageText':'document The document was not sent efrom'}
            else:
                return {'result':'ER','messageText':'Decoding error'}
# call_service_QT_BI('6b7961ec-253b-4da1-968c-90ed4ef52433')

def call_service_SCS_RPA(sid):
    resp_data = select_1().select_info_document(sid)
    if resp_data['result'] == 'OK':
        tmp_query = resp_data['messageText']
        for x in range(len(tmp_query)):
            tmp_query[x]['update_time'] = str(tmp_query[x]['update_time']).split('+')[0]
            result = data_doc(tmp_query[x]['data_document'])
            if result['result'] == 'OK':
                tmp_sub = result['messageText']['sub']
                return tmp_sub
                    
def call_service_terminate_BI(sid):
    if type_product == 'uat':
        url = 'http://203.154.135.35:5004/terminate'
    elif type_product == 'prod':
        url = 'http://203.154.135.51:5005/terminate'
    resp_data = select_1().select_info_document(sid)
    if resp_data['result'] == 'OK':
        tmp_query = resp_data['messageText']
        for x in range(len(tmp_query)):
            if 'update_time' in tmp_query[x]:
                tmp_query[x]['update_time'] = str(tmp_query[x]['update_time']).split('+')[0]
                result = data_doc(tmp_query[x]['data_document'])
                doc_id = (tmp_query[x]['doc_id'])
                dict_ppl = {"paperlessNo.":str(doc_id)}
                if result['result'] == 'OK':
                    tmp_sub = result['messageText']['sub']
                    if tmp_sub == 'eformppl':
                        tmp_json = result['messageText']
                        data_json_key = tmp_json['formdata_eform']['data_json_key']
                        # print ('data_json_key:',data_json_key)
                        for i in range(len(data_json_key)):
                            print (type(data_json_key[i]))
                            data_json_key[i].update(dict_ppl)
                            # print (data_json_key[i])
                        # print (tmp_json)
                        result_call_serv = callPost_Test(url,tmp_json)
                        # print ('result_call_serv:',result_call_serv['messageText'].json())
                        if result_call_serv['result'] == 'OK':
                            tmpmessageText = result_call_serv['messageText'].json()
                            if tmpmessageText['message'] == 'success':
                                return {'result':'OK'}
                        return {'result':'ER'}
                    else:
                        return {'result':'ER','messageText':'document The document was not sent efrom'}
                else:
                    return {'result':'ER','messageText':'Decoding error'}
            else:
                return {'result':'ER','messageText':'udate time fail'}
