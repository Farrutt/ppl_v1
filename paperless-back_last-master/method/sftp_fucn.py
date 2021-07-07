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
from method.access import *
from method.cal_BI import *
from method.cal_file import *

# print(replace_symbol_filename('sdakfnkjasnkdfnk*****'))
class sftp_robot:
    def send_file_tosftp_new_v1(self, file_list,pathFolder,path_sftp,documentType,documentId,pdf_sign_base64,file_name_sign_pdf):
        self.file_list = file_list
        self.pathFolder = pathFolder
        self.path_sftp = path_sftp
        self.documentType = documentType
        self.documentId = documentId
        self.pdf_sign_base64 = pdf_sign_base64
        self.file_name_sign_pdf = file_name_sign_pdf
        SERVER = '203.150.197.76'  
        USER = 'ftp_user'  
        PASS = 'F9wxw,jwfhovo'
        PORT = 22
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            pathFolder_current = '.' + self.pathFolder
            path_sftp = '/Create/' + documentId
            if len(self.file_list) != 0:
                for index in range(len(file_list)):
                    file_name_new = file_list[index]['file_name_new']
                    file_name_original_new = file_list[index]['file_name_original']
                    path_file_to_sftp = pathFolder_current + file_name_new
                    path_new_file_to_sftp = pathFolder_current + file_name_original_new
                    path_new_file_to_sftp_pdf_sign = pathFolder_current + (self.file_name_sign_pdf)
                    with open(path_file_to_sftp, "rb") as pdf_file:
                        encoded_string = base64.b64encode(pdf_file.read())
                    with open(path_new_file_to_sftp, "wb") as fh:
                        fh.write(base64.decodebytes(encoded_string))
                    with pysftp.Connection(SERVER, username=USER, password=PASS,cnopts=cnopts) as sftp:
                        try:
                            sftp.chdir(path_sftp)
                        except IOError as e:
                            sftp.mkdir(path_sftp)
                            sftp.chdir(path_sftp)
                        with sftp.cd(path_sftp):
                            sftp.put(path_new_file_to_sftp)
                        if len(file_list) == (index+1):
                            with open(path_new_file_to_sftp_pdf_sign, "wb") as fh:
                                fh.write(base64.b64decode(self.pdf_sign_base64))
                            with sftp.cd(path_sftp):
                                sftp.put(path_new_file_to_sftp_pdf_sign)
                    os.remove(path_new_file_to_sftp)
                insert().insert_transactionSftp('upload sftp success',self.pathFolder,self.documentType)
                return {'result':'OK','messageText':'upload sftp success','messageER':None}
            else:
                unique_folder_name = str(uuid.uuid4())
                pathFolder_current = path_global_1 + '/storage/' + unique_folder_name
                # pathFolder_current = './storage/' + unique_folder_name
                path_new_file_to_sftp_pdf_sign = pathFolder_current + '/' + self.file_name_sign_pdf
                if not os.path.exists(pathFolder_current):
                    os.makedirs(pathFolder_current)
                with pysftp.Connection(SERVER, username=USER, password=PASS,cnopts=cnopts) as sftp:
                    print(sftp)
                    try:
                        sftp.chdir(path_sftp)
                    except IOError as e:
                        sftp.mkdir(path_sftp)
                        sftp.chdir(path_sftp)
                    print(path_new_file_to_sftp_pdf_sign)
                    with open(path_new_file_to_sftp_pdf_sign, "wb") as fh:
                        fh.write(base64.b64decode(self.pdf_sign_base64))
                    with sftp.cd(path_sftp):
                        sftp.put(path_new_file_to_sftp_pdf_sign)
                os.remove(path_new_file_to_sftp_pdf_sign)
                insert().insert_transactionSftp('upload sftp success',pathFolder_current,self.documentType)
                return {'result':'OK','messageText':'upload sftp success','messageER':None}
        except Exception as e:
            print(e)
            insert().insert_transactionSftp(str(e),self.pathFolder,self.documentType)
            return {'result':'ER','messageText':None,'messageER':str(e)}

    def send_file_tosftp_new_v2(self, file_list,pathFolder,path_sftp,documentType,documentId,pdf_sign_base64,file_name_sign_pdf,sidcode=None,doc_status=None,tax_id=None):
        self.file_list = file_list
        self.pathFolder = pathFolder
        self.path_sftp = path_sftp
        self.documentType = documentType
        self.documentId = documentId
        self.pdf_sign_base64 = pdf_sign_base64
        self.file_name_sign_pdf = self.documentType + "_" + replace_symbol_filename(str(file_name_sign_pdf))
        self.sidcode = sidcode
        self.doc_status = doc_status
        self.tax_id = tax_id
        # print(self.tax_id,'tax_idAAAAAAAAAAAAAAAAA')
        checkfilename = []
        listarr_pathjson = []
        filename = str(uuid.uuid4())
        SERVER = '203.150.197.76'  
        USER = 'ftp_user'  
        PASS = 'F9wxw,jwfhovo'
        PORT = 22
        path_sftp = '/' + self.tax_id
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            pathFolder_current = path_global_1 + self.pathFolder
            print(self.documentType)
            # arrtype = ['csact','csnib','csttm','cstdc','csims','csman','csinb']
            if 'cs' in self.documentType:
                r_callsub = call_service_SCS_RPA(self.sidcode)
                if r_callsub == 'eformppl':
                    path_sftp += '/SO/Eform/SO_Create/' +documentId
                    r = select_4().select_dataeformfor_rpa_v1(self.sidcode)
                    if r['result'] == 'OK':
                        pathjsondata = path_global_1 + '/temp/' 
                        if not os.path.exists(pathjsondata):
                            os.makedirs(pathjsondata)
                        pathjsondata_file = path_global_1 + '/temp/' + filename + '.json'
                        logger.info(pathjsondata)
                        logger.info(pathjsondata_file)
                        dataeform = r['data'][0]['data_document']
                        tmpdataeform = data_doc(dataeform)
                        if tmpdataeform['result'] == 'OK':
                            eformdata = tmpdataeform['messageText']
                            if 'formdata_eform' in eformdata:
                                if 'data_json_key' in eformdata['formdata_eform']:
                                    strjsondata = (eformdata['formdata_eform']['data_json_key'])
                                    with open(pathjsondata_file, 'w', encoding='utf-8') as f:
                                        json.dump(strjsondata, f, ensure_ascii=False, indent=4)
                                    listarr_pathjson.append(str(pathjsondata_file))
                else:
                    path_sftp += '/SO/Create/' +documentId
            # elif self.documentType in arrtype:
            #     r_callsub = call_service_SCS_RPA(self.sidcode)
            #     if r_callsub == 'eformppl':
            #         path_sftp += '/SO/Eform/SO_Create/' +documentId
            #         r = select_4().select_dataeformfor_rpa_v1(self.sidcode)
            #         if r['result'] == 'OK':
            #             pathjsondata = path_global_1 + '/temp/' 
            #             if not os.path.exists(pathjsondata):
            #                 os.makedirs(pathjsondata)
            #             pathjsondata_file = path_global_1 + '/temp/' + filename + '.json'
            #             logger.info(pathjsondata)
            #             logger.info(pathjsondata_file)
            #             dataeform = r['data'][0]['data_document']
            #             tmpdataeform = data_doc(dataeform)
            #             if tmpdataeform['result'] == 'OK':
            #                 eformdata = tmpdataeform['messageText']
            #                 if 'formdata_eform' in eformdata:
            #                     if 'data_json_key' in eformdata['formdata_eform']:
            #                         strjsondata = (eformdata['formdata_eform']['data_json_key'])
            #                         with open(pathjsondata_file, 'w', encoding='utf-8') as f:
            #                             json.dump(strjsondata, f, ensure_ascii=False, indent=4)
            #                         listarr_pathjson.append(str(pathjsondata_file))
            #     else:
            #         path_sftp += '/SO/Create/' +documentId
            elif self.documentType == 'cspoc':
                path_sftp += '/POC/eform_poc/POC_create/' +documentId
                r = select_4().select_dataeformfor_rpa_v1(self.sidcode)
                if r['result'] == 'OK':
                    pathjsondata = path_global_1 + '/temp/' 
                    if not os.path.exists(pathjsondata):
                        os.makedirs(pathjsondata)
                    pathjsondata_file = path_global_1 + '/temp/' + filename + '.json'
                    logger.info(pathjsondata)
                    logger.info(pathjsondata_file)
                    dataeform = r['data'][0]['data_document']
                    tmpdataeform = data_doc(dataeform)
                    if tmpdataeform['result'] == 'OK':
                        eformdata = tmpdataeform['messageText']
                        if 'formdata_eform' in eformdata:
                            if 'data_json_key' in eformdata['formdata_eform']:
                                strjsondata = (eformdata['formdata_eform']['data_json_key'])
                                # logger.info(strjsondata)
                                with open(pathjsondata_file, 'w', encoding='utf-8') as f:
                                    json.dump(strjsondata, f, ensure_ascii=False, indent=4)
                                    # fh.write(strjsondata)
                                listarr_pathjson.append(str(pathjsondata_file))
            elif self.documentType == 'cs':
                r_callsub = call_service_SCS_RPA(self.sidcode)
                if r_callsub == 'eformppl':
                    path_sftp += '/SO/Eform/SO_Create/' +documentId
                    r = select_4().select_dataeformfor_rpa_v1(self.sidcode)
                    if r['result'] == 'OK':
                        pathjsondata = path_global_1 + '/temp/' 
                        if not os.path.exists(pathjsondata):
                            os.makedirs(pathjsondata)
                        pathjsondata_file = path_global_1 + '/temp/' + filename + '.json'
                        logger.info(pathjsondata)
                        logger.info(pathjsondata_file)
                        dataeform = r['data'][0]['data_document']
                        tmpdataeform = data_doc(dataeform)
                        if tmpdataeform['result'] == 'OK':
                            eformdata = tmpdataeform['messageText']
                            if 'formdata_eform' in eformdata:
                                if 'data_json_key' in eformdata['formdata_eform']:
                                    strjsondata = (eformdata['formdata_eform']['data_json_key'])
                                    with open(pathjsondata_file, 'w', encoding='utf-8') as f:
                                        json.dump(strjsondata, f, ensure_ascii=False, indent=4)
                                    listarr_pathjson.append(str(pathjsondata_file))
                else:
                    path_sftp += '/SO/Create/' +documentId
            elif self.documentType == 'scs':
                r_callsub = call_service_SCS_RPA(self.sidcode)
                if r_callsub == 'eformppl':
                    path_sftp += '/SO/Eform/SO_Create/' +documentId
                    r = select_4().select_dataeformfor_rpa_v1(self.sidcode)
                    if r['result'] == 'OK':
                        pathjsondata = path_global_1 + '/temp/' 
                        if not os.path.exists(pathjsondata):
                            os.makedirs(pathjsondata)
                        pathjsondata_file = path_global_1 + '/temp/' + filename + '.json'
                        logger.info(pathjsondata)
                        logger.info(pathjsondata_file)
                        dataeform = r['data'][0]['data_document']
                        tmpdataeform = data_doc(dataeform)
                        if tmpdataeform['result'] == 'OK':
                            eformdata = tmpdataeform['messageText']
                            if 'formdata_eform' in eformdata:
                                if 'data_json_key' in eformdata['formdata_eform']:
                                    strjsondata = (eformdata['formdata_eform']['data_json_key'])
                                    # logger.info(strjsondata)
                                    with open(pathjsondata_file, 'w', encoding='utf-8') as f:
                                        json.dump(strjsondata, f, ensure_ascii=False, indent=4)
                                        # fh.write(strjsondata)
                                    listarr_pathjson.append(str(pathjsondata_file))
                else:
                    path_sftp += '/SO/Create/' +documentId
            elif self.documentType == 'scst':
                r_callsub = call_service_SCS_RPA(self.sidcode)
                if r_callsub == 'eformppl':
                    path_sftp += '/SO/Eform/SO_Create/' +documentId
                    r = select_4().select_dataeformfor_rpa_v1(self.sidcode)
                    if r['result'] == 'OK':
                        pathjsondata = path_global_1 + '/temp/' 
                        if not os.path.exists(pathjsondata):
                            os.makedirs(pathjsondata)
                        pathjsondata_file = path_global_1 + '/temp/' + filename + '.json'
                        logger.info(pathjsondata)
                        logger.info(pathjsondata_file)
                        dataeform = r['data'][0]['data_document']
                        tmpdataeform = data_doc(dataeform)
                        if tmpdataeform['result'] == 'OK':
                            eformdata = tmpdataeform['messageText']
                            if 'formdata_eform' in eformdata:
                                if 'data_json_key' in eformdata['formdata_eform']:
                                    strjsondata = (eformdata['formdata_eform']['data_json_key'])
                                    with open(pathjsondata_file, 'w', encoding='utf-8') as f:
                                        json.dump(strjsondata, f, ensure_ascii=False, indent=4)
                                    listarr_pathjson.append(str(pathjsondata_file))
                else:
                    path_sftp += '/SO/Create/' +documentId
            elif self.documentType == 'tm':
                path_sftp += '/Terminate/Create/' +documentId
                r = select_4().select_dataeformfor_rpa_v1(self.sidcode)
                if r['result'] == 'OK':
                    pathjsondata = path_global_1 + '/temp/' 
                    if not os.path.exists(pathjsondata):
                        os.makedirs(pathjsondata)
                    pathjsondata_file = path_global_1 + '/temp/' + filename + '.json'
                    logger.info(pathjsondata)
                    logger.info(pathjsondata_file)
                    dataeform = r['data'][0]['data_document']
                    tmpdataeform = data_doc(dataeform)
                    if tmpdataeform['result'] == 'OK':
                        eformdata = tmpdataeform['messageText']
                        if 'formdata_eform' in eformdata:
                            if 'data_json_key' in eformdata['formdata_eform']:
                                strjsondata = (eformdata['formdata_eform']['data_json_key'])
                                # logger.info(strjsondata)
                                with open(pathjsondata_file, 'w', encoding='utf-8') as f:
                                    json.dump(strjsondata, f, ensure_ascii=False, indent=4)
                                    # fh.write(strjsondata)
                                listarr_pathjson.append(str(pathjsondata_file))
            elif self.documentType == 'tms':
                path_sftp += '/Terminate/Create/' +documentId
                r = select_4().select_dataeformfor_rpa_v1(self.sidcode)
                if r['result'] == 'OK':
                    pathjsondata = path_global_1 + '/temp/' 
                    if not os.path.exists(pathjsondata):
                        os.makedirs(pathjsondata)
                    pathjsondata_file = path_global_1 + '/temp/' + filename + '.json'
                    logger.info(pathjsondata)
                    logger.info(pathjsondata_file)
                    dataeform = r['data'][0]['data_document']
                    tmpdataeform = data_doc(dataeform)
                    if tmpdataeform['result'] == 'OK':
                        eformdata = tmpdataeform['messageText']
                        if 'formdata_eform' in eformdata:
                            if 'data_json_key' in eformdata['formdata_eform']:
                                strjsondata = (eformdata['formdata_eform']['data_json_key'])
                                # logger.info(strjsondata)
                                with open(pathjsondata_file, 'w', encoding='utf-8') as f:
                                    json.dump(strjsondata, f, ensure_ascii=False, indent=4)
                                    # fh.write(strjsondata)
                                listarr_pathjson.append(str(pathjsondata_file))
            elif self.documentType == 'po':
                tmpstatus_refdocument = False
                r = select_4().select_RefDocumnet(self.sidcode)
                if r['result'] == 'OK':
                    tmpstatus_refdocument = r['message']
                if tmpstatus_refdocument == False:
                    path_sftp += '/PO/CreatePO/' +documentId
                    r = select_4().select_dataeformfor_rpa_v1(self.sidcode)
                    if r['result'] == 'OK':
                        pathjsondata = path_global_1 + '/temp/' 
                        if not os.path.exists(pathjsondata):
                            os.makedirs(pathjsondata)
                        pathjsondata_file = path_global_1 + '/temp/' + filename + '.json'
                        logger.info(pathjsondata)
                        logger.info(pathjsondata_file)
                        dataeform = r['data'][0]['data_document']
                        tmpdataeform = data_doc(dataeform)
                        if tmpdataeform['result'] == 'OK':
                            eformdata = tmpdataeform['messageText']
                            if 'formdata_eform' in eformdata:
                                if 'data_json_key' in eformdata['formdata_eform']:
                                    strjsondata = (eformdata['formdata_eform']['data_json_key'])
                                    # logger.info(strjsondata)
                                    with open(pathjsondata_file, 'w', encoding='utf-8') as f:
                                        json.dump(strjsondata, f, ensure_ascii=False, indent=4)
                                        # fh.write(strjsondata)
                                    listarr_pathjson.append(str(pathjsondata_file))
                elif tmpstatus_refdocument == True:
                    path_sftp += '/PO/FinalPO/' +documentId
                    r = select_4().select_dataeformfor_rpa_v1(self.sidcode)
                    if r['result'] == 'OK':
                        pathjsondata = path_global_1 + '/temp/' 
                        if not os.path.exists(pathjsondata):
                            os.makedirs(pathjsondata)
                        pathjsondata_file = path_global_1 + '/temp/' + filename + '.json'
                        logger.info(pathjsondata)
                        logger.info(pathjsondata_file)
                        dataeform = r['data'][0]['data_document']
                        tmpdataeform = data_doc(dataeform)
                        if tmpdataeform['result'] == 'OK':
                            eformdata = tmpdataeform['messageText']
                            if 'formdata_eform' in eformdata:
                                if 'data_json_key' in eformdata['formdata_eform']:
                                    strjsondata = (eformdata['formdata_eform']['data_json_key'])
                                    # logger.info(strjsondata)
                                    with open(pathjsondata_file, 'w', encoding='utf-8') as f:
                                        json.dump(strjsondata, f, ensure_ascii=False, indent=4)
                                        # fh.write(strjsondata)
                                    listarr_pathjson.append(str(pathjsondata_file))
            elif self.documentType == 'poc':
                path_sftp += '/POC/eform_poc/POC_create/' +documentId
                r = select_4().select_dataeformfor_rpa_v1(self.sidcode)
                if r['result'] == 'OK':
                    pathjsondata = path_global_1 + '/temp/' 
                    if not os.path.exists(pathjsondata):
                        os.makedirs(pathjsondata)
                    pathjsondata_file = path_global_1 + '/temp/' + filename + '.json'
                    logger.info(pathjsondata)
                    logger.info(pathjsondata_file)
                    dataeform = r['data'][0]['data_document']
                    tmpdataeform = data_doc(dataeform)
                    if tmpdataeform['result'] == 'OK':
                        eformdata = tmpdataeform['messageText']
                        if 'formdata_eform' in eformdata:
                            if 'data_json_key' in eformdata['formdata_eform']:
                                strjsondata = (eformdata['formdata_eform']['data_json_key'])
                                with open(pathjsondata_file, 'w', encoding='utf-8') as f:
                                    json.dump(strjsondata, f, ensure_ascii=False, indent=4)
                                listarr_pathjson.append(str(pathjsondata_file))
                else:
                    path_sftp += '/POC/eform_poc/POC_create/' +documentId                                  
            elif self.documentType == 'spo':
                tmpstatus_refdocument = False
                r = select_4().select_RefDocumnet(self.sidcode)
                if r['result'] == 'OK':
                    tmpstatus_refdocument = r['message']
                if tmpstatus_refdocument == False:
                    path_sftp += '/PO/CreatePO/' +documentId
                elif tmpstatus_refdocument == True:
                    path_sftp += '/PO/FinalPO/' +documentId                
            elif self.documentType == 'cerhr':
                path_sftp += '/Payroll/FilePDF/' +documentId
                if self.doc_status == 'R':
                    pathjsondata = path_global_1 + '/temp/' 
                    if not os.path.exists(pathjsondata):
                        os.makedirs(pathjsondata)
                    pathjsondata_file = path_global_1 + '/temp/REJECT.txt'
                    # logger.info(pathjsondata)
                    logger.info(pathjsondata_file)
                    # dataeform = r['data'][0]['data_document']
                    # tmpdataeform = data_doc(dataeform)
                    # if tmpdataeform['result'] == 'OK':
                    #     eformdata = tmpdataeform['messageText']
                    #     if 'formdata_eform' in eformdata:
                    #         if 'data_json_key' in eformdata['formdata_eform']:
                    #             strjsondata = (eformdata['formdata_eform']['data_json_key'])
                    with open(pathjsondata_file, 'w') as f:
                        f.write("REJECT")
                        # json.dump(strjsondata, f, ensure_ascii=False, indent=4)
                    listarr_pathjson.append(str(pathjsondata_file))
            elif self.documentType == 'chman':
                path_sftp += '/Payroll/FilePDF/' +documentId
                if self.doc_status == 'R':
                    pathjsondata = path_global_1 + '/temp/' 
                    if not os.path.exists(pathjsondata):
                        os.makedirs(pathjsondata)
                    pathjsondata_file = path_global_1 + '/temp/REJECT.txt'
                    # logger.info(pathjsondata)
                    logger.info(pathjsondata_file)
                    # dataeform = r['data'][0]['data_document']
                    # tmpdataeform = data_doc(dataeform)
                    # if tmpdataeform['result'] == 'OK':
                    #     eformdata = tmpdataeform['messageText']
                    #     if 'formdata_eform' in eformdata:
                    #         if 'data_json_key' in eformdata['formdata_eform']:
                    #             strjsondata = (eformdata['formdata_eform']['data_json_key'])
                    with open(pathjsondata_file, 'w') as f:
                        f.write("REJECT")
                        # json.dump(strjsondata, f, ensure_ascii=False, indent=4)
                    listarr_pathjson.append(str(pathjsondata_file))
            elif self.documentType == 'pcm':
                path_sftp += '/grn/wait/' +documentId
            elif self.documentType == 'spr':
                path_sftp += '/PO/PRtoPO/PR/' +documentId
            elif self.documentType == 'qtnw':
                path_sftp += '/carrier/create/' +documentId
            elif self.documentType == 'qts':
                path_sftp += '/qt/Create/' +documentId
                r = select_4().select_dataeformfor_rpa_v1(self.sidcode)
                if r['result'] == 'OK':
                    pathjsondata = path_global_1 + '/temp/' 
                    if not os.path.exists(pathjsondata):
                        os.makedirs(pathjsondata)
                    pathjsondata_file = path_global_1 + '/temp/' + filename + '.json'
                    logger.info(pathjsondata)
                    logger.info(pathjsondata_file)
                    dataeform = r['data'][0]['data_document']
                    tmpdataeform = data_doc(dataeform)
                    if tmpdataeform['result'] == 'OK':
                        eformdata = tmpdataeform['messageText']
                        if 'formdata_eform' in eformdata:
                            if 'data_json_key' in eformdata['formdata_eform']:
                                strjsondata = (eformdata['formdata_eform']['data_json_key'])
                                # logger.info(strjsondata)
                                with open(pathjsondata_file, 'w', encoding='utf-8') as f:
                                    json.dump(strjsondata, f, ensure_ascii=False, indent=4)
                                    # fh.write(strjsondata)
                                listarr_pathjson.append(str(pathjsondata_file))
            elif self.documentType == 'qt':
                path_sftp += '/qt/Create/' +documentId
                r = select_4().select_dataeformfor_rpa_v1(self.sidcode)
                if r['result'] == 'OK':
                    pathjsondata = path_global_1 + '/temp/' 
                    if not os.path.exists(pathjsondata):
                        os.makedirs(pathjsondata)
                    pathjsondata_file = path_global_1 + '/temp/' + filename + '.json'
                    logger.info(pathjsondata)
                    logger.info(pathjsondata_file)
                    dataeform = r['data'][0]['data_document']
                    tmpdataeform = data_doc(dataeform)
                    if tmpdataeform['result'] == 'OK':
                        eformdata = tmpdataeform['messageText']
                        if 'formdata_eform' in eformdata:
                            if 'data_json_key' in eformdata['formdata_eform']:
                                strjsondata = (eformdata['formdata_eform']['data_json_key'])
                                # logger.info(strjsondata)
                                with open(pathjsondata_file, 'w', encoding='utf-8') as f:
                                    json.dump(strjsondata, f, ensure_ascii=False, indent=4)
                                    # fh.write(strjsondata)
                                listarr_pathjson.append(str(pathjsondata_file))
            elif self.documentType == 'cspa':
                r_callsub = call_service_SCS_RPA(self.sidcode)
                if r_callsub == 'eformppl':
                    path_sftp += '/SO/Eform/SO_Create/' +documentId
                    r = select_4().select_dataeformfor_rpa_v1(self.sidcode)
                    if r['result'] == 'OK':
                        pathjsondata = path_global_1 + '/temp/' 
                        if not os.path.exists(pathjsondata):
                            os.makedirs(pathjsondata)
                        pathjsondata_file = path_global_1 + '/temp/' + filename + '.json'
                        logger.info(pathjsondata)
                        logger.info(pathjsondata_file)
                        dataeform = r['data'][0]['data_document']
                        tmpdataeform = data_doc(dataeform)
                        if tmpdataeform['result'] == 'OK':
                            eformdata = tmpdataeform['messageText']
                            if 'formdata_eform' in eformdata:
                                if 'data_json_key' in eformdata['formdata_eform']:
                                    strjsondata = (eformdata['formdata_eform']['data_json_key'])
                                    with open(pathjsondata_file, 'w', encoding='utf-8') as f:
                                        json.dump(strjsondata, f, ensure_ascii=False, indent=4)
                                    listarr_pathjson.append(str(pathjsondata_file))
                else:
                    path_sftp += '/SO/Create/' +documentId

            print(path_sftp)
            if len(self.file_list) != 0:
                for index in range(len(file_list)):
                    file_name_new = file_list[index]['file_name_new']
                    file_name_original_new = file_list[index]['file_name_original']
                    path_file_to_sftp = pathFolder_current + file_name_new
                    # print(checkfilename)
                    if replace_symbol_filename(str(file_name_original_new)) not in checkfilename:
                        checkfilename.append(replace_symbol_filename(str(file_name_original_new)))
                        path_new_file_to_sftp = pathFolder_current + replace_symbol_filename(str(file_name_original_new))
                    else:
                        path_new_file_to_sftp = pathFolder_current + str(index) +'-' + replace_symbol_filename(str(file_name_original_new))
                    print(path_new_file_to_sftp)
                    path_new_file_to_sftp_pdf_sign = pathFolder_current + self.file_name_sign_pdf
                    try:
                        with open(path_file_to_sftp, "rb") as pdf_file:
                            encoded_string = base64.b64encode(pdf_file.read())
                        with open(path_new_file_to_sftp, "wb") as fh:
                            fh.write(base64.decodebytes(encoded_string))
                    except Exception as e:
                        pass
                    if len(listarr_pathjson) != 0:
                        with pysftp.Connection(SERVER, username=USER, password=PASS,cnopts=cnopts) as sftp:
                            try:
                                sftp.chdir(path_sftp)
                            except IOError as e:
                                sftp.mkdir(path_sftp)
                                sftp.chdir(path_sftp)
                            with sftp.cd(path_sftp):
                                sftp.put(listarr_pathjson[0])
                        listarr_pathjson = []
                    with pysftp.Connection(SERVER, username=USER, password=PASS,cnopts=cnopts) as sftp:
                        try:
                            sftp.chdir(path_sftp)
                        except IOError as e:
                            sftp.mkdir(path_sftp)
                            sftp.chdir(path_sftp)
                        try:
                            with sftp.cd(path_sftp):
                                sftp.put(path_new_file_to_sftp)
                        except Exception as e:
                            pass
                        if len(file_list) == (index+1):
                            print(path_new_file_to_sftp_pdf_sign)
                            with open(path_new_file_to_sftp_pdf_sign, "wb") as fh:
                                fh.write(base64.b64decode(self.pdf_sign_base64))
                            with sftp.cd(path_sftp):
                                sftp.put(path_new_file_to_sftp_pdf_sign)
                    try:
                        os.remove(path_new_file_to_sftp)
                    except Exception as e:
                        pass
                insert().insert_transactionSftp('upload sftp success',self.pathFolder,self.documentType)
                return {'result':'OK','messageText':'upload sftp success','messageER':None}
            else:
                unique_folder_name = str(uuid.uuid4())
                pathFolder_current = path_global_1 + '/storage/' + unique_folder_name
                path_new_file_to_sftp_pdf_sign = pathFolder_current + '/' + self.file_name_sign_pdf
                logger.info(path_new_file_to_sftp_pdf_sign)
                if not os.path.exists(pathFolder_current):
                    os.makedirs(pathFolder_current)
                if len(listarr_pathjson) != 0:
                    with pysftp.Connection(SERVER, username=USER, password=PASS,cnopts=cnopts) as sftp:
                        try:
                            sftp.chdir(path_sftp)
                        except IOError as e:
                            sftp.mkdir(path_sftp)
                            sftp.chdir(path_sftp)
                        with sftp.cd(path_sftp):
                            sftp.put(listarr_pathjson[0])
                    listarr_pathjson = []
                    
                with pysftp.Connection(SERVER, username=USER, password=PASS,cnopts=cnopts) as sftp:
                    try:
                        sftp.chdir(path_sftp)
                    except IOError as e:
                        sftp.mkdir(path_sftp)
                        sftp.chdir(path_sftp)
                    with open(path_new_file_to_sftp_pdf_sign, "wb") as fh:
                        fh.write(base64.b64decode(self.pdf_sign_base64))
                    with sftp.cd(path_sftp):
                        sftp.put(path_new_file_to_sftp_pdf_sign)
                os.remove(path_new_file_to_sftp_pdf_sign)
                insert().insert_transactionSftp('upload sftp success',pathFolder_current,self.documentType)
                return {'result':'OK','messageText':'upload sftp success','messageER':None}
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            insert().insert_transactionSftp(str(e),self.pathFolder,self.documentType)
            return {'result':'ER','messageText':None,'messageER':str(e)}

    def send_file_tosftp_v1(self,file_list,pathFolder,path_sftp,documentType):
        self.file_list = file_list
        self.pathFolder = pathFolder
        self.path_sftp = path_sftp
        self.documentType = documentType
        SERVER = '203.150.197.76'  
        USER = 'ftp_user'  
        PASS = 'F9wxw,jwfhovo'
        PORT = 22
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            pathFolder_current = '.' + self.pathFolder 
            for index in range(len(file_list)):
                file_name_new = file_list[index]['file_name_new']
                file_name_original_new = file_list[index]['file_name_original']
                if '.xls' in file_name_new or '.xlsx' in file_name_new:
                    path_file_to_sftp = pathFolder_current + file_name_new
                    path_new_file_to_sftp = pathFolder_current + file_name_original_new
                    with open(path_file_to_sftp, "rb") as pdf_file:
                        encoded_string = base64.b64encode(pdf_file.read())
                    with open(path_new_file_to_sftp, "wb") as fh:
                        fh.write(base64.decodebytes(encoded_string))     
                    with pysftp.Connection(SERVER, username=USER, password=PASS,cnopts=cnopts) as sftp:
                        with sftp.cd(path_sftp):
                            sftp.put(path_new_file_to_sftp)
                    os.remove(path_new_file_to_sftp)
            insert().insert_transactionSftp('upload sftp success',self.pathFolder,self.documentType)
            return {'result':'OK','messageText':'upload sftp success','messageER':None}
        except Exception as e:
            insert().insert_transactionSftp(str(e),self.pathFolder,self.documentType)
            return {'result':'ER','messageText':None,'messageER':str(e)}
    
    def send_file_tosftp_v1_cspoc(self,file_list,pathFolder):
        self.file_list = file_list
        self.pathFolder = pathFolder
        SERVER = '203.150.197.76'  
        USER = 'ftp_user'  
        PASS = 'F9wxw,jwfhovo'
        PORT = 22
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            pathFolder_current = '.' + self.pathFolder 
            for index in range(len(file_list)):
                file_name_new = file_list[index]['file_name_new']
                file_name_original_new = file_list[index]['file_name_original']
                if '.xls' in file_name_new or '.xlsx' in file_name_new:
                    path_file_to_sftp = pathFolder_current + file_name_new
                    path_new_file_to_sftp = pathFolder_current + file_name_original_new
                    with open(path_file_to_sftp, "rb") as pdf_file:
                        encoded_string = base64.b64encode(pdf_file.read())
                    with open(path_new_file_to_sftp, "wb") as fh:
                        fh.write(base64.decodebytes(encoded_string))     
                    with pysftp.Connection(SERVER, username=USER, password=PASS,cnopts=cnopts) as sftp:
                        with sftp.cd('/Create/CSPOC'):
                            sftp.put(path_new_file_to_sftp)
                    os.remove(path_new_file_to_sftp)
            insert().insert_transactionSftp('upload sftp success',self.pathFolder,'CSPOC')
            return {'result':'OK','messageText':'upload sftp success','messageER':None}
        except Exception as e:
            insert().insert_transactionSftp(str(e),self.pathFolder,'CSPOC')
            return {'result':'ER','messageText':None,'messageER':str(e)}