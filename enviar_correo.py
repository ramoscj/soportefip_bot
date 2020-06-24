from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
#from email import Encoders
import mimetypes

import smtplib, os
import datetime
 
class Correo(object):

	def enviar(lista_archivos:[], patrimonio, fecha_corte, remesa_generada:bool):
		msg = MIMEMultipart()
		lista_mensajes = [
			(
				' <strong>Negocios con tipo de documento NULL</strong>',
				' <strong>Negocios Duplicados</strong>',
				' <strong>Cuotas Duplicadas</strong>',
				' <strong>Cuotas sin Negocio</strong>'
			),
			(
				' <strong>, Remesas no estan generadas</strong>'
			)
		]
		# Parametros para enviar correo
		asunto = 'Revision de DATA para el proceso FIP_EJEC_DIARIO PATRIMONIO: %s y FECHA DE CORTE: %s' % (patrimonio, fecha_corte)
		password = "satelite01"
		cc = ['axel.riobo@imagicair.cl']
		bcc = ['carlos.ramos@imagicair.cl']
		msg['From'] = 'sop01@imagicair.cl'
		msg['To'] = 'richard.ruiz@adretail.cl'
		msg['Cc'] = ', '.join(cc)
		msg['Bcc'] = ', '.join(bcc)
		msg['Subject'] = asunto
		envio = datetime.datetime.now()
		mensaje = '<h2 style="color: #2b2301;">Instrucciones para realizar correcciones de inconsistencias encontradas:</h2>'
		mensaje += '<p>Para el patrimonio %s y fecha de corte %s se encontraron las siguientes inconsistencias:' % (patrimonio, fecha_corte)
		for errores_encontrados in lista_archivos:
			mensaje += lista_mensajes[0][errores_encontrados]
		if remesa_generada == False:
			mensaje += lista_mensajes[1]
		mensaje += '.&nbsp;</p>'
		mensaje += '<h3 style="color: #2b2301;">Para corregir las inconsistencia se recomienda:</h3>'
		mensaje += '<ol style="line-height: 32px;">'
		# list-style: none;
		mensaje += '<li style="clear: both;">Ejecutar los scripts .SQL enviados en orden.</li>'
		if remesa_generada == False:
			mensaje += '<li style="clear: both;">Generar remesas con el FIP_WRAP opcion 3 (para el patrimonio y fecha de corte)</li>'
		mensaje += '<li style="clear: both;">Iniciar con el proceso diario</li></ol>'
		mensaje += '<p><strong>&nbsp;</strong></p>'
		mensaje += '<p><strong>Nota: </strong>esta es una nota adicional para tener en cuenta<br/></p>'
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
				)
			nombre_archivo = 'INCONSISTENCIAS_PAT-%s_FCORT-%s' % (patrimonio, fecha_corte)
			archivo_path = 'csv_data/%s.xlsx' % (nombre_archivo)
			if (os.path.isfile(archivo_path)):
				fp = open(archivo_path,'rb')
				att = MIMEApplication(fp.read(),_subtype="xlsx")
				fp.close()
				nombre_archivo = '%s.xlsx' % nombre_archivo
				att.add_header('Content-Disposition','attachment',filename=nombre_archivo)
				msg.attach(att)
			i = 1
			for nombre_archivo in lista_archivos:
				archivo_path = 'scripts/%s.sql' % (nombre_archivo)
				part = MIMEBase('application', "octet-stream")
				part.set_payload(open(archivo_path, "rb").read())
				nombre_archivo = '%s_DELETE_%s.sql' % (str(i),lista_nombres[nombre_archivo])
				part.add_header('Content-Disposition', 'attachment' ,filename=nombre_archivo)
				msg.attach(part)
				i += 1

			# Se envia el correo
			correos = [msg['To'], msg['Cc'], msg['Bcc']]
			server = smtplib.SMTP('mail.imagicair.cl: 587')
			server.starttls()
			server.login(msg['From'], password)
			server.sendmail(msg['From'], correos, msg.as_string())
			server.quit()
			return ("%s" % (msg['To']))
		except Exception as e:
			# return ("Error: el mensaje no pudo enviarse, error - %s" % (e))
			raise

#Correo.enviar('carlos.ramos@imagicair.cl', 'sop01@imagicair.cl', 'Asunto-Prueba', 'Este es el mensaje')