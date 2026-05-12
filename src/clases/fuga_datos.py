from src.clases.incidencia import Incidencia
from src.clases.excepciones import ErrorIncidencia

class FugaDatos(Incidencia):

    def __init__(self, datos_afectados, numero_registros, origen_fuga):

        super().__init__("Fuga de datos")

        if not datos_afectados:
            raise ErrorIncidencia("Los datos afectados no pueden estar vacíos")

        if numero_registros <= 0:
            raise ErrorIncidencia("El número de registros debe ser mayor que cero")

        if not origen_fuga:
            raise ErrorIncidencia("El origen de la fuga no puede estar vacío")

        self.datos_afectados = datos_afectados
        self.numero_registros = numero_registros
        self.origen_fuga = origen_fuga

        self.calcular_riesgo()

    def calcular_riesgo(self):

        if self.numero_registros < 50:
            self.nivel_riesgo = "Bajo"
        elif self.numero_registros < 500:
            self.nivel_riesgo = "Medio"
        elif self.numero_registros < 5000:
            self.nivel_riesgo = "Alto"
        else:
            self.nivel_riesgo = "Crítico"

        return self.nivel_riesgo

    def obtener_recomendacion(self):
        return "Notificar la fuga, cambiar credenciales y revisar permisos"

    def mostrar_info(self):
        return (
            f"{super().mostrar_info()} | "
            f"Datos afectados: {self.datos_afectados} | "
            f"Número de registros: {self.numero_registros} | "
            f"Origen: {self.origen_fuga}"
        )

    def convertir_diccionario(self):
        datos = super().convertir_diccionario()
        datos["datos_afectados"] = self.datos_afectados
        datos["numero_registros"] = self.numero_registros
        datos["origen_fuga"] = self.origen_fuga
        return datos