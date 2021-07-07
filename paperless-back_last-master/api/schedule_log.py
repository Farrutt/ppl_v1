from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from method.callserver import *
from method.hashpy import *
from method.verify import *
from db.db_method import *
from db.db_method_1 import *
from db.db_method_2 import *
from db.db_method_3 import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.login import *
from api.group_api import *
from api.group_v2 import *
import os
from datetime import date
import datetime

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less


def callPost_v2_test(path, data,start_time):
    url = path
    payload = data

    todays = (date.today())
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    date_today = datetime.datetime.strptime(str(todays),"%Y-%m-%d").strftime("%d-%m-%Y")

    try:
        response = requests.post(url=url, json=payload, verify=False, stream=True)
        payload['password'] = ''
        if response.status_code == 200 or response.status_code == 201:
            time_sec = "{0:.2f}".format((time.time() - start_time))
            time_millisec = int((time.time() - start_time)*1000)
            day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
            text_to_log = day_n_time + one_url+"/api/oauth/getpwd" + ' {status: Success' + '}' + '(OneId) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec '+ str(response.status_code)
            save_log2(text_to_log)

            return {'result': 'OK','messageText': response,'status_Code':response.status_code}
            
        else:
            error_except('ER',str(response.text),'service oneAuth',response.status_code)
            time_sec = "{0:.2f}".format((time.time() - start_time))
            time_millisec = int((time.time() - start_time)*1000)
            day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
            text_to_log = day_n_time + one_url+"/api/oauth/getpwd" + ' {status: Error' + '}' + '(OneId) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec '+ str(response.status_code)
            save_log2(text_to_log)

            return {'result': 'ER','messageText': response,'status_Code':response.status_code}
    except requests.HTTPError as err:
        error_except(err,"HTTP error occurred.",'service oneid',response.status_code)
        return {'result': 'ER','messageText': "HTTP error occurred.",'status_Code':response.status_code}
    except requests.Timeout as err:
        error_except(err,"Request timed out",'service oneid',response.status_code)
        return {'result': 'ER','messageText': 'Request timed out','status_Code':response.status_code}
    except requests.ConnectionError as err:
        error_except(err,"API Connection error occurred.",'service oneid',response.status_code)
        return {'result': 'ER','messageText': 'API Connection error occurred.','status_Code':response.status_code}
    except Exception as err:
        error_except(err,"An unexpected error",'service oneid',response.status_code)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err),'status_Code':response.status_code}

def callGET_v2_test(path, data,start_time,token_header):
    url = path
    payload = data
    count_err = 0
    error_list = []
    send_chat_list = []
    count_error = 0
    message_text = None
    
    message_send_all = ''
    
    todays = (date.today())
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    date_today = datetime.datetime.strptime(str(todays),"%Y-%m-%d").strftime("%d-%m-%Y")

    try:
        response = requests.get(url=url,headers={'Authorization': payload}, verify=False, stream=True)
        tmp_payload_token = str(payload).split(' ')[1]
        if response.status_code == 200 or response.status_code == 201:

            time_sec = "{0:.2f}".format((time.time() - start_time))
            time_millisec = int((time.time() - start_time)*1000)
            day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
            text_to_log = day_n_time + one_url +"/api/account_and_biz_detail" + ' {status: Success' + '}' + '(OneId) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec '+ str(response.status_code)
            save_log2(text_to_log)

            return {'result': 'OK','messageText': response,'stastus_Code':response.status_code,'error_list':error_list,'count_error':count_error}
        
        else:
            time_sec = "{0:.2f}".format((time.time() - start_time))
            time_millisec = int((time.time() - start_time)*1000)
            message_send = url + ' ,service oneid ' + ',status: ' + str(response.status_code)
            message_text = 'แจ้งเตือน \n %s \n เวลา(sec) : %s \n เวลา(Millisec) : %s \n การส่งข้อมูลครั้งที่ : %s ' %(message_send,(str(time_sec)),(str(time_millisec)),(str(1)))
            send_chat_list.append(message_text)

            day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
            text_to_log = day_n_time + one_url +"/api/account_and_biz_detail" + ' {status: Error' + '}' + '(OneId) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec '+ str(response.status_code)
            save_log2(text_to_log)

            for cG in range (2) :
                response = requests.get(url=url,headers={'Authorization': payload}, verify=False, stream=True)
                if response.status_code == 200 :
                    count_error += 1
            
                    for x in range(len(send_chat_list)):
                        message_send_all += send_chat_list[x]
                        message_send_all += '\n'

                    time_sec = "{0:.2f}".format((time.time() - start_time))
                    time_millisec = int((time.time() - start_time)*1000)
                    send_messageToChat_v4_2(message_send_all,start_time,cG+2,token_header)

                    day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
                    text_to_log = day_n_time + one_url +"/api/account_and_biz_detail" + ' {status: Success' + '}' + '(OneId) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec '+ str(response.status_code)
                    save_log2(text_to_log)

                    return {'result':'OK','msg':response.json(),'status_Code':response.status_code,'error_list':error_list,'count_error':count_error}

                else:
                    err = error_except('ER',response.json(),'service oneid',response.status_code)
                    error_list.append(err)

                    time_sec = "{0:.2f}".format((time.time() - start_time))
                    time_millisec = int((time.time() - start_time)*1000)
                    message_send = url + ' ,service oneid ' + ',status: ' + str(response.status_code)
                    message_text = '\n แจ้งเตือน \n %s \n เวลา(sec) : %s \n เวลา(Millisec) : %s \n การส่งข้อมูลครั้งที่ : %s ' %(message_send,(str(time_sec)),(str(time_millisec)),(str(cG+2)))
                    send_chat_list.append(message_text)

                    day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
                    text_to_log = day_n_time + one_url +"/api/account_and_biz_detail" + ' {status: Error' + '}' + '(OneId) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec '+ str(response.status_code)
                    save_log2(text_to_log)
                    
                count_error += 1
            
            for x in range(len(send_chat_list)):
                message_send_all += send_chat_list[x]
                message_send_all += '\n'

            send_messageToChat_v4_2(message_send_all,start_time,cG+2,token_header)
                
            return {'result': 'ER','messageText': response,'stastus_Code':response.status_code,'error_list':error_list,'count_error':count_error}
    except requests.HTTPError as err:
        
        error_except(err,"HTTP error occurred.",'service oneid',response.status_code)
        return {'result': 'ER','messageText': "HTTP error occurred.",'stastus_Code':response.status_code}
    except requests.Timeout as err:
        
        error_except(err,"Request timed out",'service oneid',response.status_code)
        return {'result': 'ER','messageText': 'Request timed out','stastus_Code':response.status_code}
    except requests.ConnectionError as err:
        
        error_except(err,"API Connection error occurred.",'service oneid',response.status_code)
        return {'result': 'ER','messageText': 'API Connection error occurred.','stastus_Code':response.status_code}
    except Exception as err:
        
        error_except(err,"An unexpected error",'service oneid',response.status_code)
        return {'result': 'ER','messageText': 'An unexpected error: ' + str(err),'stastus_Code':response.status_code}

def login_citizen_api_v3_test():
    start_time = time.time()

    todays = (date.today())
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    date_today = datetime.datetime.strptime(str(todays),"%Y-%m-%d").strftime("%d-%m-%Y")

    try:
        tmp_json = {
            "grant_type":  "password",
            "username":     "jirayuknot",
            "password":     "m12345678",
            "client_id":    clientId,
            "client_secret":secretKey
        }
        token_bot = 'Bearer A89a857fd25805679a41ad51c3505ae3a6eaf2f84de624a6a8b1689fb1d616973b5f7fff147714ee3b9800cc99b662142'
        useridChat = 'G5e44be95e2563f002c0232b4a5b3d209174e553eba02fc3da27e28ac'
        bot_chat_id = 'Be97d0cbdfc67534abc1c5385fb268a36'

        response = callPost_v2_test(one_url+"/api/oauth/getpwd",tmp_json,start_time)
        count_error = 0
        res_arraylist = []
        error_list_all = []
        if response['result'] == 'OK':
            tmp_messageText = response['messageText'].json()     
            if tmp_messageText['result'] == 'Success':
                try:
                    username = tmp_messageText['username']
                except Exception as ex:
                    return jsonify({'result':'Fail','responseCode':401,'data':None,'errorMessage':'login fail! username not found'}),401
                token_one = tmp_messageText['token_type'] + ' '+ tmp_messageText['access_token']
                access_token_one = tmp_messageText['access_token']
                token_header = 'Bearer '+ access_token_one
                getBuz = callGET_v2_test(one_url+"/api/account_and_biz_detail",token_one,start_time,token_header)

                if getBuz['error_list'] != []:
                    error_list_all.append(getBuz['error_list'])
                
                res_list = credentials_list_v2_test("","","","","",start_time,token_header)

                if res_list['error_list'] != []:
                    error_list_all.append(res_list['error_list'])
               
                if res_list['result'] == 'OK':
                    data_msg = res_list['msg']
                    
                    try:
                        totalResult_oneAuth = data_msg['totalResult']
                        if totalResult_oneAuth == 0:

                            error_except('ER','sign profile not found','service oneAuth','500')
                            message_text = 'sign profile not found ' + ',service oneAuth' + ',status: ' + '500' 
                            send_messageToChat_v4_2(message_text,start_time,'0',token_header)

                            # return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'sign profile not found'}),200
                        else:
                            pass
                    except Exception as e:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! ' + str(e)}),200
                else:
                    ans_er = res_list['msg']
                    
                    error_except(ans_er,'list Service Error!','service oneAuth',res_list['stastus_Code'])

                    time_sec = "{0:.2f}".format((time.time() - start_time))
                    time_millisec = int((time.time() - start_time)*1000)
                    day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
                    text_to_log = day_n_time + 'Login' + ' {status: Success' + '}' + '(OneId) & PDF signing ' + '{status: Error' + '}' + '(OneAuth) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec'+ ' 500'
                    save_log(text_to_log)

                    # return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error!'}),200
                type_certifyLevel = ''
                try:
                    if res_list['result'] == 'OK':
                        res_arraylist.append({'result_listService':res_list})
                        credentialId = res_list['msg']['credentials'][0]['credentialId']
                        res_authorize = credentials_authorize_v2_test(credentialId,"","","","","","","",start_time,token_header)
                        if res_authorize['error_list'] != []:
                            error_list_all.append(res_authorize['error_list'])
                        
                        if res_authorize['result'] == 'OK':
                            res_arraylist.append({'result_authorizeService':res_authorize})
                            sadData = res_authorize['msg']['sad']
                            sign_position = {
                                "sign_llx": "0.002",
                                "sign_lly": "0.001",
                                "sign_page": "1",
                                "sign_urx": "0.09",
                                "sign_ury": "0.04",
                                "max_page": 1
                            }
                            
                            base64_string = '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CmVuZG9iagoKOSAwIG9iago8PC9UeXBlL0ZvbnQvU3VidHlwZS9UcnVlVHlwZS9CYXNlRm9udC9CQUFBQUErQXJpYWwtQm9sZE1UCi9GaXJzdENoYXIgMAovTGFzdENoYXIgMTEKL1dpZHRoc1s3NTAgNzIyIDYxMCA4ODkgNTU2IDI3NyA2NjYgNjEwIDMzMyAyNzcgMjc3IDU1NiBdCi9Gb250RGVzY3JpcHRvciA3IDAgUgovVG9Vbmljb2RlIDggMCBSCj4+CmVuZG9iagoKMTAgMCBvYmoKPDwKL0YxIDkgMCBSCj4+CmVuZG9iagoKMTEgMCBvYmoKPDwvRm9udCAxMCAwIFIKL1Byb2NTZXRbL1BERi9UZXh0XT4+CmVuZG9iagoKMSAwIG9iago8PC9UeXBlL1BhZ2UvUGFyZW50IDQgMCBSL1Jlc291cmNlcyAxMSAwIFIvTWVkaWFCb3hbMCAwIDU5NSA4NDJdL0dyb3VwPDwvUy9UcmFuc3BhcmVuY3kvQ1MvRGV2aWNlUkdCL0kgdHJ1ZT4+L0NvbnRlbnRzIDIgMCBSPj4KZW5kb2JqCgoxMiAwIG9iago8PC9Db3VudCAxL0ZpcnN0IDEzIDAgUi9MYXN0IDEzIDAgUgo+PgplbmRvYmoKCjEzIDAgb2JqCjw8L1RpdGxlPEZFRkYwMDQ0MDA3NTAwNkQwMDZEMDA3OTAwMjAwMDUwMDA0NDAwNDYwMDIwMDA2NjAwNjkwMDZDMDA2NT4KL0Rlc3RbMSAwIFIvWFlaIDU2LjcgNzczLjMgMF0vUGFyZW50IDEyIDAgUj4+CmVuZG9iagoKNCAwIG9iago8PC9UeXBlL1BhZ2VzCi9SZXNvdXJjZXMgMTEgMCBSCi9NZWRpYUJveFsgMCAwIDU5NSA4NDIgXQovS2lkc1sgMSAwIFIgXQovQ291bnQgMT4+CmVuZG9iagoKMTQgMCBvYmoKPDwvVHlwZS9DYXRhbG9nL1BhZ2VzIDQgMCBSCi9PdXRsaW5lcyAxMiAwIFIKPj4KZW5kb2JqCgoxNSAwIG9iago8PC9BdXRob3I8RkVGRjAwNDUwMDc2MDA2MTAwNkUwMDY3MDA2NTAwNkMwMDZGMDA3MzAwMjAwMDU2MDA2QzAwNjEwMDYzMDA2ODAwNkYwMDY3MDA2OTAwNjEwMDZFMDA2RTAwNjkwMDczPgovQ3JlYXRvcjxGRUZGMDA1NzAwNzIwMDY5MDA3NDAwNjUwMDcyPgovUHJvZHVjZXI8RkVGRjAwNEYwMDcwMDA2NTAwNkUwMDRGMDA2NjAwNjYwMDY5MDA2MzAwNjUwMDJFMDA2RjAwNzIwMDY3MDAyMDAwMzIwMDJFMDAzMT4KL0NyZWF0aW9uRGF0ZShEOjIwMDcwMjIzMTc1NjM3KzAyJzAwJyk+PgplbmRvYmoKCnhyZWYKMCAxNgowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMTE5OTcgMDAwMDAgbiAKMDAwMDAwMDAxOSAwMDAwMCBuIAowMDAwMDAwMjI0IDAwMDAwIG4gCjAwMDAwMTIzMzAgMDAwMDAgbiAKMDAwMDAwMDI0NCAwMDAwMCBuIAowMDAwMDExMTU0IDAwMDAwIG4gCjAwMDAwMTExNzYgMDAwMDAgbiAKMDAwMDAxMTM2OCAwMDAwMCBuIAowMDAwMDExNzA5IDAwMDAwIG4gCjAwMDAwMTE5MTAgMDAwMDAgbiAKMDAwMDAxMTk0MyAwMDAwMCBuIAowMDAwMDEyMTQwIDAwMDAwIG4gCjAwMDAwMTIxOTYgMDAwMDAgbiAKMDAwMDAxMjQyOSAwMDAwMCBuIAowMDAwMDEyNDk0IDAwMDAwIG4gCnRyYWlsZXIKPDwvU2l6ZSAxNi9Sb290IDE0IDAgUgovSW5mbyAxNSAwIFIKL0lEIFsgPEY3RDc3QjNEMjJCOUY5MjgyOUQ0OUZGNUQ3OEI4RjI4Pgo8RjdENzdCM0QyMkI5RjkyODI5RDQ5RkY1RDc4QjhGMjg+IF0KPj4Kc3RhcnR4cmVmCjEyNzg3CiUlRU9GCg=='
                            sign_string = 'iVBORw0KGgoAAAANSUhEUgAAALYAAABSBAMAAAALCzOjAAAAG1BMVEX29vY9PT24uLh7e3vX19ceHh5cXFyZmZkAAAAk/jvpAAAAAXRSTlMAQObYZgAAAAlwSFlzAAAOxAAADsQBlSsOGwAABMBJREFUWIXtWE1v20YQXZJLMkcDtQseaRROedQp4JFqIJdHQf4Ij0wRN3skCrTQsZJMaX525s0uJQc2BQoIgRw0h0T8ejPz5s3srpU629l+Vou242Hn7Siw8VNbKFqNAf2R2lRp2o0AHVe05v+SyQjYf+dUjwALmzYVpeNA+4t4nCqy3RTeKFVUCFuVNB8He9aonMZQCNujUhUVo0BH98ofq5TLRkUjlVLzfCrp/1GwPQ7ZduW1Df7jFUvn0P36Q/VY2J/vK9z1XCDvq1qeHxkUyzlKmTLvtMH1Lbg3Ml5g/q/pLd3Lz2sSpS6tXqdkifSOSIxj0cS8aDuuYnziEblVQj8V/FgqPV3ldIEPBMyvEhvLsn9aBKy+AG8tbVSGOGXzTyecJaNpcRTTZAnq2DkoWm4yG3fVv56UDBLSswo2BvFEK0N1sFYu7qAV90jIrFVCDTjAPZ9Sw1/B1aYXO2fnGef6lEr/mNpQk6UqsXwbMB0ioahNtURcCli51jZPb1+Z1wbnDBddSv8EG6ZTf2J3NR5GwmWGcNlLIBHbcKs0IBFX1j+JAjwiUh8YhwMoa5+23r7wRphJiFPn1TRExBwulyBa85U4Nv0yCdl5TFvd2Mwf2dnu88HxvVDLHsJ7hPiMe8gia/gKWWjqlwnytZRlHICeILjnw8NJx6hXIP4LBAPIXxDwVnWVfdtydls68RUWD3GJaSsvVFppCbGBVAFZ42ot3/fLJGFE2/FOdeYwEt1ilDhnkcikcroIhHefjsmE8HEKnVoqKtpTYps7xiuwEt4DcroIJYsZ9cvEZ7qk4zlI9DOQ9nW3zR127Z+LkDrKMrjUD/J68wrXQrW24/nd1PLQHp5JBQQyEjZkqrkVSkrpfYJMordVGDC7obBgMK4K13UuazBv2+/JZbQfYnwbTfcbQjFFL7bVAeo2SznKPX+llNIDZLCTHwUm2bpL6oI7CO0U9CgFbWzAYMDTTz90HDt+JR9AYhqWHEZE+aGUqTJpxq6WF29js4aUm0ATNVtLbTtLAMO6WCmfG154N4uuxUt+MVqw57nft4wzbX8Krdw5ftV0a49YBa7ylu9ka7mcT1dFt9ngntFXKdLMLnuw+eF/oBVDMNshnL26FRgN2mt69iEhzvBLVe83G9wGM+w96Pf+3YehBEsrz4yAN/fcLgfygG1qj+YSNpPz72a/2WDQr0wUt6qpe7F5JUPH8/qUILeEDn3A4rtZ8OdfRfksE3YeujWePVWXUtH+cYKngEvsoq27/rZptxtMkWqBq3dEl4jBhumRazgk22esU5IYt4WE8+IQyFOrkA4oLPZG7qUuJAE19KUfuhvD5k4AgvZF0acrfO4/uCkozjuJ+g8ixau/jkGzMvqH5CuLT9s3eqfs6qMXEj1qqfz77pQDWjnwZd+WLTvlgJYPfDmwcjOnHOGP7M++M89OBjrhTw/B0LqHkl888PWbO4XVceCJK3StPEwmsoU1Q3P0BHto5TEg48GSsvvIoZX3uC7Z4NLEgjq08nyq+GP4+VZj/h3bmX9vN24eDrOkRqoDm1hpczccWmXzwzz+0YaDZTLSOV5T6p/SlSfZcjcb688msp6lI2Gr26p333K2s53tbGf7+ewbZFmcaCfd69YAAAAASUVORK5CYII='
                            
                            res_signPdf = signing_pdfSigning_v3_test(base64_string,sadData,"","","",'CERTIFY',"","","","","","",token_header,sign_position,sign_string,start_time)
                            time_sec = "{0:.2f}".format((time.time() - start_time))
                            time_millisec = int((time.time() - start_time)*1000)

                            day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
                            text_to_log = day_n_time + 'Login' + ' {status: Success' + '}' + '(OneId) & PDF signing ' + '{status: Success' + '}' + '(OneAuth) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec'+ ' 200'
                            save_log(text_to_log)
                            
                            # return jsonify({'result':'OK','messageText':'successful','status_Code':200,'messageER':None}),200

                        else:
                            ans_er = res_authorize['msg']
                            error_except(ans_er,'error','service oneAuth',res_authorize['status_Code'])
                            
                            message_text = url_credentials_authorize_v2 + ' ,service oneAuth' + ',status: 500' 
                    

                            time_sec = "{0:.2f}".format((time.time() - start_time))
                            time_millisec = int((time.time() - start_time)*1000)
                            day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
                            text_to_log = day_n_time + 'Login' + ' {status: Success' + '}' + '(OneId) & PDF signing ' + '{status: Error' + '}' + '(OneAuth) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec'+ ' 500'
                            save_log(text_to_log)

                            # return jsonify({'result': 'ER','messageText': ans_er,'stastus_Code':res_authorize['status_Code']})
                    else:
                        ans_er = res_list['msg']
                        error_except(ans_er,'error','service oneid',res_list['status_Code'])

                        time_sec = "{0:.2f}".format((time.time() - start_time))
                        time_millisec = int((time.time() - start_time)*1000)
                        message_send = url_credentials_list_v2 + ' ,service oneAuth ' + ',status: ' + str(res_list['status_Code'])
                        message_text = '\n แจ้งเตือน \n %s \n เวลา(sec) : %s \n เวลา(Millisec) : %s \n การส่งข้อมูลครั้งที่ : %s ' %(message_send,(str(time_sec)),(str(time_millisec)),(str(1)))
                        send_messageToChat_v4_2(message_text,start_time,res_list['count_error'],token_header)

                        day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
                        text_to_log = day_n_time + 'Login' + ' {status: Success' + '}' + '(OneId) & PDF signing ' + '{status: Error' + '}' + '(OneAuth) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec'+ ' 500'
                        save_log(text_to_log)

                        # return jsonify({'result': 'ER','messageText': ans_er,'stastus_Code':res_list['status_Code']})

                except Exception as ex:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)

                    error_except('ER',str(ex),'service oneAuth')

                    time_sec = "{0:.2f}".format((time.time() - start_time))
                    time_millisec = int((time.time() - start_time)*1000)

                    day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
                    text_to_log = day_n_time + 'Login' + ' {status: Success' + '}' + '(OneId) & PDF signing ' + '{status: Error' + '}' + '(OneAuth) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec'+ ' 500'
                    save_log(text_to_log)

                    # return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! ' + str(ex)}),200
        else:
            ans_er = response['messageText'].json()

            time_sec = "{0:.2f}".format((time.time() - start_time))
            time_millisec = int((time.time() - start_time)*1000)

            day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
            text_to_log = day_n_time + 'Login' + ' {status: Error' + '}' + '(OneId) & PDF signing ' + '{status: Error' + '}' + '(OneAuth) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec'+ ' 500'
            save_log(text_to_log)

            # return jsonify({'result': 'ER','messageText': ans_er,'status_Code':response['status_Code']})
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        error_except('ER',str(e),'service oneid',response['status_Code'])
        # return jsonify({'result':'Fail','responseCode':500,'data':None,'errorMessage':str(e)})

def error_except(err,message_text,service,status_code):
    tmp_err = {}
    tmp_err = {
        'error':str(err),
        'message_text':message_text,
        'service':service,
        'status_code':status_code
    }
    return (tmp_err)

def credentials_list_v2_test(userId,userName,maxResults,pageToken,cliendData,start_time,token_header):
    try:
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        payload =  {
            "userId":   "",
            "userName": "",
            "maxResults": "",
            "pageToken": "",
            "cliendData": ""
        }
        count_error = 0
        error_list = []
        send_chat_list = []
        message_text = None
        
        message_send_all = ''

        todays = (date.today())
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        date_today = datetime.datetime.strptime(str(todays),"%Y-%m-%d").strftime("%d-%m-%Y")

        response = requests.request("POST", url_credentials_list_v2, json=(payload), headers=headers,verify=False)
        one_access_token = str(token_header).split()[1]
        if response.status_code == 200 or response.status_code == 201:
            time_sec = "{0:.2f}".format((time.time() - start_time))
            time_millisec = int((time.time() - start_time)*1000)
            day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
            text_to_log = day_n_time + url_credentials_list_v2 + ' {status: Success' + '}' + '(OneAuth) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec '+ str(response.status_code)
            save_log2(text_to_log)

            return {'result':'OK','msg':response.json(),'status_Code':response.status_code,'error_list':error_list,'count_error':count_error}
        else:

            time_sec = "{0:.2f}".format((time.time() - start_time))
            time_millisec = int((time.time() - start_time)*1000)
            message_send = url_credentials_list_v2 + ' ,service oneAuth ' + ',status: ' + str(response.status_code)
            message_text = 'แจ้งเตือน \n %s \n เวลา(sec) : %s \n เวลา(Millisec) : %s \n การส่งข้อมูลครั้งที่ : %s ' %(message_send,(str(time_sec)),(str(time_millisec)),(str(1)))
            send_chat_list.append(message_text)

            day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
            text_to_log = day_n_time + url_credentials_list_v2 + ' {status: Error' + '}' + '(OneAuth) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec '+ str(response.status_code)
            save_log2(text_to_log)

            for cG in range (2) :
                response = requests.request("POST", url_credentials_list_v2, json=(payload), headers=headers,verify=False)
                if response.status_code == 200 :
                    count_error += 1

                    for x in range(len(send_chat_list)):
                        message_send_all += send_chat_list[x]
                        message_send_all += '\n'

                    time_sec = "{0:.2f}".format((time.time() - start_time))
                    time_millisec = int((time.time() - start_time)*1000)
                    send_messageToChat_v4_2(message_send_all,start_time,cG+2,token_header)

                    day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
                    text_to_log = day_n_time + url_credentials_list_v2 + ' {status: Success' + '}' + '(OneAuth) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec '+ str(response.status_code)
                    save_log2(text_to_log)

                    return {'result':'OK','msg':response.json(),'status_Code':response.status_code,'error_list':error_list,'count_error':count_error}

                else:
                    err = error_except('ER',response.text,'service oneAuth',response.status_code)
                    error_list.append(err)

                    time_sec = "{0:.2f}".format((time.time() - start_time))
                    time_millisec = int((time.time() - start_time)*1000)
                    message_send = url_credentials_list_v2 + ' ,service oneAuth ' + ',status: ' + str(response.status_code)
                    message_text = '\n แจ้งเตือน \n %s \n เวลา(sec) : %s \n เวลา(Millisec) : %s \n การส่งข้อมูลครั้งที่ : %s ' %(message_send,(str(time_sec)),(str(time_millisec)),(str(cG+2)))
                    send_chat_list.append(message_text)

                    day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
                    text_to_log = day_n_time + url_credentials_list_v2 + ' {status: Error' + '}' + '(OneAuth) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec '+ str(response.status_code)
                    save_log2(text_to_log)
                    
                count_error += 1
            
            for x in range(len(send_chat_list)):
                message_send_all += send_chat_list[x]
                message_send_all += '\n'

            send_messageToChat_v4_2(message_send_all,start_time,cG+2,token_header)

            return {'result':'ER','msg':'messge ' + str(response.text),'stastus_Code':response.status_code,'error_list':error_list,'count_error':count_error}
    except requests.Timeout as ex:
        error_except(ex,"Timeout ",'service oneAuth',response.status_code)
        return {'result':'ER','msg':'Timeout ' + str(ex),'stastus_Code':response.status_code}
    except requests.HTTPError as ex:
        error_except(ex,"HTTPError ",'service oneAuth',response.status_code)
        return {'result':'ER','msg':'HTTPError ' + str(ex),'stastus_Code':response.status_code}
    except requests.ConnectionError as ex:
        error_except(ex,"ConnectionError ",'service oneAuth',response.status_code)
        return {'result':'ER','msg':'ConnectionError ' + str(ex),'stastus_Code':response.status_code}
    except requests.RequestException as ex:
        error_except(ex,"RequestException ",'service oneAuth',response.status_code)
        return {'result':'ER','msg':'RequestException ' + str(ex),'stastus_Code':response.status_code}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        error_except(response.status_code,ex,'service oneAuth',response.status_code)
        return {'result':'ER','msg':str(ex),'status_Code':response.status_code}

def credentials_authorize_v2_test(credentialId,credentialAuthorizationData,numSignatures,hash_data,description,clientData,pin,otp,start_time,token_header):
    try:
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        payload =  {
            "credentialId": credentialId,
            "credentialAuthorizationData": credentialAuthorizationData,
            "numSignatures": numSignatures,
            "hash": [hash_data],
            "description": description,
            "clientData": clientData,
            "pin": pin,
            "otp": otp
        }
        count_error = 0
        error_list = []
        send_chat_list = []
        message_text = None
        
        message_send_all = ''

        todays = (date.today())
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        date_today = datetime.datetime.strptime(str(todays),"%Y-%m-%d").strftime("%d-%m-%Y")

        response = requests.request("POST", url_credentials_authorize_v2, json=(payload), headers=headers,verify=False)
        one_access_token = str(token_header).split()[1]
        if response.status_code == 200 or response.status_code == 201:
            time_sec = "{0:.2f}".format((time.time() - start_time))
            time_millisec = int((time.time() - start_time)*1000)
            day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
            text_to_log = day_n_time + url_credentials_authorize_v2 + ' {status: Success' + '}' + '(OneAuth) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec '+ str(response.status_code)
            save_log2(text_to_log)

            return {'result':'OK','msg':response.json(),'status_Code':response.status_code,'error_list':error_list,'count_error':count_error}
        else:
            
            time_sec = "{0:.2f}".format((time.time() - start_time))
            time_millisec = int((time.time() - start_time)*1000)
            message_send = url_credentials_authorize_v2 + ' ,service oneAuth ' + ',status: ' + str(response.status_code)
            message_text = 'แจ้งเตือน \n %s \n เวลา(sec) : %s \n เวลา(Millisec) : %s \n การส่งข้อมูลครั้งที่ : %s ' %(message_send,(str(time_sec)),(str(time_millisec)),(str(1)))
            send_chat_list.append(message_text)
            
            day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
            text_to_log = day_n_time + url_credentials_authorize_v2 + ' {status: Error' + '}' + '(OneAuth) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec '+ str(response.status_code)
            save_log2(text_to_log)

            for cG in range (2) :
                response = requests.request("POST", url_credentials_authorize_v2, json=(payload), headers=headers,verify=False)
                if response.status_code == 200 :
                    count_error += 1

                    for x in range(len(send_chat_list)):
                        message_send_all += send_chat_list[x]
                        message_send_all += '\n'

                    time_sec = "{0:.2f}".format((time.time() - start_time))
                    time_millisec = int((time.time() - start_time)*1000)
                    send_messageToChat_v4_2(message_send_all,start_time,cG+2,token_header)

                    day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
                    text_to_log = day_n_time + url_credentials_authorize_v2 + ' {status: Success' + '}' + '(OneAuth) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec '+ str(response.status_code)
                    save_log2(text_to_log)

                    return {'result':'OK','msg':response.json(),'status_Code':response.status_code,'error_list':error_list,'count_error':count_error}
                else:
                    err = error_except('ER',response.text,'service oneAuth',response.status_code)
                    error_list.append(err)

                    time_sec = "{0:.2f}".format((time.time() - start_time))
                    time_millisec = int((time.time() - start_time)*1000)
                    message_send = url_credentials_authorize_v2 + ' ,service oneAuth ' + ',status: ' + str(response.status_code)
                    message_text = '\n แจ้งเตือน \n %s \n เวลา(sec) : %s \n เวลา(Millisec) : %s \n การส่งข้อมูลครั้งที่ : %s ' %(message_send,(str(time_sec)),(str(time_millisec)),(str(cG+2)))
                    send_chat_list.append(message_text)
                    
                    day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
                    text_to_log = day_n_time + url_credentials_authorize_v2 + ' {status: Error' + '}' + '(OneAuth) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec '+ str(response.status_code)
                    save_log2(text_to_log)

                count_error += 1
            

            for x in range(len(send_chat_list)):
                message_send_all += send_chat_list[x]
                message_send_all += '\n'

            send_messageToChat_v4_2(message_send_all,start_time,cG+2,token_header)

            return {'result':'ER','msg':response.text,'status_Code':response.status_code,'error_list':error_list,'count_error':count_error}
    except requests.Timeout as ex:
        error_except(ex,"Timeout ",'service oneAuth',response.status_code)
        return {'result':'ER','msg':'Timeout ' + str(ex),'status_Code':response.status_code}
    except requests.HTTPError as ex:
        error_except(ex,"HTTPError ",'service oneAuth',response.status_code)
        return {'result':'ER','msg':'HTTPError ' + str(ex),'status_Code':response.status_code}
    except requests.ConnectionError as ex:
        error_except(ex,"ConnectionError ",'service oneAuth',response.status_code)
        return {'result':'ER','msg':'ConnectionError ' + str(ex),'status_Code':response.status_code}
    except requests.RequestException as ex:
        error_except(ex,"RequestException ",'service oneAuth',response.status_code)
        return {'result':'ER','msg':'RequestException ' + str(ex),'status_Code':response.status_code}
    except Exception as ex:
        error_except('ER',str(ex),'service oneAuth',response.status_code)
        return {'result':'ER','msg':str(ex),'status_Code':response.status_code}

def signing_pdfSigning_v3_test(pdfData,sadData,cadData,reason,location,certifyLevel,hashAlgorithm,overwriteOriginal,visibleSignature,visibleSignaturePage,visibleSignatureRectangle,visibleSignatureImagePath,token_header,sign_position,sign_string,start_time):
    payload = ''
    one_access_token = ''
    send_chat_list = []
    message_text = None
    
    message_send_all = ''
    

    todays = (date.today())
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    date_today = datetime.datetime.strptime(str(todays),"%Y-%m-%d").strftime("%d-%m-%Y")
    try:
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        visibleSignatureRectangle = '' + sign_position['sign_llx'] + ',' + sign_position['sign_lly'] + ',' + sign_position['sign_urx'] + ',' + sign_position['sign_ury'] + ''
        visibleSignaturePage = int(sign_position['sign_page'])
        payload =  {
            "pdfData": pdfData,
            "sadData": sadData,
            "cadData": cadData,
            "reason": reason,
            "location": location,
            "certifyLevel": certifyLevel,
            "hashAlgorithm": hashAlgorithm,
            "overwriteOriginal": True,
            "visibleSignature": "Graphics",
            "visibleSignaturePage": visibleSignaturePage,
            "visibleSignatureRectangle": visibleSignatureRectangle,
            "visibleSignatureImagePath": sign_string
        }
        error_list = []
        count_error = 0
        response = requests.request("POST", url_pdfSigning_Sign_v3, json=(payload), headers=headers,verify=False)
        one_access_token = str(token_header).split()[1]
        if response.status_code == 200 or response.status_code == 201:           
            time_sec = "{0:.2f}".format((time.time() - start_time))
            time_millisec = int((time.time() - start_time)*1000)
            day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
            text_to_log = day_n_time + url_pdfSigning_Sign_v3 + ' {status: Success' + '}' + '(OneAuth) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec '+ str(response.status_code)
            save_log2(text_to_log)

            return {'result':'OK','msg':response.json(),'stastus_Code':response.status_code}
        else:
            error_except(response.status_code,str(response.text),'service oneAuth',response.status_code)

            time_sec = "{0:.2f}".format((time.time() - start_time))
            time_millisec = int((time.time() - start_time)*1000)
            message_send = url_pdfSigning_Sign_v3 + ' ,service oneAuth ' + ',status: ' + str(response.status_code)
            message_text = 'แจ้งเตือน \n %s \n เวลา(sec) : %s \n เวลา(Millisec) : %s \n การส่งข้อมูลครั้งที่ : %s ' %(message_send,(str(time_sec)),(str(time_millisec)),(str(1)))
            send_messageToChat_v4_2(message_text,start_time,'1',token_header)

            day_n_time = '['+ str(date_today)+'T'+str(current_time) +']'
            text_to_log = day_n_time + url_pdfSigning_Sign_v3 + ' {status: Error' + '}' + '(OneAuth) ' + 'Time ' + str(time_sec) + ' sec , ' + str(time_millisec) +' Millisec '+ str(response.status_code)
            save_log2(text_to_log)

        return {'result':'ER','msg':str(response.json()),'stastus_Code':response.status_code}        
    except requests.Timeout as ex:
        error_except(ex,"Timeout ",'service oneAuth',response.status_code)
        return {'result':'ER','msg':'Timeout ' + str(ex),'stastus_Code':response.status_code}
    except requests.HTTPError as ex:
        error_except(ex,"HTTPError ",'service oneAuth',response.status_code)
        return {'result':'ER','msg':'HTTPError ' + str(ex),'stastus_Code':response.status_code}
    except requests.ConnectionError as ex:
        error_except(ex,"ConnectionError ",'service oneAuth',response.status_code)
        return {'result':'ER','msg':'ConnectionError ' + str(ex),'stastus_Code':response.status_code}
    except requests.RequestException as ex:
        error_except(ex,"RequestException ",'service oneAuth',response.status_code)
        return {'result':'ER','msg':'RequestException ' + str(ex),'stastus_Code':response.status_code}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        error_except('ER',str(ex),'service oneAuth',response.status_code)
        return {'result':'ER','msg':str(ex),'stastus_Code':response.status_code}

@status_methods.route('/api/v4/OneAuth/Sign_test',methods=['POST'])
def oneAuth_API_v4_test():
    if request.method == 'POST':
        try:
            token_header = request.headers['Authorization']
        except KeyError as ex:
            return redirect(url_paperless)
        dataJson = request.json
        if 'base64_string' in dataJson and 'max_Step' in dataJson and 'Step_Num' in dataJson and 'sign_position' in dataJson and 'sign_string' in dataJson and len(dataJson) == 5:
            sign_position = dataJson['sign_position']
            sign_string = dataJson['sign_string']
            if 'sign_llx' in sign_position and 'sign_lly' in sign_position and 'sign_urx' in sign_position and 'sign_ury' in sign_position and 'sign_page' in sign_position and 'max_page' in sign_position and len(sign_position) == 6:
                res_arraylist = []
                base64_pdf_String = dataJson['base64_string']
                res_list = credentials_list_v2_test("","","","","",token_header)
                if res_list['result'] == 'OK':
                    data_msg = res_list['msg']
                    try:
                        totalResult_oneAuth = data_msg['totalResult']
                        if totalResult_oneAuth == 0:
                            return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'sign profile not found'}),200
                        else:
                            pass
                    except Exception as e:
                        return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! ' + str(e)}),200
                else:
                    ans_er = res_list['msg']
                    error_except(ans_er,'list Service Error! 007','service oneid')
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! 007'}),200
                type_certifyLevel = ''
                try:
                    if res_list['result'] == 'OK':
                        res_arraylist.append({'result_listService':res_list})
                        credentialId = res_list['msg']['credentials'][0]['credentialId']
                        res_authorize = credentials_authorize_v2_test(credentialId,"","","","","","","",token_header)
                        if res_authorize['result'] == 'OK':
                            res_arraylist.append({'result_authorizeService':res_authorize})
                            sadData = res_authorize['msg']['sad']
                            if int(sign_position['sign_page']) == int(sign_position['max_page']):
                                if int(dataJson['Step_Num']) == int(dataJson['max_Step']):
                                    type_certifyLevel = 'CERTIFY'
                                else:
                                    type_certifyLevel = 'NON-CERTIFY'
                            else:
                                if int(dataJson['Step_Num']) == int(dataJson['max_Step']):
                                    type_certifyLevel = 'NON-CERTIFY'
                                else:
                                    type_certifyLevel = 'NON-CERTIFY'
                            res_signPdf = signing_pdfSigning_v3_test(base64_pdf_String,sadData,"","","",type_certifyLevel,"","","","","","",token_header,sign_position,sign_string)
                            return jsonify({'result':'OK','messageText':res_signPdf,'status_Code':200,'messageER':None}),200

                        else:
                            ans_er = res_authorize['msg']
                            error_except(ans_er,'error','service oneid')
                            return jsonify({'result': 'ER','messageText': ans_er})
                    else:
                        ans_er = res_list['msg']
                        error_except(ans_er,'error','service oneid')
                        return jsonify({'result': 'ER','messageText': ans_er})
                    
                except Exception as ex:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    error_except('ER',str(ex),'service oneAuth')
                    return jsonify({'result':'ER','messageText':None,'status_Code':200,'messageER':'list Service Error! ' + str(ex)}),200
    
# def send_messageToChat_v4(message,token_header):
#     token_bot = 'Bearer A89a857fd25805679a41ad51c3505ae3a6eaf2f84de624a6a8b1689fb1d616973b5f7fff147714ee3b9800cc99b662142'
#     useridChat = 'G5e44be95e2563f002c0232b4a5b3d209174e553eba02fc3da27e28ac'
#     bot_chat_id = 'Be97d0cbdfc67534abc1c5385fb268a36'
#     try:
#         headers = {
#             'content-type': 'application/json',
#             'Authorization':token_bot
#         }
#         data_Json = {
#             "to": useridChat,
#             "bot_id": bot_chat_id,
#             "type": "text",
#             "message": str(message)
#         }
#         r = requests.post(url_chat,json=data_Json,headers=headers,verify=True, cert=('cert/oneid.cer', 'cert/oneid.key'))
        
#         if r.status_code == 200 or r.status_code == 201:
#             return r.json()
#         else:
#             error_except(r.status_code,str((r.json())['message']),'service oneChat',r.status_code)
#             return r.json()
#     except requests.Timeout as ex:
#         error_except(ex,"Timeout ",'service oneChat',r.status_code)
#         return {'result':'ER','msg':'Timeout ' + str(ex)}
#     except requests.HTTPError as ex:
#         error_except(ex,"HTTPError ",'service oneChat',r.status_code)
#         return {'result':'ER','msg':'HTTPError ' + str(ex)}
#     except requests.ConnectionError as ex:
#         error_except(ex,"ConnectionError ",'service oneChat',r.status_code)
#         return {'result':'ER','msg':'ConnectionError ' + str(ex)}
#     except requests.RequestException as ex:
#         error_except(ex,"RequestException ",'service oneChat',r.status_code)
#         return {'result':'ER','msg':'RequestException ' + str(ex)}
#     except Exception as ex:
#         error_except('ER',str(ex),'service oneChat',r.status_code)
#         return {'result':'ER','msg':ex}

def send_messageToChat_v4_2(message,start_time,count_error,token_header):

    token_bot = 'Bearer A89a857fd25805679a41ad51c3505ae3a6eaf2f84de624a6a8b1689fb1d616973b5f7fff147714ee3b9800cc99b662142'
    useridChat = 'G5e44be95e2563f002c0232b4a5b3d209174e553eba02fc3da27e28ac'
    bot_chat_id = 'Be97d0cbdfc67534abc1c5385fb268a36'

    time_sec = "{0:.2f}".format((time.time() - start_time))
    time_millisec = int((time.time() - start_time)*1000)
    try:
        headers = {
            'content-type': 'application/json',
            'Authorization':token_bot
        }
        data_Json = {
            "to": useridChat,
            "bot_id": bot_chat_id,
            "type": "text",
            "message": str(message)
        }
        
        r = requests.post(url_chat,json=data_Json,headers=headers,verify=True, cert=('cert/oneid.cer', 'cert/oneid.key'))
        
        if r.status_code == 200 or r.status_code == 201:
            return r.json()
        else:
            error_except(r.status_code,str((r.json())['message']),'service oneChat',r.status_code)
            return r.json()
    except requests.Timeout as ex:
        error_except(ex,"Timeout ",'service oneChat',r.status_code)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        error_except(ex,"HTTPError ",'service oneChat',r.status_code)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        error_except(ex,"ConnectionError ",'service oneChat',r.status_code)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        error_except(ex,"RequestException ",'service oneChat',r.status_code)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        error_except('ER',str(ex),'service oneChat',r.status_code)
        return {'result':'ER','msg':ex}

def save_log(text):
    today = (date.today())
    start_direc = os.getcwd()
    direc = './logger/'
    direc2 = './'+ str(today)
    ls_direc = './logger/' + str(today)
    folder_name = 'logger'
    try:
        if not os.path.exists(direc):
            os.makedirs(ls_direc)
            
           
        
        if not os.path.exists(ls_direc):
            os.makedirs(ls_direc)
             
        os.chdir(ls_direc)
        name_file = "log_all" + str(today) + ".log"
        f = open(name_file, "a")
        f.close()
        send_seve_log(text,name_file)
        os.chdir(start_direc)
    except OSError:
        print('Error: Creating directory. ' + direc2)


def save_log2(text):
    today = (date.today())
    start_direc = os.getcwd()
    direc = './logger/'
    direc2 = './'+ str(today)
    ls_direc = './logger/' + str(today)
    folder_name = 'logger'
    try:
        if not os.path.exists(direc):
            os.makedirs(ls_direc)
        
        if not os.path.exists(ls_direc):
            os.makedirs(ls_direc)
             
        os.chdir(ls_direc)
        name_file = "log_each_function_" + str(today) + ".log"
        f = open(name_file, "a")
        f.close()
        send_seve_log(text,name_file)
        os.chdir(start_direc)
    except OSError:
        print('Error: Creating directory. ' + direc2)

def save_log3(text,name):
    today = (date.today())
    start_direc = os.getcwd()
    direc = path_global_1 + '/logger/'
    # direc2 = './'+ str(today)
    ls_direc = path_global_1 + '/logger/' + str(today)
    folder_name = 'logger'
    try:
        if not os.path.exists(direc):
            os.makedirs(ls_direc)
        
        if not os.path.exists(ls_direc):
            os.makedirs(ls_direc)
             
        os.chdir(ls_direc)
        name_file = "log_"+ name + str(today) + ".log"
        f = open(name_file, "a")
        f.close()
        send_seve_log(text,name_file)
        os.chdir(start_direc)
    except OSError:
        print('Error: Creating directory. ' + ls_direc)

def send_seve_log(text,name_file):
    file_object = open(name_file, 'a')

    file_object.write('\n'+text)

    file_object.close()

@status_methods.route('/public/v1/start_schedule',methods=['POST'])
def schedule_alert_v2():
    scheduler = BackgroundScheduler()
    pid = os.getpid()
    p = psutil.Process(pid)
    print ('PID: ',pid)
    print ('Pname: ',p.name())

    check_pro = session.get("check_pro")
    print ('check_pro: ',check_pro)
    if str(check_pro) == str(pid):
        print ('STOPP')
        exit
    else:
    
        scheduler.add_job(func = login_citizen_api_v3_test, trigger="interval", seconds=30)
        scheduler.start()
    
    session["check_pro"] = str(pid)
    print ('session: ',session["check_pro"])

    return ('success')

# @status_methods.route('/api/public/v1/transaction_document_today',methods=['GET'])
# def transaction_document_today_v1():
#     result_count = select_admin_3().select_document_tologline_v1()
#     if result_count['result'] == 'OK':
#         tmpcountdoucment = result_count['messageText']
#         str_text = 'UAT_จำนวนเอกสารทั้งหมดในวันนี้ ' + str(tmpcountdoucment)
#         call_lineNotify(str_text)
#         return jsonify({'result':'OK' ,'messageText':str_text})

@status_methods.route('/api/public/v1/schedule_service',methods=['GET'])
def schedule_service_v1():
    if request.method == 'GET':
        service_list = ['RPA']
        ts = int(time.time())
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')        
        str_datetime = str(st).split(' ')[0] + ' ' + '00:00:00'
        end_datetime = str(st).split(' ')[0] + ' ' + '23:59:59'       
        # str_datetime = '2020-07-01' + ' ' + '00:00:00'
        # end_datetime = '2020-12-15' + ' ' + '23:59:59'
        # print(str_datetime)
        # return ''
        selectdata = select_2().select_service_other_log_v1(service_list,str_datetime,end_datetime)
        result_documentType = select_1().select_documentquery_('0107544000094',str_datetime,end_datetime)
        # print(selectdata['result'])
        if selectdata['result'] == 'OK':
            ts = int(time.time())
            st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
            time_str = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            st_filename = datetime.datetime.fromtimestamp(ts).strftime('%H_%M_%S')
            path = path_global_1 + '/storage/excel/service/' + str(st) + '/'
            path_indb = path_global_1 + '/storage/excel/service/' + str(st) + '/'
            # path = './storage/excel/service/' + str(st) + '/'
            # path_indb = '/storage/excel/service/' + str(st) + '/'
            if not os.path.exists(path):
                os.makedirs(path)
            unique_filename = str(st)
            filename = 'report_ppl_' + st + unique_filename
            data_excel = selectdata['messageText']
            data_excel_2 = result_documentType
            count_n = 0
            count_r = 0
            count_y = 0
            row = 1
            row_1 = 1
            col = 0
            workbook = xlsxwriter.Workbook(path + filename + '.xlsx')
            worksheet = workbook.add_worksheet()
            format1 = workbook.add_format()
            # worksheet.set_column('H:I', 1)
            merge_format = workbook.add_format({
                'bold': 1,
                # 'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            })
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
            count_document = len(data_excel_2)
            for j in range (0, count_document):
                line_2 = data_excel_2[j]
                worksheet.merge_range('H1:I1', 'อนุมัติทั้งหมด', merge_format)
                # worksheet.write(0, 7, '',format1)
                worksheet.write(1, 7, 'ประเภทเอกสาร',format1)
                worksheet.write(1, 8, 'จำนวน',format1)
                worksheet.write(row_1, 7, line_2['document_type'],format1)
                worksheet.write(row_1, 8, line_2['count'] ,format1)
                row_1 += 1
            for num in range (0, count):
                line = data_excel[num]
                if line['status'] == 'OK':
                    line['status_1'] = 'สำเร็จ'
                    line['status'] = 'success'
                elif line['status'] == 'ER':
                    line['status_1'] = 'ไม่สำเร็จ'
                    line['status'] = 'fail'
                elif line['status'] == 'NOT':
                    line['status_1'] = 'สำเร็จแต่ไม่มีเอกสารไฟล์แนบ'
                    line['status'] = 'success_not_found'
                else:
                    line['status_1'] = ''
                line['remark'] = ''
                worksheet.write(row, 0, (num+1), format1)
                worksheet.write(row, 1, line['document_id'],format1)
                worksheet.write(row, 2, line['datetime'] ,format1)
                worksheet.write(row, 3, line['status_1'] ,format1)
                if line['status'] == 'ไม่สำเร็จ':
                    worksheet.write(row, 4, line['message'] ,format1)
                    line['remark'] = line['message']
                line['index'] = (num +1)
                del(line['status_1'])
                del(line['documentType'])
                if 'message' in line:          
                    del(line['message'])
                row += 1
            url = url_bi + '/api-bot-paperless_scs'
            resultBi = callPost_v3(url,data_excel)
            
            workbook.close()
            # return ''
            mail().send_serviceLog_toemail('ทดสอบ',"jirayu.ko@mandala.co.th", "paperlessReport@one.th",path + filename + '.xlsx',filename + '.xlsx',str(st),str(time_str))
            return jsonify({'result':'OK','messageText':selectdata['messageText']})
        else:
            return jsonify({'result':'ER','messageText':selectdata['messageER']})

@status_methods.route('/api/public/v1/group_auto',methods=['GET'])
def group_auto_v1():
    tmp_day =['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    ts = int(time.time())
    hr_ts = datetime.datetime.fromtimestamp(ts).strftime('%X')
    day_ts = datetime.datetime.fromtimestamp(ts).strftime('%A')
    hr_ts_index = str(hr_ts).split(':')[0]
    hr_ts_index = str(int(hr_ts_index) * 60 * 60)
    index_day = str(tmp_day.index(day_ts))
    result_templategroup_code = select_3().select_auto_grouptemplate_v1(index_day,hr_ts_index)
    if result_templategroup_code['result'] == 'OK':
        tmpgrouptemplate_code = result_templategroup_code['messageText']
        infojson = {
            "template_group_code":tmpgrouptemplate_code
        }
        result_groupmanual = fuc_manual_group(infojson)
        tmpdata = result_groupmanual['messageText']
        if result_groupmanual['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'data':tmpdata['data'],'message':'success'},'messageER':None,'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':{'data':tmpdata['data'],'message':'fail data not found'},'status_Code':200}),200
    else:
        return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'fail data not found'},'status_Code':200}),200
    
@status_methods.route('/api/public/v1/groupv2_auto',methods=['GET'])
def group_auto_v2_api():
    tmp_day =['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    ts = int(time.time())
    hr_ts = datetime.datetime.fromtimestamp(ts).strftime('%X')
    day_ts = datetime.datetime.fromtimestamp(ts).strftime('%A')
    hr_ts_index = str(hr_ts).split(':')[0]
    hr_ts_index = str(int(hr_ts_index) * 60 * 60)
    index_day = str(tmp_day.index(day_ts))
    result_templategroup_code = select_3().select_auto_groupv2template_v1(index_day,hr_ts_index)
    if result_templategroup_code['result'] == 'OK':
        tmpgrouptemplate_code = result_templategroup_code['messageText']
        infojson = {
            "template_group_code":tmpgrouptemplate_code
        }
        result_groupmanual = fuc_manual_group_v2(infojson)
        tmpdata = result_groupmanual['messageText']
        if result_groupmanual['result'] == 'OK':
            return jsonify({'result':'OK','messageText':{'data':tmpdata['data'],'message':'success'},'messageER':None,'status_Code':200}),200
        else:
            return jsonify({'result':'ER','messageText':None,'messageER':{'data':tmpdata['data'],'message':'fail data not found'},'status_Code':200}),200
    else:
        return jsonify({'result':'ER','messageText':None,'messageER':{'data':None,'message':'fail data not found'},'status_Code':200}),200

@status_methods.route('/api/v1/schedule_timeexpire', methods=['GET'])
def schedule_timeexpire():
    result_data = select_1().select_ppl_expire()
    list_sid_noti = result_data['messageText']
    token_bot = token_service
    botchat_id = bot_id
    if list_sid_noti !=0 :
        for x in range(len(list_sid_noti)):
            email = getEmail_Incomplete(list_sid_noti[x])
            for x in range(len(email[0])):
                msg = 'แจ้งเตือน Paperless' + '\n'+'เลขที่เอกสาร ' + email[1] + '\n'+ '\n'\
                'ควรอนุมัติเอกสารภายใน ' + str(email[2])
                result_chat = send_messageToChat_v4(msg,email[0][x],token_bot,botchat_id,"")
            # for y in range(len())
    return jsonify({'result':'OK','messageText':{'message':'succuess','data':result_data['messageText']},'messageER':None,'status_Code':200}),200

@status_methods.route('/api/public/v1/schedule_business',methods=['GET'])
def schedule_business_v1():
    print()

def login_paperless_check_service():
    start_time = time.time()
    ipaddress = ''
    biz_info = []
    check_biz_id = []
    tmp_json = {
        "grant_type":  "password",
        "username":     'jirayuknot55',
        "password":     'm12345678',
        "client_id":    clientId,
        "client_secret":secretKey
    }
    response = callPost_v2(one_url+"/api/oauth/getpwd",tmp_json)
    
    if response['result'] == 'OK':
        tmp_messageText = response['messageText'].json()
        if tmp_messageText['result'] == 'Success':
            try:
                username = tmp_messageText['username']
                user_id = tmp_messageText['account_id']
            except Exception as ex:
                message_text = 'service paperless, ' +str(ex)+ ', status: ' + '401' 
                send_messageToChat_v4_3(message_text,start_time,'0')
                abort(401)
            token_one = tmp_messageText['token_type'] + ' '+ tmp_messageText['access_token']
            access_token_one = tmp_messageText['access_token']
            result_selectdb = select_2().select_citizen_login_v1(username)
            getBuz = callGET_v2(one_url+"/api/account_and_biz_detail",token_one)
            ts = time.time()
            try:
                info = {
                    'accesstoken':access_token_one
                }
                # executor.submit(login_OneChat,user_id,access_token_one)
                # executor.submit(get_account_byuserid,info,access_token_one)
            except Exception as e:
                message_text = 'service paperless, ' +str(e)+ ', status: ' + '401' 
                send_messageToChat_v4_3(message_text,start_time,'0')
                print(str(e))
                abort(401)
            if result_selectdb['result'] == 'OK':
                if getBuz['result'] == 'OK':
                    tmp_account_biz = getBuz['messageText'].json()
                    ts = time.time()
                    user_id         = tmp_account_biz['id']
                    user_email      = tmp_account_biz['thai_email']
                    user_type       = tmp_account_biz['account_category']
                    one_accesstoken = str(tmp_messageText['access_token'])
                    access_time     = ts
                    refresh_token   = tmp_messageText['refresh_token']
                    access_token_time   = ts + tmp_messageText['expires_in']
                    access_token_begin  = ts
                    hash_data       = hash_512_v2('m12345678')
                    citizen_data    = str(tmp_account_biz)
                    getBiz_details  =  tmp_account_biz['biz_detail']
                    generate_seCode =   'P7Rw2h5GUVE2LpbVNRBO'
                    result_refToken = generate_tokenPaperless(username,user_email)
                    # executor.submit(update_datalogin,user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress,getBiz_details)
                    try:
                        citizen_data = eval(citizen_data)
                    except Exception as ex:
                        message_text = 'service paperless, ' +str(ex)+ ', status: ' + '401' 
                        send_messageToChat_v4_3(message_text,start_time,'0')
                        abort(401)
                else:                       
                    message_text = 'service paperless' + ',status: ' + '401' 
                    send_messageToChat_v4_3(message_text,start_time,'0')
                    abort(401)
            else:
                if getBuz['result'] == 'OK':
                    tmp_account_biz = getBuz['messageText'].json()
                    ts = time.time()
                    user_id         = tmp_account_biz['id']
                    user_email      = tmp_account_biz['thai_email']
                    user_type       = tmp_account_biz['account_category']
                    one_accesstoken = str(tmp_messageText['access_token'])
                    access_time     = ts
                    refresh_token   = tmp_messageText['refresh_token']
                    access_token_time   = ts + tmp_messageText['expires_in']
                    access_token_begin  = ts
                    hash_data       = hash_512_v2('m12345678')
                    citizen_data    = str(tmp_account_biz)
                    getBiz_details  =  tmp_account_biz['biz_detail']
                    generate_seCode = 'P7Rw2h5GUVE2LpbVNRBO'
                    result_refToken = generate_tokenPaperless(username,user_email)
                    result_insert = insert().insert_login(user_id,username,access_time,refresh_token,result_refToken,access_token_time,access_token_begin,one_accesstoken,citizen_data,hash_data,tmp_account_biz,generate_seCode,ipaddress)
                    result_BizLoing = insert().insert_LogBizLogin(username,user_id,getBiz_details)
                else:
                    tmp_account_biz = getBuz['messageText'].json()
                    message_text = 'service paperless, ' +str(tmp_account_biz)+ ', status: ' + '401' 
                    send_messageToChat_v4_3(message_text,start_time,'0')
                    abort(401)
        try:
            # message_text = 'service paperless' + ',status: ' + '200' 
            # send_messageToChat_v4_3(message_text,start_time,'0')
            pass
        except Exception as ex:
            message_text = 'service paperless, ' +str(ex)+ ', status: ' + '401' 
            send_messageToChat_v4_3(message_text,start_time,'0')
            abort(401)
    else:
        response_msg = str((response['messageText'].json())['errorMessage'])
        res_status = str((response['messageText'].status_code))
        message_text = 'service paperless, ' +response_msg+ ', status: ' + res_status
        send_messageToChat_v4_3(message_text,start_time,'0')
        abort(401)
    
@status_methods.route('/public/v1/start_schedule_check_ppl',methods=['POST'])
def start_schedule_check_ppl():
    scheduler = BackgroundScheduler()

    pid = os.getpid()
    p = psutil.Process(pid)
    print ('PID: ',pid)
    print ('Pname: ',p.name())

    check_pro = session.get("check_pro")
    print ('check_pro: ',check_pro)
    if str(check_pro) == str(pid):
        print ('STOPP')
        exit
    else:
        scheduler.add_job(func = login_paperless_check_service, trigger="interval", seconds=10)
        scheduler.start()
    
    session["check_pro"] = str(pid)
    print ('session: ',session["check_pro"])

    return ('success')     
