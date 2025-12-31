from telegram import Update
from telegram.ext import ContextTypes

from services.backend import (
    create_reminder,
    fetch_my_reminders,
    fetch_my_tasks,
    create_task,
    service_delete_task,
    update_task_data,
)
from utils.auth import get_auth_headers
from sessions import user_sessions

async def get_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user_id = update.effective_user.id
    headers = get_auth_headers(telegram_user_id)

    """
    Displays all the reminders belonging to the authenticated user.
    """

    if not headers:
        await update.message.reply_text("🔒 Please login first")
        return

    response = await fetch_my_reminders(headers)

    if response.status_code == 401:
        user_sessions.pop(telegram_user_id, None)
        await update.message.reply_text("Session expired. Please login again.")
        return

    if response.status_code != 200:
        await update.message.reply_text("Error while fetching your reminders")
        return

    reminders = response.json()

    if not reminders:
        await update.message.reply_text("📭 No reminders found")
        return

    message = "📋 *Your reminders:*\n\n"
    for rem in reminders:
        message += f"• [{rem['id']}] — {rem['date']} — {rem['description']}\n"

    await update.message.reply_text(message)

async def add_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user_id = update.effective_user.id
    headers = get_auth_headers(telegram_user_id)

    """
    Creates a new reminder.
    Usage:
    /addreminder date | description
    """

    if not headers:
        await update.message.reply_text("🔒 Please login first")
        return

    if not context.args:
        await update.message.reply_text(
            "Correct usage:\n/addreminder year-month-day | description"
        )
        return

    raw_text = " ".join(context.args)
    parts = [p.strip() for p in raw_text.split("|")]

    payload = {
        "date": parts[0],
        "description": parts[1] if len(parts) > 1 else "",
    }

    response = await create_reminder(payload, headers)

    if response.status_code == 401:
        user_sessions.pop(telegram_user_id, None)
        await update.message.reply_text("Session expired. Please login again.")
        return

    if response.status_code == 201:
        await update.message.reply_text("✅ Reminder created successfully")
    else:
        await update.message.reply_text(
            f"Failed to create reminder ({response.status_code})"
        )