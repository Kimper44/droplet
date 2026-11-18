"""Клиент Droplet: отправка файлов на устройство в локальной сети."""

import argparse
import hashlib
import sys
from pathlib import Path

from errors import DropletError, FileReadError, ProtocolError

CHUNK_SIZE = 64 * 1024


def parse_address(address: str) -> tuple[str, int]:
    """Разбирает адрес получателя вида «хост:порт».

    Args:
        address: Адрес в формате ``"198.51.100.15:8000"``.

    Returns:
        Кортеж из хоста и номера порта.

    Raises:
        ProtocolError: Если формат адреса неверный или порт
            вне диапазона 1-65535.
    """
    address = address.strip()
    if address.count(":") != 1:
        raise ProtocolError(
            f"Адрес должен быть в формате «хост:порт», получено: {address}"
        )

    host, port_text = address.rsplit(":", 1)
    if not host:
        raise ProtocolError(f"Не указан хост в адресе: {address}")
    if not port_text:
        raise ProtocolError(f"Не указан порт в адресе: {address}")
    try:
        port = int(port_text)
    except ValueError as err:
        raise ProtocolError(f"Порт должен быть числом: {port_text}") from err
    if not 1 <= port <= 65535:
        raise ProtocolError(f"Порт вне диапазона 1-65535: {port}")

    return host, port


def file_sha256(path: str | Path) -> str:
    """Вычисляет контрольную сумму SHA-256 файла.

    Файл читается частями размером CHUNK_SIZE, поэтому функция
    подходит и для больших файлов.

    Args:
        path: Путь к файлу (строка или Path).

    Returns:
        Контрольная сумма в виде строки из 64 шестнадцатеричных символов.

    Raises:
        FileReadError: Если файл не существует, является папкой
            или не может быть прочитан.
    """
    path = Path(path)
    if not path.is_file():
        raise FileReadError(f"Файл не найден: {path}")

    hasher = hashlib.sha256()
    try:
        with path.open("rb") as f:
            while chunk := f.read(CHUNK_SIZE):
                hasher.update(chunk)
    except OSError as err:
        raise FileReadError(f"Не удалось прочитать файл: {path}") from err

    return hasher.hexdigest()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Разбирает аргументы командной строки

    Args:
        argv: Список аргументов без имени программы. Если ``None``,
            берутся аргументы, с которыми запущена программа.

    Returns:
        Объект с полями ``files`` (список путей)
            и ``to`` (адрес получателя в формате «хост:порт»).
    """
    parser = argparse.ArgumentParser(
        description="Отправка файлов на устройство Droplet в локальной сети"
    )
    parser.add_argument(
        "files", nargs="+", type=Path, help="путь к файлам для отправки"
    )
    parser.add_argument(
        "--to", required=True, help="адрес получателя в формате «хост:порт»"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Точка входа клиента: проверяет аргументы и готовит файлы к отправке.

    Args:
        argv: Список аргументов без имени программы. Если ``None``,
            берутся аргументы, с которыми запущена программа.

    Returns:
        Код завершения: 0 при успехе, 1 при ошибке.
    """
    args = parse_args(argv)
    try:
        host, port = parse_address(args.to)
        print(f"Вычисление SHA-256 для {len(args.files)} файла(-ов)...")
        for path in args.files:
            file_hash = file_sha256(path)
            print(f"    {path.name}: SHA-256 {file_hash}")
        print(f"Получатель:\n    Хост: {host}\n    Порт: {port}")
    except DropletError as err:
        print(f"Ошибка: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
