from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

from services.backend import (
    create_reminder,
    fetch_my_reminders,
    service_delete_reminder,
    update_reminder_service,
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

async def update_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user_id = update.effective_user.id
    headers = get_auth_headers(telegram_user_id)

    """
    Updates a reminder by its ID.
    Usage:
    /updatereminder id date | description
    /updatereminder id date | 
    /updatereminder id | description
    """

    if not headers:
        await update.message.reply_text("🔒 Please login first")
        return

    if not context.args:
        await update.message.reply_text(
            "Correct usage:\n/updatereminder id year-month-day (optional) | description (optional) \n At least one field is required"
        )
        return
    
    try:
        reminder_id = int(context.args[0])
        raw_text = " ".join(context.args[1:])
        parts = [p.strip() for p in raw_text.split("|")]
    except ValueError:
        await update.message.reply_text("Reminder id must be a number")
        return

    payload = {}

    #date
    if len(parts) > 0 and parts[0]:
        try:
            parsed_date = datetime.strptime(parts[0], "%Y-%m-%d").date()
            payload["date"] = str(parsed_date)
        except ValueError:
            await update.message.reply_text(
                "❌ Invalid date format. Use YYYY-MM-DD (example: 2025-09-01)"
            )
            return


    # description
    if len(parts) > 1 and parts[1]:
        payload["description"] = parts[1]

    if not payload:
        await update.message.reply_text("❌ No fields to update")
        return
    
    payload["reminder_id"] = reminder_id

    success = await update_reminder_service(payload, headers)

    if success:
        await update.message.reply_text("✅ Reminder updated successfully")
    else:
        await update.message.reply_text("❌ Failed to update Reminder")

async def delete_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user_id = update.effective_user.id
    headers = get_auth_headers(telegram_user_id)

    if not headers:
        await update.message.reply_text("🔒 Please login first")
        return

    """
    Deletes a reminder by its ID.
    Usage: /deletereminder <rem_id>
    Example: /deletereminder 2
    """

    try:
        rem_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Task id must be a number")
        return
    
    print(rem_id)
    success = await service_delete_reminder(rem_id, headers)
    print(success)

    if success:
        await update.message.reply_text(f"✅ Reminder with ID {rem_id} successfully deleted")

    else:
        await update.message.reply_text("❌ Failed to delete reminder")
    
