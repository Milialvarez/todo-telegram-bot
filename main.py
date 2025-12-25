import os
from dotenv import load_dotenv

import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import certifi

# Ensures SSL certificates are correctly resolved on Windows environments
os.environ["SSL_CERT_FILE"] = certifi.where()

# Loads environment variables from .env file
load_dotenv()

# Telegram bot token
TOKEN = os.getenv("TOKEN")

# JWT token used to authenticate against the backend API
API_TOKEN = os.getenv("API_TOKEN")

# Base URL of the FastAPI backend
BACKEND_URL = "http://localhost:8000"

# Fail fast if required environment variables are missing
if not TOKEN or not API_TOKEN:
    raise RuntimeError("Missing required environment variables")

async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Basic command to verify that the bot is running correctly.
    """
    await update.message.reply_text("Hello world")

async def get_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Retrieves the authenticated user's tasks from the backend
    and displays them in a formatted Telegram message.
    """
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/tasks/me",
            headers=headers
        )

    if response.status_code != 200:
        await update.message.reply_text("Error while fetching tasks")
        return

    tasks = response.json()

    if not tasks:
        await update.message.reply_text("📭 No tasks found")
        return

    message = "📋 *Your tasks:*\n\n"
    for task in tasks:
        message += f"• {task['title']} — _{task['status']}_\n"

    await update.message.reply_text(message, parse_mode="Markdown")

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Creates a new task by sending a POST request to the backend.
    Command usage:
    /addtask title | optional description | optional status
    """
    if not context.args:
        await update.message.reply_text(
            "Correct usage:\n/addtask title | optional description | optional status"
        )
        return

    raw_text = " ".join(context.args)
    parts = [p.strip() for p in raw_text.split("|")]

    title = parts[0]
    description = parts[1] if len(parts) > 1 else ""
    status = parts[2] if len(parts) > 2 else "pending"

    payload = {
        "title": title,
        "description": description,
        "status": status
    }

    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/tasks/",
                json=payload,
                headers=headers
            )

        if response.status_code == 201:
            await update.message.reply_text("✅ Task created successfully")
        else:
            await update.message.reply_text(
                f"Failed to create task ({response.status_code})"
            )

    except Exception:
        await update.message.reply_text("Backend connection error")

def main():
    """
    Application entry point.
    Registers command handlers and starts polling.
    """
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", say_hello))
    application.add_handler(CommandHandler("tasks", get_tasks))
    application.add_handler(CommandHandler("addtask", add_task))

    application.run_polling()

if __name__ == "__main__":
    main()
