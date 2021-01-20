from consultas import Respaldo

class RespaldoRev(object):

	def consulta_diario(entorno, dblink):
		consultas = (
			Respaldo.consultarNegocios(entorno, dblink),
			Respaldo.consultarCuotasNegocios(entorno, dblink),
			Respaldo.consultarMovExtra(entorno, dblink),
			Respaldo.consultarMovFinancieros(entorno, dblink),
			Respaldo.consultarRemesa(entorno, dblink),
			Respaldo.consultarDetalleRemesa(entorno, dblink)
			# Respaldo.consultar_negocios_nulos(entorno, dblink),
			# Respaldo.consultar_negocios_nulos(entorno, dblink)
			)
		estado = ('Negocios', 'Cuotas', 'Movimientos con Intereses', 'Movimientos Financieros', 'Remesas', 'Detalles de Remesas')
		return (consultas, estado)

	def validaciones_diario(entorno, dblink):
		consultas = (
			Respaldo.validarNegociosDocNull(entorno, dblink),
			Respaldo.validarNogociosDuplicados(entorno, dblink),
			Respaldo.validarCuotasDuplicadas(entorno, dblink),
			Respaldo.validarCuotasSinNegocio(entorno, dblink),
			Respaldo.validarNroNegociosNull(entorno, dblink),
			Respaldo.validarMovSinCuotaExtra(entorno, dblink),
			Respaldo.validarMovSinCuota(entorno, dblink),
			Respaldo.count_remesas(entorno, dblink),
			# Respaldo.validarNegociosSinCuenta(),
			Respaldo.validarClienteDuplicadoTc(),
			Respaldo.validarProcesoExistente()
		)
		estado = ('Negocios con tipo de documento NULL', 'Negocios duplicados', 'Cuotas duplicadas', 'Cuotas sin Negocio', 'Numero de Negocio NULL', 'Movimientos sin cuotas Extrafin', 'Movimientos sin cuotas', 'Negocios Sin Cuentas', 'Clientes duplicados en TC', 'Existen Registros')
		return (consultas, estado)

	def detalle_valdiario(entorno, dblink):
		consultas = (
			Respaldo.detalle_negocios_null(entorno, dblink),
			Respaldo.detalle_negocios_duplicados(entorno, dblink),
			Respaldo.detalle_cuotas_cuplicadas(entorno, dblink),
			Respaldo.detalle_cuotas_snegocio(entorno, dblink),
			Respaldo.detalle_negociosNull(entorno, dblink),
			Respaldo.detalle_mov_sincuotasV006(entorno, dblink),
			Respaldo.detalle_mov_sincuotasV016(entorno, dblink),
			Respaldo.detalle_NegocioSinCuenta(),
			[
				Respaldo.detalle_clienteDuplicado_tc(),
				Respaldo.detalle_clienteFipCuentas(),
				Respaldo.detalle_clienteDiarioNegocios(),
				Respaldo.detalle_clienteFipExtraIc(),
				Respaldo.detalle_clienteFipNegocios(),
				Respaldo.detalle_clienteFipCuentaCredito()
				# Respaldo.remesas_cantidad(entorno, dblink),
				# Respaldo.remesas_cantidad(entorno, dblink)
			]
		)
		estado = ('NEG_NULL', 'NEG_DUPLICADOS', 'CUO_DUPLICADAS', 'CUO_SNEGOCIO', 'NRO_NEGNULL', 'MOVEXTRA_SCUOTA', 'MOV_SCUOTA', 'NEG_SIN_CUENTA', 'CLIENTE_DUP_TC')
		return (consultas, estado)

	def consulta_neg_remesas(entorno, dblink):
		consultas = (
			Respaldo.consultarNegocios(entorno, dblink),
			# Respaldo.validarNroNegociosNull(entorno, dblink),
			Respaldo.consultarRemesa(entorno, dblink)
			)
		estado = ('Negocios', 'Remesas')
		return (consultas, estado)

	def cuadratura_remesas():
		consultas = (
			Respaldo.diferencias_remesas(),
			# Respaldo.test_duplicados(),
			Respaldo.asientos_contables_duplicados(),
			Respaldo.diferencias_trx2001(),
			Respaldo.diferencias_trx2003(),
			)
		estado = ('Diferencia de Remesas', 'Asientos Contables Duplicados', 'Diferencias TRX 2001', 'Diferencias TRX 2003')
		return (consultas, estado)

# x, y = RespaldoRev.cuadratura_remesas()
# print(len(x))