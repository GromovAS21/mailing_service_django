from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail

from config import settings


logger = get_task_logger(__name__)


@shared_task()
def send_email_notification(email: str, message: str) -> None:
    """Отправка уведомлений по электронной почте."""
    try:
        send_mail(subject="Уведомление", message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[email])
    except Exception as e:
        logger.error(e)


@shared_task()
def send_telegram_notification(telegram_id: int, message: str) -> None:
    """Отправка уведомлений в Telegram."""
    # try:
    #     # response = requests.post(
    #     #     f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
    #     #     data={"chat_id": telegram_id, "text": message},
    #     # )
    #     # response.raise_for_status()
    # except Exception as e:
    #     logger.error(e)
    pass
