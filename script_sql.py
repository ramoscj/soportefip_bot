from config_bot import PATRIMONIOS_TC, PAT_BOT

class ScriptSQL(object):

    def crear(archivo:int, patrimonio: int, fecha_corte: str, cantidad: int):
        try:
            archivo_path = "%s/scripts/%s.sql" % (PAT_BOT['PATH'], str(archivo))
            lista_sql = (
                ScriptSQL.scriptNegociosNull(cantidad),
                ScriptSQL.scriptNegociosDuplicados(cantidad, patrimonio, fecha_corte),
                ScriptSQL.scriptCuotasDuplicadas(cantidad, patrimonio, fecha_corte),
                ScriptSQL.scriptCuotaSinNegocio(cantidad, patrimonio, fecha_corte),
                ScriptSQL.scriptCodigoNegNull(cantidad, patrimonio, fecha_corte),
                ScriptSQL.scriptMovExtraSinCuota(cantidad, patrimonio, fecha_corte),
                ScriptSQL.scriptMovSinCuota(cantidad, patrimonio, fecha_corte),
                ScriptSQL.scriptClienteDuplicadoTc(cantidad, patrimonio, fecha_corte)
                )
            texto = lista_sql[archivo]
            with open(archivo_path, "w") as archivo:
                archivo.writelines(texto)
            return True
        except Exception as e:
            return ("Error: el sql: %s no pudo crearse. %s" % (archivo, e))

    def scriptNegociosNull(cantidad):
        texto_sql = [
                    "-- "+ str(cantidad) + " NEGOCIOS TIPO DE DOCUMENTO NULL\n"
                    "--SELECT *\n"
                    "UPDATE FIP.FIP_DIARIO_NEGOCIOS SET\n"
                    "    COD_COMERCIO = '00000400',\n"
                    "    TIPO_DOCUMENTO = '001'\n"
                    "WHERE\n"
                    "    TIPO_DOCUMENTO IS NULL;\n"
                    "COMMIT;\n"
            ]
        return texto_sql
    
    def scriptNegociosDuplicados(cantidad, pat, fecha_corte):
        texto_sql = [
                    "-- "+ str(cantidad) + " NEGOCIOS DUPLICADOS\n"
                    "--SELECT *\n"
                    "DELETE\n"
                    "FROM FIP.FIP_DIARIO_NEGOCIOS FRC WHERE\n"
                    "    (FRC.NUM_CTA_CREDITO, FRC.COD_CLIENTE, FRC.COD_EXTRAFIN, FRC.FECHA_CORTE, FRC.ROWID) IN\n"
                    "    (\n"
                    "      SELECT FN.NUM_CTA_CREDITO, FN.COD_CLIENTE, FN.COD_EXTRAFIN, FN.FECHA_CORTE, MIN(FN.ROWID)\n"
                    "        FROM FIP.FIP_DIARIO_NEGOCIOS FN\n"
                    "       WHERE FN.FECHA_CORTE = TO_DATE('"+ fecha_corte + "', 'DDMMYYYY')\n"
                    "         AND FN.CODIGO_PATRIMONIO = "+ str(pat) + "\n"
                    "         HAVING COUNT(1) > 1\n"
                    "         GROUP BY FN.NUM_CTA_CREDITO, FN.COD_CLIENTE, FN.COD_EXTRAFIN, FN.FECHA_CORTE\n"
                    "    )\n"
                    "    AND FRC.CODIGO_PATRIMONIO = "+ str(pat) + "\n"
                    "    AND FRC.FECHA_CORTE = TO_DATE('"+ fecha_corte + "', 'DDMMYYYY');\n"
                    "COMMIT;\n"
            ]
        return texto_sql
    
    def scriptCuotasDuplicadas(cantidad, pat, fecha_corte):
        texto_sql = [
                    "-- "+ str(cantidad) + " CUOTAS DUPLICADAS\n"
                    "--SELECT *\n"
                    "DELETE\n"
                    "    FROM FIP.FIP_DIARIO_CUOTANEGOCIOS FRC\n"
                    "    WHERE ( FRC.NUM_CTA_CREDITO, FRC.COD_CLIENTE, FRC.COD_EXTRAFIN, FRC.FECHA_CORTE, FRC.ROWID ) IN \n"
                    "    ( SELECT FN.NUM_CTA_CREDITO, FN.COD_CLIENTE, FN.COD_EXTRAFIN, FN.FECHA_CORTE, MIN(FN.ROWID)\n"
                    "            FROM FIP.FIP_DIARIO_CUOTANEGOCIOS FN\n"
                    "            WHERE FN.FECHA_CORTE = TO_DATE('"+ fecha_corte + "', 'DDMMYYYY')\n"
                    "            AND FN.CODIGO_PATRIMONIO = "+ str(pat) + "\n"
                    "            HAVING COUNT(1) > 1\n"
                    "            GROUP BY FN.NUM_CTA_CREDITO, FN.COD_CLIENTE, FN.COD_EXTRAFIN, FN.FECHA_CORTE, NVL(FN.NUM_CUOTA, 0) )\n"
                    "    AND FRC.CODIGO_PATRIMONIO = "+ str(pat) + "\n"
                    "    AND FRC.FECHA_CORTE = TO_DATE('"+ fecha_corte + "', 'DDMMYYYY');\n"
                    "COMMIT;\n"
            ]
        return texto_sql

    def scriptCuotaSinNegocio(cantidad, pat, fecha_corte):
        texto_sql = [
                    "-- "+ str(cantidad) + " CUOTAS SIN NEGOCIO\n"
                    "--SELECT *\n"
                    "DELETE\n"
                    "    FROM FIP.FIP_DIARIO_CUOTANEGOCIOS FDC\n"
                    "    WHERE FDC.FECHA_CORTE = TO_DATE('"+ fecha_corte + "', 'ddmmyyyy')\n"
                    "     AND FDC.CODIGO_PATRIMONIO = "+ str(pat) + "\n"
                    "     AND NOT EXISTS (\n"
                    "        SELECT 1\n"
                    "            FROM FIP.FIP_DIARIO_NEGOCIOS FDN\n"
                    "            WHERE FDN.NUM_CTA_CREDITO = FDC.NUM_CTA_CREDITO\n"
                    "             AND FDN.COD_CLIENTE = FDC.COD_CLIENTE\n"
                    "             AND FDN.COD_EXTRAFIN = FDC.COD_EXTRAFIN\n"
                    "             AND FDN.COD_EMPRESA = FDC.COD_EMPRESA\n"
                    "             AND FDN.FECHA_CORTE = FDC.FECHA_CORTE\n"
                    "             AND FDN.CODIGO_PATRIMONIO = FDC.CODIGO_PATRIMONIO);\n"
                    "COMMIT;\n"
            ]
        return texto_sql
    
    def scriptCodigoNegNull(cantidad, pat, fecha_corte):
        texto_sql = [
                    "-- "+ str(cantidad) + " NUMERO DE NEGOCIO NULL\n"
                    "--SELECT *\n"
                    "DELETE\n"
                    "    FROM FIP.FIP_DIARIO_CUOTANEGOCIOS FDC\n"
                    "    WHERE\n"
                    "     (FDC.NUM_CTA_CREDITO, FDC.COD_CLIENTE, nvl(FDC.COD_EXTRAFIN,0), FDC.COD_EMPRESA, FDC.FECHA_CORTE, FDC.CODIGO_PATRIMONIO) in (\n"
                    "        SELECT FDN.NUM_CTA_CREDITO, FDN.COD_CLIENTE, nvl(FDN.COD_EXTRAFIN,0), FDN.COD_EMPRESA, FDN.FECHA_CORTE, FDN.CODIGO_PATRIMONIO\n"
                    "            FROM FIP.FIP_DIARIO_NEGOCIOS FDN\n"
                    "            WHERE FDN.FECHA_CORTE = TO_DATE('"+ fecha_corte + "', 'ddmmyyyy')\n"
                    "            AND FDN.CODIGO_PATRIMONIO = "+ str(pat) + "\n"
                    "            and FDN.cod_extrafin is null\n"
                    "     )\n"
                    "     and FDC.FECHA_CORTE = TO_DATE('"+ fecha_corte + "', 'ddmmyyyy')\n"
                    "     and FDC.CODIGO_PATRIMONIO = "+ str(pat) + ";\n"
                    "-- "+ str(cantidad) + " NUMERO DE NEGOCIO NULL\n"
                    "DELETE\n"
                    "FROM FIP.FIP_DIARIO_NEGOCIOS FN\n"
                    "       WHERE FN.FECHA_CORTE = TO_DATE('"+ fecha_corte + "', 'ddmmyyyy')\n"
                    "         AND FN.CODIGO_PATRIMONIO = "+ str(pat) + "\n"
                    "         and fn.cod_extrafin is null;\n"
                    "COMMIT;\n"
            ]
        return texto_sql

    def scriptMovExtraSinCuota (cantidad, pat, fecha_corte):
        texto_sql = [
                    "-- "+ str(cantidad) + " MOVIMIENTO EXTRAFIN SIN CUOTA\n"
                    "--SELECT *\n"
                    "DELETE\n"
                    "FROM FIP.FIP_DIARIO_MOVNEGOCIOS SN\n"
                    "     SN.FECHA_CORTE between TO_DATE('"+ fecha_corte + "', 'ddmmyyyy') and TO_DATE('"+ fecha_corte + "', 'ddmmyyyy') + .99999\n"
                    "     AND SN.CODIGO_PATRIMONIO = "+ str(pat) + "\n"
                    "     AND SN.TIPO_MOVIMIENTO = '006'\n"
                    "     AND NOT EXISTS (\n"
                    "        select 1 from Fip_Cuenta_Credito_Ic CC where\n"
                    "         CC.CTA_NUM_CTA_CREDITO = SN.NUM_CTA_CREDITO\n"
                    "         AND CC.CTA_COD_CLIENTE = SN.COD_CLIENTE\n"
                    "         AND CC.CTA_COD_EMPRESA = SN.COD_EMPRESA)\n"
                    "     AND SN.COD_CLIENTE NOT IN (\n"
                    "        select b.COD_CLIENTE\n"
                    "          from tc_cambioprod_enc a, tc_cuenta_credito b\n"
                    "         where \n"
                    "           trunc(a.fec_estado) <= trunc(SN.FECHA_CORTE)\n"
                    "           and a.ind_estado = 'F'\n"
                    "           and b.num_cta_credito = a.num_cta_credito\n"
                    "           and b.cod_empresa = a.cod_empresa\n"
                    "           and EXISTS\n"
                    "         (SELECT 1\n"
                    "              FROM fip.Fip_Patrimonios         fp,\n"
                    "                   fip.Fip_Cartera_Clasificada fn\n"
                    "             WHERE fp.empresa = a.Cod_Empresa\n"
                    "               AND fp.estado_patrimonio = 'A'\n"
                    "               AND fn.codigo_patrimonio = fp.codigo_patrimonio\n"
                    "               AND fn.CODIGO_CLIENTE = b.Cod_Cliente\n"
                    "               and fp.codigo_patrimonio_ic = SN.CODIGO_PATRIMONIO)\n"
                    "         group by a.NUM_CTA_IC,\n"
                    "                  b.COD_CLIENTE,\n"
                    "                  b.COD_EMPRESA,\n"
                    "                  b.fec_inclusion);\n"
                    "COMMIT;\n"

            ]
        return texto_sql

    def scriptMovSinCuota (cantidad, pat, fecha_corte):
        texto_sql = [
                    "-- "+ str(cantidad) + " MOVIMIENTO EXTRAFIN SIN CUOTA\n"
                    "--SELECT *\n"
                    "DELETE\n"
                    "FROM FIP.FIP_DIARIO_MOVNEGOCIOS SN\n"
                    "     SN.FECHA_CORTE between TO_DATE('"+ fecha_corte + "', 'ddmmyyyy') and TO_DATE('"+ fecha_corte + "', 'ddmmyyyy') + .99999\n"
                    "     AND SN.CODIGO_PATRIMONIO = "+ str(pat) + "\n"
                    "     AND SN.TIPO_MOVIMIENTO <> '006'\n"
                    "     AND NOT EXISTS (\n"
                    "        select 1 from Fip_Cuenta_Credito_Ic CC where\n"
                    "         CC.CTA_NUM_CTA_CREDITO = SN.NUM_CTA_CREDITO\n"
                    "         AND CC.CTA_COD_CLIENTE = SN.COD_CLIENTE\n"
                    "         AND CC.CTA_COD_EMPRESA = SN.COD_EMPRESA)\n"
                    "     AND SN.COD_CLIENTE NOT IN (\n"
                    "        select b.COD_CLIENTE\n"
                    "          from tc_cambioprod_enc a, tc_cuenta_credito b\n"
                    "         where \n"
                    "           trunc(a.fec_estado) <= trunc(SN.FECHA_CORTE)\n"
                    "           and a.ind_estado = 'F'\n"
                    "           and b.num_cta_credito = a.num_cta_credito\n"
                    "           and b.cod_empresa = a.cod_empresa\n"
                    "           and EXISTS\n"
                    "         (SELECT 1\n"
                    "              FROM fip.Fip_Patrimonios         fp,\n"
                    "                   fip.Fip_Cartera_Clasificada fn\n"
                    "             WHERE fp.empresa = a.Cod_Empresa\n"
                    "               AND fp.estado_patrimonio = 'A'\n"
                    "               AND fn.codigo_patrimonio = fp.codigo_patrimonio\n"
                    "               AND fn.CODIGO_CLIENTE = b.Cod_Cliente\n"
                    "               and fp.codigo_patrimonio_ic = SN.CODIGO_PATRIMONIO)\n"
                    "         group by a.NUM_CTA_IC,\n"
                    "                  b.COD_CLIENTE,\n"
                    "                  b.COD_EMPRESA,\n"
                    "                  b.fec_inclusion);\n"
                    "COMMIT;\n"
            ]
        return texto_sql
    
    def scriptClienteDuplicadoTc (cantidad, pat, fecha_corte):
        patrimonioTC = PATRIMONIOS_TC.get(int(pat))
        texto_sql = [
                    "-- "+ str(cantidad) + " CLIENTES DUPLICADOS\n"
                    "--SELECT *\n"
                    "DELETE\n"
                    "FROM fip.fip_cartera_clasificada fcc\n"
                    " WHERE fcc.codigo_cliente IN\n"
                    "       (SELECT b.cod_cliente\n"
                    "          FROM tc_cambioprod_enc a, tc_cuenta_credito b\n"
                    "         WHERE a.fec_estado BETWEEN TO_DATE('"+ fecha_corte + "', 'ddmmyyyy') AND\n"
                    "               TO_DATE('"+ fecha_corte + "', 'ddmmyyyy') + .99999\n"
                    "           AND a.ind_estado = 'F'\n"
                    "           AND b.num_cta_credito = a.num_cta_credito\n"
                    "           AND b.cod_empresa = a.cod_empresa\n"
                    "           AND EXISTS\n"
                    "         (SELECT 1\n"
                    "                  FROM fip.fip_patrimonios fp, fip.fip_cartera_clasificada fn\n"
                    "                 WHERE fp.empresa = a.cod_empresa\n"
                    "                   AND fp.estado_patrimonio = 'A'\n"
                    "                   AND fn.codigo_patrimonio = fp.codigo_patrimonio\n"
                    "                   AND fn.codigo_cliente = b.cod_cliente\n"
                    "                   AND fp.codigo_patrimonio_ic = "+ str(pat) +")\n"
                    "         GROUP BY a.num_cta_ic,\n"
                    "                  b.cod_cliente,\n"
                    "                  b.cod_empresa,\n"
                    "                  b.fec_inclusion)\n"
                    "   AND fcc.codigo_patrimonio NOT IN ('1', "+ str(patrimonioTC) +", "+ str(pat) +")\n"
                    "   AND length(fcc.codigo_patrimonio) = 1;\n"
                    "\n"
                    "--SELECT *\n"
                    "DELETE\n"
                    "from fip.fip_cuentas fcc\n"
                    " where fcc.codigo_cliente in\n"
                    "       (select b.cod_cliente\n"
                    "          from tc.tc_cambioprod_enc a, tc.tc_cuenta_credito b\n"
                    "         where a.fec_estado between to_date('"+ fecha_corte + "', 'ddmmyyyy') and\n"
                    "               to_date('"+ fecha_corte + "', 'ddmmyyyy') + .99999\n"
                    "           and a.ind_estado = 'F'\n"
                    "           and b.num_cta_credito = a.num_cta_credito\n"
                    "           and b.cod_empresa = a.cod_empresa\n"
                    "           and exists\n"
                    "         (select 1\n"
                    "                  from fip.fip_patrimonios fp, fip.fip_cartera_clasificada fn\n"
                    "                 where fp.empresa = a.cod_empresa\n"
                    "                   and fp.estado_patrimonio = 'A'\n"
                    "                   and fn.codigo_patrimonio = fp.codigo_patrimonio\n"
                    "                   and fn.codigo_cliente = b.cod_cliente\n"
                    "                   and fp.codigo_patrimonio_ic = "+ str(pat) +")\n"
                    "         group by a.num_cta_ic,\n"
                    "                  b.cod_cliente,\n"
                    "                  b.cod_empresa,\n"
                    "                  b.fec_inclusion)\n"
                    "   and fcc.codigo_patrimonio not in ('1', "+ str(patrimonioTC) +", "+ str(pat) +")\n"
                    " order by fcc.codigo_cliente;\n"
                    "COMMIT;\n"
            ]
        return texto_sql

# print(ScriptSQL.crear(7, 4, '04062020', 5))