import discord
import datetime, time
import asyncio

from discord.ext import commands


from csv_file import crear_csv, crear_xls
from script_sql import ScriptSQL
from enviar_correo import Correo

from acceso_db import conexion
import cx_Oracle

from consultas import Reports, Respaldo
from respaldo_revisiones import ReportsRev, RespaldoRev

bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    print('Inicio de sesion en: {0.user}'.format(bot))

@bot.event
async def on_command_error(ctx, error):
	mensaje = str(error)
	embed = discord.Embed(
				title='Invocar comando',
				description='Para invocar un comando se debe escribir el nombre del comando seguido del patrimonio y luego la fecha de corte, separados con un espacio.',
				color=discord.Color.blue()
				)
	if isinstance(error, commands.CommandNotFound):
		await ctx.send('Error: Comando no encontrado!')
	if isinstance(error, commands.MissingRequiredArgument):
		if mensaje.find("patrimonio") >= 0:
			await ctx.channel.send('Error: Falta el argumento "PATRIMONIO" y "FECHA DE CORTE" en el comando!')
			embed.add_field(name='Ejemplo', value='"$comando_a_ejecutar 6 20052020"', inline=False)
			await ctx.send(embed=embed)
		elif mensaje.find("fecha_corte") >= 0:
			await ctx.channel.send('Error: Falta el argumento "FECHA DE CORTE" en el comando!')
			embed.add_field(name='Ejemplo', value='"$comando_a_ejecutar 6 20052020"', inline=False)
			await ctx.send(embed=embed)
	if isinstance(error, commands.BadArgument):
		if mensaje.find("patrimonio") >= 0:
			await ctx.channel.send('Error: Parametro "PATRIMONIO" incorrecto!')
			embed.add_field(name='Ejemplo', value='"$comando_a_ejecutar 6 20052020"', inline=False)
			await ctx.send(embed=embed)
		elif mensaje.find("fecha_corte") >= 0:
			await ctx.channel.send('Error: Parametro "FECHA DE CORTEeee" incorrecto!')
			embed.add_field(name='Ejemplo', value='"$comando_a_ejecutar 6 20052020"', inline=False)
			await ctx.send(embed=embed)
	else: 
		if mensaje.find("ORA-01840") >= 0 or mensaje.find("ORA-01858") >= 0:
			await ctx.channel.send('Error: Parametro "FECHA DE CORTE" incorrecto!')
			embed.add_field(name='Ejemplo', value='"$comando_a_ejecutar 6 20052020"', inline=False)
			await ctx.send(embed=embed)
		else:
			print('Error no manejado: ' + str(error))

@bot.command()
async def revision_proceso_diario(ctx, patrimonio: int, fecha_corte: str):
	data = []
	try:
		conexion_db = conexion()
		# Se crea el cuadro para dar el resumen de los resultados
		descripcion = "Este es el resumen de las validaciones realizadas para el patrimonio: %s y fecha de corte: %s" % (patrimonio, fecha_corte)
		embed = discord.Embed(
				title='Carga correcta y sin inconsistencias encontradas',
				description=descripcion, 
				timestamp=datetime.datetime.utcnow(),
				color=discord.Color.green()
				)
		# consultas, mensaje= ReportsRev.consulta_diario()
		consultas, mensaje= RespaldoRev.consulta_diario()
		await ctx.channel.send('Espere mientras se realiza la consulta...')
		# Revision de la data
		with conexion_db.cursor() as consulta_db:
			for i in range(0, len(consultas)):
				await ctx.channel.send('->Consultando ' + mensaje[i] + '...')
				consulta_db.execute(consultas[i], pat_consulta=patrimonio, fecha_consulta=fecha_corte)
				data.append(consulta_db.fetchone())
				embed.add_field(name=mensaje[i], value=data[i][0], inline=True)
		# Revision si existen registros
		total_registros = sum(data[i][0] for i in range(0,len(data)))
		if total_registros > 0:
			validaciones = []
			remesa_generada = True
			suma_remesa = data[4][0] + data[5][0]
			await ctx.channel.send('Existen registros para el patrimonio: ' + str(patrimonio) + ' fecha de corte: ' + fecha_corte)
			await ctx.channel.send('_')
			await ctx.channel.send ('Iniciando revision de la DATA:')
			# Consultas para revision de data
			# consulta_v, mensaje_v = ReportsRev.validaciones_diario()
			consulta_v, mensaje_v = RespaldoRev.validaciones_diario()
			with conexion_db.cursor() as consulta_db:
				for i in range(0, len(consulta_v)):
					await ctx.channel.send('->Consultando ' + mensaje_v[i] + '...')
					consulta_db.execute(consulta_v[i], pat_consulta=patrimonio, fecha_consulta=fecha_corte)
					validaciones.append(consulta_db.fetchone())
			await ctx.channel.send('Fin de las validaciones')
			await ctx.channel.send('_')
			# Bloque para evaluar si estan generadas las remesas
			if  suma_remesa == 0:
				remesa_generada = False
			# Se validan resultados de la revision de la data
			validaciones2 = [(1,),(1,),(1,),(1,)]
			archivos_adjuntos = []
			archivo_sql = 0
			archivo_xls = 0
			for i in range(0, len(validaciones)):
				if validaciones[i][0] > 0:
					embed.add_field(name=mensaje_v[i], value=str(validaciones[i][0]), inline=False)
					embed.title = 'Carga completa pero con inconsistencias encontradas'
					embed.color = discord.Color.red()
					#Script para corregir inconsistencia
					if ScriptSQL.crear(i, patrimonio, fecha_corte, validaciones[i][0]):
						archivo_sql += 1
					#Parametro para controlar los archivos que se adjuntaran al correo
					archivos_adjuntos.append(i)
			# Bloque para enviar correo
			total_inconsistencia = sum(i[0] for i in validaciones)
			if total_inconsistencia > 0:
				#Archivo con registros que presentan inconsistencia
				# consulta_xls, mensaje_xls = ReportsRev.detalle_valdiario()
				consulta_xls, mensaje_xls = RespaldoRev.detalle_valdiario()
				data_xls = crear_xls(patrimonio, fecha_corte, archivos_adjuntos, consulta_xls, mensaje_xls)
				if data_xls:
					archivo_xls += 1
				else:
					await ctx.channel.send(data_xls)
				repuesta = Correo.enviar(archivos_adjuntos, patrimonio, fecha_corte, remesa_generada)
				if repuesta.find('Error') >= 0:
					respuesta_embed = repuesta
				else:
					respuesta_embed = 'Se envio un correo a la direccion %s con %s archivo .XLSX y %s scripts .SQL con las indicaciones para realizar las correcciones.' % (repuesta, str(archivo_xls), str(archivo_sql))
				embed.add_field(name='NOTA', value=respuesta_embed, inline=False)
			elif suma_remesa == 0:
				sum_reports_rem = 0
				embed.color = discord.Color.dark_gold()
				embed.title = 'Carga incompleta, inconsistencias encontradas'
				error = "Las REMESAS NO ESTAN CARGADAS en la interfaz del RESPALDO para el patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
				recomendado = "Para retomar el proceso se debe ejecutar el ODI para el patrimonio y fecha de corte."
				consulta_rem, mensaje_rem = ReportsRev.consulta_remesas()
				remesa_reports = []
				# Se valida que las remesas esten generadas en el Reports
				with conexion_db.cursor() as consulta_db:
					for i in range(0, len(consulta_rem)):
						await ctx.channel.send('Consultas adicionales...')
						await ctx.channel.send('..->Consultando Remesas en Reports: ' + mensaje_rem[i] + '...')
						consulta_db.execute(consulta_rem[i], pat_consulta=patrimonio, fecha_consulta=fecha_corte)
						remesa_reports.append(consulta_db.fetchone())
				sum_reports_rem = sum(i[0] for i in remesa_reports)
				# Si las remesas no estan en el reports se cambia el mensaje
				if sum_reports_rem == 0:
					error = "Las REMESAS NO ESTAN GENERADAS en en la interfaz del REPORTS para el patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
					recomendado = "Para retomar el proceso debe ejecutar el FIP_WRAP OPCION 3 (tres) para generar las REMESAS (solo para este patrimonio y fecha de corte)."
				embed.add_field(name='Error encontrado', value=error, inline=False)
				embed.add_field(name='Recomendaciones', value=recomendado, inline=False)
		else:
			await ctx.channel.send('-')
			embed = discord.Embed(
					title='Carga incompleta, inconsistencias encontradas',
					description=descripcion, 
					timestamp=datetime.datetime.utcnow(),
					color=discord.Color.red()
					)
			# Se valida que la informacion este cargada en el Reports
			consulta_reports, mensaje_reports = ReportsRev.consulta_neg_remesas()
			data_reports = []
			await ctx.channel.send('Consultas adicionales...')
			with conexion_db.cursor() as consulta_db:
				for i in range(0, len(consulta_reports)):
					await ctx.channel.send('..->Consultando en Reports: ' + mensaje_reports[i] + '...')
					consulta_db.execute(consulta_reports[i], pat_consulta=patrimonio, fecha_consulta=fecha_corte)
					data_reports.append(consulta_db.fetchone())
			if data_reports[0][0] == 0 and data_reports[1][0] == 0:
				error = "Las INFORMACION NO ESTA GENERADA en la interfaz del REPORTS para el patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
				recomendado = "Para retomar el proceso debe ejecutar el FIP_WRAP OPCION 2 (dos) para generar los NEGOCIOS y luego el FIP_WRAP OPCION 3 (tres) para generar las REMESAS del patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
			elif data_reports[1][0] == 0:
				error = "Las REMESAS NO ESTAN GENERADAS en la interfaz del REPORTS para el patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
				recomendado = "Para retomar el proceso debe ejecutar el FIP_WRAP OPCION 3 (tres) para generar las REMESAS del patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
			elif data_reports[0][0] == 0:
				error = "La INFORMACION NO ESTA GENERADA en la interfaz del REPORTS para el patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
				recomendado = "Para retomar el proceso debe ejecutar el FIP_WRAP OPCION 2 (dos) para generar los NEGOCIOS del patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
			else:
				descripcion = "Este es el resumen de las validaciones realizadas para el patrimonio: %s y fecha de corte: %s" % (patrimonio, fecha_corte)
				error = "La INFORMACION NO ESTA CARGADA en la interfaz del RESPALDO para el patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
				recomendado = "Para retomar el proceso se debe EJECUTAR el ODI para el patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)

			embed.add_field(name='Error encontrado', value=error, inline=False)
			embed.add_field(name='Recomendaciones', value=recomendado, inline=False)
		await ctx.send(embed=embed)
	except Exception as e:
		embed = discord.Embed(
				title='Error no manejado',
				description='%s' % e,
				color=discord.Color.dark_red()
				)
		await ctx.send(embed=embed)

@bot.command()
async def test(ctx, patrimonio: int, fecha_corte: str):
	consultas, mensaje= consulta_diario()
	row = []
	await ctx.channel.send('Espere mientras se realiza la consulta...')
	cnx = conexion()
	with cnx.cursor() as cursor:
		for i in range(0, len(consultas)):
			cursor.execute(consultas[i], pat_consulta=patrimonio, fecha_consulta=fecha_corte)
			row.append(cursor.fetchone())
			await ctx.channel.send('Consultando ' + mensaje[i] + '...')
	print(sum(i[0] for i in row))

def test_csv(patrimonio, fecha_corte):
	row = []
	cnx = conexion()
	with cnx.cursor() as cursor:
		cursor.execute(Respaldo.consultar_remesas_cantidad(), pat_consulta=patrimonio, fecha_consulta=fecha_corte)
		row.append(cursor.fetchall())
	return row

bot.run('NzExOTkwMzYxMTY5NDYxMjk4.XvTpkw.uc8tW1l3HkyV6Nu5xxJTaxoV0Jw')

