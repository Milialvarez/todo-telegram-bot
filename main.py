from telegram.ext import ApplicationBuilder, CommandHandler

from config import TOKEN
from handlers.auth import login_command, logout_command, register_command
from handlers.common import get_usages, say_hello
from handlers.reminders import add_reminder, delete_reminder, get_reminders, update_reminder
from handlers.tasks import delete_task, get_tasks, add_task, update_task

def main():
    """
    Application entry point.
    Registers command handlers and starts polling.
    """
    application = ApplicationBuilder().token(TOKEN).build()

    # auth commands
    application.add_handler(CommandHandler("start", say_hello))
    application.add_handler(CommandHandler("login", login_command))
    application.add_handler(CommandHandler("logout", logout_command))
    application.add_handler(CommandHandler("register", register_command))

    #tasks commands
    application.add_handler(CommandHandler("tasks", get_tasks))
    application.add_handler(CommandHandler("addtask", add_task))
    application.add_handler(CommandHandler("updatetask", update_task))
    application.add_handler(CommandHandler("deleteTask", delete_task))
    

    #reminder commands

    application.add_handler(CommandHandler("reminders", get_reminders))
    application.add_handler(CommandHandler("addreminder", add_reminder))
    application.add_handler(CommandHandler("updatereminder", update_reminder))
    application.add_handler(CommandHandler("deletereminder", delete_reminder))

    #help

    application.add_handler(CommandHandler("help", get_usages))

    application.run_polling()

if __name__ == "__main__":
    main()
