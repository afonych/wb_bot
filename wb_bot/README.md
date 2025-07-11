# Wildberries Review Answer Bot

Telegram-бот для автоматизации ответов на отзывы покупателей Wildberries с помощью ИИ и официального API маркетплейса.

## Основные возможности
- Получение неотвеченных отзывов через WB API
- Генерация ответов с помощью OpenAI
- Подтверждение/редактирование ответов через Telegram
- Хранение данных в Supabase

## Быстрый старт
1. Клонируйте репозиторий
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Запустите бота:
   ```bash
   python bot/main.py
   ```

## Структура проекта
- `bot/` — логика Telegram-бота
- `wb_api/` — работа с Wildberries API
- `ai/` — генерация ответов через OpenAI
- `db/` — работа с Supabase
- `scheduler/` — планировщик задач 