from consultas import Reports, Respaldo
from acceso_db import conexion

class ReportsRev(object):

	def consulta_diario():
		consultas = (Reports.consultar_negocios(), 
			Reports.consultar_negocios_cuotas(), 
			Reports.consultar_movimientos_int_extra(),
			Reports.consultar_movimientos_financieros(),
			Reports.consultar_remesas(),
			Reports.consultar_remesas_detalle()
			# Reports.consultar_negocios_nulos(),
			# Reports.consultar_negocios_nulos()
			)
		estado = ('Negocios', 'Cuotas', 'Movimientos con Intereses', 'Movimientos Financieros', 'Remesas', 'Detalles de Remesas')
		return (consultas, estado)

	def validaciones_diario():
		consultas = (
			Reports.consultar_negocios_nulos(),
			Reports.consultar_negocios_duplicados(),
			Reports.consultar_cuotas_duplicadas(),
			Reports.consultar_cuotas_snegocios()
		)
		estado = ('Negocios con tipo de documento NULL', 'Negocios duplicados', 'Cuotas duplicadas', 'Cuotas sin Negocio')
		return (consultas, estado)

	def detalle_valdiario():
		consultas = (
			Reports.detalle_negocios_null(),
			Reports.detalle_negocios_duplicados(),
			Reports.detalle_cuotas_cuplicadas(),
			Reports.detalle_cuotas_snegocio()
			# Reports.consultar_remesas_cantidad(),
			# Reports.consultar_remesas_cantidad(),
			# Reports.consultar_remesas_cantidad(),
			# Reports.consultar_remesas_cantidad()
		)
		estado = ('NEG_NULL', 'NEG_DUPLICADOS', 'CUO_DUPLICADAS', 'CUO_SNEGOCIO	')
		return (consultas, estado)

	def consulta_remesas():
		consultas = (
			# Reports.consultar_negocios_nulos(),
			# Reports.consultar_negocios_nulos(),
			Reports.consultar_remesas(),
			Reports.consultar_remesas_detalle()
			)
		estado = ('Remesas', 'Detalle de Remesas')
		return (consultas, estado)

	def consulta_neg_remesas():
		consultas = (
			Reports.consultar_negocios(),
			Reports.consultar_negocios_nulos() 
			# Reports.consultar_remesas()
			)
		estado = ('Negocios', 'Remesas')
		return (consultas, estado)

class RespaldoRev(object):

	def consulta_diario():
		consultas = (Respaldo.consultar_negocios(), 
			Respaldo.consultar_negocios_cuotas(), 
			Respaldo.consultar_movimientos_int_extra(),
			Respaldo.consultar_movimientos_financieros(),
			Respaldo.consultar_remesas(),
			Respaldo.consultar_remesas_detalle()
			# Respaldo.consultar_negocios_nulos(),
			# Respaldo.consultar_negocios_nulos()
			)
		estado = ('Negocios', 'Cuotas', 'Movimientos con Intereses', 'Movimientos Financieros', 'Remesas', 'Detalles de Remesas')
		return (consultas, estado)

	def validaciones_diario():
		consultas = (
			Respaldo.consultar_negocios_nulos(),
			Respaldo.consultar_negocios_duplicados(),
			Respaldo.consultar_cuotas_duplicadas(),
			Respaldo.consultar_cuotas_snegocios()
		)
		estado = ('Negocios con tipo de documento NULL', 'Negocios duplicados', 'Cuotas duplicadas', 'Cuotas sin Negocio')
		return (consultas, estado)

	def detalle_valdiario():
		consultas = (
			Respaldo.detalle_negocios_null(),
			Respaldo.detalle_negocios_duplicados(),
			Respaldo.detalle_cuotas_cuplicadas(),
			Respaldo.detalle_cuotas_snegocio()
			# Respaldo.consultar_remesas_cantidad(),
			# Respaldo.consultar_remesas_cantidad(),
			# Respaldo.consultar_remesas_cantidad(),
			# Respaldo.consultar_remesas_cantidad()
		)
		estado = ('NEG_NULL', 'NEG_DUPLICADOS', 'CUO_DUPLICADAS', 'CUO_SNEGOCIO	')
		return (consultas, estado)