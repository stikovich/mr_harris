import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
from datetime import timedelta

# Ваш токен бота
TOKEN = 'YOUR_BOT_TOKEN'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Обработка команды /starttimer с указанием минут
    try:
        minutes = int(context.args[0])  # Теперь передаем минуты
    except IndexError:
        await update.message.reply_text("Использование: /starttimer MINUTES")
        return
    
    total_seconds = minutes * 60  # Переводим минуты в секунды
    chat_id = update.effective_chat.id
    message = await update.message.reply_text(f'Таймер запущен на {minutes} минут')

    async def edit_message():
        nonlocal total_seconds
        while total_seconds > 0:
            await asyncio.sleep(60)  # Ждем ровно одну минуту
            total_seconds -= 60      # Уменьшаем общее количество секунд на 60
            remaining_minutes = total_seconds // 60   # Получаем оставшиеся минуты
            remaining_time = f"{remaining_minutes} мин."
            
            if remaining_minutes <= 0:
                break  # Завершаем цикл, если осталось меньше минуты
                
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message.message_id,
                text=f'Оставшееся время: {remaining_time}'
            )
        
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message.message_id,
            text="Время вышло!"
        )

    asyncio.create_task(edit_message())

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('starttimer', start_timer))
    application.run_polling()

if __name__ == '__main__':
    main()





