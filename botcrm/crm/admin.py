from django.contrib import admin
from .models import Task

# Register your models here.

# Создаем класс для кастомизации отображения модели в админке
class TaskAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в списке задач
    list_display = ('title', 'status', 'creator', 'assignee', 'deadline', 'created_at')
    # Поля, по которым можно фильтровать задачи
    list_filter = ('status', 'creator', 'assignee', 'deadline')
    # Поля, по которым можно искать задачи
    search_fields = ('title', 'description', 'creator__username', 'assignee__username', 'tags')
    # Поля, которые будут доступны только для просмотра, а не для редактирования
    readonly_fields = ('created_at', 'updated_at', 'closed_at')

# Регистрируем модель Task и класс администрирования TaskAdmin
admin.site.register(Task, TaskAdmin)