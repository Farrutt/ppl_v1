#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import uvicorn
# from fastapi import FastAPI
# from fastapi.middleware.wsgi import WSGIMiddleware
from flask import *
from flask_cors import CORS, cross_origin
import waitress
from waitress import serve
import werkzeug.serving
import requests
import json
import datetime
import time
import random
import string
import numpy as np
from io import StringIO
import io
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import re
import sys
import glob
import base64
import hashlib
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from pdf2image import *
import pathlib
import shutil
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import re
import qrcode
import jwt
# from jwcrypto import jwt, jwk
from functools import wraps
import logging
import logging.config
from sqlalchemy import exc,func,desc,asc,or_,and_,create_engine,not_,text,event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import load_only,scoped_session, sessionmaker
from pathlib import Path
from config.value import *
from PyPDF2 import PdfFileWriter, PdfFileReader
from fpdf import FPDF
import png,pyqrcode
import tempfile
from PIL import Image
from resizeimage import resizeimage
import concurrent.futures
# from paramiko import Transport, SFTPClient

import pysftp
import unicodedata
import threading
import xlsxwriter
import pandas as pd
from datetime import timedelta
import socketio
from gevent import pywsgi,monkey
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication
from sqlalchemy.inspection import inspect
from apscheduler.schedulers.background import BackgroundScheduler
# from flask_restplus import *
import calendar
from dateutil.relativedelta import relativedelta, MO
from dateutil.parser import parse
from collections_extended import *
from collections import *
import collections
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask_executor import Executor
import urllib3
# from flask_profiler import Profiler
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
# import uvicorn
from flask_compress import Compress
import urllib.parse as urlparse
from urllib.parse import parse_qs
from flask_request_id import RequestID
from croniter import croniter
# import psycopg2

# import redis

# from flask_debugtoolbar import DebugToolbarExtension
# import flask_monitoringdashboard as dashboard
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
# from werkzeug.middleware.proxy_fix import ProxyFix
# monkey.patch_all()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig()
logger = logging.getLogger('waitress')
logger = logging.getLogger(__name__)
f_handler = logging.FileHandler('logging.log')
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

# logging.basicConfig(
#     level=logging.INFO,
#     format='[%(asctime)s] [%(process)d] [%(levelname)s] [%(funcName)s @ %(lineno)s]: \
#     %(message)s', datefmt='%Y-%m-%d %H:%M:%S %z'
# )

if type_product =='uat':    
    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications 
    paper_less_uat = Flask(__name__)
    # api = Api(paper_less,doc='/swagger/',version='1.0', title='Paperless API',
    # description='A simple Paperless API')
    # paper_less.wsgi_app = ProxyFix(paper_less.wsgi_app)
    sio = socketio.Server(logger=True, async_mode='gevent')
    paper_less_uat.secret_key = '068b0b5c-1180-48ca-8447-c61290f95c8d'
    paper_less_uat.wsgi_app = socketio.Middleware(sio, paper_less_uat.wsgi_app)
    CORS(paper_less_uat)
    paper_less_uat.config['EXECUTOR_TYPE'] = 'thread'
    paper_less_uat.config['EXECUTOR_MAX_WORKERS'] = 20
    Compress(paper_less_uat)
    executor = Executor(paper_less_uat)
    RequestID(paper_less_uat)
    # paper_less_uat.debug = True
    # paper_less_uat.config['SECRET_KEY'] = '068b0b5c-1180-48ca-8447-c61290f95c8d'
    # paper_less_uat.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # toolbar = DebugToolbarExtension(paper_less_uat)
elif type_product == 'prod':  
    # profiler = Profiler()
    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications 
    paper_less = Flask(__name__)
    paper_less.config["DEBUG"] = True
    # api = Api(paper_less,doc='/swagger/',version='1.0', title='Paperless API',
    # description='A simple Paperless API',behind_proxy=True)
    # paper_less.wsgi_app = ProxyFix(paper_less.wsgi_app)
    # api.as_postman(urlvars=urlvars, swagger=swagger)
    sio = socketio.Server(logger=True, async_mode='gevent')
    paper_less.secret_key = '068b0b5c-1180-48ca-8447-c61290f95c8d'
    paper_less.wsgi_app = socketio.Middleware(sio, paper_less.wsgi_app)
    CORS(paper_less)
    paper_less.config['EXECUTOR_TYPE'] = 'thread'
    paper_less.config['EXECUTOR_MAX_WORKERS'] = 20
    executor = Executor(paper_less)
    RequestID(paper_less)
    # paper_less.config["flask_profiler"] = {
    #     "enabled": paper_less.config["DEBUG"],
    #     "storage": {
    #         "engine": "sqlite"
    #     },
    #     "basicAuth":{
    #         "enabled": True,
    #         "username": "pplprod",
    #         "password": ")dY;#rmM$apz&L9I,wD;*aKwqv:6bl"
    #     },
    #     "ignore": [
    #         "^/static/.*"
    #     ]
    # }
    # profiler = Profiler()
    # profiler.init_app(paper_less)
elif type_product == 'dev':
    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications 
    paper_lessdev = Flask(__name__)
    paper_lessdev.config["DEBUG"] = True
    # api = Api(paper_less,doc='/swagger/',version='1.0', title='Paperless API',
    # description='A simple Paperless API')
    # paper_less.wsgi_app = ProxyFix(paper_less.wsgi_app)
    sio = socketio.Server(logger=True, async_mode='gevent')
    paper_lessdev.secret_key = '068b0b5c-1180-48ca-8447-c61290f95c8d'
    paper_lessdev.wsgi_app = socketio.Middleware(sio, paper_lessdev.wsgi_app)
    CORS(paper_lessdev)
    paper_lessdev.config['EXECUTOR_TYPE'] = 'thread'
    paper_lessdev.config['EXECUTOR_MAX_WORKERS'] = 5
    executor = Executor(paper_lessdev)
elif type_product == 'poc':
    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications 
    paper_less = Flask(__name__)
    paper_less.config["DEBUG"] = True
    sio = socketio.Server(logger=True, async_mode='gevent')
    paper_less.secret_key = '068b0b5c-1180-48ca-8447-c61290f95c8d'
    paper_less.wsgi_app = socketio.Middleware(sio, paper_less.wsgi_app)
    CORS(paper_less)
    paper_less.config['EXECUTOR_TYPE'] = 'thread'
    paper_less.config['EXECUTOR_MAX_WORKERS'] = 20
    executor = Executor(paper_less)
    RequestID(paper_less)


def print_log(data):
    print(data)