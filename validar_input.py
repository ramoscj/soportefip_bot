import datetime

def validarPatrimonioFecha(patrimonio, fecha_corte):
    try:
        fechaAnho = str(fecha)[0:4]
        fechaMes = str(fecha)[4:6]
        fechaDia = str(fecha)[6:8]
        fechaSalida = datetime.date(int(fechaAnho), int(fechaMes), int(fechaDia))
        return fechaSalida
    except Exception as e:
        errorMsg = "Error %s, formato correcto YYYYMMDD | %s" % (fecha, e)
        # return errorMsg
        raise Exception(errorMsg)

# print(validarPatrimonioFecha(4,'1'))