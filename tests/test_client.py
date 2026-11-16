"""Тесты для модуля client."""

import hashlib
from pathlib import Path

import pytest

import client
from errors import ProtocolError, FileReadError


def test_parse_address_ok():
    result = client.parse_address("198.51.100.25:8000")
    assert result == ("198.51.100.25", 8000)


def test_parse_address_no_colon():
    with pytest.raises(ProtocolError):
        client.parse_address("198.51.100.25")


def test_parse_address_extra_colon():
    with pytest.raises(ProtocolError):
        client.parse_address("198.51.100.25:8000:8000")


def test_parse_address_empty_host():
    with pytest.raises(ProtocolError):
        client.parse_address(":8000")


def test_parse_address_empty_port():
    with pytest.raises(ProtocolError):
        client.parse_address("198.51.100.25:")


def test_parse_address_port_not_number():
    with pytest.raises(ProtocolError):
        client.parse_address("198.51.100.25:abc")


def test_parse_address_port_out_of_range():
    with pytest.raises(ProtocolError):
        client.parse_address("198.51.100.25:80000")


def test_file_sha256_ok(tmp_path):
    file = tmp_path / "file.txt"
    file.write_bytes(b"test")
    assert client.file_sha256(file) == hashlib.sha256(b"test").hexdigest()


def test_file_sha256_ok_str_path(tmp_path):
    file = tmp_path / "file.txt"
    file.write_bytes(b"test")
    file_str = str(file)
    assert client.file_sha256(file_str) == hashlib.sha256(b"test").hexdigest()


def test_file_sha256_large(tmp_path):
    data = b"x" * 200_000
    file = tmp_path / "file.txt"
    file.write_bytes(data)
    assert client.file_sha256(file) == hashlib.sha256(data).hexdigest()


def test_file_sha256_empty(tmp_path):
    data = b""
    file = tmp_path / "file.txt"
    file.write_bytes(data)
    assert client.file_sha256(file) == hashlib.sha256(data).hexdigest()


def test_file_sha256_missing(tmp_path):
    with pytest.raises(FileReadError):
        client.file_sha256(tmp_path / "nope.txt")


def test_file_sha256_directory(tmp_path):
    with pytest.raises(FileReadError):
        client.file_sha256(tmp_path)


def test_file_sha256_read_error(tmp_path, monkeypatch):
    file = tmp_path / "file.txt"
    file.write_bytes(b"test")

    def broken_open(self, *args, **kwargs):
        raise PermissionError(f"Отказано в доступе: {file}")

    monkeypatch.setattr(Path, "open", broken_open)

    with pytest.raises(FileReadError):
        client.file_sha256(file)
