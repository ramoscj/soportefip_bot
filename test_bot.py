import cx_Oracle
from consultas import Reports, Respaldo
from enviar_correo import Correo

patrimonio = 61
fecha_corte = "15052020"

cnx = cx_Oracle.connect("tcexplorer", "anita", "NOVA.DIN.CL")
row = [1,2,3,4,0,6]
row2 = [1,2,3,4]

#cursor.execute(Reports.consultar_negocios(), pat_consulta=patrimonio, fecha_consulta=fecha_corte)
#row.append(cursor.fetchone())
#print(row[0][0])
#print(reports_negocios())

consultas_reports = (Reports.consultar_negocios(), 
		Reports.consultar_negocios_cuotas(), 
		Reports.consultar_movimientos_int_extra(),
		Reports.consultar_movimientos_financieros(),
		Reports.consultar_remesas(),
		Reports.consultar_remesas_detalle()
		)
consultas_estado = ('Negocios', 'Cuotas', 'Movimientos con Intereses', 'Movimientos Financieros', 'Remesas', 'Detalles de Remesas')

# with cnx.cursor() as cursor:
# 	for i in range(0, len(consultas_reports)):
# 		if len(row) == 0 or len(row) != 0:
# 			print('Consultando ' + consultas_estado[i] + '...')
# 		cursor.execute(consultas_reports[i], pat_consulta=patrimonio, fecha_consulta=fecha_corte)
# 		row.append(cursor.fetchone())

class Reports_validar():

	def negocios_nulos(patrimonio, fecha_corte):
		with cnx.cursor() as cursor:
			print('Consultando Negocios con tipo de documento NULL...')
			cursor.execute(Respaldo.consultar_negocios_nulos(), pat_consulta=patrimonio, fecha_consulta=fecha_corte)
			return (cursor.fetchone())

	def negocios_duplicados(patrimonio, fecha_corte):
		with cnx.cursor() as cursor:
			print('Consultando Negocios duplicados...')
			cursor.execute(Respaldo.consultar_negocios_nulos(), pat_consulta=patrimonio, fecha_consulta=fecha_corte)
			return (cursor.fetchone())

	def cuotas_duplicadas(patrimonio, fecha_corte):
		with cnx.cursor() as cursor:
			print('Consultando Cuotas duplicadas...')
			cursor.execute(Respaldo.consultar_cuotas_duplicadas(), pat_consulta=patrimonio, fecha_consulta=fecha_corte)
			return (cursor.fetchone())

	def cuotas_sin_negocio(patrimonio, fecha_corte):
		with cnx.cursor() as cursor:
			print('Consultando Cuotas sin Negocio...')
			cursor.execute(Respaldo.consultar_cuotas_snegocios(), pat_consulta=patrimonio, fecha_consulta=fecha_corte)
			return (cursor.fetchone())



j = 0

for resultado in row:
	if resultado > 0:
		j += 1
	
if j == 6:
	print('Carga correcta del patrimonio: ' + str(patrimonio) + ' fecha de corte: ' + fecha_corte)
	# Iniciar revision de DATA
	print ('_____________________________')
	print('')
	print ('Iniciando revision de DATA:')
	negocios_nulos = Reports_validar.negocios_nulos(patrimonio, fecha_corte)
	negocios_duplicados = Reports_validar.negocios_duplicados(patrimonio, fecha_corte)
	cuotas_duplicadas = Reports_validar.cuotas_duplicadas(patrimonio, fecha_corte)
	cuotas_sin_negocios = Reports_validar.cuotas_sin_negocio(patrimonio, fecha_corte)
	print ('Fin de las validaciones')
	print ('_____________________________')
	# Se validan resultados de la revision de la DATA
	if negocios_nulos[0] > 0:
		print('Hay que corregir negocios con tipo de documento NULL')
	elif negocios_duplicados[0] > 0:
		print('Hay que corregir negocios duplicados')
	elif cuotas_duplicadas is not None:
		print('Hay que corregir cuotas duplicadas')
	elif cuotas_sin_negocios[0] > 0:
		print('Hay que corregir cuotas sin negocio')
	else:
		print('Validaciones de DATA OK!')
		Correo.enviar('carlos.ramos@imagicair.cl', 'sop01@imagicair.cl', 'Asunto-Prueba', 'Este es el mensaje' )
else:
	print ('_____________________________')
	print('')
	print('Carga incompleta, registros cargados:')
	i = 0
	remesas = 0
	conteo_registros = 0
	for resultado in row:
		print('Cantidad de ' + consultas_estado[i] + ': ' + str(resultado))
		i += 1
		conteo_registros = conteo_registros + resultado
		if resultado == 0 and i == 4:
			remesas = 1
	if conteo_registros == 0:
		print('_____________________________')
		print('Hay que cargar todo')
	elif remesas == 1:
		print('_____________________________')
		print('Hay que corregir remesas')
	
		