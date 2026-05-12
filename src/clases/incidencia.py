from interfaces import Recomendaciones
from excepciones import ErrorIncidencia


class Incidencia(Recomendaciones):

    def __init__(self, tipo):

        if not tipo:
            raise ErrorIncidencia("El tipo de incidencia no puede estar vacío")

        self.tipo = tipo
        self.nivel_riesgo = "Sin calcular"

    def calcular_riesgo(self):
        self.nivel_riesgo = "Bajo"
        return self.nivel_riesgo

    def obtener_recomendacion(self):
        return "Revisar la incidencia con el equipo de ciberseguridad"

    def mostrar_info(self):
        return f"{self.tipo} | Riesgo: {self.nivel_riesgo}"

    def convertir_diccionario(self):
        return {
            "tipo": self.tipo,
            "nivel_riesgo": self.nivel_riesgo,
            "recomendacion": self.obtener_recomendacion()
        }

    def __str__(self):
        return self.mostrar_info()