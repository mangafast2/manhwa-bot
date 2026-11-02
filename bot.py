import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")

CHAPTERS = {
    "chapter_1": [],
    "chapter_2": [],
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "سلام! 👋\n"
            "به ربات مانگا هنتای خوش اومدی.\n\n"
            "برای دریافت چپتر، از لینک همان چپتر در کانال وارد ربات شو."
        )
        return

    chapter = context.args[0]

    if chapter not in CHAPTERS:
        await update.message.reply_text("این چپتر پیدا نشد!")
        return

    messages = CHAPTERS[chapter]

    if not messages:
        await update.message.reply_text(
            "این چپتر هنوز آماده نیست. لطفاً بعداً دوباره امتحان کن."
        )
        return

    for message_id in messages:
        await context.bot.copy_message(
            chat_id=update.effective_chat.id,
            from_chat_id=SOURCE_CHANNEL,
            message_id=message_id,
        )

def main():
    if not BOT_TOKEN or not SOURCE_CHANNEL:
        raise RuntimeError("BOT_TOKEN and SOURCE_CHANNEL must be configured.")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
