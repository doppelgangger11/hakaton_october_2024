from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User, AbstractUser  # для связи с пользователями
from django.db import models


class User_tg(AbstractUser):
    telegram_id = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)  # Разрешаем пустые значения
    username = models.CharField(max_length=255, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_tg_set',  # Уникальное имя обратной ссылки для групп
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_tg_permissions_set',  # Уникальное имя обратной ссылки для разрешений
        blank=True,
    )

    class Meta:
        verbose_name = "Telegram User"
        verbose_name_plural = "Telegram Users"

    def __str__(self):
        return self.username

class Task(models.Model):
    # Поля задачи
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)  # Название
    description = models.TextField(blank=True, null=True)  # Описание
    last_activity = models.DateTimeField(blank=True, null=True)  # Последняя активность
    deadline = models.DateTimeField(blank=True, null=True)  # Крайний срок
    creator = models.ForeignKey(User_tg, related_name='created_tasks', on_delete=models.SET_NULL, null=True, blank=True)  # Постановщик
    assignee = models.ForeignKey(User_tg, related_name='assigned_tasks', on_delete=models.SET_NULL, null=True, blank=True)  # Исполнитель
    co_executors = models.ManyToManyField(User_tg, related_name='coexecutors_tasks', blank=True)  # Соисполнители
    observers = models.ManyToManyField(User_tg, related_name='observed_tasks', blank=True)  # Наблюдатели

    # Статус задачи
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')  # Статус

    project = models.CharField(max_length=255, blank=True, null=True)  # Проект
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    start_date = models.DateTimeField(blank=True, null=True)  # Дата начала работы
    updated_at = models.DateTimeField(auto_now=True)  # Дата изменения
    closed_at = models.DateTimeField(blank=True, null=True)  # Дата закрытия
    planned_duration = models.CharField(max_length=255, blank=True, null=True)  # Планируемая длительность
    consider_working_hours = models.BooleanField(default=False)  # Учитывать рабочее время
    estimate = models.FloatField(blank=True, null=True)  # Оценка
    deadline_change_allowed = models.BooleanField(default=False)  # Разрешено изменять крайний срок
    time_spent = models.DurationField(blank=True, null=True)  # Затрачено
    tags = models.CharField(max_length=255, blank=True, null=True)  # Теги
    lead = models.CharField(max_length=255, blank=True, null=True)  # Лид
    contact = models.CharField(max_length=255, blank=True, null=True)  # Контакт
    company = models.CharField(max_length=255, blank=True, null=True)  # Компания
    deal = models.CharField(max_length=255, blank=True, null=True)  # Сделка
    crm = models.CharField(max_length=255, blank=True, null=True)  # CRM

    # Связь с базовой задачей
    base_task_id = models.IntegerField(blank=True, null=True)  # ID базовой задачи
    base_task_title = models.CharField(max_length=255, blank=True, null=True)  # Название базовой задачи
    flow = models.CharField(max_length=255, blank=True, null=True)  # Поток

    def __str__(self):
        return self.title