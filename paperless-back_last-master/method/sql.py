# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *

def connect_sql(sql,parameter,type_sql,db,type_db):
    try:
        if type_sql == 'master':            
            con = psycopg2.connect(database="paper_less_uat", user="jirayu", password="paperless@n12345678", host="10.0.0.50", port="5432")
            print("Database opened successfully")
            # connection.close()
            return con
        elif type_sql == 'slave':
            with slave.connect() as connection:
                print(connection)
            connection.close()
    except Exception as e:
        print(str(e))
    finally:
        con.close()
