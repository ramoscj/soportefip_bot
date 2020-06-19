class ScriptCaso(object):
    def script_sql_diario(self, argument):
        nombre = 'script_' + str(argument)
        metodo = getattr(self, nombre, lambda: "Script invalido")
        return metodo()
 
    def script_1(self):
        return "January"
 
    def script_2(self):
        return "February"
 
    def script_3(self):
        return "March"