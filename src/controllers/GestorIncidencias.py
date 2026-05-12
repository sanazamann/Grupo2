import pandas as pd

from src.clases.incidencia import Incidencia
from src.clases.excepciones import ErrorIncidencia
from src.utils import persistence

class GestorIncidencias:

    def __init__(self, nombre):

        if not nombre:
            raise ErrorIncidencia("El nombre del gestor no puede estar vacío")

        self.nombre = nombre
        self.lista_incidencias = []

    def agregar_incidencia(self, incidencia):

        if not isinstance(incidencia, Incidencia):
            raise TypeError("Solo se pueden agregar objetos de tipo Incidencia")

        self.lista_incidencias.append(incidencia)

    def mostrar_incidencias(self):

        if len(self.lista_incidencias) == 0:
            print("No hay incidencias registradas")
        else:
            for i, incidencia in enumerate(self.lista_incidencias):
                print(i, "-", incidencia.mostrar_info())

    def filtrar_por_tipo(self, tipo):

        encontrados = []

        for incidencia in self.lista_incidencias:
            if incidencia.tipo == tipo:
                encontrados.append(incidencia)

        return encontrados

    def filtrar_por_riesgo(self, riesgo):

        encontrados = []

        for incidencia in self.lista_incidencias:
            if incidencia.nivel_riesgo == riesgo:
                encontrados.append(incidencia)

        return encontrados

    def convertir_a_dataframe(self):

        datos = []

        for incidencia in self.lista_incidencias:
            datos.append(incidencia.convertir_diccionario())

        return pd.DataFrame(datos)

    def guardar_en_json(self, archivo):

        datos = []

        for incidencia in self.lista_incidencias:
            datos.append(incidencia.convertir_diccionario())

        persistence.guardar_json(datos, archivo)

    def cargar_desde_json(self, archivo):

        return persistence.cargar_json(archivo)

    def guardar_en_csv(self, archivo):

        df = self.convertir_a_dataframe()
        persistence.guardar_csv(df, archivo)

    def contar_por_tipo(self):

        contador = {}

        for incidencia in self.lista_incidencias:
            if incidencia.tipo not in contador:
                contador[incidencia.tipo] = 1
            else:
                contador[incidencia.tipo] += 1

        return contador

    def contar_por_riesgo(self):

        contador = {}

        for incidencia in self.lista_incidencias:
            if incidencia.nivel_riesgo not in contador:
                contador[incidencia.nivel_riesgo] = 1
            else:
                contador[incidencia.nivel_riesgo] += 1

        return contador

    def __str__(self):
        return f"Gestor: {self.nombre} | Incidencias: {len(self.lista_incidencias)}"