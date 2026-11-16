"""Hub central para registrar y operar dispositivos."""

from .base import Dispositivo
from .common import DatoInvalido, Duplicado, NoEncontrado, Utils
from .interfaces import Conmutable, Medible


class Hub:
    """Almacena dispositivos por ID y ejecuta operaciones polimórficas."""

    def __init__(self) -> None:
        self._dispositivos: dict[str, Dispositivo] = {}

    def registrar(self, disp: Dispositivo) -> None:
        if not isinstance(disp, Dispositivo):
            raise DatoInvalido("Solo se pueden registrar objetos Dispositivo.")
        if disp.id in self._dispositivos:
            raise Duplicado(f"El ID '{disp.id}' ya existe")
        self._dispositivos[disp.id] = disp

    def listar(self) -> list[Dispositivo]:
        return list(self._dispositivos.values())

    def obtener(self, id: str) -> Dispositivo:
        if not Utils.validar_id(id) or id.strip() not in self._dispositivos:
            raise NoEncontrado(f"No existe el dispositivo '{id}'")
        return self._dispositivos[id.strip()]

    def operar_todos(self) -> None:
        """Ejecuta las operaciones disponibles según cada Protocol."""
        for dispositivo in self.listar():
            if isinstance(dispositivo, Medible):
                print(
                    f"{dispositivo.id} -> lectura = "
                    f"{dispositivo.leer_valor():.2f} ºC"
                )

            if isinstance(dispositivo, Conmutable):
                dispositivo.encender()
                print(f"{dispositivo.id} -> encender() -> OK")
                dispositivo.apagar()
                print(f"{dispositivo.id} -> apagar() -> OK")

    def estadisticas(self) -> dict[str, int]:
        resultado: dict[str, int] = {}
        for dispositivo in self._dispositivos.values():
            nombre_tipo = dispositivo.tipo()
            resultado[nombre_tipo] = resultado.get(nombre_tipo, 0) + 1
        return resultado
