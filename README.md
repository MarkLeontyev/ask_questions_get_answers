# Modular FastAPI App

Модульное приложение на FastAPI с SQLAlchemy, Pydantic, Postgres (в Docker) и тестами pytest.

## Быстрый старт (Docker)

1. Перейдите в каталог:
   ```bash
   cd ask_questions_get_answers/backend
   ```
2. Запустите:
   ```bash
   docker compose up --build
   ```
3. Откройте `http://localhost:8000/docs` для Swagger UI.

Переменные окружения: см. `docker-compose.yml` (переменная `DATABASE_URL`).

## Тесты

```bash
pytest
```

## Структура
- `backend/` — сервис API (FastAPI)
  - `app/main.py` — вход приложения, подключение роутера
  - `app/api/router.py` — маршруты API (вопросы/ответы)
  - `app/core/config.py` — конфигурация (`DATABASE_URL` и др.)
  - `app/db/base.py` — базовый класс `Base` для моделей
  - `app/db/session.py` — `engine`, `SessionLocal`, зависимость `get_db`
  - `app/models/` — модели SQLAlchemy: `questions.py`, `answers.py`
  - `app/schemas/` — Pydantic-схемы: `question.py`, `answer.py`
  - `app/crud/` — бизнес-логика CRUD: `question.py`, `answer.py`
  - `tests/` — интеграционные тесты pytest: `conftest.py`, `test_questions.py`, `test_answers.py`
  - `requirements.txt` — зависимости
  - `pytest.ini` — настройки pytest
  - `Dockerfile`, `docker-compose.yml` — контейнеризация
