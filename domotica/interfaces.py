"""Protocols que describen capacidades, sin imponer una jerarquía."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Medible(Protocol):
    def leer_valor(self) -> float:
        """Devuelve la lectura actual del dispositivo."""


@runtime_checkable
class Conmutable(Protocol):
    """Dispositivo que puede activarse y desactivarse."""

    def encender(self) -> None:
        """Activa el dispositivo."""


    def apagar(self) -> None:
        """Desactiva el dispositivo."""


@runtime_checkable
class Actualizable(Protocol):
    def actualizar_firmware(self, version: str) -> None:
        """Actualiza el firmware si la versión tiene un formato válido."""
