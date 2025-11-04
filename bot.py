import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.error import RetryAfter
import asyncio
from datetime import timedelta
import os

TOKEN = os.getenv('TOKEN')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            try:
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                return

            seconds -= 1
            remaining_time = str(timedelta(seconds=seconds))

            while True:
                try:
                    await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message.message_id,
                        text=f'Оставшееся время: {remaining_time}'
                    )
                    break
                except RetryAfter as e:
                    wait_time = min(e.retry_after, 5)  # ограничиваем время ожидания максимум 5 сек
                    logger.warning(f"Превышение лимита запросов. Ждем {wait_time} секунд.")
                    # Вычитаем время ожидания из таймера
                    seconds -= int(wait_time)
                    if seconds < 0:
                        seconds = 0
                    await asyncio.sleep(wait_time)

        while True:
            try:
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message.message_id,
                    text="Время вышло!"
                )
                break
            except RetryAfter as e:
                wait_time = min(e.retry_after, 5)
                logger.warning(f"Превышение лимита запросов. Ждем {wait_time} секунд.")
                await asyncio.sleep(wait_time)

    asyncio.create_task(edit_message())

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('starttimer', start_timer))
    application.run_polling()

if __name__ == '__main__':
    main()


