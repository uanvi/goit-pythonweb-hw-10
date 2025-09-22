# Contacts API

REST API для управління контактами на FastAPI + SQLAlchemy + PostgreSQL.

## Швидкий старт

```bash
# Клонувати та перейти в папку
git clone <repository-url>
cd goit-pythonweb-hw-04

# Створити .env файл
cp .env.example .env

# Запустити через Docker
docker-compose up -d

# Застосувати міграції
docker-compose exec app alembic upgrade head
```

## API Endpoints

- `POST /contacts/` - Створити контакт
- `GET /contacts/` - Список контактів (з пошуком)
- `GET /contacts/{id}` - Отримати контакт
- `PUT /contacts/{id}` - Оновити контакт
- `DELETE /contacts/{id}` - Видалити контакт
- `GET /contacts/birthdays/upcoming` - Дні народження (7 днів)

## Пошук контактів

```bash
GET /contacts/?first_name=John&last_name=Doe&email=john
```

## Документація

- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Локальна розробка

```bash
# Встановити залежності
pip install -r requirements.txt

# Запустити PostgreSQL
docker run -d --name postgres -p 5433:5432 \
  -e POSTGRES_USER=contacts_user \
  -e POSTGRES_PASSWORD=contacts_password \
  -e POSTGRES_DB=contacts_db \
  postgres:15

# Міграції
alembic upgrade head

# Запустити API
uvicorn src.main:app --reload
```

## Технології

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- Docker
