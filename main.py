from telegram.ext import ApplicationBuilder, CommandHandler

from config import TOKEN
from handlers.common import say_hello
from handlers.tasks import get_tasks, add_task

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
