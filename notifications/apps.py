"""Модуль приложения для отправки уведомлений."""

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """Класс настройки приложения."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "notifications"
