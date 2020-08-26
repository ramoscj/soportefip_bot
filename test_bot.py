from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
#from email import Encoders
import mimetypes
import platform

import smtplib, os
import datetime

from config_bot import PAT_BOT, CORREOS

try:
    msg = MIMEMultipart()
    asunto = 'Revision de DATA para el proceso FIP_EJEC_DIARIO PATRIMONIO'
    password = "satelite01"
    agregados = ', '.join(CORREOS['CC'])
    print(agregados)
    destinatario = CORREOS['TO']
    msg['To'] = destinatario
    msg['From'] = 'sop01@imagicair.cl'
    msg['Cc'] = agregados

    correos = agregados.split(',') + [destinatario]
    server = smtplib.SMTP('mail.imagicair.cl:587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], correos, msg.as_string())
    server.quit()
except Exception as e:
    print(e)