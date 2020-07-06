class ScriptSQL(object):

    def crear(archivo:int, patrimonio: int, fecha_corte: str, cantidad: int):
        try:
            archivo_path = "scripts/%s.sql" % (str(archivo))
            lista_sql = (
                ScriptSQL.sql_negocios_null(cantidad),
                ScriptSQL.sql_negocios_duplicados(cantidad, patrimonio, fecha_corte),
                ScriptSQL.sql_cuotas_duplicadas(cantidad, patrimonio, fecha_corte),
                ScriptSQL.sql_cuotas_snegocio(cantidad, patrimonio, fecha_corte),
                ScriptSQL.sql_nroneg_null(cantidad, patrimonio, fecha_corte)
                )
            texto = lista_sql[archivo]
            with open(archivo_path, "w") as archivo:
                archivo.writelines(texto)
            return True
        except Exception as e:
            return ("Error: el sql: %s no pudo crearse. %s" % (archivo, e))

    def sql_negocios_null(cantidad):
        texto_sql = [
                    "-- "+ str(cantidad) + " NEGOCIOS TIPO DE DOCUMENTO NULL\n"
                    "UPDATE FIP.FIP_DIARIO_NEGOCIOS\n"
                    "SET\n"
                    "    COD_COMERCIO = '00000400',\n"
                    "    TIPO_DOCUMENTO = '001'\n"
                    "WHERE\n"
                    "    TIPO_DOCUMENTO IS NULL;\n"
                    "COMMIT;\n"
            ]
        return texto_sql
    
    def sql_negocios_duplicados(cantidad, pat, fecha_corte):
        texto_sql = [
                    "-- "+ str(cantidad) + " NEGOCIOS DUPLICADOS\n"
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
    
    def sql_cuotas_duplicadas(cantidad, pat, fecha_corte):
        texto_sql = [
                    "-- "+ str(cantidad) + " CUOTAS DUPLICADAS\n"
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

    def sql_cuotas_snegocio(cantidad, pat, fecha_corte):
        texto_sql = [
                    "-- "+ str(cantidad) + " CUOTAS SIN NEGOCIO\n"
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
    
    def sql_nroneg_null(cantidad, pat, fecha_corte):
        texto_sql = [
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

#print(ScriptSQL.crear(0, 4, '04062020', 4))