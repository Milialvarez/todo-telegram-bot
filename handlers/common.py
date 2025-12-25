from telegram import Update
from telegram.ext import ContextTypes

async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Basic command to verify that the bot is running correctly.
    """
    await update.message.reply_text("Hello world")
