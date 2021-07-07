#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import db_config
from config.lib import *
from config.value import *
from method.convert import *
from method.access import *
from method.publicqrcode import *
from method.document import *
from controller.mail_string import *
from controller.validate import *
from db.db_method import *
from api.chat import *
from api.mail import *
from api.auth import *
from api.onechain import *
from api.pdf import *
from api.textpng import *
from api.file import *



if type_product =='uat':
    status_methods = paper_less_uat
elif type_product =='prod':
    status_methods = paper_less
elif type_product == 'dev':
    status_methods = paper_lessdev
elif type_product =='poc':
    status_methods = paper_less


@status_methods.route('/api/v1/testMailATT', methods=['POST'])
def testMailATT():
    # fill in the variables
    smtp_server = "mailtx.inet.co.th"                          # for smtp.gmail.com
    from_address = "jirayu.ko@mandala.co.th"
    to_address = "jirayu.ko@mandala.co.th"                  # e.g. username2@gmail.com
    subject = "Subject_here"
    mail_body = "Body content here"
    attachment_1 = r"gre_research_validity_data.pdf"       # e.g. file = r"C:\Folder1\text1.txt" # if you attach more than two files here, be sure to append them to the files dictionary below, as done for attachemnt_1 and attachment_2.
    attachment_2 = r"requirement.txt"
    sid_ = ''
    folder_name = '6f0233f6-6036-484d-81df-6a308b32a068'
    path_file = os.getcwd() + '/storage/6f0233f6-6036-484d-81df-6a308b32a068/'
    msg = MIMEMultipart()
    msg['Subject'] =  subject
    msg['To'] = to_address
    msg.attach(MIMEText(mail_body))
    files = []
    for r, d, f in os.walk(path_file):
        for file in f:
            files.append(os.path.join(r, file))

    print(files)
    # files = []
    # files.append(attachment_1)
    # files.append(attachment_2)
    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(file, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(file)))
        msg.attach(part)

    server = smtplib.SMTP(smtp_server)
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()

    # Host = "mailtx.inet.co.th"
    # mail_content = '''Hello,
    # This is a test mail.
    # In this mail we are sending some attachments.
    # The mail is sent using Python SMTP library.
    # Thank You
    # '''
    # From = 'jirayu.ko@mandala.co.th'
    # To = 'sarawut.si@inet.co.th'
    # #Setup the MIME
    # message = MIMEMultipart()
    # message['From'] = From
    # message['To'] = To
    # message['Subject'] = 'A test mail sent by Python. It has an attachment.'
    # #The subject line
    # #The body and the attachments for the mail
    # message.attach(MIMEText(mail_content, 'plain'))
    # attach_file_name = 'gre_research_validity_data.pdf'
    # attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
    # payload = MIMEBase('application', 'pdf')
    # payload.set_payload((attach_file).read())
    # encoders.encode_base64(payload) #encode the attachment
    # #add payload header with filename
    # payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    # message.attach(payload)
    # #Create SMTP session for sending the mail
    # s = smtplib.SMTP(Host)
    # s.sendmail(From, To, message.as_string())
    # s.quit()
    # print('Mail Sent')
    return ''
