#interfaz

from abc import ABC, abstractmethod


class Recomendaciones(ABC):

    @abstractmethod
    def obtener_recomendacion(self):
        pass