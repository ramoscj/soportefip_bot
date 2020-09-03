from consultas import Reports

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
			# Reports.consultar_negocios_nulos()
			Reports.consultar_remesas(),
			Reports.consultar_remesas_detalle()
			)
		estado = ('Remesas', 'Detalle de Remesas')
		return (consultas, estado)

	def consulta_neg_remesas():
		consultas = (
			Reports.consultar_negocios(),
			# Reports.consultar_negocios_nulos(),
			# Reports.consultar_negocios_nulos()
			Reports.consultar_remesas()
			)
		estado = ('Negocios', 'Remesas')
		return (consultas, estado)
