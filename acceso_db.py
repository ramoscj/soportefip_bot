import cx_Oracle

def conexion():
    try:
        cnx = cx_Oracle.connect("tcexplorer", "anita", "NOVA.DIN.CL")
        # cnx = cx_Oracle.connect("fip", "fip", "NOVADESA.WORLD")
        return cnx
    except Exception as e:
        raise Exception("Problemas en la conexion DB. Error: - %s" % (e))