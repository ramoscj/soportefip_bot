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

	def consultarNegocios(entorno, dblink):
		consulta = "select count(1) from %s.fip_diario_negocios%s where codigo_patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999" % (entorno, dblink)
		return consulta

	def consultarCuotasNegocios(entorno, dblink):
		consulta = "select count(1) from %s.fip_diario_cuotanegocios%s where codigo_patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999" % (entorno, dblink)
		return consulta

	def consultarMovExtra(entorno, dblink):
		consulta = "select count(1) from %s.fip_diario_movnegocios%s where codigo_patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') and tipo_movimiento = '006'" % (entorno, dblink)
		return consulta

	def consultarMovFinancieros(entorno, dblink):
		consulta = "select count(1) from %s.fip_diario_movnegocios%s where codigo_patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and tipo_movimiento <> '006'" % (entorno, dblink)
		return consulta

	def consultarRemesa(entorno, dblink):
		consulta = "select count(1) from %s.fip_diarioremesa%s where patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999" % (entorno, dblink)
		return consulta

	def consultarDetalleRemesa(entorno, dblink):
		consulta = "select count(1) from %s.fip_diariodet_remesa%s where patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999" % (entorno, dblink)
		return consulta

	# CONSULTAS PARA VALIDAR ERRORES *********************************

	def validarNroNegociosNull(entorno, dblink):
		consulta = "select count(1) from %s.fip_diario_negocios%s where codigo_patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and cod_extrafin is null" % (entorno, dblink)
		return consulta

	def validarNegociosDocNull(entorno, dblink):
		consulta = "select count(1) from %s.fip_diario_negocios%s where fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and codigo_patrimonio = :pat_consulta and tipo_documento is null" % (entorno, dblink)
		return consulta

	def validarCuotasDuplicadas(entorno, dblink):
		consulta = "select count(1) from %s.fip_diario_cuotanegocios%s  frc where (FRC.num_cta_credito, FRC.cod_cliente, FRC.cod_extrafin, FRC.fecha_corte, frc.rowid) IN (SELECT fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, MIN(fn.rowid) FROM %s.fip_diario_cuotanegocios%s FN WHERE FN.FECHA_CORTE = to_date(:fecha_consulta, 'ddmmyyyy') AND FN.CODIGO_PATRIMONIO = :pat_consulta having count(1) > 1 group by fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, nvl(fn.num_cuota, 0)) and frc.CODIGO_PATRIMONIO = :pat_consulta AND FRC.FECHA_CORTE = to_date(:fecha_consulta, 'ddmmyyyy')" % (entorno, dblink, entorno, dblink)
		return consulta

	def validarNogociosDuplicados(entorno, dblink):
		consulta = "select count(1) from %s.fip_diario_negocios%s frc where (frc.num_cta_credito, frc.cod_cliente, frc.cod_extrafin, frc.fecha_corte, frc.rowid) in ( select fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, min(fn.rowid) from %s.fip_diario_negocios%s fn where fn.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and fn.codigo_patrimonio = :pat_consulta having count(1) > 1 group by fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte ) and frc.codigo_patrimonio = :pat_consulta and frc.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999" % (entorno, dblink, entorno, dblink)
		return consulta

	def validarCuotasSinNegocio(entorno, dblink):
		consulta = "select count(1) from %s.fip_diario_cuotanegocios%s fdc where fdc.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') and fdc.codigo_patrimonio = :pat_consulta and not exists (select 1 from %s.fip_diario_negocios%s fdn where fdn.num_cta_credito = fdc.num_cta_credito and fdn.cod_cliente = fdc.cod_cliente and fdn.cod_extrafin = fdc.cod_extrafin and fdn.cod_empresa = fdc.cod_empresa and fdn.fecha_corte = fdc.fecha_corte and fdn.codigo_patrimonio = fdc.codigo_patrimonio)" % (entorno, dblink, entorno, dblink)
		return consulta

	def validarMovSinCuotaExtra(entorno, dblink):
		consulta = "select count(1) from %s.fip_diario_movnegocios%s sn where sn.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and sn.codigo_patrimonio = :pat_consulta and sn.tipo_movimiento = '006'and not exists (select 1 from fip_cuenta_credito_ic cc where cc.cta_num_cta_credito = sn.num_cta_credito and cc.cta_cod_cliente = sn.cod_cliente and cc.cta_cod_empresa = sn.cod_empresa ) and sn.cod_cliente not in (select b.cod_cliente from tc_cambioprod_enc a, tc_cuenta_credito b where trunc(a.fec_estado) <= trunc(SN.FECHA_CORTE) and a.ind_estado = 'F' and b.num_cta_credito = a.num_cta_credito and b.cod_empresa = a.cod_empresa and exists (select 1 from fip.fip_patrimonios fp, fip.fip_cartera_clasificada fn where fp.empresa = a.cod_empresa and fp.estado_patrimonio = 'A'and fn.codigo_patrimonio = fp.codigo_patrimonio and fn.codigo_cliente = b.cod_cliente and fp.codigo_patrimonio_ic = sn.codigo_patrimonio) group by a.num_cta_ic, b.cod_cliente, b.cod_empresa, b.fec_inclusion)" % (entorno, dblink)
		return consulta

	def validarMovSinCuota(entorno, dblink):
		consulta = "select count(1) from %s.fip_diario_movnegocios%s sn where sn.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and sn.codigo_patrimonio = :pat_consulta and sn.tipo_movimiento <> '006' and not exists (select 1 from fip_cuenta_credito_ic cc where cc.cta_num_cta_credito = sn.num_cta_credito and cc.cta_cod_cliente = sn.cod_cliente and cc.cta_cod_empresa = sn.cod_empresa ) and sn.cod_cliente not in (select b.cod_cliente from tc_cambioprod_enc a, tc_cuenta_credito b where trunc(a.fec_estado) <= trunc(SN.FECHA_CORTE) and a.ind_estado = 'F' and b.num_cta_credito = a.num_cta_credito and b.cod_empresa = a.cod_empresa and exists (select 1 from fip.fip_patrimonios fp, fip.fip_cartera_clasificada fn where fp.empresa = a.cod_empresa and fp.estado_patrimonio = 'A' and fn.codigo_patrimonio = fp.codigo_patrimonio and fn.codigo_cliente = b.cod_cliente and fp.codigo_patrimonio_ic = sn.codigo_patrimonio) group by a.num_cta_ic, b.cod_cliente, b.cod_empresa, b.fec_inclusion)" % (entorno, dblink)
		return consulta

	def validarClienteDuplicadoTc():
		consulta = "select count(1) from fip.fip_cartera_clasificada fcc where fcc.codigo_cliente in (select b.cod_cliente from tc_cambioprod_enc a, tc_cuenta_credito b where a.fec_estado between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and a.ind_estado = 'F' and b.num_cta_credito = a.num_cta_credito and b.cod_empresa = a.cod_empresa and exists (select 1 from fip.fip_patrimonios fp, fip.fip_cartera_clasificada fn where fp.empresa = a.cod_empresa and fp.estado_patrimonio = 'A' and fn.codigo_patrimonio = fp.codigo_patrimonio and fn.codigo_cliente = b.cod_cliente and fp.codigo_patrimonio_ic = :pat_consulta) group by a.num_cta_ic, b.cod_cliente, b.cod_empresa, b.fec_inclusion) and fcc.codigo_patrimonio not in ('1', :pat_consultatc, :pat_consulta) and length(fcc.codigo_patrimonio) = 1"
		return consulta

	# def consultar_clienteDuplicado_tc():
	# 	consulta = "select count(1) from fip.fip_cartera_clasificada fcc where fcc.codigo_cliente in (select b.cod_cliente from tc_cambioprod_enc a, tc_cuenta_credito b where a.fec_estado between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and a.ind_estado = 'F' and b.num_cta_credito = a.num_cta_credito and b.cod_empresa = a.cod_empresa and exists (select 1 from fip.fip_patrimonios fp, fip.fip_cartera_clasificada fn where fp.empresa = a.cod_empresa and fp.estado_patrimonio = 'A' and fn.codigo_patrimonio = fp.codigo_patrimonio and fn.codigo_cliente = b.cod_cliente and fp.codigo_patrimonio_ic = :pat_consulta) group by a.num_cta_ic, b.cod_cliente, b.cod_empresa, b.fec_inclusion) and fcc.codigo_patrimonio not in ('1', :pat_consultatc, :pat_consulta) and length(fcc.codigo_patrimonio) = 1"
	# 	return consulta

	def validarCuentasMigradasDuplicadas():

		consulta = "SELECT count(1) from fip.fip_cuenta_credito_ic fcci, (select a.num_cta_ic, b.cod_cliente, b.cod_empresa, b.fec_inclusion from tc.tc_cambioprod_enc a, tc.tc_cuenta_credito b where a.fec_estado between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') + .99999 and a.ind_estado = 'F'and b.num_cta_credito = a.num_cta_credito and b.cod_empresa = a.cod_empresa and exists (select 1 from fip.fip_patrimonios fp, fip.fip_cartera_clasificada fn where fp.empresa = a.cod_empresa and fp.estado_patrimonio = 'A' and fn.codigo_patrimonio = fp.codigo_patrimonio and fn.codigo_cliente = b.cod_cliente and fp.codigo_patrimonio_ic = :pat_consulta) group by a.num_cta_ic, b.cod_cliente, b.cod_empresa, b.fec_inclusion) cuentasTC WHERE fcci.cta_num_cta_credito = cuentasTC.num_cta_ic AND fcci.cta_cod_cliente = cuentasTC.cod_cliente"
		return consulta

	def validarProcesoExistente():
		consulta = "SELECT COUNT(1) FROM fip.fip_extra_ic WHERE EXT_CODIGO_PATRIMONIO = :pat_consulta AND EXT_FECHA_CORTE BETWEEN to_date(:fecha_consulta, 'ddmmyyyy') AND to_date(:fecha_consulta, 'ddmmyyyy') + .99999 AND EXT_TIPO_PROCESO = 'CN'"
		return consulta

	# CONSULTAS OBTENER REGISTROS CON ERRORES *********************************

	def detalle_negocios_null(entorno, dblink):
		consulta = "select sn.codigo_patrimonio, sn.num_cta_credito, sn.cod_cliente, sn.cod_extrafin, sn.fecha_corte, nvl(sn.tipo_documento, 'NULL') as tipo_documento from %s.fip_diario_negocios%s sn where sn.codigo_patrimonio = :pat_consulta and sn.fecha_corte = to_date(:fecha_consulta, 'ddmmyyyy') and sn.tipo_documento is null" % (entorno, dblink)
		return consulta

	def detalle_negocios_duplicados(entorno, dblink):
		consulta = "select frc.codigo_patrimonio, frc.num_cta_credito, frc.cod_cliente, frc.cod_extrafin, frc.fecha_corte, nvl(frc.tipo_documento, 'NULL') as tipo_documento from %s.fip_diario_negocios%s frc where (frc.num_cta_credito, frc.cod_cliente, frc.cod_extrafin, frc.fecha_corte, frc.rowid) in ( select fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, min(fn.rowid) from %s.fip_diario_negocios%s fn where fn.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and fn.codigo_patrimonio = :pat_consulta having count(1) > 1 group by fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte ) and frc.codigo_patrimonio = :pat_consulta and frc.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999" % (entorno, dblink, entorno, dblink)
		return consulta

	def detalle_cuotas_cuplicadas(entorno, dblink):
		consulta = "select frc.CODIGO_PATRIMONIO, FRC.num_cta_credito, FRC.cod_cliente, FRC.cod_extrafin, FRC.fecha_corte, nvl(FRC.num_cuota, 0) as num_cuota from %s.fip_diario_cuotanegocios%s frc where (FRC.num_cta_credito, FRC.cod_cliente, FRC.cod_extrafin, FRC.fecha_corte, frc.rowid) IN (SELECT fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, MIN(fn.rowid) FROM %s.fip_diario_cuotanegocios%s FN WHERE FN.FECHA_CORTE = to_date(:fecha_consulta, 'ddmmyyyy') AND FN.CODIGO_PATRIMONIO = :pat_consulta having count(1) > 1 group by fn.num_cta_credito, fn.cod_cliente, fn.cod_extrafin, fn.fecha_corte, nvl(fn.num_cuota, 0)) and frc.CODIGO_PATRIMONIO = :pat_consulta AND FRC.FECHA_CORTE = to_date(:fecha_consulta, 'ddmmyyyy')" % (entorno, dblink, entorno, dblink)
		return consulta

	def detalle_cuotas_snegocio(entorno, dblink):
		consulta = "select  fdc.codigo_patrimonio, fdc.num_cta_credito, fdc.cod_cliente, fdc.cod_extrafin, fdc.fecha_corte, nvl(fdc.num_cuota, 0) from %s.fip_diario_cuotanegocios%s fdc where fdc.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') and fdc.codigo_patrimonio = :pat_consulta and not exists (select 1 from %s.fip_diario_negocios%s fdn where fdn.num_cta_credito = fdc.num_cta_credito and fdn.cod_cliente = fdc.cod_cliente and fdn.cod_extrafin = fdc.cod_extrafin and fdn.cod_empresa = fdc.cod_empresa and fdn.fecha_corte = fdc.fecha_corte and fdn.codigo_patrimonio = fdc.codigo_patrimonio)" % (entorno, dblink, entorno, dblink)
		return consulta

	def detalle_negociosNull(entorno, dblink):
		consulta = "select codigo_patrimonio, num_cta_credito, cod_cliente, cod_extrafin, fecha_corte, nvl(tipo_documento, 'NULL') as tipo_documento from %s.fip_diario_negocios%s where codigo_patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and cod_extrafin is null" % (entorno, dblink)
		return consulta

	def detalle_mov_sincuotasV006(entorno, dblink):
		consulta = "select sn.CODIGO_PATRIMONIO, sn.num_cta_credito, sn.cod_cliente, nvl(sn.cod_extrafin,0) as cod_extrafin, sn.fecha_corte, sn.tipo_movimiento from %s.fip_diario_movnegocios%s sn where sn.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and sn.codigo_patrimonio = :pat_consulta and sn.tipo_movimiento = '006'and not exists (select 1 from fip_cuenta_credito_ic cc where cc.cta_num_cta_credito = sn.num_cta_credito and cc.cta_cod_cliente = sn.cod_cliente and cc.cta_cod_empresa = sn.cod_empresa ) and sn.cod_cliente not in (select b.cod_cliente from tc_cambioprod_enc a, tc_cuenta_credito b where trunc(a.fec_estado) <= trunc(SN.FECHA_CORTE) and a.ind_estado = 'F' and b.num_cta_credito = a.num_cta_credito and b.cod_empresa = a.cod_empresa and exists (select 1 from fip.fip_patrimonios fp, fip.fip_cartera_clasificada fn where fp.empresa = a.cod_empresa and fp.estado_patrimonio = 'A'and fn.codigo_patrimonio = fp.codigo_patrimonio and fn.codigo_cliente = b.cod_cliente and fp.codigo_patrimonio_ic = sn.codigo_patrimonio) group by a.num_cta_ic, b.cod_cliente, b.cod_empresa, b.fec_inclusion)" % (entorno, dblink)
		return consulta

	def detalle_mov_sincuotasV016(entorno, dblink):
		consulta = "select sn.CODIGO_PATRIMONIO, sn.num_cta_credito, sn.cod_cliente, nvl(sn.cod_extrafin,0) as cod_extrafin, sn.fecha_corte, sn.tipo_movimiento from %s.fip_diario_movnegocios%s sn where sn.fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and sn.codigo_patrimonio = :pat_consulta and sn.tipo_movimiento <> '006'and not exists (select 1 from fip_cuenta_credito_ic cc where cc.cta_num_cta_credito = sn.num_cta_credito and cc.cta_cod_cliente = sn.cod_cliente and cc.cta_cod_empresa = sn.cod_empresa ) and sn.cod_cliente not in (select b.cod_cliente from tc_cambioprod_enc a, tc_cuenta_credito b where trunc(a.fec_estado) <= trunc(SN.FECHA_CORTE) and a.ind_estado = 'F' and b.num_cta_credito = a.num_cta_credito and b.cod_empresa = a.cod_empresa and exists (select 1 from fip.fip_patrimonios fp, fip.fip_cartera_clasificada fn where fp.empresa = a.cod_empresa and fp.estado_patrimonio = 'A' and fn.codigo_patrimonio = fp.codigo_patrimonio and fn.codigo_cliente = b.cod_cliente and fp.codigo_patrimonio_ic = sn.codigo_patrimonio) group by a.num_cta_ic, b.cod_cliente, b.cod_empresa, b.fec_inclusion)" % (entorno, dblink)
		return consulta

	#  CLIENTES DUPLICADOS *********************************

	def detalle_clienteDuplicado_tc():
		consulta = "select * from fip.fip_cartera_clasificada fcc where fcc.codigo_cliente in (select b.cod_cliente from tc_cambioprod_enc a, tc_cuenta_credito b where a.fec_estado between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and a.ind_estado = 'F' and b.num_cta_credito = a.num_cta_credito and b.cod_empresa = a.cod_empresa and exists (select 1 from fip.fip_patrimonios fp, fip.fip_cartera_clasificada fn where fp.empresa = a.cod_empresa and fp.estado_patrimonio = 'A' and fn.codigo_patrimonio = fp.codigo_patrimonio and fn.codigo_cliente = b.cod_cliente and fp.codigo_patrimonio_ic = :pat_consulta) group by a.num_cta_ic, b.cod_cliente, b.cod_empresa, b.fec_inclusion) and fcc.codigo_patrimonio not in ('1', :pat_consultatc, :pat_consulta) and length(fcc.codigo_patrimonio) = 1"
		return consulta

	def detalle_clienteFipCuentas():
		# consulta = "select * from fip.fip_cuentas fcc where fcc.codigo_cliente in (select b.cod_cliente from tc.tc_cambioprod_enc a, tc.tc_cuenta_credito b where a.fec_estado between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') + .99999 and a.ind_estado = 'F' and b.num_cta_credito = a.num_cta_credito and b.cod_empresa = a.cod_empresa and exists (select 1 from fip.fip_patrimonios fp, fip.fip_cartera_clasificada fn where fp.empresa = a.cod_empresa and fp.estado_patrimonio = 'A' and fn.codigo_patrimonio = fp.codigo_patrimonio and fn.codigo_cliente = b.cod_cliente and fp.codigo_patrimonio_ic = :pat_consulta) group by a.num_cta_ic, b.cod_cliente, b.cod_empresa, b.fec_inclusion) and fcc.codigo_patrimonio not in ('1', :pat_consultatc, :pat_consulta) order by fcc.codigo_cliente"
		consulta = "SELECT * FROM fip.fip_cuentas fcc WHERE fcc.codigo_cliente IN (SELECT fcc.codigo_cliente FROM fip.fip_cartera_clasificada fcc WHERE fcc.codigo_cliente IN (SELECT b.cod_cliente FROM tc_cambioprod_enc a, tc_cuenta_credito b WHERE a.fec_estado BETWEEN TO_DATE(:fecha_consulta, 'ddmmyyyy') AND TO_DATE(:fecha_consulta, 'ddmmyyyy') +.99999 AND a.ind_estado = 'F'AND b.num_cta_credito = a.num_cta_credito AND b.cod_empresa = a.cod_empresa AND EXISTS (SELECT 1 FROM fip.fip_patrimonios fp, fip.fip_cartera_clasificada fn WHERE fp.empresa = a.cod_empresa AND fp.estado_patrimonio = 'A'AND fn.codigo_patrimonio = fp.codigo_patrimonio AND fn.codigo_cliente = b.cod_cliente AND fp.codigo_patrimonio_ic = :pat_consulta ) GROUP BY a.num_cta_ic, b.cod_cliente, b.cod_empresa, b.fec_inclusion ) AND fcc.codigo_patrimonio NOT IN ('1', :pat_consultatc, :pat_consulta ) AND length(fcc.codigo_patrimonio) = 1 ) ORDER BY fcc.codigo_cliente"
		return consulta

	def detalle_clienteDiarioNegocios():
		consulta = "select frc.codigo_patrimonio, frc.num_cta_credito, frc.cod_cliente, frc.cod_extrafin, frc.fecha_corte, nvl(frc.tipo_documento, 'NULL') as tipo_documento from reports.fip_diario_negocios@kamet.din.cl frc where (frc.num_cta_credito) in (select en.num_cta_ic from tc_cambioprod_enc en where en.num_cta_credito in (SELECT fcc.numero_cuenta FROM fip.fip_cuentas fcc WHERE fcc.codigo_cliente IN (SELECT fcc.codigo_cliente FROM fip.fip_cartera_clasificada fcc WHERE fcc.codigo_cliente IN (SELECT b.cod_cliente FROM tc_cambioprod_enc a, tc_cuenta_credito b WHERE a.fec_estado BETWEEN TO_DATE(:fecha_consulta, 'ddmmyyyy') AND TO_DATE(:fecha_consulta, 'ddmmyyyy') + .99999 AND a.ind_estado = 'F'AND b.num_cta_credito = a.num_cta_credito AND b.cod_empresa = a.cod_empresa AND EXISTS (SELECT 1 FROM fip.fip_patrimonios fp, fip.fip_cartera_clasificada fn WHERE fp.empresa = a.cod_empresa AND fp.estado_patrimonio = 'A'AND fn.codigo_patrimonio = fp.codigo_patrimonio AND fn.codigo_cliente = b.cod_cliente AND fp.codigo_patrimonio_ic = :pat_consulta) GROUP BY a.num_cta_ic, b.cod_cliente, b.cod_empresa, b.fec_inclusion) AND fcc.codigo_patrimonio NOT IN ('1', :pat_consultatc, :pat_consulta) AND length(fcc.codigo_patrimonio) = 1 ))) order by frc.num_cta_credito"
		return consulta

	def detalle_clienteFipExtraIc():
		consulta = "select fei.ext_codigo_patrimonio, fei.cta_num_cta_credito, fei.cta_cod_cliente, fei.ext_codigo_extrafinanciamiento, fei.ext_fecha_corte, fei.ext_tipo_proceso from fip.fip_extra_ic fei where (fei.cta_num_cta_credito) in (select en.num_cta_ic from tc_cambioprod_enc en where en.num_cta_credito in (SELECT fcc.numero_cuenta FROM fip.fip_cuentas fcc WHERE fcc.codigo_cliente IN (SELECT fcc.codigo_cliente FROM fip.fip_cartera_clasificada fcc WHERE fcc.codigo_cliente IN (SELECT b.cod_cliente FROM tc_cambioprod_enc a, tc_cuenta_credito b WHERE a.fec_estado BETWEEN TO_DATE(:fecha_consulta, 'ddmmyyyy') AND TO_DATE(:fecha_consulta, 'ddmmyyyy') + .99999 AND a.ind_estado = 'F'AND b.num_cta_credito = a.num_cta_credito AND b.cod_empresa = a.cod_empresa AND EXISTS (SELECT 1 FROM fip.fip_patrimonios fp, fip.fip_cartera_clasificada fn WHERE fp.empresa = a.cod_empresa AND fp.estado_patrimonio = 'A'AND fn.codigo_patrimonio = fp.codigo_patrimonio AND fn.codigo_cliente = b.cod_cliente AND fp.codigo_patrimonio_ic = :pat_consulta) GROUP BY a.num_cta_ic, b.cod_cliente, b.cod_empresa, b.fec_inclusion) AND fcc.codigo_patrimonio NOT IN ('1', :pat_consultatc, :pat_consulta) AND length(fcc.codigo_patrimonio) = 1 ))) order by fei.cta_num_cta_credito"
		return consulta

	def detalle_clienteFipNegocios():
		consulta = "select fn.codigo_patrimonio, fn.numero_cuenta, fn.codigo_cliente, fn.numero_negocio, fn.fecha_informado, fn.ind_est_vendido from fip_negocios fn where (fn.numero_cuenta) in (select en.num_cta_ic from tc_cambioprod_enc en where en.num_cta_credito in (SELECT fcc.numero_cuenta FROM fip.fip_cuentas fcc WHERE fcc.codigo_cliente IN (SELECT fcc.codigo_cliente FROM fip.fip_cartera_clasificada fcc WHERE fcc.codigo_cliente IN (SELECT b.cod_cliente FROM tc_cambioprod_enc a, tc_cuenta_credito b WHERE a.fec_estado BETWEEN TO_DATE(:fecha_consulta, 'ddmmyyyy') AND TO_DATE(:fecha_consulta, 'ddmmyyyy') + .99999 AND a.ind_estado = 'F' AND b.num_cta_credito = a.num_cta_credito AND b.cod_empresa = a.cod_empresa AND EXISTS (SELECT 1 FROM fip.fip_patrimonios fp, fip.fip_cartera_clasificada fn WHERE fp.empresa = a.cod_empresa AND fp.estado_patrimonio = 'A'AND fn.codigo_patrimonio = fp.codigo_patrimonio AND fn.codigo_cliente = b.cod_cliente AND fp.codigo_patrimonio_ic = :pat_consulta) GROUP BY a.num_cta_ic, b.cod_cliente, b.cod_empresa, b.fec_inclusion) AND fcc.codigo_patrimonio NOT IN ('1', :pat_consultatc, :pat_consulta) AND length(fcc.codigo_patrimonio) = 1 ) )) order by fn.numero_cuenta"
		return consulta

	def detalle_clienteFipCuentaCredito():
		consulta = "select fcc.cta_num_cta_credito, fcc.cta_cod_cliente, fcc.cta_fecha_corte, fcc.cta_tipo_proceso, fcc.cta_fecha_actualizacion from fip.fip_cuenta_credito_ic fcc where (fcc.cta_num_cta_credito) in (select en.num_cta_ic from tc_cambioprod_enc en where en.num_cta_credito in (SELECT fcc.numero_cuenta FROM fip.fip_cuentas fcc WHERE fcc.codigo_cliente IN (SELECT fcc.codigo_cliente FROM fip.fip_cartera_clasificada fcc WHERE fcc.codigo_cliente IN (SELECT b.cod_cliente FROM tc_cambioprod_enc a, tc_cuenta_credito b WHERE a.fec_estado BETWEEN TO_DATE(:fecha_consulta, 'ddmmyyyy') AND TO_DATE(:fecha_consulta, 'ddmmyyyy') + .99999 AND a.ind_estado = 'F'AND b.num_cta_credito = a.num_cta_credito AND b.cod_empresa = a.cod_empresa AND EXISTS (SELECT 1 FROM fip.fip_patrimonios fp, fip.fip_cartera_clasificada fn WHERE fp.empresa = a.cod_empresa AND fp.estado_patrimonio = 'A'AND fn.codigo_patrimonio = fp.codigo_patrimonio AND fn.codigo_cliente = b.cod_cliente AND fp.codigo_patrimonio_ic = :pat_consulta) GROUP BY a.num_cta_ic, b.cod_cliente, b.cod_empresa, b.fec_inclusion) AND fcc.codigo_patrimonio NOT IN ('1', :pat_consultatc, :pat_consulta) AND length(fcc.codigo_patrimonio) = 1) )) order by fcc.cta_cod_cliente"
		return consulta

	# CONSULTAS PARA PRUEBAS

	def remesas_cantidad(entorno, dblink):
		consulta = "select nro_remesa, patrimonio, tipo_movimiento, num_cta_credito, cod_cliente, org_code from %s.fip_diariodet_remesa%s where patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999 and ROWNUM <= 20" % (entorno, dblink)
		return consulta

	def count_remesas(entorno, dblink):
		consulta = "select count(1) from %s.fip_diariodet_remesa%s where patrimonio = :pat_consulta and fecha_corte between to_date(:fecha_consulta, 'ddmmyyyy') and to_date(:fecha_consulta, 'ddmmyyyy') +.99999" % (entorno, dblink)
		return consulta

	def diferencias_remesas():
		consulta = "SELECT remesa.rem_patrimonio remesa_patrimonio, remesa.rem_nro_remesa numero_remesa, nvl(remesa.red_fecha_corte, movimientos.fecha_movimiento) remesa_fecha_corte, remesa.red_tipo_movimiento remesa_tipo_movimiento, remesa.red_cta_credito_remesa remesa_cuenta ,remesa.monto_rem remesa_monto ,nvl(movimientos.monto_mov, 0) mov_monto, movimientos.numero_cuenta mov_cuenta, movimientos.tipo_movimiento mov_tipo_movimiento, nvl(movimientos.fecha_movimiento, remesa.red_fecha_corte) mov_fecha_movimiento, nvl(remesa.monto_rem, 0) + nvl(movimientos.monto_mov, 0) diferencia FROM (SELECT re.rem_patrimonio ,re.red_cta_credito_remesa ,re.rem_nro_remesa ,re.red_fecha_corte ,re.red_tipo_movimiento ,SUM(re.red_monto_movimiento) monto_rem FROM fip.fip_detalle_remesa_ic re WHERE re.rem_patrimonio = :pat_consulta AND re.red_fecha_corte BETWEEN to_date(:fecha_inicio, 'ddmmyyyy') AND to_date(:fecha_fin, 'ddmmyyyy') +.99999 AND re.red_tipo_movimiento IN (4, 6, 16) GROUP BY re.rem_patrimonio ,re.red_cta_credito_remesa ,re.rem_nro_remesa ,re.red_fecha_corte ,re.red_tipo_movimiento) remesa FULL OUTER JOIN (SELECT mov.codigo_patrimonio ,mov.numero_cuenta ,mov.numero_remesa ,mov.fecha_movimiento ,mov.tipo_movimiento ,SUM(mov.monto) monto_mov FROM fip.fip_movimientos_diarios mov WHERE mov.codigo_patrimonio = :pat_consulta AND mov.fecha_movimiento BETWEEN to_date(:fecha_inicio, 'ddmmyyyy') AND to_date(:fecha_fin, 'ddmmyyyy') +.99999 AND mov.tipo_movimiento IN (4, 6, 16) AND mov.numero_remesa IS NOT NULL GROUP BY mov.codigo_patrimonio ,mov.numero_cuenta ,mov.numero_remesa ,mov.fecha_movimiento ,mov.tipo_movimiento) movimientos ON (remesa.rem_patrimonio = movimientos.codigo_patrimonio AND remesa.rem_nro_remesa = movimientos.numero_remesa AND remesa.red_fecha_corte = movimientos.fecha_movimiento AND remesa.red_tipo_movimiento = movimientos.tipo_movimiento AND remesa.red_cta_credito_remesa = movimientos.numero_cuenta) HAVING nvl(remesa.monto_rem, 0) + nvl(movimientos.monto_mov, 0) <> 0 group by remesa.rem_patrimonio, remesa.rem_nro_remesa, remesa.red_fecha_corte, remesa.red_tipo_movimiento, remesa.red_cta_credito_remesa, movimientos.numero_cuenta, remesa.monto_rem, movimientos.monto_mov, movimientos.tipo_movimiento, movimientos.fecha_movimiento order by remesa_fecha_corte, numero_remesa, mov_fecha_movimiento, movimientos.tipo_movimiento"
		return consulta


	def asientos_contables_duplicados():
		consulta = "select count(1) cantidad, fmdo.FECHA_MOVIMIENTO from fip.fip_movimientos_diarios fmdo where (fmdo.codigo_cliente, fmdo.numero_cuenta, nvl(fmdo.numero_negocio, 1), fmdo.numero_movimiento, fmdo.rowid) in (select fp2.codigo_cliente, fp2.numero_cuenta, nvl(fp2.numero_negocio, 1), fp2.numero_movimiento, min(rowid) idt from fip.fip_movimientos_diarios fp2 where fp2.CODIGO_PATRIMONIO = :pat_consulta and fp2.FECHA_MOVIMIENTO BETWEEN to_date(:fecha_inicio, 'ddmmyyyy') AND to_date(:fecha_fin, 'ddmmyyyy') +.99999 having count(1) > 1 group by fp2.codigo_cliente, fp2.numero_cuenta, fp2.numero_negocio, fp2.numero_movimiento ) group by fmdo.FECHA_MOVIMIENTO"
		return consulta

	def diferencias_trx2001():
		consulta = "SELECT mo.mon_movimiento - remesa.monto_rem diferencia FROM fip.fip_mov_financieros mo ,(SELECT SUM(re.red_monto_movimiento) monto_rem FROM fip.fip_detalle_remesa_ic re WHERE re.rem_patrimonio = :pat_consulta AND re.red_fecha_corte BETWEEN to_date(:fecha_inicio, 'ddmmyyyy') AND to_date(:fecha_inicio, 'ddmmyyyy') + .99999 AND re.red_tipo_movimiento IN (6) GROUP BY re.rem_patrimonio ,re.rem_nro_remesa ,re.red_fecha_corte ,re.red_tipo_movimiento) remesa WHERE mo.fec_movimiento BETWEEN to_date(:fecha_inicio, 'ddmmyyyy') AND to_date(:fecha_inicio, 'ddmmyyyy') + .99999 AND mo.codigo_patrimonio = :pat_consulta AND mo.tip_transaccion = 2 AND mo.tip_subtransac IN (2003)"
		return consulta

	def diferencias_trx2003():
		consulta = "SELECT mo.mon_movimiento - rem_mov.total diferencia FROM fip.fip_mov_financieros mo ,(SELECT remesa.monto_rem + nvl(movimientos.monto_mov, 0) total FROM (SELECT SUM(re.red_monto_movimiento) monto_rem FROM fip.fip_detalle_remesa_ic re WHERE re.rem_patrimonio = :pat_consulta AND re.red_fecha_corte BETWEEN to_date(:fecha_inicio, 'ddmmyyyy') AND to_date(:fecha_inicio, 'ddmmyyyy') + .99999 AND re.red_tipo_movimiento IN (4, 16)) remesa ,(SELECT SUM(-1 * mov.monto) monto_mov FROM fip.fip_movimientos_diarios mov WHERE mov.codigo_patrimonio = :pat_consulta AND mov.fecha_movimiento BETWEEN to_date(:fecha_inicio, 'ddmmyyyy') AND to_date(:fecha_inicio, 'ddmmyyyy') + .99999 AND mov.tipo_movimiento IN (14) AND mov.numero_remesa IS NOT NULL) movimientos) rem_mov WHERE mo.fec_movimiento BETWEEN to_date(:fecha_inicio, 'ddmmyyyy') AND to_date(:fecha_inicio, 'ddmmyyyy') + .99999 AND mo.codigo_patrimonio = :pat_consulta AND mo.tip_transaccion = 2 AND mo.tip_subtransac IN (2001)"
		return consulta

	def test_duplicados():
		consulta = "select count(1) cantidad, fmdo.FECHA_MOVIMIENTO from fip.fip_movimientos_diarios fmdo where fmdo.CODIGO_PATRIMONIO = :pat_consulta and fmdo.FECHA_MOVIMIENTO BETWEEN to_date(:fecha_inicio, 'ddmmyyyy') AND to_date(:fecha_fin, 'ddmmyyyy') +.99999 group by fmdo.FECHA_MOVIMIENTO"
		return consulta

# print(Respaldo.consultarNegocios('reports', '@kamet.din.cl'))