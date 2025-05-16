import re


def is_email(address: str) -> bool:
    """Проверяет, является ли строка email-адресом."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, address) is not None
