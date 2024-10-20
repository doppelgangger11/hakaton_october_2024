CATEGORIES = {
    'Открытый люк на дороге': {
        'keywords': ['люк', 'дорога', 'открытый', 'крышка'], 'days': 2
    },
    'Отключение электричества': {
        'keywords': ['электричество', 'свет', 'отключить'], 'days': 2
    },
    'Консультация по компетенции': {
        'keywords': ['консультация', 'совет', 'вопрос'], 'days': 2
    },
    'Вывоз ТБО': {
        'keywords': ['тбо', 'мусор', 'вывоз', 'уборка'], 'days': 3
    },
    'Уборка дворов (сан. очистка)': {
        'keywords': ['уборка', 'двор', 'саночистка'], 'days': 3
    },
    'Вывоз валки': {
        'keywords': ['валка', 'вывоз'], 'days': 3
    },
    'Вывоз веток': {
        'keywords': ['ветки', 'веток', 'вывоз', 'ветка', 'ветвь'], 'days': 5
    },
    'Ремонт и содержание автополива': {
        'keywords': ['автополив', 'ремонт', 'полив'], 'days': 5
    },
    'Освещение не работает': {
        'keywords': ['освещение', 'свет', 'фонарь', 'не работает'], 'days': 5
    },
    'Уборка улиц (сан. очистка)': {
        'keywords': ['уборка', 'улица', 'саночистка'], 'days': 5
    },
    'Санитарная обрезка': {
        'keywords': ['санитарная', 'обрезка', 'ветки'], 'days': 10
    },
    'Валка сухих/аварийных деревьев': {
        'keywords': ['дерево', 'сухое', 'аварийное', 'валка'], 'days': 10
    },
    'Ремонт детских элементов': {
        'keywords': ['детский', 'элемент', 'ремонт'], 'days': 10
    },
    'Ремонт сантехники/труб': {
        'keywords': ['ремонт', 'сантехника', 'труба', 'труб', 'трубы', 'вода', 'лужи', 'потоп', 'затопило'], 'days': 15
    },
    'Другие вопросы': {
        'keywords': ['вопрос', 'другое'], 'days': 5
    }
}
def classify_text(text):
    """Классифицирует текст по ключевым словам."""
    for category, data in CATEGORIES.items():
        if any(keyword in text.lower() for keyword in data['keywords']):
            return category, data['days']
    return 'Другие вопросы', 5




"""
from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from keywords import classify_text
from crm.views import save_message_to_db
import asyncio

# Настройте токен бота

bot = Bot(token=setings.TELEGRAM_BOT_TOKEN)
router = Router()

@router.message()
async def handle_message(message: Message):
    category, days = classify_text(message.text)
    save_message_to_db(
        title=message.text,
        creator=message.from_user.full_name,
        project="Default Project",
        category=category,
        days=days
    )
    await message.reply(f"Сообщение зарегистрировано: {category}. Срок выполнения: {days} дней.")

async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

class Command(BaseCommand):
    help = 'Запуск Telegram-бота'

    def handle(self, *args, **kwargs):
        asyncio.run(main())
"""