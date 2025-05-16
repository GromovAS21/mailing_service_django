"""Модуль моделей для БД."""

from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models


class Notification(models.Model):
    """Модель уведомлений."""

    class DelayChoices(models.IntegerChoices):
        """Варианты задержки уведомления."""

        NO_DELAY = 0, "Нет задержки"
        ONE_HOUR = 1, "Задержка 1 час"
        ONE_DAY = 2, "Задержка 1 день"

    message = models.TextField(
        vernose_name="Текст уведомления",
        validators=[
            MinLengthValidator(1, "Сообщение не может быть пустым"),
            MaxLengthValidator(1024, "Максимальная длина сообщения - 1024 символов"),
        ],
    )
    delay = models.IntegerField(
        choices=DelayChoices, default=DelayChoices.NO_DELAY, verbose_name="Задержка уведомления"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания уведомления")

    def __str__(self):
        """Возвращает номер идентификатор уведомления."""
        return f"Notification N {self.id}"
