from incidencia import Incidencia
from excepciones import ErrorIncidencia


class AtaqueFuerzaBruta(Incidencia):

    def __init__(self, intentos, red, acceso_admin, utiliza_contrasenas):

        super().__init__("Ataque de fuerza bruta")

        if intentos < 0:
            raise ErrorIncidencia("Los intentos no pueden ser negativos")

        if red < 0:
            raise ErrorIncidencia("La red no puede ser negativa")

        self.intentos = intentos
        self.red = red
        self.acceso_admin = acceso_admin
        self.utiliza_contrasenas = utiliza_contrasenas

        self.calcular_riesgo()

    def calcular_riesgo(self):

        if self.intentos < 20:
            self.nivel_riesgo = "Bajo"
        elif self.intentos < 100:
            self.nivel_riesgo = "Medio"
        elif self.intentos < 300:
            self.nivel_riesgo = "Alto"
        else:
            self.nivel_riesgo = "Crítico"

        if self.acceso_admin:
            self.nivel_riesgo = "Crítico"

        return self.nivel_riesgo

    def obtener_recomendacion(self):
        return "Bloquear la IP, limitar intentos y activar doble autenticación"

    def mostrar_info(self):
        return (
            f"{super().mostrar_info()} | "
            f"Intentos: {self.intentos} | "
            f"Red: {self.red} | "
            f"Acceso admin: {self.acceso_admin} | "
            f"Usa contraseñas: {self.utiliza_contrasenas}"
        )

    def convertir_diccionario(self):
        datos = super().convertir_diccionario()
        datos["intentos"] = self.intentos
        datos["red"] = self.red
        datos["acceso_admin"] = self.acceso_admin
        datos["utiliza_contrasenas"] = self.utiliza_contrasenas
        return datos