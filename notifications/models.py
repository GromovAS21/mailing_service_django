"""Модуль моделей для БД."""

from django.core.validators import MaxLengthValidator, MaxValueValidator, MinLengthValidator, MinValueValidator
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
    delay = models.IntegerField(choices=DelayChoices, verbose_name="Задержка уведомления")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания уведомления")

    def __str__(self) -> str:
        """Возвращает номер идентификатор уведомления."""
        return f"Notification N {self.id}"


class Recipient(models.Model):
    """Модель получателей."""

    email = models.EmailField(
        unique=True,
        verbose_name="Адрес получателя",
        blank=True,
        null=True,
    )
    telegram_id = models.PositiveIntegerField(
        unique=True,
        verbose_name="Telegram ID получателя",
        blank=True,
        null=True,
        validators=[MinValueValidator(100000000), MaxValueValidator(9999999999)],
    )
    notifications = models.ManyToManyField(
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


class DeliveryLog(models.Model):
    """Модель логов доставки уведомлений."""

    class StatusChoices(models.TextChoices):
        """Варианты статусов доставки уведомления."""

        SUCCESS = "success", "Успешно"
        FAILED = "failed", "Ошибка"

    notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, related_name="delivery_logs", verbose_name="Уведомление"
    )
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, verbose_name="Получатель")
    status = models.CharField(max_length=50, choices=StatusChoices, verbose_name="Статус доставки")
    error_message = models.TextField(blank=True, null=True, verbose_name="Сообщение об ошибке")

    def __str__(self) -> str:
        """Возвращает информацию о статусе доставки уведомления."""
        return f"Log for Notification {self.notification} for Recipient{self.recipient} - {self.status}"
