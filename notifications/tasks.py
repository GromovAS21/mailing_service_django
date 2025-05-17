import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail

from config import settings
from config.settings import TELEGRAM_BOT_TOKEN


logger = get_task_logger(__name__)  # логгер для отслеживания ошибок в задачах


@shared_task()
def send_email_notification(email: str, message: str) -> None:
    """
    Отправка уведомлений по электронной почте.

    Args:
        email (str): адрес электронной почты.
        message (str): текст уведомления.
    Returns:
        None.
    """
    try:
        send_mail(subject="Уведомление", message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[email])
    except Exception as e:
        logger.error(e)


@shared_task()
def send_telegram_notification(telegram_id: int, message: str) -> None:
    """
    Отправка уведомлений в Telegram.

    Args:
        telegram_id (int): идентификатор пользователя Telegram.
        message (str): текст уведомления.
    Returns:
        None.
    """
    try:
        params = {"chat_id": telegram_id, "text": message}
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", params=params)
    except Exception as e:
        logger.error(e)
    pass
