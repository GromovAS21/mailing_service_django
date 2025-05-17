import re


def validate_is_email(address: str) -> bool:
    """
    Проверяет, является ли строка email-адресом.

    Args:
        address(str): строка для проверки.
    Returns:
        bool: True, если строка является email-адресом, иначе False.
    """
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, address) is not None


def validate_telegram_id(telegram_id: int) -> bool:
    """
    Проверяет, является ли строка Telegram ID корректным.

    Args:
        telegram_id(int): строка для проверки.
    Returns:
        bool: True, если строка является корректным Telegram ID, иначе False.
    """
    return 10 >= len(str(telegram_id)) >= 9
