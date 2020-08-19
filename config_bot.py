import os

PATRIMONIOS_TC = {4: 2, 6: 5, 8: 7, 10: 0}

ENTORNO_FIP = {'DB': 'FIP', 'DBLINK': ''}
ENTORNO_REPORTS = {'DB': 'REPORTS', 'DBLINK': '@kamet.din.cl'}

PAT_BOT = {'PATH': str(os.getcwd())}

CORREOS = {'TO': 'richard.ruiz@adretail.cl', 
        'TO2': 'sop01@imagicair.cl', 
        'CC': ['operaciones@abcdin.cl', 'axel.riobo@imagicair.cl', 'eduardo@imagicair.cl'], 
        'CC2': ['carlos.ramos@imagicair.cl',]
    }