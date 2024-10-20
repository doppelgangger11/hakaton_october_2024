from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from crm.keywords import classify_text
from django.conf import settings 
from crm.views import save_message_to_db
import asyncio

# Настройте токен бота

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
router = Router()

@router.message()
async def handle_message(message: Message):
    try:
        category, days = classify_text(message.text)


        # Сохранение сообщения в базу данных
        await save_message_to_db(
            title=message.text,
            creator=message.from_user,  # Передаем объект Telegram User
            category=category,
            days=days
        )

        await message.reply(f"Сообщение зарегистрировано: {category}. Срок выполнения: {days} дней.")
    except Exception as e:
        await message.reply("Произошла ошибка при обработке вашего сообщения.")
        print(f"Ошибка: {e}")  # Логируйте ошибку для дальнейшего анализа

async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

class Command(BaseCommand):
    help = 'Запуск Telegram-бота'

    def handle(self, *args, **kwargs):
        asyncio.run(main())