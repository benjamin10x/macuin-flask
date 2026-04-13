# MACUIN Flask

Panel interno construido con Flask.

## Arquitectura actual

- Flask no se conecta a PostgreSQL.
- Flask consume la API `macuin-api` por HTTP.
- La persistencia vive únicamente en FastAPI + PostgreSQL.

## Ejecución recomendada

Desde la raíz del proyecto:

```bash
docker compose up --build
```

Luego abre:

- `http://localhost:5000`

## Variables importantes

- `API_BASE_URL`
- `API_TIMEOUT`
- `SECRET_KEY`

## Credenciales demo

- correo: `admin@macuin.com`
- contraseña: `admin123`
