# Блог на FastAPI  

🚀 **Современное веб-приложение для ведения блога** с аутентификацией, асинхронными задачами и эффективным управлением данными.  

## 📌 Основные возможности  

- **Регистрация и аутентификация** через `fastapi-users` (JWT, OAuth2)  
- **CRUD для постов (категорий и тегов), комментариев и реакций на комментарии**  
- **Деревья комментариев**
- **Система лайков/дизлайков на посты**
- **Подсчетов просмотров постов**
- **Асинхронные задачи** (Celery + Redis): отправка email-уведомлений, обработка медиа  
- **Реляционная база данных** (PostgreSQL) с миграциями через Alembic  
- **Высокая производительность** благодаря асинхронному FastAPI  
- **Кеширование** (Redis) для ускорения работы  

## 🛠 Технологический стек  

- **Backend**: FastAPI (+ fastapi-users)  
- **База данных**: PostgreSQL (+ SQLAlchemy ORM, Alembic для миграций)  
- **Асинхронные задачи**: Celery + Redis (брокер и кеш)  
- **Аутентификация**: JWT, OAuth2 (через `fastapi-users`)  
- **Деплой**: Docker (опционально)  

## ⚙️ Установка и запуск  

1. **Клонировать репозиторий**  
   ```bash  
   git clone https://github.com/ваш-репозиторий/blog-fastapi.git  
   cd blog-fastapi 
   
2. **Настройка окружения**
   
   Создать .env файл на основе .env.example:

   DATABASE_URL=postgresql+asyncpg://user:password@localhost/blog_db  
   REDIS_URL=redis://localhost:6379  
   SECRET_KEY=your-secret-key

3. **Запуск контейнеров (Docker)**
    ```bash
   docker-compose up -d  
Или вручную:
- Установить зависимости: pip install -r requirements.txt

- Запустить Postgres + Redis

- Применить миграции: alembic upgrade head

- Запустить FastAPI: uvicorn app.main:app --reload

- Запустить Celery: celery -A app.tasks.celery_app worker --loglevel=info

4. **Документация API**

   После запуска документация доступна по адресу:

    **Swagger**: http://localhost:8000/docs

    **ReDoc**: http://localhost:8000/redoc


Автор: Yegor Kozinov

Версия: 1.0.0