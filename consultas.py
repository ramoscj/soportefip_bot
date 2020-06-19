class Reports(object):

	def consultar_negocios():
		consulta = "select count(1) from reports.fip_diario_negocios@kamet.din.cl where codigo_patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999"
		return consulta

	def consultar_negocios_cuotas():
		consulta = "select count(1) from reports.fip_diario_cuotanegocios@kamet.din.cl where codigo_patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999"
		return consulta

	def consultar_movimientos_int_extra():
		consulta = "select count(1) from reports.fip_diario_movnegocios@kamet.din.cl where codigo_patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') and tipo_movimiento = '006'"
		return consulta

	def consultar_movimientos_financieros():
		consulta = "select count(1) from reports.fip_diario_movnegocios@kamet.din.cl where codigo_patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and tipo_movimiento <> '006'"
		return consulta

	def consultar_remesas():
		consulta = "select count(1) from reports.fip_diarioremesa@kamet.din.cl where patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999"
		return consulta

	def consultar_remesas_detalle():
		consulta = "select count(1) from reports.fip_diariodet_remesa@kamet.din.cl where patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999"
		return consulta

	# CONSULTAS PARA VALIDAR ERRORES *********************************

	def consultar_negocios_nulos():
		consulta = "select count(1) from reports.fip_diario_negocios@kamet.din.cl where fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and codigo_patrimonio = :pat_consulta and tipo_documento is null"
		return consulta

	def consultar_cuotas_duplicadas():
		consulta = "select count(1) from reports.fip_diario_cuotanegocios@kamet.din.cl  frc where (FRC.num_cta_credito, FRC.cod_cliente, FRC.cod_extrafin, FRC.fecha_corte, frc.rowid) IN (SELECT fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, MIN(fn.rowid) FROM reports.fip_diario_cuotanegocios@kamet.din.cl FN WHERE FN.FECHA_CORTE = to_date(:fecha_consulta, 'ddmmyyyy') AND FN.CODIGO_PATRIMONIO = :pat_consulta having count(1) > 1 group by fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, nvl(fn.num_cuota, 0)) and frc.CODIGO_PATRIMONIO = :pat_consulta AND FRC.FECHA_CORTE = to_date(:fecha_consulta, 'ddmmyyyy')"
		return consulta

	def consultar_negocios_duplicados():
		consulta = "select count(1) from reports.fip_diario_negocios@kamet.din.cl frc where (frc.num_cta_credito, frc.cod_cliente, frc.cod_extrafin, frc.fecha_corte, frc.rowid) in ( select fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, min(fn.rowid) from reports.fip_diario_negocios@kamet.din.cl fn where fn.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and fn.codigo_patrimonio = :pat_consulta having count(1) > 1 group by fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte ) and frc.codigo_patrimonio = :pat_consulta and frc.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999"
		return consulta

	def consultar_cuotas_snegocios():		
		consulta = "select count(1) from reports.fip_diario_cuotanegocios@kamet.din.cl fdc where fdc.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') and fdc.codigo_patrimonio = :pat_consulta and not exists (select 1 from reports.fip_diario_negocios@kamet.din.cl fdn where fdn.num_cta_credito = fdc.num_cta_credito and fdn.cod_cliente = fdc.cod_cliente and fdn.cod_extrafin = fdc.cod_extrafin and fdn.cod_empresa = fdc.cod_empresa and fdn.fecha_corte = fdc.fecha_corte and fdn.codigo_patrimonio = fdc.codigo_patrimonio)"
		return consulta

	def detalle_negocios_null():
		consulta = "select sn.codigo_patrimonio, sn.num_cta_credito, sn.cod_cliente, sn.cod_extrafin, sn.fecha_corte, nvl(sn.tipo_documento, 'NULL') from reports.fip_diario_negocios@kamet.din.cl sn where sn.codigo_patrimonio = :pat_consulta and sn.fecha_corte = to_date(:fecha_consulta, 'ddmmyyyy') and sn.tipo_documento is null"
		return consulta

	def detalle_negocios_duplicados():
		consulta = "select frc.codigo_patrimonio, frc.num_cta_credito, frc.cod_cliente, frc.cod_extrafin, frc.fecha_corte, frc.tipo_documento from reports.fip_diario_negocios@kamet.din.cl frc where (frc.num_cta_credito, frc.cod_cliente, frc.cod_extrafin, frc.fecha_corte, frc.rowid) in ( select fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, min(fn.rowid) from reports.fip_diario_negocios@kamet.din.cl fn where fn.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and fn.codigo_patrimonio = :pat_consulta having count(1) > 1 group by fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte ) and frc.codigo_patrimonio = :pat_consulta and frc.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999"
		return consulta

	def detalle_cuotas_cuplicadas():
		consulta = "select frc.CODIGO_PATRIMONIO, FRC.num_cta_credito, FRC.cod_cliente, FRC.cod_extrafin, FRC.fecha_corte, nvl(FRC.num_cuota, 0) from reports.fip_diario_cuotanegocios@kamet.din.cl frc where (FRC.num_cta_credito, FRC.cod_cliente, FRC.cod_extrafin, FRC.fecha_corte, frc.rowid) IN (SELECT fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, MIN(fn.rowid) FROM reports.fip_diario_cuotanegocios@kamet.din.cl FN WHERE FN.FECHA_CORTE = to_date(:fecha_consulta, 'ddmmyyyy') AND FN.CODIGO_PATRIMONIO = :pat_consulta having count(1) > 1 group by fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, nvl(fn.num_cuota, 0)) and frc.CODIGO_PATRIMONIO = :pat_consulta AND FRC.FECHA_CORTE = to_date(:fecha_consulta, 'ddmmyyyy')"
		return consulta

	def detalle_cuotas_snegocio():
		consulta = "select  fdc.codigo_patrimonio, fdc.num_cta_credito, fdc.cod_cliente, fdc.cod_extrafin, fdc.fecha_corte, nvl(fdc.num_cuota, 0) from reports.fip_diario_cuotanegocios@kamet.din.cl fdc where fdc.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') and fdc.codigo_patrimonio = :pat_consulta and not exists (select 1 from reports.fip_diario_negocios@kamet.din.cl fdn where fdn.num_cta_credito = fdc.num_cta_credito and fdn.cod_cliente = fdc.cod_cliente and fdn.cod_extrafin = fdc.cod_extrafin and fdn.cod_empresa = fdc.cod_empresa and fdn.fecha_corte = fdc.fecha_corte and fdn.codigo_patrimonio = fdc.codigo_patrimonio)"
		return consulta

	def consultar_remesas_cantidad():
		consulta = "select nro_remesa, patrimonio, tipo_movimiento, num_cta_credito, cod_cliente, org_code from reports.fip_diariodet_remesa@kamet.din.cl where patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and ROWNUM <= 20"
		return consulta
		
class Respaldo(object):

	def consultar_negocios():
		consulta = "select count(1) from fip.fip_diario_negocios where codigo_patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999"
		return consulta

	def consultar_negocios_cuotas():
		consulta = "select count(1) from fip.fip_diario_cuotanegocios where codigo_patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999"
		return consulta

	def consultar_movimientos_int_extra():
		consulta = "select count(1) from fip.fip_diario_movnegocios where codigo_patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') and tipo_movimiento = '006'"
		return consulta

	def consultar_movimientos_financieros():
		consulta = "select count(1) from fip.fip_diario_movnegocios where codigo_patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and tipo_movimiento <> '006'"
		return consulta

	def consultar_remesas():
		consulta = "select count(1) from fip.fip_diarioremesa where patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999"
		return consulta

	def consultar_remesas_detalle():
		consulta = "select count(1) from fip.fip_diariodet_remesa where patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999"
		return consulta

	# CONSULTAS PARA VALIDAR ERRORES *********************************

	def consultar_negocios_nulos():
		consulta = "select count(1) from fip.fip_diario_negocios where fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and codigo_patrimonio = :pat_consulta and tipo_documento is null"
		return consulta

	def consultar_cuotas_duplicadas():
		consulta = "select count(1) from fip.fip_diario_cuotanegocios  frc where (FRC.num_cta_credito, FRC.cod_cliente, FRC.cod_extrafin, FRC.fecha_corte, frc.rowid) IN (SELECT fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, MIN(fn.rowid) FROM fip.fip_diario_cuotanegocios FN WHERE FN.FECHA_CORTE = to_date(:fecha_consulta, 'ddmmyyyy') AND FN.CODIGO_PATRIMONIO = :pat_consulta having count(1) > 1 group by fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, nvl(fn.num_cuota, 0)) and frc.CODIGO_PATRIMONIO = :pat_consulta AND FRC.FECHA_CORTE = to_date(:fecha_consulta, 'ddmmyyyy')"
		return consulta

	def consultar_negocios_duplicados():
		consulta = "select count(1) from fip.fip_diario_negocios frc where (frc.num_cta_credito, frc.cod_cliente, frc.cod_extrafin, frc.fecha_corte, frc.rowid) in ( select fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, min(fn.rowid) from fip.fip_diario_negocios fn where fn.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and fn.codigo_patrimonio = :pat_consulta having count(1) > 1 group by fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte ) and frc.codigo_patrimonio = :pat_consulta and frc.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999"
		return consulta

	def consultar_cuotas_snegocios():		
		consulta = "select count(1) from fip.fip_diario_cuotanegocios fdc where fdc.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') and fdc.codigo_patrimonio = :pat_consulta and not exists (select 1 from fip.fip_diario_negocios fdn where fdn.num_cta_credito = fdc.num_cta_credito and fdn.cod_cliente = fdc.cod_cliente and fdn.cod_extrafin = fdc.cod_extrafin and fdn.cod_empresa = fdc.cod_empresa and fdn.fecha_corte = fdc.fecha_corte and fdn.codigo_patrimonio = fdc.codigo_patrimonio)"
		return consulta

	def detalle_negocios_null():
		consulta = "select sn.codigo_patrimonio, sn.num_cta_credito, sn.cod_cliente, sn.cod_extrafin, sn.fecha_corte, nvl(sn.tipo_documento, 'NULL') from fip.fip_diario_negocios sn where sn.codigo_patrimonio = :pat_consulta and sn.fecha_corte = to_date(:fecha_consulta, 'ddmmyyyy') and sn.tipo_documento is null"
		return consulta

	def detalle_negocios_duplicados():
		consulta = "select frc.codigo_patrimonio, frc.num_cta_credito, frc.cod_cliente, frc.cod_extrafin, frc.fecha_corte, frc.tipo_documento from fip.fip_diario_negocios frc where (frc.num_cta_credito, frc.cod_cliente, frc.cod_extrafin, frc.fecha_corte, frc.rowid) in ( select fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, min(fn.rowid) from fip.fip_diario_negocios fn where fn.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and fn.codigo_patrimonio = :pat_consulta having count(1) > 1 group by fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte ) and frc.codigo_patrimonio = :pat_consulta and frc.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999"
		return consulta

	def detalle_cuotas_cuplicadas():
		consulta = "select frc.CODIGO_PATRIMONIO, FRC.num_cta_credito, FRC.cod_cliente, FRC.cod_extrafin, FRC.fecha_corte, nvl(FRC.num_cuota, 0) from fip.fip_diario_cuotanegocios frc where (FRC.num_cta_credito, FRC.cod_cliente, FRC.cod_extrafin, FRC.fecha_corte, frc.rowid) IN (SELECT fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, MIN(fn.rowid) FROM fip.fip_diario_cuotanegocios FN WHERE FN.FECHA_CORTE = to_date(:fecha_consulta, 'ddmmyyyy') AND FN.CODIGO_PATRIMONIO = :pat_consulta having count(1) > 1 group by fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, nvl(fn.num_cuota, 0)) and frc.CODIGO_PATRIMONIO = :pat_consulta AND FRC.FECHA_CORTE = to_date(:fecha_consulta, 'ddmmyyyy')"
		return consulta

	def detalle_cuotas_snegocio():
		consulta = "select  fdc.codigo_patrimonio, fdc.num_cta_credito, fdc.cod_cliente, fdc.cod_extrafin, fdc.fecha_corte, nvl(fdc.num_cuota, 0) from fip.fip_diario_cuotanegocios fdc where fdc.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') and fdc.codigo_patrimonio = :pat_consulta and not exists (select 1 from fip.fip_diario_negocios fdn where fdn.num_cta_credito = fdc.num_cta_credito and fdn.cod_cliente = fdc.cod_cliente and fdn.cod_extrafin = fdc.cod_extrafin and fdn.cod_empresa = fdc.cod_empresa and fdn.fecha_corte = fdc.fecha_corte and fdn.codigo_patrimonio = fdc.codigo_patrimonio)"
		return consulta

	def consultar_remesas_cantidad():
		consulta = "select nro_remesa, patrimonio, tipo_movimiento, num_cta_credito, cod_cliente, org_code from fip.fip_diariodet_remesa where patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and ROWNUM <= 20"
		return consulta