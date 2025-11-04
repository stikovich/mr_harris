import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import time
import asyncio
from datetime import timedelta
import os
TOKEN = os.getenv('TOKEN')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Обработка команды /starttimer с указанием секунд
    try:
        seconds = int(context.args[0])
    except IndexError:
        await update.message.reply_text("Использование: /starttimer SECONDS")
        return
    
    chat_id = update.effective_chat.id
    message = await update.message.reply_text(f'Таймер запущен на {seconds} секунд')

    async def edit_message():
        nonlocal seconds
        while seconds > 0:
            await asyncio.sleep(1)
            seconds -= 1
            remaining_time = str(timedelta(seconds=seconds))
            await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=f'Оставшееся время: {remaining_time}')
        
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="Время вышло!")

    asyncio.create_task(edit_message())

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('starttimer', start_timer))
    application.run_polling()

if __name__ == '__main__':
    main()


