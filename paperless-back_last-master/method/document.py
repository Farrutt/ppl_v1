# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from db.db_method import *
from config.lib import *
from method.hashpy import *
from db.db_Class import *
from config.value import *
from method.access import *
from method.other import *

class document_:
    def genarate_document_ID(self,document_type):
        self.document_type = document_type
        if self.document_type != None:
            if len(str(self.document_type).replace(' ','')) != 0:
                self.document_type = document_type
            else:
                self.document_type = 'OTHER'
        else:
            self.document_type = 'OTHER'
        print(self.document_type)
        ts = int(time.time())
        now1 = datetime.datetime.fromtimestamp(ts)
        thai_year = now1.year + 543
        datayear = str(thai_year)[2:]
        print(datayear)
        json_result = {}
        result_Select_numberDocument = paper_lessnumber_document.query.filter(paper_lessnumber_document.document_type==self.document_type).first()
        # result_Select = paper_lessdocument.query.filter(paper_lessdocument.documentType==self.document_type).order_by((paper_lessdocument.timest).desc()).first()
        if result_Select_numberDocument != None:
            json_result['document_current'] = result_Select_numberDocument.document_current
            json_result['document_lenght'] = result_Select_numberDocument.document_lenght
            doclength = json_result['document_lenght']
            if json_result['document_current'] < 10:
                docno = json_result['document_current'] + 1
                doclength = '00000000'
            elif json_result['document_current'] < 100:
                docno = json_result['document_current'] + 1
                doclength = '0000000'
            elif json_result['document_current'] < 1000:
                docno = json_result['document_current'] + 1
                doclength = '000000'
            elif json_result['document_current'] < 10000:
                docno = json_result['document_current'] + 1
                doclength = '00000'
            elif json_result['document_current'] < 100000:
                docno = json_result['document_current'] + 1
                doclength = '0000'
            elif json_result['document_current'] < 1000000:
                docno = json_result['document_current'] + 1
                doclength = '000'
            elif json_result['document_current'] < 10000000:
                docno = json_result['document_current'] + 1
                doclength = '00'
            elif json_result['document_current'] < 100000000:
                docno = json_result['document_current'] + 1
                doclength = '0'
            elif json_result['document_current'] < 1000000000:
                docno = json_result['document_current'] + 1
                doclength = ''
            else:
                docno = json_result['document_current'] + 1
                doclength = ''
            sum_documnet_ID = self.document_type + '-' + datayear + doclength + str(docno)
            try:
                selectResult = paper_lessnumber_document.query.filter(paper_lessnumber_document.document_type==self.document_type).first()
                if selectResult != None:
                    selectResult.document_current = docno
                    selectResult.document_lenght = doclength
                    db.session.commit()
                    print(sum_documnet_ID)
                    return {'result':'OK','messageText':{'documentID':sum_documnet_ID}}
                else:
                    return {'result':'ER','messageText':{'documentID':None},'messageER':'cant update'}
            except Exception as e:
                return {'result':'ER','messageText':{'documentID':None},'messageER':str(e)}
            
            
        else:
            document_lenght = '000000000'
            current_number = '1'
            try:
                insert_result = paper_lessnumber_document(document_current=int(current_number),document_lenght=document_lenght,document_type=self.document_type)
                db.session.add(insert_result)
                db.session.flush()
                db.session.commit()
                sum_documnet_ID = self.document_type + '-' + datayear + document_lenght + current_number
                print(sum_documnet_ID)
                return {'result':'OK','messageText':{'documentID':sum_documnet_ID}}
            except Exception as e:
                return {'result':'ER','messageText':{'documentID':None},'messageER':str(e)}
            

            


        
