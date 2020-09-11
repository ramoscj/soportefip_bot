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


from acceso_db import conexion
from respaldo_revisiones import RespaldoRev
from validar_input import validarFechaCorte, fechaDiaSiguiente

from alive_progress import alive_bar

from csv_file import crearXlsDescuadraturas

def CuadraturasRemesas(patrimonio, fechaCorteInicio, fechaCorteFin):
	try:
		fechaInicio = validarFechaCorte(fechaCorteInicio)
		fechaFinal = validarFechaCorte(fechaCorteFin)
		diferenciasTRX = dict()
		restaTrxRemesas = dict()

		with alive_bar(4) as bar:
			diferenciasMontos, cuentasConDiferencias = DiferenciasRemesas(patrimonio, fechaCorteInicio, fechaCorteFin)
			bar()
			print('Diferencias por Remesas Ok')
			asientosDuplicados = AsientosContablesDuplicados(patrimonio, fechaCorteInicio, fechaCorteFin)
			bar()
			print('Asientos duplicados Ok')

			while fechaInicio <= fechaFinal:
				diferenciasTRX[fechaInicio.strftime("%d-%m-%Y")] = DiferenciasAsientosContables(patrimonio, fechaInicio.strftime("%d%m%Y"))

				if diferenciasTRX[fechaInicio.strftime("%d-%m-%Y")].get('DIFERENCIA_TRX') and diferenciasMontos[fechaInicio.strftime("%d-%m-%Y")].get('DIFERENCIA_POR_CUENTAS'):
					montoTRX = diferenciasTRX[fechaInicio.strftime("%d-%m-%Y")]['DIFERENCIA_TRX']
					montoRemesas = diferenciasMontos[fechaInicio.strftime("%d-%m-%Y")]['DIFERENCIA_POR_CUENTAS']
					restaTrxRemesas[fechaInicio.strftime("%d-%m-%Y")] = montoTRX + montoRemesas
				fechaInicio = fechaDiaSiguiente(fechaInicio)
			bar()
			print('Diferencias por TRX Ok')
			crearXlsDescuadraturas(patrimonio, fechaCorteInicio, fechaCorteFin, cuentasConDiferencias)
			bar()
			print('XLSX Creado!')
		return True
	except Exception as e:
		print(e)

def DiferenciasRemesas(patrimonio, fechaCorteInicio, fechaCorteFin):
	try:
		consultaDiferenciaRemesas, mensaje = RespaldoRev.cuadratura_remesas()
		conexionDB = conexion()
		diferenciasMontos = dict()
		with conexionDB.cursor() as consulta_db:
			for i in range(0, 1):
				consulta_db.execute(consultaDiferenciaRemesas[i], pat_consulta= patrimonio, fecha_inicio= fechaCorteInicio, fecha_fin= fechaCorteFin)
				columns = [col[0] for col in consulta_db.description]
				consulta_db.rowfactory = lambda *args: dict(zip(columns, args))
				data = consulta_db.fetchall()

				for diferencias in range(0, len(data)):
					fechaCorte = data[diferencias]['MOV_FECHA_MOVIMIENTO']
					diferencia = data[diferencias]['DIFERENCIA']
					if type(fechaCorte) is datetime.datetime:
						fechaCorte = fechaCorte.strftime("%d-%m-%Y")
					if not diferenciasMontos.get(fechaCorte):
						diferenciasMontos[fechaCorte] =  {'DIFERENCIA_POR_CUENTAS': diferencia}
					else:
						diferenciasMontos[fechaCorte]['DIFERENCIA_POR_CUENTAS'] += diferencia
		diferenciaPorCuentas = [data, columns]
		return diferenciasMontos, diferenciaPorCuentas
	except Exception as e:
		print(e)

def AsientosContablesDuplicados(patrimonio, fechaCorteInicio, fechaCorteFin):
	try:
		consultaAsientosContDuplicados, mensaje = RespaldoRev.cuadratura_remesas()
		conexionDB = conexion()
		movimientosDuplicados = dict()
		with conexionDB.cursor() as consulta_db:
			for i in range(1, 2):
				consulta_db.execute(consultaAsientosContDuplicados[i], pat_consulta= patrimonio, fecha_inicio= fechaCorteInicio, fecha_fin= fechaCorteFin)
				columns = [col[0] for col in consulta_db.description]
				consulta_db.rowfactory = lambda *args: dict(zip(columns, args))
				data = consulta_db.fetchall()

				for duplicados in range(0, len(data)):
					fechaCorte = data[duplicados]['FECHA_MOVIMIENTO']
					if type(fechaCorte) is datetime.datetime:
						fechaCorte = fechaCorte.strftime("%d-%m-%Y")
					movimientosDuplicados = {fechaCorte: {'MOV_DUPLICADOS': data[duplicados]['CANTIDAD']}}

		return movimientosDuplicados
	except Exception as e:
		print(e)

def DiferenciasAsientosContables(patrimonio, fechaCorte):
	try:
		consultaAsientosContDuplicados, mensaje = RespaldoRev.cuadratura_remesas()
		conexionDB = conexion()
		diferenciasTRX = {'DIFERENCIA_TRX': 0}
		data = []
		with conexionDB.cursor() as consulta_db:
			for i in range(2, 4):
				consulta_db.execute(consultaAsientosContDuplicados[i], pat_consulta= patrimonio, fecha_inicio= fechaCorte)
				columns = [col[0] for col in consulta_db.description]
				consulta_db.rowfactory = lambda *args: dict(zip(columns, args))
				data.append(consulta_db.fetchone())

		for valor in range(0, len(data)):
			if data[valor] is not None:
				diferenciasTRX['DIFERENCIA_TRX'] += int(data[valor]['DIFERENCIA'])
		return diferenciasTRX
	except Exception as e:
		print(e)

print(CuadraturasRemesas(6, '01092020', '05092020'))
# print(crearXlsDescuadraturas(6, '01092020', '05092020', z[0], z[1]))
# DiferenciasRemesas(6, '01092020', '01092020')
# print(y)

