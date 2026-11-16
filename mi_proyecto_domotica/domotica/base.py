"""Clase abstracta común a todos los dispositivos."""

from abc import ABC, abstractmethod

from .common import DatoInvalido, Utils


class Dispositivo(ABC):
    """Representa la información común a cualquier dispositivo."""

    def __init__(self, id: str, nombre: str, fabricante: str) -> None:
        # Se usan las propiedades para aplicar las validaciones también
        # durante la construcción del objeto.
        self.id = id
        self.nombre = nombre
        self.fabricante = fabricante

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, valor: str) -> None:
        if not Utils.validar_id(valor):
            raise DatoInvalido(f"ID inválido: {valor!r}")
        self._id = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalido("El nombre debe ser un texto no vacío.")
        self._nombre = valor.strip()

    @property
    def fabricante(self) -> str:
        return self._fabricante

    @fabricante.setter
    def fabricante(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalido("El fabricante debe ser un texto no vacío.")
        self._fabricante = valor.strip()

    # Getters y setters explícitos, además de las propiedades de Python.
    def get_id(self) -> str:
        return self.id

    def set_id(self, valor: str) -> None:
        self.id = valor

    def get_nombre(self) -> str:
        return self.nombre

    def set_nombre(self, valor: str) -> None:
        self.nombre = valor

    def get_fabricante(self) -> str:
        return self.fabricante

    def set_fabricante(self, valor: str) -> None:
        self.fabricante = valor

    @abstractmethod
    def tipo(self) -> str:
        """Devuelve el nombre del tipo concreto de dispositivo."""

    def __str__(self) -> str:
        return (
            f"[{self.tipo()}] {self.nombre} "
            f"(id={self.id}, fabricante={self.fabricante})"
        )
