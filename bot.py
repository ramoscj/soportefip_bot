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

from consultas import Respaldo
from respaldo_revisiones import RespaldoRev
from reports_revisiones import ReportsRev

from config_bot import PATRIMONIOS_TC, ENTORNO_FIP, ENTORNO_REPORTS

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
			embed.add_field(name='Ejemplo', value='">comando_a_ejecutar 6 20052020"', inline=False)
			await ctx.send(embed=embed)
		elif mensaje.find("fecha_corte") >= 0:
			await ctx.channel.send('Error: Falta el argumento "FECHA DE CORTE" en el comando!')
			embed.add_field(name='Ejemplo', value='">comando_a_ejecutar 6 20052020"', inline=False)
			await ctx.send(embed=embed)
	if isinstance(error, commands.BadArgument):
		if mensaje.find("patrimonio") >= 0:
			await ctx.channel.send('Error: Parametro "PATRIMONIO" incorrecto!')
			embed.add_field(name='Ejemplo', value='">comando_a_ejecutar 6 20052020"', inline=False)
			await ctx.send(embed=embed)
		elif mensaje.find("fecha_corte") >= 0:
			await ctx.channel.send('Error: Parametro "FECHA DE CORTE" incorrecto!')
			embed.add_field(name='Ejemplo', value='">comando_a_ejecutar 6 20052020"', inline=False)
			await ctx.send(embed=embed)
	else:
		if mensaje.find("ORA-01840") >= 0 or mensaje.find("ORA-01858") >= 0:
			await ctx.channel.send('Error: Parametro "FECHA DE CORTE" incorrecto!')
			embed.add_field(name='Ejemplo', value='">comando_a_ejecutar 6 20052020"', inline=False)
			await ctx.send(embed=embed)
		else:
			await ctx.send('Error no manejado: ' + str(error))

@bot.command()
async def revision_proceso_diario(ctx, patrimonio: int, fecha_corte: str):
	registrosRespaldo = []
	nota = False
	await ctx.channel.send('Iniciando proceso -> PATRIMONIO: %s FECHA_CORTE: %s, porfavor espere...' % (patrimonio, fecha_corte))
	try:
		conexionDB = conexion()
		entorno = ENTORNO_FIP['DB']
		dblink = ENTORNO_FIP['DBLINK']
		# Se crea el cuadro para dar el resumen de los resultados
		embed = discord.Embed(
					title='Carga correcta y sin inconsistencias encontradas',
					description="Este es el resumen de las validaciones realizadas para el patrimonio: %s y fecha de corte: %s" % (patrimonio, fecha_corte),
					timestamp=datetime.datetime.utcnow(),
					color=discord.Color.green()
				)
		# Consultas SQL y texto para seguimiento
		consultaDiario, mensaje = RespaldoRev.consulta_diario(entorno, dblink)
		await ctx.channel.send('Iniciando las consultas DB: %s' % str(conexionDB))
		# Revision para el aptrimonio y fecha de corte
		with conexionDB.cursor() as consulta_db:
			for i in range(0, len(consultaDiario)):
				await ctx.channel.send('->Consultando ' + mensaje[i] + '...')
				consulta_db.execute(consultaDiario[i], pat_consulta= patrimonio, fecha_consulta= fecha_corte)
				resultado = consulta_db.fetchone()
				if resultado[0] > 0:
					registrosRespaldo.append(resultado[0])
					embed.add_field(name= mensaje[i], value= resultado[0], inline= True)

		if len(registrosRespaldo) == 6:
			erroresEncontrados = []
			await ctx.channel.send('Existen registros para el patrimonio: ' + str(patrimonio) + ' fecha de corte: ' + fecha_corte)
			await ctx.channel.send('_')
			await ctx.channel.send ('Iniciando revision de la DATA:')
			# Consultas SQL y texto para seguimiento
			consultaValidarCarga, mensajeValidacion = RespaldoRev.validaciones_diario(entorno, dblink)
			with conexionDB.cursor() as consulta_db:
				for i in range(0, len(consultaValidarCarga)):
					await ctx.channel.send('->Consultando ' + mensajeValidacion[i] + '...')
					if i == 7:
						patTC = PATRIMONIOS_TC.get(patrimonio)
						consulta_db.execute(consultaValidarCarga[i], pat_consulta=patrimonio, fecha_consulta=fecha_corte, pat_consultatc= patTC)
					else:
						consulta_db.execute(consultaValidarCarga[i], pat_consulta=patrimonio, fecha_consulta=fecha_corte)
					resultado = consulta_db.fetchone()
					erroresEncontrados.append(resultado[0])
			await ctx.channel.send('Fin de las validaciones')
			await ctx.channel.send('_')
			# erroresEncontrados = [(1,),(1,),(1,),(1,),(1,)]
			archivoSqlAdjunto = []
			archivo_sql = 0
			archivo_xls = 0
			# Bloque para agregar las inconsistencias a la salida por pantalla
			for i in range(0, len(erroresEncontrados)):
				if erroresEncontrados[i] > 0:
					embed.add_field(name= mensajeValidacion[i], value= str(erroresEncontrados[i]), inline= False)
					embed.title = 'Carga completa pero con inconsistencias encontradas'
					embed.color = discord.Color.red()
					# Script para corregir inconsistencia
					if i != 8:
						if ScriptSQL.crear(i, patrimonio, fecha_corte, erroresEncontrados[i]):
							archivo_sql += 1
							archivoSqlAdjunto.append(i)
						#Parametro para controlar los archivos que se adjuntaran al correo
			# Bloque para enviar correo
			if len(archivoSqlAdjunto) > 0:
				consultaErrorData, mensajeErrorData = RespaldoRev.detalle_valdiario(entorno, dblink)
				data_xls = crear_xls(patrimonio, fecha_corte, archivoSqlAdjunto, consultaErrorData, mensajeErrorData)
				if data_xls:
					archivo_xls += 1
				# Se envia correo con las indicaciones
				repuesta = Correo.enviar(archivoSqlAdjunto, patrimonio, fecha_corte)
				respuesta_embed = 'Se envio un correo a la direccion %s con %s archivo .XLSX y %s scripts .SQL con las indicaciones para realizar las correcciones.' % (repuesta, str(archivo_xls), str(archivo_sql))
				embed.add_field(name='NOTA', value=respuesta_embed, inline=False)
		else:
			dblink_reports = ENTORNO_REPORTS['DBLINK']
			await ctx.channel.send('-')
			embed.title = 'Carga de la información para realizar revisón INCOMPLETA'
			embed.color = discord.Color.red()
			# Consultas SQL y texto para seguimiento
			consulta_reports, mensaje_reports = RespaldoRev.consulta_neg_remesas('reports', dblink_reports)
			data_reports = []
			# Se valida que la informacion este cargada en el Reports
			await ctx.channel.send('Consultas adicionales...')
			with conexionDB.cursor() as consulta_db:
				for i in range(0, len(consulta_reports)):
					await ctx.channel.send('..->Consultando en Reports: ' + mensaje_reports[i] + '...')
					consulta_db.execute(consulta_reports[i], pat_consulta=patrimonio, fecha_consulta=fecha_corte)
					data_reports.append(consulta_db.fetchone())
			negocios_remesas = int(data_reports[0][0]) + int(data_reports[1][0])
			remesas_reports = int(data_reports[1][0])
			negocios_reports = int(data_reports[0][0])
			if  negocios_remesas == 0:
				error, recomendado, nota_msj = Mensaje.fip_wrap2_3(patrimonio, fecha_corte)
			elif remesas_reports == 0:
				error, recomendado, nota_msj = Mensaje.fip_wrap3(negocios_reports, patrimonio, fecha_corte)
			elif negocios_reports == 0:
				error, recomendado, nota_msj = Mensaje.fip_wrap2(patrimonio, fecha_corte)
			else:
				error, recomendado, nota_msj = Mensaje.reports_odi(patrimonio, fecha_corte)
			if len(registrosRespaldo) >= 1:
				nota_msj = "Si ya realizo la ejecucion del proceso ODI, espere a que este finalice y luego vuelva a ejecutar la revisión"
				embed.color = discord.Color.dark_gold()
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
async def test(ctx):
	await ctx.send('Hola estoy aqui!!')

@bot.command()
async def vpn_active(ctx):
	try:
		programa = 'vpncli.exe'
		parametros = 'my_key.dat'
		cp = subprocess.run(['C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\%s' % programa, '-s', '<', '..\..\%s' % parametros], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		await ctx.send('Conectando VPN: %s - %s' % (cp.stdout, cp.stderr))
	except Exception as e:
		raise e

@bot.command()
async def vpnActiveLinux(ctx):
	try:
		cp = subprocess.run('sudo bash /usr/bin/start_vpn.sh', shell=True)
		await ctx.channel.send('Conectando VPN: %s' % cp.returncode)
		conexionDB = conexion()
		await ctx.send('Conexion con DB: %s OK' % str(conexionDB))
		conexionDB.close
	except Exception as e:
		await ctx.send('Error VPN: %s' % e)

@bot.command()
async def vpnDeactiveLinux(ctx):
	try:
		cp = subprocess.run('sudo bash /usr/bin/stop_vpn.sh', shell=True)
		await ctx.send('Desconectando VPN: %s' % cp.returncode)
	except Exception as e:
		await ctx.send('Error VPN: %s' % e)

bot.run(TOKEN())

