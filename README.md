# Droplet

[English](#en) | [Русский](#ru)

<a name="en"></a>

Local network file sharing over HTTP with automatic device discovery via UDP.

Droplet lets you send files between computers on the same local network without cables, cloud services or a central server. Devices find each other automatically, the receiver confirms each transfer, and file integrity is verified with SHA-256.

> 🚧 The project is in active development.

## Project structure

```
droplet/
├── server.py          # HTTP server that receives files
├── client.py          # HTTP client that sends files
├── discovery.py       # UDP device discovery
├── gui.py             # Graphical interface
├── tests/             # Tests
└── requirements.txt   # Dependencies
```

## Tech stack

- [Flask](https://flask.palletsprojects.com/) — HTTP server
- [Requests](https://requests.readthedocs.io/) — HTTP client
- [tqdm](https://tqdm.github.io/) — progress bar
- `socket`, `hashlib`, `threading` — Python standard library

## Team

- Vnukov Alexander — role
- Pastushkova Sofya — role
- Simakov Kirill — role

Course project for the AIP course, MIEM HSE University, 2026.

---

<a name="ru"></a>

## Droplet — русская версия

Передача файлов по локальной сети через HTTP с автоматическим обнаружением устройств по UDP.

Droplet позволяет пересылать файлы между компьютерами в одной локальной сети без проводов, облачных сервисов и центрального сервера. Устройства находят друг друга автоматически, получатель подтверждает каждую передачу, а целостность файла проверяется по хэшу SHA-256.

> 🚧 Проект в активной разработке.

### Структура проекта

```
droplet/
├── server.py          # HTTP-сервер для приёма файлов
├── client.py          # HTTP-клиент для отправки файлов
├── discovery.py       # Обнаружение устройств по UDP
├── gui.py             # Графический интерфейс
├── tests/             # Тесты
└── requirements.txt   # Зависимости
```

### Технологии

- [Flask](https://flask.palletsprojects.com/) — HTTP-сервер
- [Requests](https://requests.readthedocs.io/) — HTTP-клиент
- [tqdm](https://tqdm.github.io/) — прогресс-бар
- `socket`, `hashlib`, `threading` — стандартная библиотека Python

### Команда

- Внуков Александр — роль
- Пастушкова Софья О. — роль
- Симаков Кирилл С. — роль

Учебный проект по предмету «АИП», МИЭМ НИУ ВШЭ, 2026.