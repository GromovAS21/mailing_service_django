"""Модель сериализаторов для модели уведомлений."""

from typing import List, Union

from rest_framework import serializers

from notifications.models import Notification, Recipient


class NotificationSerializer(serializers.Serializer):
    """Сериализатор уведомления."""

    recipient = serializers.ListField(child=serializers.CharField(max_length=150), write_only=True)

    class Meta:
        """Метаданные сериализатора."""

        model = Notification
        fields = ("message", "recipient", "delay")

    def validate_recipient(self, value: Union[str, list]) -> List[str]:
        """
        Валидация поля получателей на наличие одного получателя или списка получателей.

        Args:
            value (Union[str, list]): Один получатель или список получателей.

        Returns:
            List[str]: Список получателей.
        """
        if isinstance(value, str):
            return [value]
        return value

    def create(self, validated_data) -> Notification:
        """Создание уведомления и получателей уведомления."""
        recipients = validated_data.pop("recipient")
        notification = Notification.objects.create(**validated_data)

        for address in recipients:
            if isinstance(address, str):
                recipient, created = Recipient.objects.get_or_create(email=address)
                recipient.notifications.add(notification)
            else:
                recipient, created = Recipient.objects.get_or_create(telegram_id=address)
                recipient.notifications.add(notification)

        return notification
