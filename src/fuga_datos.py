from incidencia import Incidencia
from error_incidencia import ErrorIncidencia


class FugaDatos(Incidencia):

    def __init__(self, tipo, nivel_riesgo,
                 datos_afectados,
                 numero_registros,
                 origen_fuga):

        super().__init__(tipo, nivel_riesgo)

        if numero_registros <= 0:
            raise ErrorIncidencia("Número de registros inválido")

        self.datos_afectados = datos_afectados
        self.numero_registros = numero_registros
        self.origen_fuga = origen_fuga

    def obtener_recomendacion(self):
        return "Cambiar credenciales y revisar permisos."

    def mostrar_info(self):
        return (
            f"{super().mostrar_info()} | "
            f"Datos afectados: {self.datos_afectados} | "
            f"Registros: {self.numero_registros}"
        )