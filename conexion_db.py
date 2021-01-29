import psycopg2
from config_bot import ACCESO_DB
import datetime, time
from validar_input import validarFechaCorte

def conectorDb():
    try:
        cnx = psycopg2.connect(
            database=ACCESO_DB['NOMBRE_DB'],
            user=ACCESO_DB['USUARIO'],
            password=ACCESO_DB['CLAVE'],
            host=ACCESO_DB['SERVIDOR'],
            port=ACCESO_DB['PUERTO']
        )
        return cnx
    except Exception as e:
        raise Exception('Error al conectar DB - %s' % e)

def insertarConsulta(consulta: dict):
    sql = """INSERT INTO fip_consultabot_bitacora (fecha_consulta, patrimonio, fecha_corte, hora_inicio, hora_fin, error, envio_script)
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cnx = None
    fechaConsulta = consulta['FECHA_CONSULTA']
    patrimonio = consulta['PATRIMONIO']
    fechaCorte = validarFechaCorte(consulta['FECHA_CORTE'])
    horaInicio = consulta['HORA_INICIO']
    horaFin = consulta['HORA_FIN']
    error = consulta['ERROR']
    envioScript = consulta['ENVIO_SCRIPT']
    try:
        cnx = conectorDb()
        cursor = cnx.cursor()
        cursor.execute(sql, (fechaConsulta, patrimonio, fechaCorte, horaInicio, horaFin, error, envioScript))
        cnx.commit()
        cursor.close()
        return True
    except Exception as e:
        raise Exception('Error InsertDB: %s - %s' % (e ,e))
    finally:
        if cnx is not None:
            cursor.close()
            cnx.close()

# x = datetime.datetime.now()
# data = {'FECHA_CONSULTA': x.strftime("%d/%m/%Y"), 'PATRIMONIO': 4, 'FECHA_CORTE': '01052020', 'HORA_INICIO': x.strftime("%X"), 'HORA_FIN': x.strftime("%X"), 'ERROR': 0, 'ENVIO_SCRIPT': 1}
# print(insertarConsulta(data))
