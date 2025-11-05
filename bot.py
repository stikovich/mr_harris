import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
from datetime import datetime, timedelta

# Токен вашего бота
TOKEN = '8006784472:AAG_-QBmWNQRz46VQ21ydP1n7W1kxZZASU4'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Обработка команды /starttimer с указанием даты
    try:
        date_str = context.args[0]
        target_date = datetime.strptime(date_str, '%d.%m.%Y')  # Парсим введённую дату
    except (IndexError, ValueError):
        await update.message.reply_text('Использование: /starttimer DD.MM.YYYY')
        return
    
    chat_id = update.effective_chat.id
    current_time = datetime.now()
    delta = target_date - current_time
    total_seconds = max(delta.total_seconds(), 0)  # Проверяем, чтобы разница была положительной
    initial_message = await update.message.reply_text(f'ВОЗВРАЩЕНИЕ?: {target_date.strftime("%d.%m.%Y")}')

    async def edit_message():
        nonlocal total_seconds
        while total_seconds > 0:
            await asyncio.sleep(60)  # Ожидание одной минуты
            total_seconds -= 60     # Уменьшение общего количества секунд на 60
            days_left = total_seconds // (3600*24)              # Дни
            hours_left = (total_seconds % (3600*24)) // 3600   # Остаточные часы
            minutes_left = ((total_seconds % 3600) // 60)      # Минуты
            
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=initial_message.message_id,
                text=f'Увидимся через {days_left:.0f} дн. {hours_left:.0f} ч. {minutes_left:.0f} мин.'
            )
        
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=initial_message.message_id,
            text='Новый Год'
        )

    asyncio.create_task(edit_message())

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('starttimer', start_timer))
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()

