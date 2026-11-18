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


def test_parse_args_ok():
    args = client.parse_args(
        ["test1.txt", "test2.txt", "--to", "198.51.100.50:8000"]
    )
    assert args.files == [Path("test1.txt"), Path("test2.txt")]
    assert args.to == "198.51.100.50:8000"


def test_parse_args_missing_to():
    with pytest.raises(SystemExit):
        client.parse_args(["test.txt"])


def test_main_ok(tmp_path, capsys):
    file = tmp_path / "file.txt"
    file.write_bytes(b"test")
    code = client.main([str(file), "--to", "198.51.100.50:8000"])
    assert code == 0
    assert "file.txt" in capsys.readouterr().out


def test_main_bad_address(tmp_path, capsys):
    file = tmp_path / "file.txt"
    file.write_bytes(b"test")
    code = client.main([str(file), "--to", "198.51.100.50:abc"])
    assert code == 1
    assert "Ошибка" in capsys.readouterr().err


def test_main_bad_port(tmp_path, capsys):
    file = tmp_path / "none.txt"
    code = client.main([str(file), "--to", "198.51.100.50:8000"])
    assert code == 1
    assert "Ошибка" in capsys.readouterr().err
