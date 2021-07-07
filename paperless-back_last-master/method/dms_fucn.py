#!/usr/bin/env python3
# -*- coding: utf-8 -*-
username = "admin"
password="abcABC123"
path_file_upload="D:\\C10T006549\\testUpload01.txt"
url = "https://be1dms-ppl.inet.co.th/alfresco"
id_folder = '60c26d7e-3127-4e23-a73f-eeb69e3fdea2'

def add_file_to_dms(url, username, password, id_folder, path_file_upload):
    s = requests.Session()
    s.auth = (username, password)
    groups = "test"
    # Add Files to DMS
    dms_path_add_file = "/api/-default-/public/alfresco/versions/1/nodes/"+id_folder+"/children"
    files_name = {
        'filedata': open(path_file_upload, 'rb')
    }
    response_addfile_one=s.request("POST", url + dms_path_add_file, files=files_name).json()
    # print (response_addfile_one)

    # Add Permission files
    path_permission_file_one = "/api/-default-/public/alfresco/versions/1/nodes/" + response_addfile_one['entry']['id']
    payload =   {
                    "permissions":
                    { 
                        "isInheritanceEnabled":False,
                        "locallySet":
                        [
                            {  
                                "authorityId":"GROUP_" + groups + "",
                                "name":"Preview",
                                "accessStatus":"ALLOWED"
                            }
                        ]
                    }
                }
    s.request("PUT", url + path_permission_file_one, data=payload).json()
    return {'import_result':'success'}

# print(add_file_to_dms(url, username, password, id_folder, path_file_upload))