"""Модуль моделей для БД."""

from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class Notification(models.Model):
    """Модель уведомлений."""

    class DelayChoices(models.IntegerChoices):
        """Варианты задержки уведомления."""

        NO_DELAY = 0, "Нет задержки"
        ONE_HOUR = 1, "Задержка 1 час"
        ONE_DAY = 2, "Задержка 1 день"

    message = models.TextField(
        verbose_name="Текст уведомления",
        validators=[
            MinLengthValidator(1, "Сообщение не может быть пустым"),
            MaxLengthValidator(1024, "Максимальная длина сообщения - 1024 символов"),
        ],
    )
    delay = models.IntegerField(
        choices=DelayChoices, default=DelayChoices.NO_DELAY, verbose_name="Задержка уведомления"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания уведомления")

    def __str__(self) -> str:
        """Возвращает номер идентификатор уведомления."""
        return f"Notification N {self.id}"


class Recipient(models.Model):
    """Модель получателей."""

    email = (
        models.EmailField(
            unique=True,
            verbose_name="Адрес получателя",
            blank=True,
            null=True,
        ),
    )
    telegram_id = models.PositiveBigIntegerField(
        unique=True,
        verbose_name="Telegram ID получателя",
        blank=True,
        null=True,
    )
    notification = models.ManyToManyField(
        Notification, related_name="recipients", verbose_name="Уведомления получателя", blank=True
    )

    def __str__(self) -> str:
        """Возвращает email или telegram_id получателя."""
        return self.email if self.email else f"{self.telegram_id}"

    def clean(self) -> None:
        """Проверяет, что введён либо email, либо telegram_id."""
        if self.email and self.telegram_id:
            raise ValidationError("Может быть введён только один адрес получателя: email или telegram_id")
        if not self.email and not self.telegram_id:
            raise ValidationError("Необходимо ввести адрес получателя: email или telegram_id")
