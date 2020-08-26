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
 
class Correo(object):

	def enviar(lista_archivos:[], patrimonio, fecha_corte):
		msg = MIMEMultipart()
		lista_mensajes = [
			(
				'<strong>Negocios con tipo de documento NULL</strong>',
				'<strong>Negocios Duplicados</strong>',
				'<strong>Cuotas Duplicadas</strong>',
				'<strong>Cuotas sin Negocio</strong>',
				'<strong>Numero de Negocio en NULL</strong>',
				'<strong>Movimientos ExtraFin sin Cuotas</strong>',
				'<strong>Movimientos sin Cuotas</strong>'
			),
			(
				'<strong>Remesas no estan generadas en la interfaz del Reports</strong>',
				'<strong>Remesas no estan generadas en la interfaz del Respaldo</strong>'
			)
		]
		# Parametros para enviar correo
		asunto = 'Revision de DATA para el proceso FIP_EJEC_DIARIO PATRIMONIO: %s FECHA DE CORTE: %s' % (patrimonio, fecha_corte)
		password = "satelite01"
		sistema = platform.platform()
		agregados = ', '.join(CORREOS['CC'])
		destinatario = CORREOS['TO']
		msg['To'] = destinatario
		msg['From'] = 'sop01@imagicair.cl'
		msg['Cc'] = agregados
		msg['Subject'] = asunto
		envio = datetime.datetime.now()
		mensaje = '<h2 style="color: #2b2301;">Instrucciones para realizar correcciones de inconsistencias encontradas:</h2>'
		mensaje += '<p>Para el patrimonio %s y fecha de corte %s se encontraron las siguientes inconsistencias:' % (patrimonio, fecha_corte)
		mensaje += '<ol style="line-height: 32px; list-style-type: square;">'
		for errores_encontrados in lista_archivos:
			mensaje += '<li style="clear: both;">%s</li>' % lista_mensajes[0][errores_encontrados]
		mensaje += '</ol></p>'
		mensaje += '<h3 style="color: #2b2301;">Para corregir las inconsistencia se recomienda:</h3>'
		mensaje += '<ol style="line-height: 32px;">'
		mensaje += '<li style="clear: both;">Ejecutar los scripts .SQL enviados en orden.</li>'
		mensaje += '<li style="clear: both;">Ralizar nuevamente la revisión para confirmar que no existan errores.</li>'
		mensaje += '<li style="clear: both;">Iniciar con el proceso diario.</li></ol>'
		mensaje += '<p><strong>&nbsp;</strong></p>'
		mensaje += '<p><strong>Nota: </strong>Si tiene alguna duda con las  indicaciones enviadas por favor enviar un correo electronico a la direccion: <strong>sop01@imagicair.cl</strong><br/></p>'
		mensaje += '<p><strong>Enviado: </strong> %s</p>' % (envio.strftime("%b %d %Y %H:%M"))
		body = MIMEText(str(mensaje), 'html')
		msg.attach(body)

		try:
			# Adjuntar CSV
			lista_nombres = (
				'negocios_documentoNULL_PAT-%s_FCORTE-%s' % (patrimonio, fecha_corte),
				'negocios_duplicados_PAT-%s_FCORTE-%s' % (patrimonio, fecha_corte),
				'cuotas_duplicadas_PAT-%s_FCORTE-%s' % (patrimonio, fecha_corte),
				'cuotas_sin_negocio_PAT-%s_FCORTE-%s' % (patrimonio, fecha_corte),
				'numero_negNULL_PAT-%s_FCORTE-%s' % (patrimonio, fecha_corte),
				'movExtrafin_scuota_PAT-%s_FCORTE-%s' % (patrimonio, fecha_corte),
				'movimiento_scuota_PAT-%s_FCORTE-%s' % (patrimonio, fecha_corte)
				)
			nombre_archivo = 'INCONSISTENCIAS_PAT-%s_FCORT-%s' % (patrimonio, fecha_corte)
			archivo_path = '%s/csv_data/%s.xlsx' % (PAT_BOT['PATH'], nombre_archivo)
			if (os.path.isfile(archivo_path)):
				fp = open(archivo_path,'rb')
				att = MIMEApplication(fp.read(),_subtype="xlsx")
				fp.close()
				nombre_archivo = '%s.xlsx' % nombre_archivo
				att.add_header('Content-Disposition','attachment',filename=nombre_archivo)
				msg.attach(att)
			i = 1
			for nombre_archivo in lista_archivos:
				archivo_path = '%s/scripts/%s.sql' % (PAT_BOT['PATH'], nombre_archivo)
				part = MIMEBase('application', "octet-stream")
				part.set_payload(open(archivo_path, "rb").read())
				nombre_archivo = '%s_DELETE_%s.sql' % (str(i),lista_nombres[nombre_archivo])
				part.add_header('Content-Disposition', 'attachment' ,filename=nombre_archivo)
				msg.attach(part)
				i += 1

			# Se envia el correo
			correos = agregados.split(',') + [destinatario]
			server = smtplib.SMTP('mail.imagicair.cl:587')
			server.starttls()
			server.login(msg['From'], password)
			server.sendmail(msg['From'], correos, msg.as_string())
			server.quit()
			return ("%s" % (msg['To']))
		except Exception as e:
			raise Exception("El correo no pudo enviarse, error: %s" % (e))