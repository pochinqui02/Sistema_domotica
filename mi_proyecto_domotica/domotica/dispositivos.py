"""Implementación de los dispositivos concretos del sistema."""

import math

from .base import Dispositivo
from .common import DatoInvalido, Utils


def _validar_numero_finito(valor: object, campo: str) -> float:
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise DatoInvalido(f"{campo} debe ser un número.")
    resultado = float(valor)
    if not math.isfinite(resultado):
        raise DatoInvalido(f"{campo} debe ser un número finito.")
    return resultado


class SensorTemperatura(Dispositivo):
    """Sensor que proporciona una lectura de temperatura en grados Celsius."""

    def __init__(
        self, id: str, nombre: str, fabricante: str, celsius: float
    ) -> None:
        super().__init__(id, nombre, fabricante)
        self.celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, valor: float) -> None:
        self._celsius = _validar_numero_finito(valor, "La temperatura")

    def leer_valor(self) -> float:
        return self.celsius

    def calibrar(self, offset: float) -> None:
        """Aplica una corrección a la lectura del sensor."""
        self.celsius = self.celsius + _validar_numero_finito(offset, "El offset")

    def tipo(self) -> str:
        return "SensorTemperatura"

    def __str__(self) -> str:
        return f"{super().__str__()}, temperatura={self.celsius:.2f} ºC"


class BombillaInteligente(Dispositivo):
    """Bombilla con brillo, estado de encendido y firmware."""

    def __init__(
        self,
        id: str,
        nombre: str,
        fabricante: str,
        brillo: int = 0,
        encendida: bool = False,
    ) -> None:
        super().__init__(id, nombre, fabricante)
        self.brillo = brillo
        self.encendida = encendida
        self._version_firmware = "1.0.0"

    @property
    def brillo(self) -> int:
        return self._brillo

    @brillo.setter
    def brillo(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise DatoInvalido("El brillo debe ser un número entero entre 0 y 100.")
        if not 0 <= valor <= 100:
            raise DatoInvalido("El brillo debe estar entre 0 y 100.")
        self._brillo = valor

    @property
    def encendida(self) -> bool:
        return self._encendida

    @encendida.setter
    def encendida(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise DatoInvalido("El estado de la bombilla debe ser booleano.")
        self._encendida = valor

    @property
    def version_firmware(self) -> str:
        return self._version_firmware

    def encender(self) -> None:
        self.encendida = True

    def apagar(self) -> None:
        self.encendida = False

    def actualizar_firmware(self, version: str) -> None:
        if not Utils.validar_version(version):
            raise DatoInvalido(
                f"Versión de firmware inválida: {version!r}. "
                "Formato esperado X.Y.Z (por ejemplo, 1.2.3)."
            )
        self._version_firmware = version.strip()

    def tipo(self) -> str:
        return "BombillaInteligente"

    def __str__(self) -> str:
        estado = "encendida" if self.encendida else "apagada"
        return (
            f"{super().__str__()}, brillo={self.brillo}, "
            f"estado={estado}, firmware={self.version_firmware}"
        )


class CerraduraInteligente(Dispositivo):
    """Cerradura que puede bloquearse y desbloquearse."""

    def __init__(
        self,
        id: str,
        nombre: str,
        fabricante: str,
        bloqueada: bool = True,
    ) -> None:
        super().__init__(id, nombre, fabricante)
        self.bloqueada = bloqueada

    @property
    def bloqueada(self) -> bool:
        return self._bloqueada

    @bloqueada.setter
    def bloqueada(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise DatoInvalido("El estado de la cerradura debe ser booleano.")
        self._bloqueada = valor

    def bloquear(self) -> None:
        self.bloqueada = True

    def desbloquear(self) -> None:
        self.bloqueada = False

    # Adaptadores para cumplir el Protocol Conmutable.
    # En una cerradura, encender equivale a bloquear y apagar a desbloquear.
    def encender(self) -> None:
        self.bloquear()

    def apagar(self) -> None:
        self.desbloquear()

    def tipo(self) -> str:
        return "CerraduraInteligente"

    def __str__(self) -> str:
        estado = "bloqueada" if self.bloqueada else "desbloqueada"
        return f"{super().__str__()}, estado={estado}"
