import cx_Oracle

def conexion():
    try:
        cnx = cx_Oracle.connect("tcexplorer", "anita", "NOVA.DIN.CL")
        # cnx = cx_Oracle.connect("fip", "fip", "NOVADESA.WORLD")
        return cnx
    except:
        # return ("Error: conexion DB - %s" % (e))
        raise

import datetime, time
# then = datetime.datetime.now() + datetime.timedelta(seconds=100)
# while then > datetime.datetime.now():
#     print('sleeping')
#     time.sleep(10)

def Cronometro():
    suma=0
    valor = 15
    while (suma<=100):
        if valor == suma:
            print('segundos:%s' %suma)
            valor *= 2
        suma += 15
        time.sleep(15)
# Cronometro()
