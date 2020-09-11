import datetime
from dateutil.relativedelta import relativedelta

def validarPatrimonioFecha(patrimonio, fecha_corte):
    try:
        fechaAnho = str(fecha_corte)[0:4]
        fechaMes = str(fecha_corte)[4:6]
        fechaDia = str(fecha_corte)[6:8]
        fechaSalida = datetime.date(int(fechaAnho), int(fechaMes), int(fechaDia))
        return fechaSalida
    except Exception as e:
        errorMsg = "Error validarPatrimonioFecha %s, formato correcto YYYYMMDD | %s" % (fecha_corte, e)
        raise Exception(errorMsg)

def validarFechaCorte(fecha_corte):
    try:
        fechaDia = str(fecha_corte)[0:2]
        fechaMes = str(fecha_corte)[2:4]
        fechaAnho = str(fecha_corte)[4:8]
        fechaSalida = datetime.date(int(fechaAnho), int(fechaMes), int(fechaDia))
        return fechaSalida
    except Exception as e:
        errorMsg = "Error validarFechaCorte %s, formato correcto YYYYMMDD | %s" % (fecha_corte, e)
        raise Exception(errorMsg)

def fechaDiaSiguiente(fecha):
    try:
        fechaSalida = fecha + relativedelta(days=1)
        return fechaSalida
    except Exception as e:
        errorMsg = "Error fechaDiaSiguiente %s, formato correcto YYYYMMDD | %s" % (fecha, e)
        raise Exception(errorMsg)

# print(fechaDiaSiguiente(datetime.date(2020, 1, 13)))
# print(validarFechaCorte('01052020'))