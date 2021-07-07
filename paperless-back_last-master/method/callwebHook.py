#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config.lib import *
from config.value import *
from db.db_method import *
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *
from db.db_method_4 import *
from db.db_method_5 import *

def call_webhookService(sid_code):
    data = {
        "name_service":"WEBHOOK"
    }
    response = ''
    result_select = select().select_ForWebHook(sid_code)
    if result_select['result'] == 'OK' and str(result_select['messageText']['webHook']).replace(' ','') != '':
        del(result_select['messageText']['email_center'])
        webhook_Data = result_select['messageText']
        url = result_select['messageText']['webHook']
        parsed = urlparse.urlparse(url)
        if 'cid' in parse_qs(parsed.query):  
            r_OTHERs = call_serviceOTHERs(sid_code)
            # print(r_OTHERs['result'])
            for u in range(len(r_OTHERs['data'])):
                tmpdata = r_OTHERs['data'][u]
                tmpUrl = tmpdata['url']
                tmp_Data = tmpdata['data']
                try:
                    response = requests.post(tmpUrl, json=tmpdata,headers={'Content-Type': 'application/json'},verify=False)
                    insert().insert_tran_log_v1(str(response),'OK',str(tmpdata),tmpUrl,"")
                    info_r = {"service":data['name_service'] + '_PDF_Service',"status":True,"message":'success ' + str(response.text)}
                except requests.HTTPError as err:
                    pass
                    insert().insert_tran_log_v1(str(response),'ER',str(tmpdata),tmpUrl,"")
                    info_r = {"service":data['name_service'] + '_PDF_Service',"status":False,"message":str(err)}
                except requests.Timeout as err:
                    pass
                    insert().insert_tran_log_v1(str(response),'ER',str(tmpdata),tmpUrl,"")
                    info_r = {"service":data['name_service'] + '_PDF_Service',"status":False,"message":str(err)}
                except requests.ConnectionError as err:
                    pass
                    insert().insert_tran_log_v1(str(response),'ER',str(tmpdata),tmpUrl,"")
                    info_r = {"service":data['name_service'] + '_PDF_Service',"status":False,"message":str(err)}
                except Exception as err:
                    pass
                    insert().insert_tran_log_v1(str(response),'ER',str(tmpdata),tmpUrl,"")
                    info_r = {"service":data['name_service'] + '_PDF_Service',"status":False,"message":str(err)}
            return (info_r)

def call_webhookService_group(group_id):
    data = {
        "name_service":"Group_WEBHOOK"
    }
    response = ''
    r_OTHERs = call_serviceOTHERs_Group(group_id)
    if r_OTHERs['result'] != 'ER':
        for u in range(len(r_OTHERs['data'])):
            tmpdata = r_OTHERs['data'][u]
            tmpUrl = tmpdata['url']
            tmp_Data = tmpdata['data']
            try:
                response = requests.post(tmpUrl, json=tmpdata,headers={'Content-Type': 'application/json'},verify=False)
                insert().insert_tran_log_v1(str(response),'OK',str(tmpdata),tmpUrl,"")
                info_r = {"service":data['name_service'] + '_PDF_Service',"status":True,"message":'success ' + str(response.text)}
            except requests.HTTPError as err:
                pass
                insert().insert_tran_log_v1(str(response),'ER',str(tmpdata),tmpUrl,"")
                info_r = {"service":data['name_service'] + '_PDF_Service',"status":False,"message":str(err)}
            except requests.Timeout as err:
                pass
                insert().insert_tran_log_v1(str(response),'ER',str(tmpdata),tmpUrl,"")
                info_r = {"service":data['name_service'] + '_PDF_Service',"status":False,"message":str(err)}
            except requests.ConnectionError as err:
                pass
                insert().insert_tran_log_v1(str(response),'ER',str(tmpdata),tmpUrl,"")
                info_r = {"service":data['name_service'] + '_PDF_Service',"status":False,"message":str(err)}
            except Exception as err:
                pass
                insert().insert_tran_log_v1(str(response),'ER',str(tmpdata),tmpUrl,"")
                info_r = {"service":data['name_service'] + '_PDF_Service',"status":False,"message":str(err)}
        return (info_r)

def call_serviceGroup(sid_code):
    pass

def call_serviceOTHERs(sid_code):
    tmparrresult = []
    r_webhook = select_4().select_ForWebHook_v2(sid_code)
    # return r_webhook
    if r_webhook['result'] == 'OK':
        tmpdata = r_webhook['messageText']
        url = tmpdata['webHook']
        try:
            tmpurl = url.split('|')
        except Exception as e:
            tmpurl = url
        tmpdata_01 = []
        for n in range(len(tmpurl)):
            url = tmpurl[n]
            tmpdata['webHook'] = url
            parsed = urlparse.urlparse(url)
            if 'cid' in parse_qs(parsed.query):
                tmpcid = parse_qs(parsed.query)['cid'][0]
                r = select_4().select_service_id(tmpcid)
                tmpservice_id = r['data'][0]['code']
                tmpData = encode_secret_key(tmpservice_id,tmpdata)
                if tmpData['result'] == 'OK':
                    url = url + '&service_id=' + tmpservice_id
                    tmparrresult.append({'result':'OK','data':tmpData['messageText'],'url':url})
        return {'result':'OK','data':tmparrresult}

def call_serviceOTHERs_Group(group_id):
    tmparrresult = []
    try:
        r_webhook = select_4().select_ForWebHook_group_v1(group_id)
        # return r_webhook
        if r_webhook['result'] == 'OK':
            tmpdata = r_webhook['messageText']['group_detail']
            url = tmpdata['group_webhook']
            try:
                tmpurl = url.split('|')
            except Exception as e:
                tmpurl = url
            for n in range(len(tmpurl)):
                url = tmpurl[n]
                parsed = urlparse.urlparse(url)
                if 'cid' in parse_qs(parsed.query):
                    tmpcid = parse_qs(parsed.query)['cid'][0]
                    r = select_4().select_service_id(tmpcid)
                    tmpservice_id = r['data'][0]['code']
                    tmpData = encode_secret_key(tmpservice_id,tmpdata)
                    if tmpData['result'] == 'OK':
                        url = url + '&service_id=' + tmpservice_id
                        tmparrresult.append({'result':'OK','data':tmpData['messageText'],'url':url})
            return {'result':'OK','data':tmparrresult}
        return {'result':'ER'}
    except Exception as e:
        return {'result':'ER'}

def call_lineNotify(strtext):
    url = 'https://notify-api.line.me'
    
    multipart_data = MultipartEncoder(
        fields={
                'message':strtext
            }
    )
    headers = {
        'content-type': multipart_data.content_type,
        'Authorization': "Bearer SA2nV7C9oiQhr0hYFdIWbm5q3lWJP77smluT9Y4ZjBT",
        'cache-control': "no-cache"
    }
    response = requests.post(url + '/api/notify', data=multipart_data,headers=headers)
    # payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"message\"\r\n\r\n" + strtext + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    
    # response = requests.request("POST", url + '/api/notify', data=payload, headers=headers,verify=False)

def callWebHook_slack_v1(err_message,request_data,url_data):
    try:
        payload = {
            "blocks": [
                {
                    "type": "section",
                    "block_id": "section789",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Notification*\n" + err_message
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": '' +  '\n\n url ' + url_data
                    }
                }
            ]
        }
        headers = {
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url_slack, json=payload, headers=headers)
        # response.raise_for_status()
        print(response.text)
        return response.json()
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