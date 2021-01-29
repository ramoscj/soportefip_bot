from acceso_db import conexion
from respaldo_revisiones import RespaldoRev
from validar_input import validarFechaCorte, fechaDiaSiguiente

from alive_progress import alive_bar
import datetime

from csv_file import crearXlsDescuadraturas
from script_sql import ScriptSqlUpdateTrx

def CuadraturasRemesas(patrimonio, fechaCorteInicio, fechaCorteFin):
	try:
		diferenciasTRX = dict()
		restaTrxRemesas = dict()
		montosRemesaTrx = dict()

		with alive_bar(5) as bar:

			diferenciaRemesas, cuentasConDiferencias = DiferenciasRemesas(patrimonio, fechaCorteInicio, fechaCorteFin)
			bar()
			print('Diferencias por Remesas Ok')

			movimientosDuplicados = MovimientosDuplicados(patrimonio, fechaCorteInicio, fechaCorteFin)
			bar()
			print('Movimientos duplicados Ok')

			for fechaConDiferencias in diferenciaRemesas.keys():
				diferenciasTRX[fechaConDiferencias] = DiferenciasAsientosContables(patrimonio, fechaConDiferencias)

				if diferenciasTRX[fechaConDiferencias].get('DIFERENCIA_TRX') and diferenciaRemesas[fechaConDiferencias].get('DIFERENCIA_POR_CUENTAS'):
					montoTRX = diferenciasTRX[fechaConDiferencias]['DIFERENCIA_TRX']
					montoRemesas = diferenciaRemesas[fechaConDiferencias]['DIFERENCIA_POR_CUENTAS']
					restaTrxRemesas[fechaConDiferencias] = montoTRX + montoRemesas
					montosRemesaTrx[fechaConDiferencias] = {'DIFERENCIA_TRX': montoTRX, 'DIFERENCIA_REMESA': montoRemesas}
			bar()
			print('Diferencias por TRX Ok')

			crearXlsDescuadraturas(patrimonio, fechaCorteInicio, fechaCorteFin, cuentasConDiferencias, montosRemesaTrx, movimientosDuplicados)
			bar()
			print('XLSX Creado')

			ScriptSqlUpdateTrx.crearSql(patrimonio, list(diferenciaRemesas.keys()))
			bar()
			print('Script SQL Creado')

		return True
	except Exception as e:
		raise Exception('Error en CuadraturasRemesas: %s' % e)

def DiferenciasRemesas(patrimonio, fechaCorteInicio, fechaCorteFin):
	try:
		consultaDiferenciaRemesas, mensaje = RespaldoRev.cuadratura_remesas()
		conexionDB = conexion()
		diferenciasMontos = dict()
		with conexionDB.cursor() as consulta_db:
			for i in range(0, 1):
				consulta_db.execute(consultaDiferenciaRemesas[i], pat_consulta= patrimonio, fecha_inicio= fechaCorteInicio, fecha_fin= fechaCorteFin)
				columns = [col[0] for col in consulta_db.description]
				consulta_db.rowfactory = lambda *args: dict(zip(columns, args))
				data = consulta_db.fetchall()

				for diferencias in range(0, len(data)):
					fechaCorte = data[diferencias]['MOV_FECHA_MOVIMIENTO']
					diferencia = data[diferencias]['DIFERENCIA']
					if type(fechaCorte) is datetime.datetime:
						fechaCorte = fechaCorte.strftime("%d%m%Y")
					if not diferenciasMontos.get(fechaCorte):
						diferenciasMontos[fechaCorte] =  {'DIFERENCIA_POR_CUENTAS': diferencia}
					else:
						diferenciasMontos[fechaCorte]['DIFERENCIA_POR_CUENTAS'] += diferencia
		diferenciaPorCuentas = [data, columns]
		return diferenciasMontos , diferenciaPorCuentas
	except Exception as e:
		raise Exception('Error en DiferenciasRemesas: %s' % e)

def MovimientosDuplicados(patrimonio, fechaCorteInicio, fechaCorteFin):
	try:
		consultaAsientosContDuplicados, mensaje = RespaldoRev.cuadratura_remesas()
		conexionDB = conexion()
		movimientosDuplicados = dict()
		with conexionDB.cursor() as consulta_db:
			for i in range(1, 2):
				consulta_db.execute(consultaAsientosContDuplicados[i], pat_consulta= patrimonio, fecha_inicio= fechaCorteInicio, fecha_fin= fechaCorteFin)
				columns = [col[0] for col in consulta_db.description]
				consulta_db.rowfactory = lambda *args: dict(zip(columns, args))
				data = consulta_db.fetchall()

				for duplicados in range(0, len(data)):
					fechaCorte = data[duplicados]['FECHA_MOVIMIENTO']
					if type(fechaCorte) is datetime.datetime:
						fechaCorte = fechaCorte.strftime("%d%m%Y")
					movimientosDuplicados[fechaCorte] = {'MOV_DUPLICADOS': data[duplicados]['CANTIDAD']}

		return movimientosDuplicados
	except Exception as e:
		raise Exception('Error en MovimientosDuplicados: %s' % e)

def DiferenciasAsientosContables(patrimonio, fechaCorte):
	try:
		consultaMontosAsientosCont, mensaje = RespaldoRev.cuadratura_remesas()
		conexionDB = conexion()
		diferenciasTRX = {'DIFERENCIA_TRX': 0}
		data = []
		with conexionDB.cursor() as consulta_db:
			for i in range(2, 4):
				consulta_db.execute(consultaMontosAsientosCont[i], pat_consulta= patrimonio, fecha_inicio= fechaCorte)
				columns = [col[0] for col in consulta_db.description]
				consulta_db.rowfactory = lambda *args: dict(zip(columns, args))
				data.append(consulta_db.fetchone())

		for valor in range(0, len(data)):
			if data[valor] is not None:
				diferenciasTRX['DIFERENCIA_TRX'] += int(data[valor]['DIFERENCIA'])
		return diferenciasTRX
	except Exception as e:
		raise Exception('Error en DiferenciasAsientosContables: %s' % e)

print(CuadraturasRemesas(10, '01012021', '15012021'))
# print(crearXlsDescuadraturas(6, '01092020', '05092020', z[0], z[1]))
# x, y = DiferenciasRemesas(6, '01012020', '20012020')
# for a in x.keys():
# a = list(x.keys())
# print(a)
# print(a[0])
# print(a[-1])