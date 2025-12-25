import os
from dotenv import load_dotenv

import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()

load_dotenv()

TOKEN = os.getenv("TOKEN")
API_TOKEN = os.getenv("API_TOKEN")
BACKEND_URL = "http://localhost:8000"  

if not TOKEN or not API_TOKEN:
    raise RuntimeError("Faltan variables de entorno")

async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello world")

async def get_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/tasks/me",
            headers=headers
        )

    if response.status_code != 200:
        await update.message.reply_text("Error al obtener tareas")
        return

    tasks = response.json()

    if not tasks:
        await update.message.reply_text("📭 No tenés tareas")
        return

    message = "📋 *Tus tareas:*\n\n"
    for task in tasks:
        message += f"• {task['title']} — _{task['status']}_\n"

    await update.message.reply_text(message, parse_mode="Markdown")


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", say_hello))
    application.add_handler(CommandHandler("tasks", get_tasks))

    application.run_polling()

if __name__ == "__main__":
    main()
