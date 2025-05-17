from datetime import datetime, timedelta, timezone
from typing import Optional, Union

from notifications.models import DeliveryLog, Notification, Recipient
from notifications.tasks import send_email_notification, send_telegram_notification


def get_time_delay(delay: int) -> timedelta:
    """
    Возвращает timedelta для заданной задержки.

    Args:
        delay(int): задержка отправки уведомления (0 - без задержки, 1 - через час, 2 - через день).
    Returns:
        timedelta: время задержки.
    """
    delay_mapping = {0: timedelta(0), 1: timedelta(hours=1), 2: timedelta(days=1)}
    return delay_mapping[delay]


def create_log(recipient: Recipient, notification: Notification, status: str, error: Optional[str]) -> None:
    """
    Создание записи в таблице DeliveryLog.

    Args:
        recipient(Recipient): объект получателя уведомления.
        notification(Notification): объект уведомления.
        status(bool): статус отправки уведомления (True - успешно, False - с ошибкой).
        error(str, optional): сообщение об ошибке, если статус False.
    Returns:
        None
    """
    log = DeliveryLog.objects.create(recipient=recipient, notification=notification)
    log.status = DeliveryLog.StatusChoices.SUCCESS if status else DeliveryLog.StatusChoices.FAILED
    log.error_message = error if not status else None
    log.save()


def send_notification(recipients: Union[str, int, list], message_id: int, delay: int) -> None:
    """
    Отправка уведомлений.

    Args:
        recipients(str, int, list): получатель уведомления (email-адрес или ID пользователя).
        message_id(int): ID сообщения уведомления.
        delay(int): задержка отправки уведомления (0 - без задержки, 1 - через час, 2 - через день).
    """
    if not isinstance(recipients, list):
        recipients = [recipients]

    for address in recipients:
        task_datetime = datetime.now(timezone.utc) + get_time_delay(delay)
        notification = Notification.objects.get(id=message_id)

        if isinstance(address, int):
            recipient = Recipient.objects.get(telegram_id=address)
        else:
            recipient = Recipient.objects.get(email=address)

        try:
            if recipient.telegram_id:
                send_telegram_notification.apply_async(
                    args=[recipient.telegram_id, notification.message], eta=task_datetime
                )
            else:
                send_email_notification.apply_async(args=[recipient.email, notification.message], eta=task_datetime)
            # Если сообщение отправлено успешно, создаем запись в БД с соответствующим логом
            create_log(recipient, notification, status=DeliveryLog.StatusChoices.SUCCESS, error=None)
        except Exception as e:
            # Если сообщение не отправлено, создаем запись в БД с соответствующим логом
            create_log(recipient, notification, status=DeliveryLog.StatusChoices.FAILED, error=str(e))
