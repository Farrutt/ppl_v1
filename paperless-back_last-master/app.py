# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from config.lib import *
from api.api import *
from api.api2 import *
from api.api3 import *
from api.login import *
from api.apiBiz import *
from api.file import *
from api.dashboard import *
from api.template_api import *
from api.sendmail_api import *
from api.document_api import *
from api.chat_api import *
from api.image_api import *
from api.department_api import *
from api.mail_api import *
from api.auth_api import *
from api.dashboard_admin import *
from api.other_api import *
from api.sio import *
from api.register import *
from api.excel_report import *
from api.profile import *
from api.step_api import *
from api.wbhook import *
# from api.onebox_api import *
from api.schedule_log import *
from api.schedule_chat import *
from api.group_api import *
from api.approve_api import *
from api.draft_document import *
from api.qrcode import *
from api.permission_api import *
from api.access_api import *
from api.contact_us import *
from api.group_v2 import *
from api.package_api import *
from api.tracking_api import *
# from swagger.api import *
# def run_server():
#     if paper_less.debug:
#         application = DebuggedApplication(app)
#     else:
#         application = app

#     if type_product == 'uat':
#         paper_less_uat.run(debug = True, port = 8310, host = '0.0.0.0', threaded = True)
#     elif type_product == 'prod':
#         # from gevent import pywsgi
#         # try:
#         #     from geventwebsocket.handler import WebSocketHandler
#         #     websocket = True
#         # except ImportError:
#         #     websocket = False

#         # if websocket:
#         #     paper_less.debug = True
#         #     server = pywsgi.WSGIServer(('0.0.0.0', 8300), paper_less, handler_class=WebSocketHandler)
#         #     server.serve_forever()
#         #     # serve_forever()
#         # else:
#         #     paper_less.debug = True
#         #     server = pywsgi.WSGIServer(('0.0.0.0', 8300), paper_less)
#         #     server.serve_forever()
#         paper_less.run(debug = True, port = 8300, host = '0.0.0.0', threaded = True)
#         # serve(paper_less, host = '0.0.0.0', port = 8300, threads = True)
#     elif type_product == 'dev':
#         paper_lessdev.run(debug = True, port = 8310, host = '0.0.0.0', threaded = True)
#         # serve(paper_less, host = '0.0.0.0', port = 8300, threads = True)
# @werkzeug.serving.run_with_reloader
# def run_server():
#     if type_product == 'uat':
#         paper_less_uat.debug = True
#         waitress.serve(paper_less_uat, listen='0.0.0.0:8310')
#     elif type_product == 'prod':
#         paper_less.debug = True
#         waitress.serve(paper_less, listen='0.0.0.0:8300')
#     elif type_product == 'dev':
#         paper_lessdev.debug = True
#         waitress.serve(paper_lessdev, listen='0.0.0.0:8320')
    
if __name__ == "__main__":
    if type_product == 'uat':
        # run_server()
        # start_check_approve_v1()
        paper_less_uat.run(debug = True, port = 8310, host = '0.0.0.0', threaded = True)
        # uvicorn.run("app:app", host="0.0.0.0", port=8310, log_level="info",reload=True,workers=4)
        # serve(paper_less_uat, port = 8310, host = '0.0.0.0')
    elif type_product == 'prod':
        # from werkzeug.serving import run_simple
        # paper_less.debug = True
        # run_simple('0.0.0.0', 8300, paper_less)
        paper_less.run(debug=True, port = 8300, host = '0.0.0.0', threaded = True)
        # run_server()
        # serve(paper_less, port = 8300, host = '0.0.0.0')
    elif type_product == 'dev':
        pass
        # uvicorn.run("app:app", host="0.0.0.0", port=8320, log_level="info",reload=True,workers=4)
        # uvicorn.run(paper_lessdev, host="0.0.0.0", port=8320, log_level="info",reload=True,workers=4)
        # app.mount("/service", WSGIMiddleware(paper_lessdev))
        paper_lessdev.run(debug = True, port = 8320, host = '0.0.0.0', threaded = True)
        # run_server()
        # serve(paper_lessdev, port = 8320, host = '0.0.0.0')
    elif type_product == 'poc':
        paper_less.run(debug=True, port = 8300, host = '0.0.0.0', threaded = True)
        
