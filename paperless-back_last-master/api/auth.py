#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config.lib import *
from config.value import *
from db.db_method import *

def send_tosign(page,llx,lly,urx,ury,userName,stringPicture,stringPdf,token_header):
    try:
        payload = "{\n    \"serviceName\": \"Etax\",\n    \"type\": \"personal\",\n    \"page\": \""+page+"\",\n    \"llx\": \""+llx+"\",\n    \"lly\": \""+lly+"\",\n    \"urx\": \""+urx+"\",\n    \"ury\": \""+ury+"\",\n    \"userName\": \""+userName+"\",\n    \"stringPicture\": \""+stringPicture+"\",\n    \"stringPdf\": \""+stringPdf+"\"\n}"

        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        response = requests.request("POST", uat_url_auth, data=(payload), headers=headers,verify=False)
        response.raise_for_status()
        if response.json()['responseCode'] == 200:
            return {'result':'OK','msg':response.json()}
        else:
            return {'result':'ER','msg':response.json()}
    except requests.Timeout as ex:
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        return {'result':'ER','msg':str(ex)}

def credentials_authorize_v2(credentialId,credentialAuthorizationData,numSignatures,hash_data,description,clientData,pin,otp,token_header):
    time_duration = ''
    one_access_token = ''
    try:
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        # hash array Data
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
        response = requests.request("POST", url_credentials_authorize_v2, json=(payload), headers=headers,verify=False,timeout=10)
        # print()
        time_duration = str(int(response.elapsed.total_seconds() * 1000))
        one_access_token = str(token_header).split()[1]
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url_credentials_authorize_v2,one_access_token,time_duration)
            return {'result':'OK','msg':response.json()}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER',str(payload),url_credentials_authorize_v2,one_access_token,time_duration)
            return {'result':'ER','msg':response.text}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_credentials_authorize_v2,one_access_token,time_duration)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_credentials_authorize_v2,one_access_token,time_duration)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_credentials_authorize_v2,one_access_token,time_duration)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_credentials_authorize_v2,one_access_token,time_duration)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_credentials_authorize_v2,one_access_token,time_duration)
        return {'result':'ER','msg':str(ex)}

def credentials_list_v3(userId,userName,maxResults,pageToken,cliendData,token_header):
    time_duration = ''
    try:
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        payload =  {
            "userId":   userId,
            "userName": userName,
            "maxResults": maxResults,
            "pageToken": pageToken,
            "cliendData": cliendData
        }
        response = requests.request("POST", url_credentials_list_v2, json=(payload), headers=headers,verify=False,timeout=5)
        one_access_token = str(token_header).split()[1]
        time_duration = str(int(response.elapsed.total_seconds() * 1000))
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url_credentials_list_v2,one_access_token,time_duration)
            return {'result':'OK','msg':response.json(),'status_Code':response.status_code}
        else:
            for x in range(2):
                response = requests.request("POST", url_credentials_list_v2, json=(payload), headers=headers,verify=False,timeout=5)
                if response.status_code == 200 or response.status_code == 201:
                    insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url_credentials_list_v2,one_access_token,time_duration)
                    return {'result':'OK','msg':response.json(),'status_Code':response.status_code}
            insert().insert_tran_log_v1(str(response.text),'ER ' + str(response.status_code),str(payload),url_credentials_list_v2,one_access_token,time_duration)
            return {'result':'ER','msg':'messge ' + str(response.text)}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_credentials_list_v2,one_access_token,time_duration)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_credentials_list_v2,one_access_token,time_duration)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_credentials_list_v2,one_access_token,time_duration)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_credentials_list_v2,one_access_token,time_duration)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_credentials_list_v2,one_access_token,time_duration)
        return {'result':'ER','msg':str(ex),'status_Code':response.status_code}


def credentials_list_v2(userId,userName,maxResults,pageToken,cliendData,token_header):
    time_duration = ''
    one_access_token = ''
    try:
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        payload =  {
            "userId":   userId,
            "userName": userName,
            "maxResults": maxResults,
            "pageToken": pageToken,
            "cliendData": cliendData
        }
        response = requests.request("POST", url_credentials_list_v2, json=(payload), headers=headers,verify=False)
        one_access_token = str(token_header).split()[1]
        time_duration = str(int(response.elapsed.total_seconds() * 1000))
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url_credentials_list_v2,one_access_token,time_duration)
            return {'result':'OK','msg':response.json(),'status_Code':response.status_code}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER ' + str(response.status_code),str(payload),url_credentials_list_v2,one_access_token,time_duration)
            return {'result':'ER','msg':'messge ' + str(response.text),'code':response.status_code}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_credentials_list_v2,one_access_token,time_duration)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_credentials_list_v2,one_access_token,time_duration)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_credentials_list_v2,one_access_token,time_duration)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_credentials_list_v2,one_access_token,time_duration)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_credentials_list_v2,one_access_token,time_duration)
        return {'result':'ER','msg':str(ex),'status_Code':response.status_code}

def signing_pdfSigning_v2(pdfData,sadData,cadData,reason,location,certifyLevel,hashAlgorithm,overwriteOriginal,visibleSignature,visibleSignaturePage,visibleSignatureRectangle,visibleSignatureImagePath,token_header):
    try:
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        payload =  {
            "pdfData": pdfData,
            "sadData": sadData,
            "cadData": cadData,
            "reason": reason,
            "location": location,
            "certifyLevel": certifyLevel,
            "hashAlgorithm": hashAlgorithm,
            "overwriteOriginal": overwriteOriginal,
            "visibleSignature": visibleSignature,
            "visibleSignaturePage": 0,
            "visibleSignatureRectangle": visibleSignatureRectangle,
            "visibleSignatureImagePath": visibleSignatureImagePath
        }
        response = requests.request("POST", url_pdfSigning_Sign_v2, json=(payload), headers=headers,verify=False)
        response.raise_for_status()
        # print(payload , url_pdfSigning_Sign_v2)
        return {'result':'OK','msg':response.json()}
    except requests.Timeout as ex:
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        return {'result':'ER','msg':str(ex)}

def signing_pdfSigning_v3(pdfData,sadData,cadData,reason,location,certifyLevel,hashAlgorithm,overwriteOriginal,visibleSignature,visibleSignaturePage,visibleSignatureRectangle,visibleSignatureImagePath,token_header,sign_position,sign_string):
    payload = ''
    one_access_token = ''
    time_duration = ''
    try:
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        visibleSignatureRectangle = '' + sign_position['sign_llx'] + ',' + sign_position['sign_lly'] + ',' + sign_position['sign_urx'] + ',' + sign_position['sign_ury'] + ''
        # print(visibleSignatureRectangle)
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
        response = requests.request("POST", url_pdfSigning_Sign_v3, json=(payload), headers=headers,verify=False,timeout=40)
        one_access_token = str(token_header).split()[1]
        time_duration = str(int(response.elapsed.total_seconds() * 1000))
        if response.status_code == 200 or response.status_code == 201:            
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url_pdfSigning_Sign_v3,one_access_token,time_duration)
            return {'result':'OK','msg':response.json()}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER ' + str(response.status_code),str(payload),url_pdfSigning_Sign_v3,one_access_token,time_duration)
            return {'result':'ER','msg':'messge ' + str(response.text)}        
        # print(payload , url_pdfSigning_Sign_v2)
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_pdfSigning_Sign_v3,one_access_token,time_duration)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_pdfSigning_Sign_v3,one_access_token,time_duration)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_pdfSigning_Sign_v3,one_access_token,time_duration)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_pdfSigning_Sign_v3,one_access_token,time_duration)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_pdfSigning_Sign_v3,one_access_token,time_duration)
        return {'result':'ER','msg':str(ex)}

def createNote_andSign_pdf_v1(pdfData,sadData,cadData,reason,location,certifyLevel,hashAlgorithm,overwriteOriginal,visibleSignature,visibleSignaturePage,visibleSignatureRectangle,visibleSignatureImagePath,token_header,sign_position,sign_string):
    try:
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        visibleSignatureRectangle = '' + sign_position['sign_llx'] + ',' + sign_position['sign_lly'] + ',' + sign_position['sign_urx'] + ',' + sign_position['sign_ury'] + ''
        print(visibleSignatureRectangle)
        visibleSignaturePage = int(sign_position['sign_page'])
        payload = {
            "pdfData": pdfData,
            "noteDisplayPage": "",
            "noteDisplayRectangle": "",
            "noteDisplayImage": "",
            "noteTitle": "",
            "noteText": "",
            "pdfSigningObj": {
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
        }
        response = requests.request("POST", url_createNoteAndSign_v1, json=(payload), headers=headers,verify=False)
        one_access_token = str(token_header).split()[1]
        if response.status_code == 200 or response.status_code == 201:  
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url_createNoteAndSign_v1,one_access_token)
            return {'result':'OK','msg':response.json()}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER ' + str(response.status_code),str(payload),url_createNoteAndSign_v1,one_access_token)
            return {'result':'ER','msg':'messge ' + str(response.text)}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_createNoteAndSign_v1,one_access_token)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_createNoteAndSign_v1,one_access_token)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_createNoteAndSign_v1,one_access_token)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_createNoteAndSign_v1,one_access_token)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_createNoteAndSign_v1,one_access_token)
        return {'result':'ER','msg':str(ex)}

def addHistory_pdf_v1(pdfData,historyData,token_header):
    try:
        payload = {}
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        payload =  {
            "pdfData": pdfData,
            "historyData": historyData
        }
        print(payload)
        response = requests.request("POST", url_addHistory_v1, json=(payload), headers=headers,verify=False)
        one_access_token = str(token_header).split()[1]
        if response.status_code == 200 or response.status_code == 201:  
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url_addHistory_v1,one_access_token)
            return {'result':'OK','msg':response.json()}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER ' + str(response.status_code),str(payload),url_addHistory_v1,one_access_token)
            return {'result':'ER','msg':'messge ' + str(response.text)}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_addHistory_v1,one_access_token)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_addHistory_v1,one_access_token)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_addHistory_v1,one_access_token)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_addHistory_v1,one_access_token)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_addHistory_v1,one_access_token)
        return {'result':'ER','msg':str(ex)}

def createNote_pdf_v1(pdfData,noteDisplayPage,noteDisplayRectangle,noteDisplayImage,noteTitle,noteText,token_header):
    try:
        if noteDisplayPage != 'all':
            noteDisplayPage = int(noteDisplayPage)
        payload = {}
        time_duration = ''
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        payload =  {
            "pdfData": pdfData,
            "noteDisplayPage": (noteDisplayPage),
            "noteDisplayRectangle": noteDisplayRectangle,
            "noteDisplayImage": noteDisplayImage,
            "noteTitle": noteTitle,
            "noteText": noteText
        }
        # print(payload)
        response = requests.request("POST", url_createNote_v1, json=(payload), headers=headers,verify=False)
        # print(response)
        time_duration = str(int(response.elapsed.total_seconds() * 1000))
        one_access_token = str(token_header).split()[1]
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload),url_createNote_v1,one_access_token)
            return {'result':'OK','msg':response.json()}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER ' + str(response.status_code),str(payload),url_createNote_v1,one_access_token,time_duration)
            return {'result':'ER','msg':'messge ' + str(response.text),'code':response.status_code}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_createNote_v1,one_access_token,time_duration)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_createNote_v1,one_access_token,time_duration)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_createNote_v1,one_access_token,time_duration)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_createNote_v1,one_access_token,time_duration)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload),url_createNote_v1,one_access_token,time_duration)
        return {'result':'ER','msg':str(ex)}

def oneAuth_get_set_sign_v2(token_header,type_sign,credentialId,image_base64_sign):
    if type_sign == 'get':
        try:
            headers = {
                'Content-Type': "application/json",
                'Authorization': token_header
            }
            payload =  {
                "credentialId": credentialId,
                "cadData": ""
            }
            response = requests.request("POST", url_oneAuth+'/webservice/api/v2/credentials/getImage', json=(payload), headers=headers,verify=False)
            one_access_token = str(token_header).split()[1]
            if response.status_code == 200 or response.status_code == 201:
                insert().insert_tran_log_v1(str(response.json()),'OK',str(payload), url_oneAuth+'/webservice/api/v2/credentials/getImage',one_access_token)
                return {'result':'OK','msg':response.json()}
            else:
                insert().insert_tran_log_v1(str(response.text),'ER ' + str(response.status_code),str(payload),url_oneAuth+'/webservice/api/v2/credentials/getImage',one_access_token)
                return {'result':'ER','msg':'messge ' + str(response.text)}
        except requests.Timeout as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(payload), url_oneAuth+'/webservice/api/v2/credentials/getImage',one_access_token)
            return {'result':'ER','msg':'Timeout ' + str(ex)}
        except requests.HTTPError as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(payload), url_oneAuth+'/webservice/api/v2/credentials/getImage',one_access_token)
            return {'result':'ER','msg':'HTTPError ' + str(ex)}
        except requests.ConnectionError as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(payload), url_oneAuth+'/webservice/api/v2/credentials/getImage',one_access_token)
            return {'result':'ER','msg':'ConnectionError ' + str(ex)}
        except requests.RequestException as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(payload), url_oneAuth+'/webservice/api/v2/credentials/getImage',one_access_token)
            return {'result':'ER','msg':'RequestException ' + str(ex)}
        except Exception as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(payload), url_oneAuth+'/webservice/api/v2/credentials/getImage',one_access_token)
            return {'result':'ER','msg':str(ex)}
    elif type_sign == 'set':
        try:
            headers = {
                'Content-Type': "application/json",
                'Authorization': token_header
            }
            payload =  {
                "credentialId": credentialId,
                "cadData": "",
                "imageData": image_base64_sign
            }
            response = requests.request("POST", url_oneAuth+'/webservice/api/v2/credentials/setImage', json=(payload), headers=headers,verify=False)
            one_access_token = str(token_header).split()[1]
            if response.status_code == 200 or response.status_code == 201:
                insert().insert_tran_log_v1(str(response.json()),'OK',str(payload), url_oneAuth+'/webservice/api/v2/credentials/setImage',one_access_token)
                return {'result':'OK','msg':response.json()}
            else:
                insert().insert_tran_log_v1(str(response.text),'ER ' + str(response.status_code),str(payload),url_oneAuth+'/webservice/api/v2/credentials/setImage',one_access_token)
                return {'result':'ER','msg':'messge ' + str(response.text)}
        except requests.Timeout as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(payload), url_oneAuth+'/webservice/api/v2/credentials/setImage',one_access_token)
            return {'result':'ER','msg':'Timeout ' + str(ex)}
        except requests.HTTPError as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(payload), url_oneAuth+'/webservice/api/v2/credentials/setImage',one_access_token)
            return {'result':'ER','msg':'HTTPError ' + str(ex)}
        except requests.ConnectionError as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(payload), url_oneAuth+'/webservice/api/v2/credentials/setImage',one_access_token)
            return {'result':'ER','msg':'ConnectionError ' + str(ex)}
        except requests.RequestException as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(payload), url_oneAuth+'/webservice/api/v2/credentials/setImage',one_access_token)
            return {'result':'ER','msg':'RequestException ' + str(ex)}
        except Exception as ex:
            insert().insert_tran_log_v1(str(ex),'ER',str(payload), url_oneAuth+'/webservice/api/v2/credentials/setImage',one_access_token)
            return {'result':'ER','msg':str(ex)}

def get_pdfData_v1(pdfData,token_header):
    try:
        one_access_token = None
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        payload =  {
             "pdfData": pdfData
        }
        url = url_oneAuth+'/webservice/api/v2/document/validateDocument'
        response = requests.request("POST", url, json=(payload), headers=headers,verify=False)
        one_access_token = str(token_header).split()[1]
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload), url,one_access_token)
            return {'result':'OK','msg':response.json()}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER ' + str(response.status_code),str(payload),url,one_access_token)
            return {'result':'ER','msg':'messge ' + str(response.text)}
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':str(ex)}

def doc_addAttachment_v1(pdfData,count,list_attachItem,token_header):
    try:        
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        payload = {
            "pdfData" : pdfData,
            "itemNo" : count,
            "attachItem" : list_attachItem
        }
        url = url_oneAuth+'/webservice/api/v2/document/addAttachment'
        response = requests.request("POST", url, json=(payload), headers=headers,verify=False)
        one_access_token = str(token_header).split()[1]
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload), url,one_access_token)
            return {'result':'OK','msg':response.json()}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER ' + str(response.status_code),str(payload),url,one_access_token)
            return {'result':'ER','msg':'messge ' + str(response.text)}            
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':str(ex)}

def doc_addAttachment_v2(pdfData,count,list_attachItem,token_header):
    try:        
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        payload = {
            "pdfData" : pdfData,
            "itemNo" : count,
            "attachItem" : list_attachItem
        }
        url = url_oneAuth+'/webservice/api/v2/document/addAttachment'
        response = requests.request("POST", url, json=(payload), headers=headers,verify=False)
        one_access_token = str(token_header).split()[1]
        if response.status_code == 200 or response.status_code == 201:
            # insert().insert_tran_log_v1(str(response.json()),'OK',str(payload), url,one_access_token)
            return {'result':'OK','msg':response.json()}
        else:
            # insert().insert_tran_log_v1(str(response.text),'ER ' + str(response.status_code),str(payload),url,one_access_token)
            return {'result':'ER','msg':'messge ' + str(response.text),'code':response.status_code}            
    except requests.Timeout as ex:
        # insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        # insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        # insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        # insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        # insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':str(ex)}

def signatureJson_api_auth_v1(payload,token_header):
    try:        
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        url = url_oneAuth+'/webservice/api/v2/signing/jsonSigning'
        response = requests.request("POST", url, json=(payload), headers=headers,verify=False)
        one_access_token = str(token_header).split()[1]
        print(response)
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload), url,one_access_token)
            return {'result':'OK','msg':response.json()}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER ' + str(response.status_code),str(payload),url,one_access_token)
            return {'result':'ER','msg':'messge ' + str(response.text),'code':response.status_code}            
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':str(ex)}

def signaturePDFJson_api_auth_v1(payload,token_header):
    try:        
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        url = url_oneAuth+'/webservice/api/v2/signing/jsonPdfSigning'
        response = requests.request("POST", url, json=(payload), headers=headers,verify=False)
        one_access_token = str(token_header).split()[1]
        print(response)
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload), url,one_access_token)
            return {'result':'OK','msg':response.json()}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER ' + str(response.status_code),str(payload),url,one_access_token)
            return {'result':'ER','msg':'messge ' + str(response.text),'code':response.status_code}            
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':str(ex)}

def checkDocumentStatus_v1(payload,token_header):
    try:        
        headers = {
            'Content-Type': "application/json",
            'Authorization': token_header
        }
        url = url_oneAuth+'/webservice/api/v2/document/checkDocumentStatus'
        response = requests.request("POST", url, json=(payload), headers=headers,verify=False)
        one_access_token = str(token_header).split()[1]
        if response.status_code == 200 or response.status_code == 201:
            insert().insert_tran_log_v1(str(response.json()),'OK',str(payload), url,one_access_token)
            return {'result':'OK','msg':response.json()}
        else:
            insert().insert_tran_log_v1(str(response.text),'ER ' + str(response.status_code),str(payload),url,one_access_token)
            return {'result':'ER','msg':'messge ' + str(response.text),'code':response.status_code}            
    except requests.Timeout as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'Timeout ' + str(ex)}
    except requests.HTTPError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'HTTPError ' + str(ex)}
    except requests.ConnectionError as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'ConnectionError ' + str(ex)}
    except requests.RequestException as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':'RequestException ' + str(ex)}
    except Exception as ex:
        insert().insert_tran_log_v1(str(ex),'ER',str(payload), url,one_access_token)
        return {'result':'ER','msg':str(ex)}