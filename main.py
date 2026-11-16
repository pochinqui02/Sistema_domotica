"""Demostración de la aplicación modular de domótica."""

from domotica import (
    Actualizable,
    BombillaInteligente,
    CerraduraInteligente,
    Conmutable,
    DatoInvalido,
    Duplicado,
    Hub,
    Medible,
    NoEncontrado,
    SensorTemperatura,
    Utils,
)


def crear_dispositivo(definicion: dict):
    """Construye una subclase a partir de un diccionario de configuración."""
    tipo = definicion["tipo"].lower()
    datos_comunes = {
        "id": definicion["id"],
        "nombre": definicion["nombre"],
        "fabricante": definicion["fabricante"],
    }

    if tipo == "sensor":
        return SensorTemperatura(
            **datos_comunes, celsius=definicion["celsius"]
        )
    if tipo == "bombilla":
        return BombillaInteligente(
            **datos_comunes,
            brillo=definicion["brillo"],
            encendida=definicion.get("encendida", False),
        )
    if tipo == "cerradura":
        return CerraduraInteligente(
            **datos_comunes,
            bloqueada=definicion.get("bloqueada", True),
        )

    raise DatoInvalido(f"Tipo de dispositivo desconocido: {tipo!r}")


def main() -> None:
    print("=== DEMO DOMÓTICA — INICIO ===\n")
    hub = Hub()
    print("Creando Hub... OK")

    definiciones = [
        {
            "id": "S001", "tipo": "sensor", "nombre": "Sensor Cocina",
            "fabricante": "Acme", "celsius": 22.5,
        },
        {
            "id": "B001", "tipo": "bombilla", "nombre": "Bombilla Salón",
            "fabricante": "Lumen", "brillo": 80, "encendida": False,
        },
        {
            "id": "C001", "tipo": "cerradura", "nombre": "Puerta Principal",
            "fabricante": "SafeCo", "bloqueada": True,
        },
        {
            "id": "S002", "tipo": "sensor", "nombre": "Sensor Dormitorio",
            "fabricante": "Acme", "celsius": 19.3,
        },
        {
            "id": "B002", "tipo": "bombilla", "nombre": "Bombilla Pasillo",
            "fabricante": "Lumen", "brillo": 50,
        },
        {
            "id": "C002", "tipo": "cerradura", "nombre": "Puerta Garaje",
            "fabricante": "SafeCo", "bloqueada": False,
        },
        {
            "id": "001", "tipo": "sensor", "nombre": "ID incorrecto",
            "fabricante": "Acme", "celsius": 20.0,
        },
        {
            "id": "B001", "tipo": "bombilla", "nombre": "Bombilla duplicada",
            "fabricante": "Lumen", "brillo": 40,
        },
        {
            "id": "B003", "tipo": "bombilla", "nombre": "Brillo incorrecto",
            "fabricante": "Lumen", "brillo": 150,
        },
    ]

    print("\nValidando e instanciando dispositivos:")
    for definicion in definiciones:
        identificador = definicion.get("id", "")
        if not Utils.validar_id(identificador):
            print(f"ERROR: ID {identificador!r} inválido -> se omite")
            continue

        try:
            dispositivo = crear_dispositivo(definicion)
            hub.registrar(dispositivo)
            print(f"OK: {dispositivo}")
        except Duplicado as error:
            print(f"ERROR: Duplicado -> {error}; se omite")
        except DatoInvalido as error:
            print(f"ERROR: Dato inválido -> {error}; se omite")

    dispositivos = hub.listar()
    print(f"\nRegistro en Hub completado: {len(dispositivos)} dispositivos.")

    print("\nListado de dispositivos:")
    for dispositivo in dispositivos:
        print(f"- {dispositivo}")

    print("\nCapacidades detectadas:")
    resumen_capacidades: dict[str, list[str]] = {}
    for dispositivo in dispositivos:
        capacidades = []
        if isinstance(dispositivo, Medible):
            capacidades.append("Medible")
        if isinstance(dispositivo, Conmutable):
            capacidades.append("Conmutable")
        if isinstance(dispositivo, Actualizable):
            capacidades.append("Actualizable")
        resumen_capacidades[dispositivo.id] = capacidades
        texto = ", ".join(capacidades) if capacidades else "Sin capacidades"
        print(f"{dispositivo.id} -> {texto}")

    print("\nOperar todos (polimorfismo):")
    hub.operar_todos()

    print("\nAcciones específicas:")
    sensor = next(d for d in dispositivos if isinstance(d, SensorTemperatura))
    lectura_anterior = sensor.leer_valor()
    sensor.calibrar(0.70)
    print(
        f"{sensor.id}: calibración +0.70 ºC -> "
        f"{lectura_anterior:.2f} ºC a {sensor.leer_valor():.2f} ºC"
    )

    bombillas = [d for d in dispositivos if isinstance(d, BombillaInteligente)]
    bombilla = bombillas[0]
    brillo_anterior = bombilla.brillo
    bombilla.brillo = 90
    print(f"{bombilla.id}: brillo {brillo_anterior} -> {bombilla.brillo}")
    try:
        bombilla.actualizar_firmware("1.2.3")
        print(
            f'{bombilla.id}: actualizar_firmware("1.2.3") -> '
            f"OK (versión {bombilla.version_firmware})"
        )
    except DatoInvalido as error:
        print(f"ERROR al actualizar firmware: {error}")

    segunda_bombilla = bombillas[1]
    try:
        segunda_bombilla.actualizar_firmware("1.0")
    except DatoInvalido as error:
        print(f"{segunda_bombilla.id}: versión incorrecta -> {error}")

    cerradura = next(
        d for d in dispositivos if isinstance(d, CerraduraInteligente)
    )
    estado = "bloqueada" if cerradura.bloqueada else "desbloqueada"
    print(f"{cerradura.id}: estado inicial -> {estado}")
    cerradura.desbloquear()
    print(f"{cerradura.id}: desbloquear() -> OK")
    cerradura.bloquear()
    print(f"{cerradura.id}: bloquear() -> OK")

    print("\nEstadísticas por tipo:")
    estadisticas = hub.estadisticas()
    for tipo, cantidad in estadisticas.items():
        print(f"{tipo}: {cantidad}")
    print(f"Total dispositivos: {len(dispositivos)}")

    total_medibles = sum(isinstance(d, Medible) for d in dispositivos)
    total_conmutables = sum(isinstance(d, Conmutable) for d in dispositivos)
    total_actualizables = sum(isinstance(d, Actualizable) for d in dispositivos)
    print("\nResumen de capacidades:")
    print(f"Medibles: {total_medibles}")
    print(f"Conmutables: {total_conmutables}")
    print(f"Actualizables: {total_actualizables}")

    print("\nPruebas de errores controlados:")
    try:
        hub.registrar(bombilla)
    except Duplicado as error:
        print(f"Registrar de nuevo {bombilla.id} -> ERROR: {error}")

    print(f'Validar ID "A_01" -> {Utils.validar_id("A_01")}')
    print(f'Validar versión "1.0" -> {Utils.validar_version("1.0")}')

    try:
        segunda_bombilla.actualizar_firmware("v1.2.3")
    except DatoInvalido as error:
        print(f'Actualizar firmware a "v1.2.3" -> ERROR: {error}')

    try:
        hub.obtener("X999")
    except NoEncontrado as error:
        print(f"Consultar X999 -> ERROR: {error}")

    print(f'\nEjemplo de ID generado: {Utils.fabricar_id("b", 1)}')
    print("\n=== DEMO DOMÓTICA — FIN ===")


if __name__ == "__main__":
    main()
