"""Исключения программы Droplet."""


class DropletError(Exception):
    """Базовое исключение для всех ошибок программы Droplet."""


class ProtocolError(DropletError):
    """Некорректные данные: адрес, сообщение или ответ сервера."""


class FileReadError(DropletError):
    """Не удалось найти или прочитать локальный файл."""
