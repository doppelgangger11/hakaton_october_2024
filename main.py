import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import Message
import asyncio
from transformers import pipeline
from token_tg import TOKEN

# Токен Telegram-бота
API_TOKEN = TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
router = Router()
dp = Dispatcher()

# Загрузка модели для классификации на русском
classifier = pipeline(
    "text-classification", 
    model="cointegrated/rubert-tiny2", 
    tokenizer="cointegrated/rubert-tiny2", 
    framework="pt"  # Используем PyTorch
)

# Функция для классификации сообщений
def is_request(message: str) -> bool:
    result = classifier(message)[0]
    print(result)
    label, score = result['label'], result['score']
    print(f"Классификация: {label}, Вероятность: {score}")  # Для отладки
    return label == 'LABEL_1' and score > 0.54  # Настройка порога вероятности

# Обработчик текстовых сообщений
@router.message()
async def handle_message(message: Message):
    if is_request(message.text):
        await message.reply("Это обращение. Спасибо! Мы зарегистрировали ваше сообщение.")
    else:
        await message.reply("Сообщение не классифицировано как обращение.")

# Основная функция для запуска бота
async def main():
    dp.include_router(router)  # Подключаем маршрутизатор
    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем старые обновления
    await dp.start_polling(bot)  # Запускаем опрос

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())