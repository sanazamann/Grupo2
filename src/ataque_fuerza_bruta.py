# models/ataque_fuerza_bruta.py

from models.incidencia import Incidencia
from src.clases.error_incidencia import ErrorIncidencia


class AtaqueFuerzaBruta(Incidencia):

    def __init__(self, tipo, nivel_riesgo,
                 intentos, red,
                 acceso_admin, utiliza_contrasenas):

        super().__init__(tipo, nivel_riesgo)

        if intentos < 0:
            raise ErrorIncidencia("Intentos inválidos")

        self.intentos = intentos
        self.red = red
        self.acceso_admin = acceso_admin
        self.utiliza_contrasenas = utiliza_contrasenas

    def obtener_recomendacion(self):
        return "Activar autenticación multifactor."

    def mostrar_info(self):
        return (
            f"{super().mostrar_info()} | "
            f"Intentos: {self.intentos} | "
            f"Red: {self.red}"
        )