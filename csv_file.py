import csv
from io import BytesIO
import xlsxwriter

from respaldo_revisiones import ReportsRev, RespaldoRev
from consultas import Respaldo

from acceso_db import conexion

def crear_csv(nombre_archivo, registros:[]):
    archivo = 'csv_data/%s.csv' % (str(nombre_archivo))
    encabezado = [('NUM_CTA_CREDITO', 'COD_CLIENTE', 'COD_EXTRAFIN', 'FECHA_CORTE', 'TIPO_DOCUMENTO')]
    try:
        with open(archivo, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(encabezado)
            for x in registros:
                writer.writerows(x)
        return True
    except Exception as e:
        return ("Error: el csv: %s no pudo crearse. %s" % (nombre_archivo, e))

def crear_xls(patrimonio, fecha_corte, revisiones:[], consultas:(), mensaje:()):
    
    # Create a workbook and add a worksheet.
    nombre_archivo = 'INCONSISTENCIAS_PAT-%s_FCORT-%s' % (patrimonio, fecha_corte)
    workbook = xlsxwriter.Workbook('csv_data/%s.xlsx' % nombre_archivo)
    conexion_db = conexion()
    titulos = (
        'NEGOCIOS CON TIPO DE DOCUMENTO NULL',
        'NEGOCIOS DUPLICADOS',
        'CUOTAS DUPLICADAS',
        'CUOTAS SIN NEGOCIO'
    )
    encabezado = [
        ('COD_PATRIMONIO', 'NUM_CTA_CREDITO', 'COD_CLIENTE', 'COD_EXTRAFIN', 'FECHA_CORTE', 'TIPO_DOCUMENTO'),
        ('COD_PATRIMONIO', 'NUM_CTA_CREDITO', 'COD_CLIENTE', 'COD_EXTRAFIN', 'FECHA_CORTE', 'TIPO_DOCUMENTO'),
        ('COD_PATRIMONIO', 'NUM_CTA_CREDITO', 'COD_CLIENTE', 'COD_EXTRAFIN', 'FECHA_CORTE', 'NUM_CUOTA'),
        ('COD_PATRIMONIO', 'NUM_CTA_CREDITO', 'COD_CLIENTE', 'COD_EXTRAFIN', 'FECHA_CORTE', 'NUM_CUOTA')
    ]
    columnas = ('A', 'B', 'C', 'D', 'E', 'F')

    bold = workbook.add_format({'bold': True, 'font_name': 'Arial', 'font_size': 13, 'align': 'center', 'valign': 'vcenter', 'locked': True, 'border': 2, 'bg_color': '#3CB371'})
    bold2 = workbook.add_format({'bold': True, 'font_name': 'Arial', 'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'locked': True, 'border': 2, 'bg_color': '#FFA500'})
    format_data = workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': 'center', 'locked': True, 'border': 1})

    # consultas, mensaje = ReportsRev.detalle_valdiario()
    # consultas, mensaje = RespaldoRev.detalle_valdiario()
    try:
        for i in range(0, len(revisiones)):
            data = []
            # Nombrando cada hoja
            worksheet = workbook.add_worksheet('%s' % mensaje[revisiones[i]])
            # Ingresando el titulo de cada hoja
            worksheet.merge_range('A1:F1', '%s' % titulos[revisiones[i]], bold)
            # Inmovilizar paneles
            worksheet.freeze_panes('A3')
            # Ajustar ancho de columnas
            with conexion_db.cursor() as cursor:
                cursor.execute(consultas[revisiones[i]], pat_consulta=patrimonio, fecha_consulta=fecha_corte)
                data.append(cursor.fetchall())
            row = 1
            col = 0
            for x in encabezado[revisiones[i]]:
                ajustar = '%s%s:%s%s' % (columnas[col], 2, columnas[col], 2)
                worksheet.set_column(ajustar, 20)
                worksheet.write(row, col, x, bold2)
                col += 1
            row = 2
            col = 0
            for x in range(0,len(data)):
                for j in range(0,len(data[x])):
                    col = 0
                    for dato in range(0,len(data[x][j])):
                        worksheet.write(row, col, data[x][j][dato], format_data)
                        col += 1
                    row += 1
        workbook.close()
        return True
    except Exception as e:
        # return ("Error: archivo .XLS - %s" % (e))
        raise

# print(crear_xls(4, '11062020', [1,1,1,1]))

    