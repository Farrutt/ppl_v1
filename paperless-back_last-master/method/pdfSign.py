#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config.lib import *
from config.value import *
from db.db_method import *

def createfile_pdfsign_v1(pdfdata,hashpdf):  
    folder_name = str(uuid.uuid4())
    file_name = str(uuid.uuid4())
    path_pdf = path_global_1 + '/storage/pdfsign/' + folder_name + '/original/' 
    path_pdf_sign = path_global_1 + '/storage/pdfsign/' + folder_name + '/sign/'
    path_data = path_global_1 + '/storage/pdfsign/' + folder_name
    arr_pathpdf = [path_data,path_pdf,path_pdf_sign]
    for path in arr_pathpdf:
        if not os.path.exists(path):
            os.makedirs(path)
    try:
        org_addressfile = path_pdf + file_name + '.txt'
        hash_addressfile = path_pdf + file_name + '-hash.txt'   
        with open(org_addressfile, 'w') as out_file:
            out_file.write(pdfdata)
        with open(hash_addressfile, 'w') as out_file:
            out_file.write(hashpdf)
        return {'result':'OK','path_pdf':org_addressfile,'path_pdfhash':hash_addressfile,'path_pdfsign':path_pdf_sign,'path_data':path_data}
    except Exception as e:
        print(str(e))
        return {'result':'ER'}

def updatefile_pdfsign_v1(pdfdata,hashpdf,pathsignpdf):
    file_name = str(uuid.uuid4())
    folder_name = str(uuid.uuid4())
    try:
        if pathsignpdf != None:
            org_addressfile = pathsignpdf +'/sign/'+ file_name + '.txt'
            hash_addressfile = pathsignpdf +'/sign/'+ file_name + '-hash.txt'   
            with open(org_addressfile, 'w') as out_file:
                out_file.write(pdfdata)
            with open(hash_addressfile, 'w') as out_file:
                out_file.write(hashpdf)
            return {'result':'OK','path_pdf':org_addressfile,'path_pdfhash':hash_addressfile}
        else:
            pathsignpdf = path_global_1 + '/storage/pdfsign/' + folder_name
            path_pdf = path_global_1 + '/storage/pdfsign/' + folder_name + '/original/' 
            path_pdf_sign = path_global_1 + '/storage/pdfsign/' + folder_name + '/sign/'
            arr_pathpdf = [pathsignpdf,path_pdf,path_pdf_sign]
            for path in arr_pathpdf:
                print(path)
                if not os.path.exists(path):
                    os.makedirs(path)
            org_addressfile = pathsignpdf +'/sign/'+ file_name + '.txt'
            hash_addressfile = pathsignpdf +'/sign/'+ file_name + '-hash.txt'   
            with open(org_addressfile, 'w') as out_file:
                out_file.write(pdfdata)
            with open(hash_addressfile, 'w') as out_file:
                out_file.write(hashpdf)
            return {'result':'OK','path_pdf':org_addressfile,'path_pdfhash':hash_addressfile,'path_data':pathsignpdf}
    except Exception as e:
        print(str(e))
        return {'result':'ER'}

def readfile_pdfsign_v1(pathsignpdf):
    try:  
        with open(pathsignpdf, "r") as file:
            lines = [line.rstrip() for line in file]
        return {'result':'OK','basePDF':lines}
    except Exception as e:
        print(str(e))
        return {'result':'ER'}