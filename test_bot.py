from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
#from email import Encoders
import mimetypes
import platform

import smtplib, os
import datetime

from config_bot import PAT_BOT, CORREOS, PATRIMONIOS_TC
from acceso_db import conexion
from respaldo_revisiones import RespaldoRev
from csv_file import crear_xls

def testCorreo():
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


def testClienteDuplicado():
	patrimonio = 4
	fecha_corte = '18012019'
	revisiones = 7
	consultas, mensaje = RespaldoRev.detalle_valdiario('FIP', '')
	registrosXlsx = []
	encabezadoDbXlsx = []
	conexion_db = conexion()
	titulos = (
	'NEGOCIOS CON TIPO DE DOCUMENTO NULL',
	'NEGOCIOS DUPLICADOS',
	'CUOTAS DUPLICADAS',
	'CUOTAS SIN NEGOCIO',
	'NUMERO DE NEGOCIO NULL',
	'MOVIMIENTOS INTERES EXTRAFIN SIN CUOTAS (006)',
	'MOVIMIENTOS SIN CUOTAS (004, 007, 008, 009, 010, 011, 014, 016)',
	'CLIENTES DUPLICADOS PATRIMONIOS TC'
	)
	with conexion_db.cursor() as cursor:
		if revisiones == 7:
			for k in range(0,len(consultas[revisiones])):
				patTC = PATRIMONIOS_TC.get(patrimonio)
				cursor.execute(consultas[revisiones][k], pat_consulta=patrimonio, fecha_consulta=fecha_corte, pat_consultatc=patTC)
				columns = [col[0] for col in cursor.description]
				cursor.rowfactory = lambda *args: dict(zip(columns, args))
				data = cursor.fetchall()
				encabezadoDbXlsx.append(columns)
				if len(data) > 0:
					registrosXlsx.append(data)
				else:
					registrosXlsx.append('')
				print(k)
	return registrosXlsx


patrimonio = 4
fecha_corte = '18012019'
revisiones = [7]
consultas, mensaje = RespaldoRev.detalle_valdiario('FIP', '')
print(crear_xls(patrimonio, fecha_corte, revisiones, consultas, mensaje))