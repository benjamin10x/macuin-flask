# Sistema Administrador de Tienda de Autopartes

Aplicación web desarrollada con **Flask** para la gestión y administración de una tienda de autopartes.

## Características

- Gestión completa de catálogo de autopartes
- Control de inventario y stock
- Reportes y estadísticas
- Interfaz web moderna y responsiva

## Tecnologías

- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, Font Awesome
- **Contenedor**: Docker, Docker Compose

## Instalación

### Con Docker (Recomendado)

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/macuin-flask.git
   cd macuin-flask
   ```

2. Ejecuta con Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Accede a la aplicación en `http://localhost:5000`

### Instalación Local

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Configura la base de datos PostgreSQL y actualiza `config.py`

3. Ejecuta la aplicación:
   ```bash
   python run.py
   ```

## Uso

- **Autopartes**: Gestiona el catálogo de productos
- **Inventario**: Monitorea stock y alertas
- **Reportes**: Visualiza estadísticas y análisis

## Estructura del Proyecto

```
macuin-flask/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   ├── services.py
│   ├── templates/
│   └── static/
├── config.py
├── run.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```  
