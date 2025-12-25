from telegram import Update
from telegram.ext import ContextTypes

from services.backend import fetch_my_tasks, create_task, update_task_status

async def get_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Displays all tasks belonging to the authenticated user.
    """
    response = await fetch_my_tasks()

    if response.status_code != 200:
        await update.message.reply_text("Error while fetching tasks")
        return

    tasks = response.json()

    if not tasks:
        await update.message.reply_text("📭 No tasks found")
        return

    message = "📋 *Your tasks:*\n\n"
    for task in tasks:
        message += f"• [{task['id']}] {task['title']} — _{task['status']}_\n"

    await update.message.reply_text(message, parse_mode="Markdown")


async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Creates a new task.
    Usage:
    /addtask title | optional description | optional status
    """
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

    response = await create_task(payload)

    if response.status_code == 201:
        await update.message.reply_text("✅ Task created successfully")
    else:
        await update.message.reply_text(
            f"Failed to create task ({response.status_code})"
        )

async def update_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Updates the status of a task by its ID.
    Usage: /updatetask <task_id> <status>
    Example: /updatetask 5 completed
    """

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n/updatetask <task_id> <status>"
        )
        return

    task_id = context.args[0]
    status = context.args[1].lower()

    valid_statuses = {"pending", "in_progress", "completed"}

    if status not in valid_statuses:
        await update.message.reply_text(
            "Invalid status. Allowed values: pending, in_progress, completed"
        )
        return

    success = await update_task_status(task_id, status)

    if success:
        await update.message.reply_text("✅ Task updated successfully")
    else:
        await update.message.reply_text("❌ Failed to update task")