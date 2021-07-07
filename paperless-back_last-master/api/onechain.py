#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config.lib import *
from config.value import *

def Login_OneChain():
    try:
        payload = {
            "username": "onebilling",
            "orgName": "OneChain"
        }
        headers = {
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url_onechain_ForUploadFile+"/api/v1/login", json=payload, headers=headers,verify=False)
        response.raise_for_status()
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

def QueryFile_OneChain(tokenHeader,user_id,file_Id):
    try:
        payload = {
            "user_id": user_id,
            "file_id": file_Id
        }
        headers = {
            'Content-Type': "application/json",
            'Authorization' : "Bearer " + tokenHeader
        }
        response = requests.request("POST", url_onechain_ForUploadFile+"/api/v1/query/file", json=payload, headers=headers,verify=False)
        response.raise_for_status()
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

def Convert_ArrBuffer_To_Base64(data):
    try:
        payload = {
            "arrayBuffer": data
        }
        headers = {
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url_onechain_ForUploadFile+"/api/v1/convert", json=payload, headers=headers,verify=False)
        response.raise_for_status()
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
