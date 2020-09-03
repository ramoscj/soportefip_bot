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

def CuadraturasRemesas(patrimonio, fechaCorteInicio, fechaCorteFin):
    try:
        diferenciasMontos = DiferenciasRemesas(patrimonio, fechaCorteInicio, fechaCorteFin)
        asientosDuplicados = AsientosContablesDuplicados(patrimonio, fechaCorteInicio, fechaCorteFin)
        return diferenciasMontos, asientosDuplicados
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
                    fechaCorte = data[diferencias]['MOVIMIENTO_FECHA_MOVIMIENTO']
                    diferencia = data[diferencias]['DIFERENCIA']
                    if type(fechaCorte) is datetime.datetime:
                        fechaCorte = fechaCorte.strftime("%d-%m-%Y")
                    if not diferenciasMontos.get(fechaCorte):
                        diferenciasMontos[fechaCorte] =  {'TOTAL_DIFERENCIA': diferencia}
                    else:
                        diferenciasMontos[fechaCorte]['TOTAL_DIFERENCIA'] += diferencia
        return diferenciasMontos
    except Exception as e:
        print(e)

def AsientosContablesDuplicados(patrimonio, fechaCorteInicio, fechaCorteFin):
    try:
        consultaAsientosContDuplicados, mensaje = RespaldoRev.cuadratura_remesas()
        conexionDB = conexion()
        asientosDuplicados = dict()
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
                    asientosDuplicados = {fechaCorte: {'CANTIDAD': data[duplicados]['CANTIDAD']}}

        return asientosDuplicados
    except Exception as e:
        print(e)

print(CuadraturasRemesas(6, '01082020', '25082020'))