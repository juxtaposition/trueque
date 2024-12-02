# Proyecto Django de Tienda de Cómics

Este es un proyecto Django que simula una tienda de cómics online.

## Requisitos previos

- Python 3.x
- pip (gestor de paquetes de Python)
- virtualenv (recomendado)

## Configuración del entorno

1. Clona el repositorio:
   ```
   git clone https://github.com/juxtaposition/di-habitos-2024/tree/develoment
   cd di-habitos-2024
   ```

2. Crea y activa un entorno virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # En Unix o MacOS
   venv\Scripts\activate     # En Windows
   ```

3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno:
   - Copia el archivo `.env.example` a `.env` y edita las variables según sea necesario.

5. Aplica las migraciones:
   ```
   python manage.py migrate
   ```

## Ejecutar el proyecto

1. Asegúrate de que el entorno virtual esté activado.

2. Ejecuta el servidor de desarrollo:
   ```
   python manage.py runserver
   ```

3. Abre un navegador y visita `http://127.0.0.1:8000`
