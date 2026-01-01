from telegram import Update
from telegram.ext import ContextTypes

async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Basic command to verify that the bot is running correctly.
    """
    await update.message.reply_text("Hello world")

async def get_usages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This command shows all the commands of the system and examples of usage of each one
    """

    message = (
    "🤖 *Help — Available Commands*\n\n"

    "👤 Authentication\n"
    "- /register username email password\n"
    "  Example: /register mili mili@mail.com 123456\n\n"
    "- /login email password\n"
    "  Example: /login mili@mail.com 123456\n\n"
    "- /logout\n"
    "  Example: /logout\n\n"

    "📝 Tasks\n"
    "- /tasks\n"
    "  Show all your tasks\n\n"
    "- /addtask title | description | status\n"
    "  Example: /addtask Buy milk | Go to the supermarket | pending\n\n"
    "- /updatetask task_id title | description | status\n"
    "  Examples:\n"
    "  /updatetask 5 New title | | completed\n"
    "  /updatetask 5 | New description |\n"
    "  /updatetask 5 | | in_progress\n\n"
    "- /deletetask task_id\n"
    "  Example: `/deletetask 3`\n\n"

    "⏰ Reminders\n"
    "- /reminders\n"
    "  Show all your reminders\n\n"
    "- /addreminder YYYY-MM-DD | description\n"
    "  Example: /addreminder 2025-09-01 | Pay rent\n\n"
    "- /updatereminder reminder_id date | description\n"
    "  Examples:\n"
    "  /updatereminder 2 2025-10-01 |\n"
    "  /updatereminder 2 | Doctor appointment\n\n"
    "- /deletereminder reminder_id\n"
    "  Example: /deletereminder 2\n\n"

    "✨ Tip: You must be logged in to manage tasks and reminders.\n"
)


    await update.message.reply_text(message)


