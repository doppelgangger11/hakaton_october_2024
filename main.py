import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import Message
import asyncio
from transformers import pipeline
from token_tg import TOKEN
import re
from keywords import CATEGORIES

# Токен Telegram-бота
API_TOKEN = TOKEN
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

def normalize_text(text):
    """Приводим текст к нижнему регистру и убираем знаки препинания."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Убираем все, кроме слов и пробелов
    return text

def classify_text(text):
    """Классифицируем текст на основе ключевых слов."""
    text = normalize_text(text)
    
    for category, data in CATEGORIES.items():
        if any(keyword in text for keyword in data['keywords']):
            return category, data['days']
    
    # Если ничего не подошло, возвращаем категорию "Другие вопросы"
    return 'Другие вопросы', CATEGORIES['Другие вопросы']['days']

# Обработчик текстовых сообщений
@router.message()
async def handle_message(message: Message):
    category, days = classify_text(message.text)

    if category != 'Другие вопросы':
        response = (
            f"Это обращение классифицировано как: '{category}'.\n"
            f"Срок выполнения: {days} дней."
        )
    else:
        response = (
            "Ваше сообщение не подошло под известные категории.\n"
            "Мы зарегистрировали его как 'Другие вопросы'."
        )

    await message.reply(response)

# Основная функция для запуска бота
async def main():
    dp.include_router(router)  # Подключаем маршрутизатор
    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем старые обновления
    await dp.start_polling(bot)  # Запускаем опрос

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())