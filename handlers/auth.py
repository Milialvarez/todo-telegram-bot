from telegram import Update
from telegram.ext import ContextTypes

from services.backend import login
from sessions import user_sessions


async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Logs a user into the system and stores the JWT token in memory.
    Usage: /login email password
    """
    if len(context.args) != 2:
        await update.message.reply_text(
            "Usage:\n/login email password"
        )
        return

    email, password = context.args
    telegram_user_id = update.effective_user.id

    token = await login(email, password)

    if not token:
        await update.message.reply_text("❌ Invalid credentials")
        return

    user_sessions[telegram_user_id] = token

    await update.message.reply_text("✅ Login successful")


async def logout_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Logs the user out by removing the token from memory.
    """
    telegram_user_id = update.effective_user.id

    if telegram_user_id in user_sessions:
        del user_sessions[telegram_user_id]
        await update.message.reply_text("👋 Logged out successfully")
    else:
        await update.message.reply_text("You are not logged in")
