import discord
from discord.ext import commands

import datetime, time
import asyncio
import subprocess

from csv_file import crear_csv, crear_xls
from script_sql import ScriptSQL
from enviar_correo import Correo
from embed_mensajes import Mensaje

from acceso_db import conexion
from bot_token import TOKEN

from consultas import Reports, Respaldo
from respaldo_revisiones import RespaldoRev
from reports_revisiones import ReportsRev

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
	nota = False
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
		# Consultas SQL y texto para seguimiento
		consultas, mensaje= RespaldoRev.consulta_diario()
		await ctx.channel.send('Espere mientras se realiza la consulta...')
		# Revision para el aptrimonio y fecha de corte
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
			remesa_generada = 0
			suma_remesa = data[4][0] + data[5][0]
			await ctx.channel.send('Existen registros para el patrimonio: ' + str(patrimonio) + ' fecha de corte: ' + fecha_corte)
			await ctx.channel.send('_')
			await ctx.channel.send ('Iniciando revision de la DATA:')
			# Consultas SQL y texto para seguimiento
			consulta_v, mensaje_v = RespaldoRev.validaciones_diario()
			with conexion_db.cursor() as consulta_db:
				for i in range(0, len(consulta_v)):
					await ctx.channel.send('->Consultando ' + mensaje_v[i] + '...')
					consulta_db.execute(consulta_v[i], pat_consulta=patrimonio, fecha_consulta=fecha_corte)
					validaciones.append(consulta_db.fetchone())
			await ctx.channel.send('Fin de las validaciones')
			await ctx.channel.send('_')
			# Se valida que las remesas esten generadas en el Respaldo
			if  suma_remesa == 0:
				remesa_generada = 1
			validaciones2 = [(1,),(1,),(1,),(1,),(1,)]
			archivos_adjuntos = []
			archivo_sql = 0
			archivo_xls = 0
			# Bloque para agregar las inconsistencias a la salida por pantalla
			for i in range(0, len(validaciones)):
				if validaciones[i][0] > 0:
					embed.add_field(name=mensaje_v[i], value=str(validaciones[i][0]), inline=False)
					embed.title = 'Carga completa pero con inconsistencias encontradas'
					embed.color = discord.Color.red()
					# Script para corregir inconsistencia
					if ScriptSQL.crear(i, patrimonio, fecha_corte, validaciones[i][0]):
						archivo_sql += 1
					#Parametro para controlar los archivos que se adjuntaran al correo
					archivos_adjuntos.append(i)
			# Bloque para enviar correo
			total_inconsistencia = sum(i[0] for i in validaciones)
			if total_inconsistencia > 0:
				# Consultas SQL y texto para seguimiento
				consulta_rem, mensaje_rem = ReportsRev.consulta_remesas()
				remesa_reports = []
				# Se valida que las remesas esten generadas en el Reports
				await ctx.channel.send('Consultas adicionales en Reports...')
				with conexion_db.cursor() as consulta_db:
					for i in range(0, len(consulta_rem)):
						await ctx.channel.send('..->Consultando Remesas en Reports: ' + mensaje_rem[i] + '...')
						consulta_db.execute(consulta_rem[i], pat_consulta=patrimonio, fecha_consulta=fecha_corte)
						remesa_reports.append(consulta_db.fetchone())
				await ctx.channel.send('_')
				sum_reports_rem = sum(i[0] for i in remesa_reports)
				# Bloque para evaluar si estan generadas las remesas en el Reports
				if  sum_reports_rem == 0:
					remesa_generada = 2
				#Archivo con registros que presentan inconsistencia
				consulta_xls, mensaje_xls = RespaldoRev.detalle_valdiario()
				data_xls = crear_xls(patrimonio, fecha_corte, archivos_adjuntos, consulta_xls, mensaje_xls)
				if data_xls:
					archivo_xls += 1
				# Se envia correo con las indicaciones
				repuesta = Correo.enviar(archivos_adjuntos, patrimonio, fecha_corte, remesa_generada)
				respuesta_embed = 'Se envio un correo a la direccion %s con %s archivo .XLSX y %s scripts .SQL con las indicaciones para realizar las correcciones.' % (repuesta, str(archivo_xls), str(archivo_sql))
				embed.add_field(name='NOTA', value=respuesta_embed, inline=False)
			elif suma_remesa == 0:
				sum_reports_rem = 0
				embed.color = discord.Color.dark_gold()
				embed.title = 'Carga de la información INCOMPLETA'
				# Mensajes para mostrar en panatalla
				error, recomendado, nota_msj = Mensaje.remesas_respaldo( patrimonio, fecha_corte)
				# Consultas SQL y texto para seguimiento
				consulta_rem, mensaje_rem = ReportsRev.consulta_remesas()
				remesa_reports = []
				# Se valida que las remesas esten generadas en el Reports
				await ctx.channel.send('Consultas adicionales en Reports...')
				with conexion_db.cursor() as consulta_db:
					for i in range(0, len(consulta_rem)):
						await ctx.channel.send('..->Consultando Remesas en Reports: ' + mensaje_rem[i] + '...')
						consulta_db.execute(consulta_rem[i], pat_consulta=patrimonio, fecha_consulta=fecha_corte)
						remesa_reports.append(consulta_db.fetchone())
				sum_reports_rem = sum(i[0] for i in remesa_reports)
				# Si las remesas no estan en el reports se cambia el mensaje
				if sum_reports_rem == 0:
					# Mensajes para mostrar en panatalla
					error, recomendado, nota_msj = Mensaje.remesas_reports(str(data[0][0]), patrimonio, fecha_corte)
				embed.add_field(name='ERROR ENCONTRADO', value=error, inline=False)
				embed.add_field(name='RECOMENDACIONES', value=recomendado, inline=False)
				embed.add_field(name='NOTA', value=nota_msj, inline=False)
		else:
			await ctx.channel.send('-')
			embed = discord.Embed(
					title='Carga de la información para realizar revisón INCOMPLETA',
					description=descripcion, 
					timestamp=datetime.datetime.utcnow(),
					color=discord.Color.red()
					)
			# Consultas SQL y texto para seguimiento
			consulta_reports, mensaje_reports = ReportsRev.consulta_neg_remesas()
			data_reports = []
			# Se valida que la informacion este cargada en el Reports
			await ctx.channel.send('Consultas adicionales...')
			with conexion_db.cursor() as consulta_db:
				for i in range(0, len(consulta_reports)):
					await ctx.channel.send('..->Consultando en Reports: ' + mensaje_reports[i] + '...')
					consulta_db.execute(consulta_reports[i], pat_consulta=patrimonio, fecha_consulta=fecha_corte)
					data_reports.append(consulta_db.fetchone())
			negocios_remesas = data_reports[0][0] + data_reports[1][0]
			negocios_reports = data_reports[0][0]
			remesas_reports = data_reports[1][0]
			if  negocios_remesas == 0:
				# Mensajes para mostrar en panatalla
				error, recomendado, nota_msj = Mensaje.fip_wrap2_3(patrimonio, fecha_corte)
			elif remesas_reports == 0:
				# Mensajes para mostrar en panatalla
				error, recomendado, nota_msj = Mensaje.fip_wrap3(patrimonio, fecha_corte)
			elif negocios_reports == 0:
				# Mensajes para mostrar en panatalla
				error, recomendado, nota_msj = Mensaje.fip_wrap2(patrimonio, fecha_corte)
			else:
				# Mensajes para mostrar en panatalla
				error, recomendado, nota_msj = Mensaje.reports_odi(patrimonio, fecha_corte)
			embed.add_field(name='ERROR ENCONTRADO', value=error, inline=False)
			embed.add_field(name='RECOMENDACIONES', value=recomendado, inline=False)
			embed.add_field(name='NOTA', value=nota_msj, inline=False)
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
	consultas, mensaje= RespaldoRev.consulta_diario()
	row = []
	await ctx.channel.send('Espere mientras se realiza la consulta...')
	cnx = conexion()
	with cnx.cursor() as cursor:
		for i in range(0, len(consultas)):
			cursor.execute(consultas[i], pat_consulta=patrimonio, fecha_consulta=fecha_corte)
			row.append(cursor.fetchone())
			await ctx.channel.send('Consultando ' + mensaje[i] + '...')
	print(sum(i[0] for i in row))

@bot.command()
async def vpn_active(ctx):
	try:
		programa = 'vpncli.exe'
		parametros = 'my_key.dat'
		cp = subprocess.run(['C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\%s' % programa, '-s', '<', '..\..\%s' % parametros], shell=True)
		await ctx.send('Conectado: %s' % cp)
	except Exception as e:
		raise e

@bot.command()
async def vpnActiveLinux(ctx):
	try:
		cp = subprocess.run(['sh','/home/ubuntu/config_vpn/vpn_cisco/my_key.sh'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		await ctx.send('Conectando VPN: %s - %s' % (cp.stdout, cp.stderr))
	except Exception as e:
		await ctx.send('Error VPN: %s' % e)

bot.run(TOKEN())

