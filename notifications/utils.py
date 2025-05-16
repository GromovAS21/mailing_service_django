import re
from datetime import datetime, timedelta, timezone
from typing import Union

from notifications.tasks import send_email_notification, send_telegram_notification


def is_email(address: str) -> bool:
    """
    Проверяет, является ли строка email-адресом.

    Args:
        address(str): строка для проверки.
    Returns:
        bool: True, если строка является email-адресом, иначе False.
    """
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, address) is not None


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


def send_notification(recipients: Union[str, int, list], message: str, delay: int) -> None:
    """
    Отправка уведомлений.

    Args:
        recipients(str, int, list): получатель уведомления (email-адрес или ID пользователя).
        message(str): сообщение уведомления.
        delay(int): задержка отправки уведомления (0 - без задержки, 1 - через час, 2 - через день).
    """
    if not isinstance(recipients, list):
        recipients = [recipients]

    for recipient in recipients:
        task_datetime = datetime.now(timezone.utc) + get_time_delay(delay)
        if isinstance(recipient, int):
            status, error = send_telegram_notification.apply_async(args=[recipient, message], eta=task_datetime)
        else:
            status, error = send_email_notification.apply_async(args=[recipient, message], eta=task_datetime)
