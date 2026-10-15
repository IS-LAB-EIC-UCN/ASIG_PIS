# Ejemplo de vertical slice: `[B] Registrar recurso`

Este paquete implementa en Python el ejemplo usado en el ticket de salida:

> Como coordinador logístico, quiero registrar un recurso operativo,
> para que CrisisOps pueda conocer qué recursos existen y utilizarlos
> posteriormente en las operaciones de respuesta.

## Capas

```text
HTTP request
    ↓
router.py
    ↓
service.py
    ↓
repository.py
    ↓
models.py / SQLAlchemy
    ↓
PostgreSQL
```

La validación de entrada/salida está separada en `schemas.py`.

## Regla de negocio del ejemplo

Todo recurso nuevo queda inicialmente en estado `AVAILABLE`.
El cliente no decide el estado inicial.

## Estructura

```text
crisisops_vertical_slice_example/
├── src/
│   └── crisisops_example/
│       ├── main.py
│       ├── core/
│       │   └── database.py
│       └── resources/
│           ├── router.py
│           ├── schemas.py
│           ├── service.py
│           ├── repository.py
│           └── models.py
├── migrations/
│   ├── env.py
│   └── versions/
│       └── 0001_create_resources.py
├── tests/
│   └── test_resources.py
├── alembic.ini
├── pyproject.toml
└── .env.example
```

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

python -m pip install -e ".[dev]"
```

## Base de datos

Por defecto se utiliza SQLite para que el ejemplo pueda ejecutarse inmediatamente.

Para usar PostgreSQL:

```bash
export DATABASE_URL="postgresql+psycopg://crisisops:crisisops@localhost:5432/crisisops"
```

o configura la variable equivalente en tu entorno.

Aplicar migraciones:

```bash
alembic upgrade head
```

## Ejecutar API

```bash
uvicorn crisisops_example.main:app --reload
```

Luego:

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

## Probar el endpoint

```bash
curl -X POST http://localhost:8000/resources \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Ambulancia 03",
        "type": "AMBULANCE",
        "location": "La Serena"
      }'
```

Respuesta esperada:

```json
{
  "id": 1,
  "name": "Ambulancia 03",
  "type": "AMBULANCE",
  "status": "AVAILABLE",
  "location": "La Serena"
}
```

## Ejecutar pruebas

```bash
pytest -q
```

## Qué observar en clase

1. `router.py` conoce HTTP, pero no implementa la regla de negocio.
2. `service.py` aplica la regla `status = AVAILABLE`.
3. `repository.py` encapsula el acceso a datos.
4. `models.py` define el modelo ORM.
5. Alembic versiona la creación de la tabla.
6. La prueba verifica el comportamiento observable de todo el slice.
