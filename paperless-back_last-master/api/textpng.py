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



def gentext_topng():
    import pytesseract       
  
    # adds image processing capabilities 
    from PIL import Image     
    
    # converts the text to speech   
    import pyttsx3            
    
    #translates into the mentioned language 
    from googletrans import Translator       
    
    # opening an image from the source path 
    img = Image.open('text1.png')      
    
    # describes image format in the output 
    print(img)                           
    # path where the tesseract module is installed 
    pytesseract.pytesseract.tesseract_cmd ='C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'   
    # converts the image to result and saves it into result variable 
    result = pytesseract.image_to_string(img)    
    # write text in a text file and save it to source path    
    with open('abc.txt',mode ='w') as file:   
        
        file.write(result) 
        print(result) 
                    
    p = Translator()                       
    # translates the text into german language 
    k = p.translate(result,dest='german')       
    print(k) 
    engine = pyttsx3.init() 
    
    # an audio will be played which speaks the test if pyttsx3 recognizes it 
    engine.say(k)                              
    engine.runAndWait() 