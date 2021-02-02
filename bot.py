import discord
from discord.ext import commands

import datetime, time
import pytz
import subprocess

from csv_file import crear_csv, crear_xls
from script_sql import ScriptSQL
from enviar_correo import Correo
from embed_mensajes import Mensaje
from conexion_db import insertarConsulta

from acceso_db import conexion

from consultas import Respaldo
from respaldo_revisiones import RespaldoRev
from reports_revisiones import ReportsRev

from config_bot import PATRIMONIOS_TC, ENTORNO_FIP, ENTORNO_REPORTS, TOKEN_BOT

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
	tz = pytz.timezone('America/Santiago')
	fechaProceso = datetime.datetime.now(tz=tz)
	horaInicioProceso = fechaProceso.strftime('%H:%M:%S')
	errorProceso = 0
	envioScript = 0
	await ctx.channel.send(':regional_indicator_i::regional_indicator_n::regional_indicator_i::regional_indicator_c::regional_indicator_i::regional_indicator_o:  -> PATRIMONIO: %s FECHA_CORTE: %s, porfavor espere...' % (patrimonio, fecha_corte))
	try:
		conexionDB = conexion()
		entorno = ENTORNO_FIP['DB']
		dblink = ENTORNO_FIP['DBLINK']
		# Se crea el cuadro para dar el resumen de los resultados
		embed = discord.Embed(
					title=':hugging: Carga correcta y sin inconsistencias encontradas :thumbsup:',
					description="Este es el resumen de las validaciones realizadas para el patrimonio: %s y fecha de corte: %s" % (patrimonio, fecha_corte),
					timestamp=fechaProceso,
					color=discord.Color.green()
				)
		# Consultas SQL y texto para seguimiento
		consultaDiario, mensaje = RespaldoRev.consulta_diario(entorno, dblink)
		await ctx.channel.send('Iniciando las consultas DB: %s' % str(conexionDB))
		# Revision para el aptrimonio y fecha de corte
		with conexionDB.cursor() as consulta_db:
			for i in range(0, len(consultaDiario)):
				consulta_db.execute(consultaDiario[i], pat_consulta= patrimonio, fecha_consulta= fecha_corte)
				resultado = consulta_db.fetchone()
				if resultado[0] > 0:
					registrosRespaldo.append(resultado[0])
					embed.add_field(name= mensaje[i], value= resultado[0], inline= True)
					await ctx.channel.send(':fast_forward: Consultando ' + ':white_check_mark: ' + mensaje[i])
				else:
					await ctx.channel.send(':fast_forward: Consultando ' + ':x: ' + mensaje[i])

		if len(registrosRespaldo) == 6:
			erroresEncontrados = []
			await ctx.channel.send(':bar_chart: Existen registros para el patrimonio: ' + str(patrimonio) + ' fecha de corte: ' + fecha_corte)
			await ctx.channel.send ('.:regional_indicator_r::regional_indicator_e::regional_indicator_v::regional_indicator_i::regional_indicator_s::regional_indicator_i::regional_indicator_o::regional_indicator_n:  :regional_indicator_d::regional_indicator_e:  :regional_indicator_l::regional_indicator_a:  :regional_indicator_d::regional_indicator_a::regional_indicator_t::regional_indicator_a:')
			# Consultas SQL y texto para seguimiento
			consultaValidarCarga, mensajeValidacion = RespaldoRev.validaciones_diario(entorno, dblink)
			with conexionDB.cursor() as consulta_db:
				for i in range(0, len(consultaValidarCarga)):
					if i == 8:
						patTC = PATRIMONIOS_TC.get(patrimonio)
						consulta_db.execute(consultaValidarCarga[i], pat_consulta=patrimonio, fecha_consulta=fecha_corte, pat_consultatc= patTC)
					else:
						consulta_db.execute(consultaValidarCarga[i], pat_consulta=patrimonio, fecha_consulta=fecha_corte)
					resultado = consulta_db.fetchone()
					erroresEncontrados.append(resultado[0])
					if resultado[0] > 0:
						await ctx.channel.send(':fast_forward: Consultando :x: ' + mensajeValidacion[i])
					else:
						await ctx.channel.send(':fast_forward: Consultando :white_check_mark: ' + mensajeValidacion[i])
			await ctx.channel.send('.:regional_indicator_f::regional_indicator_i::regional_indicator_n:  :regional_indicator_d::regional_indicator_e:  :regional_indicator_l::regional_indicator_a:  :regional_indicator_r::regional_indicator_e::regional_indicator_v::regional_indicator_i::regional_indicator_s::regional_indicator_i::regional_indicator_o::regional_indicator_n:')
			# erroresEncontrados = [(1,),(1,),(1,),(1,),(1,)]
			archivoSqlAdjunto = []
			archivo_sql = 0
			archivo_xls = 0
			# Bloque para agregar las inconsistencias a la salida por pantalla
			for i in range(0, len(erroresEncontrados)):
				if erroresEncontrados[i] > 0:
					errorProceso = 1
					embed.add_field(name= ':x: %s' % mensajeValidacion[i], value= str(erroresEncontrados[i]), inline= False)
					embed.title = ':thinking: Carga completa pero con inconsistencias encontradas :thumbsdown:'
					embed.color = discord.Color.red()
					# Script para corregir inconsistencia
					if i != 9:
						if ScriptSQL.crear(i, patrimonio, fecha_corte, erroresEncontrados[i]):
							archivo_sql += 1
							archivoSqlAdjunto.append(i)
							envioScript = 1
					else:
						error = 'El Patrimonio: %s fecha de corte: %s tiene una ejeucion en el SATELITE.' % (patrimonio, fecha_corte)
						recomendaciones = 'Si no reconoce esta ejeucion y desea realizar una nueva favor informar al correo: sop01@imagicair.cl y solicite script para realizar el borrado del proceso existente.'
						embed.add_field(name=':no_entry_sign: ERROR ENCONTRADO', value=error, inline=False)
						embed.add_field(name=':loudspeaker: RECOMENDACIONES', value=recomendaciones, inline=False)
			# Bloque para enviar correo
			if len(archivoSqlAdjunto) > 0:
				consultaErrorData, mensajeErrorData = RespaldoRev.detalle_valdiario(entorno, dblink)
				data_xls = crear_xls(patrimonio, fecha_corte, archivoSqlAdjunto, consultaErrorData, mensajeErrorData)
				if data_xls:
					archivo_xls += 1
				# Se envia correo con las indicaciones
				repuesta = Correo.enviar(archivoSqlAdjunto, patrimonio, fecha_corte)
				respuesta_embed = 'Se envio un correo a la direccion: :incoming_envelope: %s con %s archivo .XLSX y %s scripts .SQL con las indicaciones para realizar las correcciones.' % (repuesta, str(archivo_xls), str(archivo_sql))
				embed.add_field(name='NOTA', value=respuesta_embed, inline=False)
		else:
			errorProceso = 1
			dblink_reports = ENTORNO_REPORTS['DBLINK']
			await ctx.channel.send(':x: No existen registros para el patrimonio: ' + str(patrimonio) + ' fecha de corte: ' + fecha_corte)
			embed.title = ':dizzy_face: Carga de la información para realizar revisón INCOMPLETA :thumbsdown:'
			embed.color = discord.Color.red()
			# Consultas SQL y texto para seguimiento
			consulta_reports, mensaje_reports = RespaldoRev.consulta_neg_remesas('reports', dblink_reports)
			data_reports = []
			# Se valida que la informacion este cargada en el Reports
			await ctx.channel.send('Consultas adicionales...')
			with conexionDB.cursor() as consulta_db:
				for i in range(0, len(consulta_reports)):
					await ctx.channel.send(':fast_forward: Consultando en Reports: ' + mensaje_reports[i])
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
			embed.add_field(name=':no_entry_sign: ERROR ENCONTRADO', value=error, inline=False)
			embed.add_field(name=':loudspeaker: RECOMENDACIONES', value=recomendado, inline=False)
			embed.add_field(name=':memo: NOTA', value=nota_msj, inline=False)
		await ctx.send(embed=embed)

		# Insertar registro de consulta en la DB
		horaFinProceso = datetime.datetime.now(tz=tz)
		data = {'FECHA_CONSULTA': fechaProceso.date(), 'PATRIMONIO': patrimonio, 'FECHA_CORTE': fecha_corte, 'HORA_INICIO': horaInicioProceso, 'HORA_FIN': horaFinProceso.strftime("%H:%M:%S"), 'ERROR': errorProceso, 'ENVIO_SCRIPT': envioScript}
		insertarConsulta(data)

	except Exception as e:
		embed = discord.Embed(
				title='Error no manejado :person_facepalming:',
				description='%s' % e,
				color=discord.Color.dark_red()
				)
		await ctx.send(embed=embed)

@bot.command()
async def test(ctx):
	await ctx.send('Hola estoy aqui!!')

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

bot.run(TOKEN_BOT)

