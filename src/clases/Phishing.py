from src.clases.incidencia import Incidencia
from src.clases.excepciones import ErrorIncidencia


class Phishing(Incidencia):

    def __init__(self, canal, enlace_sospechoso, remitente_desconocido):

        super().__init__("Phishing")

        if not canal:
            raise ErrorIncidencia("El canal no puede estar vacío")

        self.canal = canal
        self.enlace_sospechoso = enlace_sospechoso
        self.remitente_desconocido = remitente_desconocido

        self.calcular_riesgo()

    def calcular_riesgo(self):

        puntos = 0

        if self.enlace_sospechoso:
            puntos += 1

        if self.remitente_desconocido:
            puntos += 1

        if puntos == 0:
            self.nivel_riesgo = "Bajo"
        elif puntos == 1:
            self.nivel_riesgo = "Medio"
        else:
            self.nivel_riesgo = "Alto"

        return self.nivel_riesgo

    def obtener_recomendacion(self):
        return "No abrir enlaces sospechosos y comprobar siempre el remitente"

    def mostrar_info(self):
        return (
            f"{super().mostrar_info()} | "
            f"Canal: {self.canal} | "
            f"Enlace sospechoso: {self.enlace_sospechoso} | "
            f"Remitente desconocido: {self.remitente_desconocido}"
        )

    def convertir_diccionario(self):
        datos = super().convertir_diccionario()
        datos["canal"] = self.canal
        datos["enlace_sospechoso"] = self.enlace_sospechoso
        datos["remitente_desconocido"] = self.remitente_desconocido
        return datos