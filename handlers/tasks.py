from telegram import Update
from telegram.ext import ContextTypes

from services.backend import (
    fetch_my_tasks,
    create_task,
    service_delete_task,
    update_task_status,
)
from utils.auth import get_auth_headers
from sessions import user_sessions


async def get_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user_id = update.effective_user.id
    headers = get_auth_headers(telegram_user_id)

    """
    Displays all tasks belonging to the authenticated user.
    """

    if not headers:
        await update.message.reply_text("🔒 Please login first")
        return

    response = await fetch_my_tasks(headers)

    if response.status_code == 401:
        user_sessions.pop(telegram_user_id, None)
        await update.message.reply_text("Session expired. Please login again.")
        return

    if response.status_code != 200:
        await update.message.reply_text("Error while fetching tasks")
        return

    tasks = response.json()

    if not tasks:
        await update.message.reply_text("📭 No tasks found")
        return

    message = "📋 *Your tasks:*\n\n"
    for task in tasks:
        message += f"• [{task['id']}] {task['title']} — {task['description']} — {task['status']}\n"

    await update.message.reply_text(message)



async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user_id = update.effective_user.id
    headers = get_auth_headers(telegram_user_id)

    """
    Creates a new task.
    Usage:
    /addtask title | optional description | optional status
    """

    if not headers:
        await update.message.reply_text("🔒 Please login first")
        return

    if not context.args:
        await update.message.reply_text(
            "Correct usage:\n/addtask title | optional description | optional status"
        )
        return

    raw_text = " ".join(context.args)
    parts = [p.strip() for p in raw_text.split("|")]

    payload = {
        "title": parts[0],
        "description": parts[1] if len(parts) > 1 else "",
        "status": parts[2] if len(parts) > 2 else "pending",
    }

    response = await create_task(payload, headers)

    if response.status_code == 401:
        user_sessions.pop(telegram_user_id, None)
        await update.message.reply_text("Session expired. Please login again.")
        return

    if response.status_code == 201:
        await update.message.reply_text("✅ Task created successfully")
    else:
        await update.message.reply_text(
            f"Failed to create task ({response.status_code})"
        )


async def update_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user_id = update.effective_user.id
    headers = get_auth_headers(telegram_user_id)

    """
    Updates the status of a task by its ID.
    Usage: /updatetask <task_id> <status>
    Example: /updatetask 5 completed
    """

    if not headers:
        await update.message.reply_text("🔒 Please login first")
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n/updatetask <task_id> <status>"
        )
        return

    try:
        task_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Task id must be a number")
        return

    status = context.args[1].lower()

    valid_statuses = {"pending", "in_progress", "completed"}

    if status not in valid_statuses:
        await update.message.reply_text(
            "Invalid status. Allowed values: pending, in_progress, completed"
        )
        return

    success = await update_task_status(task_id, status, headers)

    if success:
        await update.message.reply_text("✅ Task updated successfully")
    else:
        await update.message.reply_text("❌ Failed to update task")

async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user_id = update.effective_user.id
    headers = get_auth_headers(telegram_user_id)

    if not headers:
        await update.message.reply_text("🔒 Please login first")
        return

    """
    Deletes a task by its ID.
    Usage: /deletetask <task_id>
    Example: /deletetask 2
    """

    try:
        task_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Task id must be a number")
        return
    
    success = await service_delete_task(task_id, headers)

    if success:
        await update.message.reply_text(f"✅ Task with ID {task_id} successfully deleted")

    else:
        await update.message.reply_text("❌ Failed to update task")
    


