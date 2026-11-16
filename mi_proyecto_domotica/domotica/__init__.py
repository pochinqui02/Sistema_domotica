"""Paquete principal del sistema de domótica."""

from .base import Dispositivo
from .common import DatoInvalido, Duplicado, NoEncontrado, Utils
from .dispositivos import (
    BombillaInteligente,
    CerraduraInteligente,
    SensorTemperatura,
)
from .hub import Hub
from .interfaces import Actualizable, Conmutable, Medible

__all__ = [
    "Dispositivo",
    "SensorTemperatura",
    "BombillaInteligente",
    "CerraduraInteligente",
    "Hub",
    "Medible",
    "Conmutable",
    "Actualizable",
    "DatoInvalido",
    "Duplicado",
    "NoEncontrado",
    "Utils",
]
