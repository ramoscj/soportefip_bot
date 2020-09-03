
class Mensaje(object):

    def reports_odi(patrimonio, fecha_corte):
        error = "La INFORMACION NO ESTA CARGADA en la interfaz del RESPALDO para el patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
        recomendado = "Para retomar el proceso se debe EJECUTAR el ODI para el patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
        nota_msj = "La informacion ya se encuentra generada en la interfaz del REPORTS para el patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
        return error, recomendado, nota_msj

    def fip_wrap2(patrimonio, fecha_corte):
        error = "La INFORMACION NO ESTA GENERADA en la interfaz del REPORTS para el patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
        recomendado = "Para retomar el proceso debe ejecutar el FIP_WRAP OPCION 2 (dos) para generar los NEGOCIOS del patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
        nota_msj = "Las remesas ya se encuentran generados en la interfaz del REPORTS para el patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
        return error, recomendado, nota_msj

    def fip_wrap3(negocios, patrimonio, fecha_corte):
        error = "Las REMESAS NO ESTAN GENERADAS en la interfaz del REPORTS para el patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
        recomendado = "Para retomar el proceso debe ejecutar el FIP_WRAP OPCION 3 (tres) para generar las REMESAS del patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
        nota_msj = "Los Negocios (%s) ya se encuentran generados en la interfaz del REPORTS para el patrimonio: %s y fecha de corte: %s." % (negocios, patrimonio, fecha_corte)
        return error, recomendado, nota_msj

    def fip_wrap2_3(patrimonio, fecha_corte):
        error = "Las INFORMACION NO ESTA GENERADA en la interfaz del REPORTS para el patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
        recomendado = "Para retomar el proceso debe ejecutar el FIP_WRAP OPCION 2 (dos) para generar los NEGOCIOS y luego el FIP_WRAP OPCION 3 (tres) para generar las REMESAS del patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
        nota_msj = "Si no tiene el nivel de acceso necesario para ejecutar este proceso contactar con el Supervisor"
        return error, recomendado, nota_msj

    def remesas_reports(negocios, patrimonio, fecha_corte):
        error = "Las REMESAS NO ESTAN GENERADAS en en la interfaz del REPORTS para el patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
        recomendado = "Para retomar el proceso debe ejecutar el FIP_WRAP OPCION 3 (tres) para generar las REMESAS (solo para este patrimonio y fecha de corte)."
        nota_msj = "Los Negocios (%s) ya se encuentran generados en la interfaz del REPORTS para el patrimonio: %s y fecha de corte: %s." % (negocios, patrimonio, fecha_corte)
        return error, recomendado, nota_msj

    def remesas_respaldo(patrimonio, fecha_corte):
        error = "Las REMESAS NO ESTAN CARGADAS en la interfaz del RESPALDO para el patrimonio: %s y fecha de corte: %s." % (patrimonio, fecha_corte)
        recomendado = "Para retomar el proceso se debe ejecutar el ODI para el patrimonio y fecha de corte."
        nota_msj = "Si ya realizo la ejecucion del proceso ODI, espere a que este finalice y luego vuelva a ejecutar la revisión"
        return error, recomendado, nota_msj