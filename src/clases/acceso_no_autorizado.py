from src.clases.incidencia import Incidencia
from src.clases.excepciones import ErrorIncidencia

class AccesoNoAutorizado(Incidencia):

    def __init__(self, usuario_afectado, sistema_afectado, privilegios_admin):

        super().__init__("Acceso no autorizado")

        if not usuario_afectado:
            raise ErrorIncidencia("El usuario afectado no puede estar vacío")

        if not sistema_afectado:
            raise ErrorIncidencia("El sistema afectado no puede estar vacío")

        self.usuario_afectado = usuario_afectado
        self.sistema_afectado = sistema_afectado
        self.privilegios_admin = privilegios_admin

        self.calcular_riesgo()

    def calcular_riesgo(self):

        if self.privilegios_admin:
            self.nivel_riesgo = "Crítico"
        else:
            self.nivel_riesgo = "Alto"

        return self.nivel_riesgo

    def obtener_recomendacion(self):
        return "Revocar permisos, revisar logs y cambiar la contraseña"

    def mostrar_info(self):
        return (
            f"{super().mostrar_info()} | "
            f"Usuario afectado: {self.usuario_afectado} | "
            f"Sistema afectado: {self.sistema_afectado} | "
            f"Privilegios admin: {self.privilegios_admin}"
        )

    def convertir_diccionario(self):
        datos = super().convertir_diccionario()
        datos["usuario_afectado"] = self.usuario_afectado
        datos["sistema_afectado"] = self.sistema_afectado
        datos["privilegios_admin"] = self.privilegios_admin
        return datos