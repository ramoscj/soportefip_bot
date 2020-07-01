from consultas import Respaldo

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