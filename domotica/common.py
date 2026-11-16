"""Utilidades y excepciones comunes.

Este módulo solo depende de la biblioteca estándar; no importa dispositivos
ni el Hub para evitar dependencias circulares.
"""

import re


class DatoInvalido(ValueError):
    """Se lanza cuando un dato no cumple el formato o las reglas de negocio."""


class Duplicado(Exception):
    """Se lanza cuando se intenta registrar una clave que ya existe."""


class NoEncontrado(Exception):
    """Se lanza cuando no existe el elemento solicitado."""


class Utils:
    """Funciones auxiliares para validar y generar datos del dominio."""

    _PATRON_ID = re.compile(r"^[A-Za-z][A-Za-z0-9-]*$")
    _PATRON_VERSION = re.compile(r"^\d+\.\d+\.\d+$")

    @staticmethod
    def validar_id(texto: str) -> bool:
        """Comprueba que el ID comienza por una letra y no contiene espacios."""
        if not isinstance(texto, str):
            return False
        candidato = texto.strip()
        return bool(candidato and Utils._PATRON_ID.fullmatch(candidato))

    @staticmethod
    def fabricar_id(prefijo: str, n: int) -> str:
        """Genera un identificador del tipo B001, S012 o HUB007."""
        if not isinstance(prefijo, str) or not prefijo.strip():
            raise DatoInvalido("ID generado inválido: ''")

        prefijo_normalizado = prefijo.strip().upper()

        if isinstance(n, bool) or not isinstance(n, int) or n < 1:
            candidato = f"{prefijo_normalizado}{n}" if isinstance(n, int) else ""
            raise DatoInvalido(f"ID generado inválido: '{candidato}'")

        candidato = f"{prefijo_normalizado}{n:03d}"
        if not Utils.validar_id(candidato):
            raise DatoInvalido(f"ID generado inválido: '{candidato}'")
        return candidato

    @staticmethod
    def validar_version(version: str) -> bool:
        """Valida una versión numérica con el formato X.Y.Z."""
        if not isinstance(version, str):
            return False
        return bool(Utils._PATRON_VERSION.fullmatch(version.strip()))
