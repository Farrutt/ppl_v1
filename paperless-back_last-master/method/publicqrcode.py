#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from controller.mail_string import *
from controller.validate import *
from db.db_method import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *

if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less


def genarateQrcode_public(url):
    path = 'temp/qr/'
    if not os.path.exists(path):
        os.makedirs(path)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    data = url
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    unique_qrcode = str(uuid.uuid4())
    img.save(path + unique_qrcode + ".jpg")
    path_qrcode = path + unique_qrcode + ".jpg"
    with open(path_qrcode, "rb") as imageFile:
        str_qr = base64.b64encode(imageFile.read())
    str_qr = (str_qr).decode('utf8')
    os.remove(path_qrcode)
    return str_qr


def genPdf_Topng_qr_pulic(urx,ury,llx,lly,stringPicture):
    urx = urx
    ury = ury
    llx = llx
    lly = lly
    stringPicture = stringPicture
    # url = pyqrcode.create(content,mode='binary')
    # url.png('qrcode.png',scale=6,module_color=[0,0,0,128],background=[0x00,0xC0,0xFF])
    try:
        imgdata = base64.b64decode(stringPicture)
        namefile = uuid.uuid4().hex
        path = './temp/sign/'  # I assume you have a way of picking unique filenames
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + namefile + '.png', 'wb') as f:
            f.write(imgdata)
            f.close()            
    except Exception as ex:
        return {'result':'ER','messageText':None}
    try:
        pdf = FPDF()
        pdf.add_page()
        width = urx*100
        height = ury*100
        percentTomm_width = (width * 210) / 100
        percentTomm_height = (height * 297) / 100
        
        gan_x = llx * 100
        gan_y = (1 - lly) * 100
        percentTomm_x = (gan_x * 210) / 100
        percentTomm_y = (gan_y * 297) / 100
        # percentTomm_x = (percentTomm_x-percentTomm_width)
        percentTomm_y = (percentTomm_y-percentTomm_height)
    except Exception as ex:
        return {'result':'ER','path':None}
    # print(percentTomm_width , percentTomm_height , percentTomm_x,percentTomm_y)
    pdf.image(path + namefile + '.png', x=percentTomm_x, y=percentTomm_y, w=percentTomm_width,h=percentTomm_height)
    os.remove(path + namefile + '.png')
    pdf.output(path + namefile + '.pdf','F')
    return {'result':'OK','messageText':path + namefile + '.pdf'}


def merge_png_to_pdf_qrCode_public(page,base64_string_pdf,pathPng_Pdf):
    page = page - 1
    base64_string_pdf = base64_string_pdf
    pathPng_Pdf  = pathPng_Pdf
    path = './temp/pdf/'
    namefile = uuid.uuid4().hex
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        with open(os.path.join(path + namefile + '.pdf'), 'wb') as filepdf:
            filepdf.write(base64.decodestring(str(base64_string_pdf).encode('utf8')))
        path_Pdf = path + namefile + '.pdf'
    except Exception as ex:
        return {'result':'ER','messageText':None}
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
    path_nameFile = './temp/pdf_qr/'
    if not os.path.exists(path_nameFile):
        os.makedirs(path_nameFile)
    try:
        with open(path_nameFile + namefile +".pdf", 'wb') as fh:
            pdf_writer.write(fh)
        with open(path_nameFile + namefile +".pdf", "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        string_Pdf = (encoded_string).decode('utf8')
        string_hashPdf = hashlib.sha512(encoded_string).hexdigest()
        return {'result':'OK','messageText':{'responseCode':200,'responseHash':string_hashPdf,'responseMessage':'PDF upload complete.','responsePdf':(encoded_string).decode('utf8')}}
    except Exception as ex:
        return {'result':'ER','messageText': 'err message ' +  str(ex)}