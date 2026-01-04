# Telegram Task & Reminder Bot

## Descripción

Este proyecto es un **bot de Telegram desarrollado en Python** que permite **gestionar tareas y recordatorios** de manera simple e intuitiva. El bot funciona como **cliente de un backend desarrollado en FastAPI**, consumiendo su API para realizar operaciones CRUD sobre tareas, manejar estados y programar recordatorios asociados a cada usuario.

El objetivo principal del proyecto es ofrecer una interfaz conversacional ligera (Telegram) conectada a un backend robusto, seguro y escalable.

---

## Funcionalidades

* Crear tareas con distintos estados (pending / in progress / completed).
* Listar tareas del usuario autenticado.
* Actualizar y eliminar tareas.
* Crear y gestionar recordatorios.
* Autenticación mediante token contra el backend.
* Respuestas claras y estructuradas para una mejor experiencia de usuario.
* Manejo de errores y validaciones.

---

## Arquitectura

El bot **no maneja lógica de negocio compleja ni persistencia**. Su responsabilidad es:

* Interpretar comandos de Telegram.
* Validar datos de entrada.
* Comunicarse con la API REST del backend FastAPI.
* Mostrar los resultados al usuario.

Toda la lógica de negocio, autenticación, validaciones avanzadas y acceso a base de datos viven en el backend.

---

## Tecnologías utilizadas

### Lenguaje

* Python 3.11+

### Bot y comunicación

* python-telegram-bot
* HTTPX (cliente HTTP asíncrono)

### Backend (consumido por el bot)

* FastAPI
* Pydantic
* SQLAlchemy
* PostgreSQL
* JWT para autenticación

### Entorno y herramientas

* venv (entornos virtuales)
* Git & GitHub
* Docker (en backend)

---

## Requisitos

* Python 3.11 o superior
* Token de bot de Telegram (BotFather)
* Backend FastAPI en ejecución

---

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/tu-usuario/telegram-task-bot.git
cd telegram-task-bot
```

2. Crear y activar un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\\Scripts\\activate     # Windows
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:

Crear un archivo `.env` con:

```env
TOKEN=your_telegram_bot_token
```

---

## Ejecución

Para iniciar el bot:

```bash
python main.py
```

El bot quedará escuchando mensajes y comandos desde Telegram.

---

## Comandos disponibles

* `/start` – Comando de prueba, retorna un hello world.
* `/help` – Muestra todos los comandos disponibles.
* `/tasks` – Lista tareas.
* `/addtask` – Crea una nueva tarea.
* `/updatetask` – Actualiza una tarea.
* `/deletetask` – Elimina una tarea.
* `/reminders` – Obtiene recordatorios.
* `/addreminder` – Agrega un recordatorio.
* `/updatereminder` – Actualiza un recordatorio.
* `/deletereminder` – Elimina un recordatorio.

---

## Buenas prácticas aplicadas

* Código modular y organizado.
* Tipado y validaciones con Pydantic.
* Separación clara entre cliente (bot) y servidor (API).
* Manejo centralizado de errores.
* Uso de entornos virtuales (`venv`).
* Variables sensibles fuera del código fuente.

---

## Estado del proyecto

Proyecto en desarrollo activo. Se planea agregar:

* Mejoras en la experiencia conversacional.
* Recordatorios programados con jobs.
* Tests automatizados.
* Logs estructurados.

---

## Autora

Milagros Alvarez

Desarrolladora Backend en formación

