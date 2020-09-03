import os
import platform

PATRIMONIOS_TC = {4: 2, 6: 5, 8: 7, 10: 0}

ENTORNO_FIP = {'DB': 'FIP', 'DBLINK': ''}
ENTORNO_REPORTS = {'DB': 'REPORTS', 'DBLINK': '@kamet.din.cl'}
CORREOS = {'TO': 'richard.ruiz@adretail.cl',
        'TO2': 'sop01@imagicair.cl',
        'CC': ['richie172118@gmail.com', 'operaciones@abcdin.cl', 'axel.riobo@imagicair.cl', 'eduardo@imagicair.cl', 'sop01@imagicair.cl'],
        'CC2': ['carlos.ramos@imagicair.cl', 'ramoscj.trading@gmail.com']
    }

sistema = platform.platform()
if sistema.startswith('Windows-10'):
    SO = str(os.getcwd())
else:
    SO = '/home/ubuntu/bot/soportefip_bot'
PAT_BOT = {'PATH': SO}
# print(PAT_BOT['PATH'])