# Sistema de domótica en Python

Aplicación modular que simula un sistema de domótica. Un `Hub` central registra y gestiona sensores de temperatura, bombillas inteligentes y cerraduras.

## Estructura

```text
mi_proyecto_domotica/
├── domotica/
│   ├── __init__.py
│   ├── base.py
│   ├── common.py
│   ├── dispositivos.py
│   ├── hub.py
│   └── interfaces.py
├── main.py
├── README.md
├── enlace_github.txt
└── .gitignore
```

## Contenido principal

- **`Dispositivo`**: clase abstracta con los atributos comunes y sus propiedades.
- **`SensorTemperatura`**: permite consultar y calibrar la temperatura.
- **`BombillaInteligente`**: permite encender, apagar, modificar el brillo y actualizar el firmware.
- **`CerraduraInteligente`**: permite bloquear y desbloquear. También adapta esas acciones a `encender()` y `apagar()` para implementar el Protocol `Conmutable`.
- **Protocols**: `Medible`, `Conmutable` y `Actualizable` describen capacidades mediante duck typing.
- **`Hub`**: registra los dispositivos, los lista, ejecuta operaciones polimórficas y calcula estadísticas.
- **`common.py`**: contiene las excepciones propias y las utilidades de validación y generación de IDs.
z