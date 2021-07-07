#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *

filewatermark = r'watermark.pdf'

def make_watermarker_reject_cancel(strtext,strtext2):
    path = path_global_1 + '/storage/watermark/data/'
    namefile = uuid.uuid4().hex
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        pdfmetrics.registerFont(TTFont('THSarabunNew', path_global_1 + '/font/THSarabunNew.ttf')) # 
    except Exception as e:
        pass
    #ดึงไฟล์ THSarabunNew.ttf มาลงทะเบียนฟอนต์ในโค้ด
    path_Pdf = path + namefile + ".pdf"
    c = canvas.Canvas(path_Pdf) # ไฟล์ที่จะเขียน
    c.setFont("THSarabunNew", 30) # กำหนดฟอนต์ที่ใช้ และขนาดคือ 30
    datastringtext = strtext
    c.setFillColor('red',0.35)
    c.saveState()
    c.translate(500,100)
    c.rotate(45)
    c.drawCentredString(0,0,datastringtext)
    # c.drawCentredString(0,20,strtext2)
    c.drawCentredString(0,300,datastringtext)
    c.drawCentredString(0,270,strtext2)
    c.drawCentredString(0,600,datastringtext)
    c.drawCentredString(0,580,strtext2)
    c.drawCentredString(50,450,datastringtext)
    c.drawCentredString(50,420,strtext2)
    c.drawCentredString(50,150,datastringtext)
    c.drawCentredString(50,120,strtext2)
    c.restoreState()
    c.save()
    return path_Pdf

def make_watermarker(username):
    path = './temp/water/'
    namefile = uuid.uuid4().hex
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        path_Pdf = path + namefile + '.pdf'
    except Exception as ex:
        return {'result':'ER','messageText':None}
    pdfmetrics.registerFont(TTFont('RobotoBold', 'font/Roboto-Bold.ttf'))
    c = canvas.Canvas(path_Pdf)
    c.setFont("RobotoBold",50)
    username = username.upper()
    # c.setFillGray(0.5,0.5)
    c.setFillColor('gray',0.35)
    c.saveState()
    c.translate(500,100)
    c.rotate(45)
    c.drawCentredString(0,0,username)
    c.drawCentredString(50,450,username)
    c.drawCentredString(50,150,username)
    c.drawCentredString(0,300,username)
    c.drawCentredString(0,600,username)
    c.restoreState()
    c.save()
    return path_Pdf

def mergepdf_reject_cancel(page,base64_string_pdf,pdfbase64_watermarker,username):
    base64_string_pdf = base64_string_pdf
    pathPng_Pdf  = pdfbase64_watermarker
    username = username
    path = './temp/pdf/'
    namefile = uuid.uuid4().hex
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        with open(os.path.join(path + namefile + '.pdf'), 'wb') as filepdf:
            filepdf.write(base64.decodestring(str(base64_string_pdf).encode('utf8')))
        path_Pdf = path + namefile + '.pdf'
    except Exception as ex:
        print(str(ex))
        return {'result':'ER','messageText':str(e)}
    try:
        watermark = PdfFileReader(pathPng_Pdf)
        # watermark_page = watermark.getPage(page)
    except Exception as ex:
        os.remove(path_Pdf)
        os.remove(pathPng_Pdf)
        return {'result':'ER','messageText': 'page err message ' +  str(ex)}
    try:
        pdf = PdfFileReader(path_Pdf)
        pdf_writer = PdfFileWriter()
    except Exception as ex:
        os.remove(path_Pdf)
        os.remove(pathPng_Pdf)
        return {'result':'ER','messageText': 'err message ' +  str(ex)}
    
    for p in range(page):
        print(p)
        page = pdf.getPage(p)
        page.mergePage(watermark.getPage(0))
        pdf_writer.addPage(page)
        
    # for page in range(pdf.getNumPages()):
    #     pdf_page = pdf.getPage(page)
    #     pdf_page.mergePage(watermark_page)
    #     pdf_writer.addPage(pdf_page)
    os.remove(path_Pdf)
    os.remove(pathPng_Pdf)
    namefile = uuid.uuid4().hex
    path_nameFile = './temp/pdf_sign/'
    if not os.path.exists(path_nameFile):
        os.makedirs(path_nameFile)
    try:
        with open(path_nameFile + namefile +".pdf", 'wb') as fh:
            pdf_writer.write(fh)
        with open(path_nameFile + namefile +".pdf", "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        string_Pdf = (encoded_string).decode('utf8')
        string_hashPdf = hashlib.sha512(encoded_string).hexdigest()
        # result_insertLogPDF = insert().insert_LogPDF(username,string_hashPdf)
        # if result_insertLogPDF['result'] == 'OK':
        return {'result':'OK','messageText':{'responseCode':200,'responseHash':string_hashPdf,'responseMessage':'PDF upload complete.','responsePdf':(encoded_string).decode('utf8')}}
        # else:
        #     return {'result':'ER','messageText': 'err message ' + 'can;t insert'}
    except Exception as ex:
        return {'result':'ER','messageText': 'err message ' +  str(ex)}

def mergepdf(page,base64_string_pdf,pdfbase64_watermarker,username):
    page = page - 1
    base64_string_pdf = base64_string_pdf
    pathPng_Pdf  = pdfbase64_watermarker
    username = username
    path = './temp/pdf/'
    namefile = uuid.uuid4().hex
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        with open(os.path.join(path + namefile + '.pdf'), 'wb') as filepdf:
            filepdf.write(base64.decodestring(str(base64_string_pdf).encode('utf8')))
        path_Pdf = path + namefile + '.pdf'
    except Exception as ex:
        print(str(ex))
        return {'result':'ER','messageText':str(e)}
    
    
    
    try:
        watermark = PdfFileReader(pathPng_Pdf)
        watermark_page = watermark.getPage(page)
    except Exception as ex:
        os.remove(path_Pdf)
        os.remove(pathPng_Pdf)
        return {'result':'ER','messageText': 'page err message ' +  str(ex)}
    
    try:
        pdf = PdfFileReader(path_Pdf)
        pdf_writer = PdfFileWriter()
    except Exception as ex:
        os.remove(path_Pdf)
        os.remove(pathPng_Pdf)
        return {'result':'ER','messageText': 'err message ' +  str(ex)}
    

    for page in range(pdf.getNumPages()):
        pdf_page = pdf.getPage(page)
        pdf_page.mergePage(watermark_page)
        pdf_writer.addPage(pdf_page)
    os.remove(path_Pdf)
    os.remove(pathPng_Pdf)
    namefile = uuid.uuid4().hex
    path_nameFile = './temp/pdf_sign/'
    if not os.path.exists(path_nameFile):
        os.makedirs(path_nameFile)
    try:
        with open(path_nameFile + namefile +".pdf", 'wb') as fh:
            pdf_writer.write(fh)
        with open(path_nameFile + namefile +".pdf", "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        string_Pdf = (encoded_string).decode('utf8')
        string_hashPdf = hashlib.sha512(encoded_string).hexdigest()
        # result_insertLogPDF = insert().insert_LogPDF(username,string_hashPdf)
        # if result_insertLogPDF['result'] == 'OK':
        return {'result':'OK','messageText':{'responseCode':200,'responseHash':string_hashPdf,'responseMessage':'PDF upload complete.','responsePdf':(encoded_string).decode('utf8')}}
        # else:
        #     return {'result':'ER','messageText': 'err message ' + 'can;t insert'}
    except Exception as ex:
        return {'result':'ER','messageText': 'err message ' +  str(ex)}