# Установка инструментов

## Git

Планируемые команды в Ubuntu Server:

```bash
sudo apt update
sudo apt install -y git
git --version
```

**Результат:** не проверено. Версию Git нужно записать после выполнения команды.

## Python и виртуальное окружение

Планируемые команды:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
python3 --version
python3 -m pip --version
python3 -m venv .venv
source .venv/bin/activate
which python
```

**Результат:** в Ubuntu Server пока не выполнялось.

## Зависимости проекта

В репозитории в файле `Мой проект/requirements.txt` указаны:

```text
gigachat==0.2.3
python-dotenv==1.0.1
```

После перехода в папку проекта и активации `.venv`:

```bash
python -m pip install -r requirements.txt
python -m pip list
python -m pip check
```

**Результат установки и pip check:** не проверено в Ubuntu Server.

## Конфигурация

В коде используются переменные `GIGACHAT_CREDENTIALS` и `GIGACHAT_SCOPE`. Файл `.env.example` по ожидаемому пути `Мой проект/.env.example` при проверке репозитория не найден. Поэтому нельзя копировать его командой `cp .env.example .env`, пока шаблон не будет создан или не будет проверен фактический способ передачи переменных.

Не публиковать реальные ключи и файл `.env`. Если ключи будут вводиться в Ubuntu, хранить их только локально.

## Ошибки и исправления

Ошибки установки пока не зафиксированы, поскольку установка в Ubuntu ещё не выполнялась. После проверки сюда нужно добавить точный текст каждой ошибки и выполненные действия.
