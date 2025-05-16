"""Модель сериализаторов для модели уведомлений."""

from typing import List

from rest_framework import serializers

from notifications.models import Notification, Recipient
from notifications.utils import is_email


class RecipientField(serializers.Field):
    """Поле получателя уведомления."""

    def to_internal_value(self, data) -> List[str]:
        """Преобразование получателя в список."""
        if isinstance(data, (str, int)):
            return [data]
        elif isinstance(data, list):
            return data


class NotificationSerializer(serializers.ModelSerializer):
    """Сериализатор уведомления."""

    recipient = RecipientField(write_only=True)

    class Meta:
        """Метаданные сериализатора."""

        model = Notification
        fields = ("message", "recipient", "delay")
        extra_kwargs = {"message": {"required": True}, "delay": {"required": True}}

    def create(self, validated_data) -> Notification:
        """
        Создание уведомления и получателей уведомления.

        Args:
            validated_data: Валидированные данные.
        Returns:
            Созданное уведомление.
        """
        recipients = validated_data.pop("recipient")
        notification = Notification.objects.create(**validated_data)

        for address in recipients:
            if isinstance(address, int):
                recipient, created = Recipient.objects.get_or_create(telegram_id=address)
                recipient.notifications.add(notification)
            elif is_email(address):
                recipient, created = Recipient.objects.get_or_create(email=address)
                recipient.notifications.add(notification)
            else:
                raise serializers.ValidationError({"recipient": "Невалидный адрес получателя."})
        return notification
