import csv
from io import BytesIO
import xlsxwriter
import datetime

from respaldo_revisiones import RespaldoRev
from reports_revisiones import ReportsRev
from consultas import Respaldo

from acceso_db import conexion

from config_bot import PATRIMONIOS_TC, PAT_BOT

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

    nombre_archivo = 'INCONSISTENCIAS_PAT-%s_FCORT-%s' % (patrimonio, fecha_corte)
    workbook = xlsxwriter.Workbook('%s/csv_data/%s.xlsx' % (PAT_BOT['PATH'], nombre_archivo))
    conexion_db = conexion()
    titulos = (
        'NEGOCIOS CON TIPO DE DOCUMENTO NULL',
        'NEGOCIOS DUPLICADOS',
        'CUOTAS DUPLICADAS',
        'CUOTAS SIN NEGOCIO',
        'NUMERO DE NEGOCIO NULL',
        'MOVIMIENTOS INTERES EXTRAFIN SIN CUOTAS (006)',
        'MOVIMIENTOS SIN CUOTAS (004, 007, 008, 009, 010, 011, 014, 016)',
        'CLIENTES DUPLICADOS PATRIMONIOS TC'
    )
    TablasClientesDup = [
        {0: ''},
        {1: 'FIP.FIP_CUENTAS'},
        {2: 'FIP.FIP_DIARIO_NEGOCIOS'},
        {3: 'FIP.FIP_EXTRA_IC'},
        {4: 'FIP.FIP_NEGOCIOS'},
        {5: 'FIP.FIP_CUENTA_CREDITO_IC'}
    ]
    columnas = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')

    bold = workbook.add_format({'bold': True, 'font_name': 'Arial', 'font_size': 13, 'align': 'center', 'valign': 'vcenter', 'locked': True, 'border': 2, 'bg_color': '#3CB371'})
    bold2 = workbook.add_format({'bold': True, 'font_name': 'Arial', 'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'locked': True, 'border': 2, 'bg_color': '#FFA500'})
    bold3 = workbook.add_format({'bold': True, 'font_name': 'Arial', 'font_size': 10, 'align': 'left', 'valign': 'vcenter', 'locked': True})
    format_data = workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': 'center', 'locked': True, 'border': 1})
    try:
        for i in range(0, len(revisiones)):
            registrosXlsx = []
            encabezadoDbXlsx = []
            # Nombrando cada hoja
            worksheet = workbook.add_worksheet('%s' % mensaje[revisiones[i]])
            # Ingresando el titulo de cada hoja
            worksheet.merge_range('A1:F1', '%s' % titulos[revisiones[i]], bold)
            # Inmovilizar paneles
            worksheet.freeze_panes('A3')
            # Ajustar ancho de columnas
            with conexion_db.cursor() as cursor:
                if revisiones[i] == 7:
                    for k in range(0,len(consultas[revisiones[i]])):
                        patTC = PATRIMONIOS_TC.get(patrimonio)
                        cursor.execute(consultas[revisiones[i]][k], pat_consulta=patrimonio, fecha_consulta=fecha_corte, pat_consultatc=patTC)
                        columns = [col[0] for col in cursor.description]
                        cursor.rowfactory = lambda *args: dict(zip(columns, args))
                        data = cursor.fetchall()
                        encabezadoDbXlsx.append(columns)
                        if len(data) > 0:
                            registrosXlsx.append(data)
                        else:
                            registrosXlsx.append('')
                else:
                    cursor.execute(consultas[revisiones[i]], pat_consulta=patrimonio, fecha_consulta=fecha_corte)
                    columns = [col[0] for col in cursor.description]
                    cursor.rowfactory = lambda *args: dict(zip(columns, args))
                    data = cursor.fetchall()
                    encabezadoDbXlsx.append(columns)
                    if len(data) > 0:
                        registrosXlsx.append(data)
                    else:
                        registrosXlsx.append('')
            row = 1
            for consulta in range(0,len(registrosXlsx)):
                col = 0
                if consulta > 0:
                    worksheet.write(row, 0, TablasClientesDup[consulta].get(consulta), bold3)
                    row += 1
                for k in encabezadoDbXlsx[consulta]:
                    ajustar = '%s%s:%s%s' % (columnas[col], 2, columnas[col], 2)
                    worksheet.set_column(ajustar, 20)
                    worksheet.write(row, col, k, bold2)
                    col += 1
                row += 1
                for fila in range(0, len(registrosXlsx[consulta])):
                    col = 0
                    for key, valor in registrosXlsx[consulta][fila].items():
                        if type(valor) is datetime.datetime:
                            valor = valor.strftime("%d/%m/%Y")
                        worksheet.write(row, col, valor, format_data)
                        worksheet.write(row+1, col, '',)
                        col += 1
                    row += 1
                row += 1
        workbook.close()
        return True
    except Exception as e:
        raise Exception("Error al crear archivo .XLS. Error: %s" % (e))

# consulta_xls, mensaje_xls = RespaldoRev.detalle_valdiario('fip', '')
# data_xls = crear_xls(4, '12082020', [7], consulta_xls, mensaje_xls)
# print(data_xls)