import re
from datetime import datetime, timedelta, timezone
from typing import Union

from notifications.tasks import send_email_notification, send_telegram_notification


def is_email(address: str) -> bool:
    """Проверяет, является ли строка email-адресом."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, address) is not None


def get_time_delay(delay: int) -> timedelta:
    """Возвращает timedelta для заданной задержки."""
    delay_mapping = {0: timedelta(0), 1: timedelta(hours=1), 2: timedelta(days=1)}
    return delay_mapping[delay]


def send_notification(recipients: Union[str, int, list], message: str, delay: int) -> None:
    """Отправка уведомлений."""
    if not isinstance(recipients, list):
        recipients = [recipients]

    for recipient in recipients:
        task_datetime = datetime.now(timezone.utc) + get_time_delay(delay)
        if isinstance(recipient, int):
            send_telegram_notification.apply_async(args=[recipient, message], eta=task_datetime)
        else:
            send_email_notification.apply_async(args=[recipient, message], eta=task_datetime)
