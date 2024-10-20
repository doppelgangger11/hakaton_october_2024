from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Update
import asyncio
from crm.keywords import classify_text
from django.conf import settings
from crm.models import Task, User_tg
from django.utils.timezone import now
from datetime import timedelta
from asgiref.sync import sync_to_async
from datetime import datetime

# Инициализация бота
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
router = Router()

# Обработчик сообщений бота (как в вашем коде)
@dp.message()
async def handle_message(message):
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
"""
@csrf_exempt  # Отключаем проверку CSRF для Webhook
def telegram_webhook(request):
    # Обрабатывает входящие запросы Webhook от Telegram
    if request.method == 'POST':
        update = Update.parse_raw(request.body)
        asyncio.run(dp.process_update(update)) # type: ignore
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'invalid request'}, status=400)
"""

from asgiref.sync import sync_to_async

@sync_to_async
def get_or_create_user(creator):
    print(f"Creating or getting user: {creator.id}, {creator.first_name}, {creator.last_name}, {creator.username}")
    user, _ = User_tg.objects.get_or_create(
        telegram_id=creator.id,
        defaults={
            'first_name': creator.first_name,
            'last_name': creator.last_name or '',
            'username': creator.username or '',
        },
    )

    print(f"Creating or getting user: {creator.id}, {creator.first_name}, {creator.last_name}")
    return user

@sync_to_async
def create_task(title, creator_user, description, days):
    """Создает новую задачу в базе данных."""
    if not isinstance(days, int):
        raise ValueError("days должно быть целым числом")
    
    print(f"Days: {days}, Type: {type(days)}")

    # Убедитесь, что days является целым числом и > 0
    if days <= 0:
        raise ValueError("Срок выполнения должен быть положительным числом")
    
    # Вычисляем дату дедлайна
    deadline = datetime.now() + timedelta(days=days)
    
    Task.objects.create(
        title=title,
        description=description,
        creator=creator_user,
        assignee=creator_user,  # Или назначьте другого пользователя
        status="In Progress",  # Пример статуса
        planned_duration=days
    )

async def save_message_to_db(title, creator, description, category, days):
    """Сохраняет сообщение в базу данных как задачу."""
    creator_user = await get_or_create_user(creator)  # Получаем пользователя из БД
    await create_task(title, creator_user, description, days)  # Создаем задачу