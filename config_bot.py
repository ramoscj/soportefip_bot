import os
import platform

DEBUG = False

if DEBUG:
    if os.environ.get('SERVIDOR_DB') is None:
        ACCESO_DB = {
            'SERVIDOR': 'localhost',
            'NOMBRE_DB': 'botfip',
            'USUARIO': 'postgres',
            'CLAVE': '5325106',
            'PUERTO': '5432',
        }
    else:
        ACCESO_DB = {
            'SERVIDOR': os.environ['SERVIDOR_DB'],
            'NOMBRE_DB': os.environ['NOMBRE_DB'],
            'USUARIO': os.environ['USUARIO_DB'],
            'CLAVE': os.environ['CLAVE_DB'],
            'PUERTO': os.environ['PUERTO_DB'],
        }
    CORREOS = {
        'FROM': 'sop01@imagicair.cl',
        'PASSWD': os.environ['CORREO_PASSWORD'],
        'TO': 'sop01@imagicair.cl',
        'CC': ['carlos.ramos@imagicair.cl']
    }
else:
    ACCESO_DB = {
        'SERVIDOR': os.environ['SERVIDOR_DB'],
        'NOMBRE_DB': os.environ['NOMBRE_DB'],
        'USUARIO': os.environ['USUARIO_DB'],
        'CLAVE': os.environ['CLAVE_DB'],
        'PUERTO': os.environ['PUERTO_DB'],
    }
    CORREOS = {
        'FROM': 'sop01@imagicair.cl',
        'PASSWD': os.environ['CORREO_PASSWORD'],
        'TO': 'richard.ruiz@adretail.cl',
        'CC': ['richie172118@gmail.com', 'operaciones@abcdin.cl', 'sop01@imagicair.cl']
    }

# Token BOT discord
TOKEN_BOT = os.environ['TOKEN_BOT']

# Directorio para manejar archivos de la aplicacion
PAT_BOT = {'PATH': str(os.getcwd())}

PATRIMONIOS_TC = {4: 2, 6: 5, 8: 7, 10: 0}

ENTORNO_FIP = {'DB': 'FIP', 'DBLINK': ''}
ENTORNO_REPORTS = {'DB': 'REPORTS', 'DBLINK': '@kamet.din.cl'}