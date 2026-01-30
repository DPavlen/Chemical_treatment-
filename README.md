# Chemical-treatment

## 1. [Описание проекта](#1)
## 2. [Функционал API и технические особенности](#2)
## 3. [Стек технологий](#3)
## 4. [Запуск проекта через Docker Compose](#4)
## 5. [Автор проекта](#5)

## 1. Описание проекта <a id=1></a>

__API-сервис для рендеринга химических структур:__
- Визуализация молекул из SMILES-строк и MOL-файлов
- Поддержка форматов PNG и SVG
- Настраиваемые размеры изображений
- Возможность скачивания результата

__Аутентификация (JWT):__
- Регистрация новых пользователей
- Получение и обновление JWT-токенов
- Привязка запросов к пользователям

__Логирование запросов (RequestLog):__
- Автоматическая запись всех API-запросов в базу данных
- Фиксируются: пользователь, SMILES, формат, размеры, время ответа, статус
- Просмотр истории через Django Admin

## 2. Функционал API и технические особенности <a id=2></a>

__Документация API:__
- http://localhost:8000/api/v1/swagger/ — автоматическая генерация документации с помощью Swagger
- http://localhost:8000/api/v1/redoc/ — документация с помощью ReDoc

__Реализована JWT-аутентификация:__
<details>
    <summary>Эндпоинты аутентификации</summary>
    <ul>
     <li>POST /api/v1/auth/register/ — Регистрация нового пользователя</li>
     <li>POST /api/v1/auth/token/ — Получение JWT токена (логин)</li>
     <li>POST /api/v1/auth/token/refresh/ — Обновление токена</li>
    </ul>
</details>

__Реализована работа с химическими структурами:__
<details>
    <summary>Эндпоинты рендеринга молекул</summary>
    <ul>
     <li>GET /api/v1/answer/?smiles=CCO&format=png — Рендеринг из SMILES строки</li>
     <li>POST /api/v1/answer/ — Рендеринг из SMILES или MOL-файла</li>
    </ul>
</details>

__Параметры запроса:__
- `smiles` (обязательный) — SMILES-строка молекулы (например: CCO для этанола)
- `format` — формат изображения: `png`, `svg` (по умолчанию `png`)
- `width` — ширина изображения в пикселях
- `height` — высота изображения в пикселях
- `download` — `true` для скачивания файла

__Логирование в RequestLog:__
- Все запросы автоматически сохраняются в базу данных
- Записываются: пользователь, HTTP метод, SMILES, наличие MOL-файла, размеры, формат, статус, ошибка, время ответа (мс), User-Agent
- Просмотр в Django Admin: http://localhost:8000/admin/chemicals/requestlog/

## 3. Стек технологий <a id=3></a>

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-6495ED?style=flat-square&logo=django)](https://www.djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.15-6495ED?style=flat-square)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16_alpine-blue?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/Nginx-1.22.1-green?style=flat-square&logo=nginx)](https://nginx.org/ru/)
[![Docker](https://img.shields.io/badge/Docker-blue?style=flat-square&logo=docker)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker_Compose-blue?style=flat-square&logo=docker)](https://docs.docker.com/compose/)
[![JWT](https://img.shields.io/badge/JWT-SimpleJWT_5.3-orange?style=flat-square)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![Swagger](https://img.shields.io/badge/Swagger-drf--spectacular_0.29-green?style=flat-square&logo=swagger)](https://drf-spectacular.readthedocs.io/)
[![Indigo](https://img.shields.io/badge/EPAM_Indigo-1.33-purple?style=flat-square)](https://lifescience.opensource.epam.com/indigo/)
[![Pillow](https://img.shields.io/badge/Pillow-11.0-yellow?style=flat-square)](https://pillow.readthedocs.io/)

## 4. Запуск проекта через Docker Compose <a id=4></a>

Склонируйте проект из репозитория:

```shell
git clone git@github.com:DPavlen/Chemical_treatment-.git
```

Перейдите в директорию проекта:

```shell
cd Chemical-treatment/
```

Ознакомьтесь с `.env.example` и создайте файл `.env`:

```shell
cp .env.example .env
nano .env
```

Добавьте строки, содержащиеся в файле `.env.example` и подставьте свои значения.

Пример из .env файла:

```dotenv
# Django settings
SECRET_KEY=ваш-секретный-ключ-django    # Секретный ключ Django
DEBUG=True                               # True для разработки, False для продакшена

# Allowed hosts (через запятую)
ALLOWED_HOSTS=127.0.0.1,localhost        # Список разрешенных хостов

# Database PostgreSQL
POSTGRES_DB=chemical_treatment           # Название базы данных
POSTGRES_USER=ваш-пользователь           # Имя пользователя PostgreSQL
POSTGRES_PASSWORD=ваш-пароль             # Пароль PostgreSQL
DB_HOST=db                               # Хост БД (db для Docker)
DB_PORT=5432                             # Порт PostgreSQL
```

Находясь в директории **Chemical-treatment/** выполните команду:

```shell
docker compose up --build
```

> **Примечание.** Добавьте флаг **-d** для запуска в фоновом режиме.

После запуска выполните миграции и создайте суперпользователя:

```shell
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

__Или через Makefile:__

```shell
make build          # Собрать контейнеры
make up             # Запустить контейнеры
make migrate        # Применить миграции
make createsuperuser # Создать суперпользователя
```

> **Примечание.** Для пересборки и запуска одной командой:
```shell
make rebuild
```

По завершении всех операций проект будет доступен:
- Приложение: http://localhost:8000
- Swagger: http://localhost:8000/api/v1/swagger/
- ReDoc: http://localhost:8000/api/v1/redoc/
- Django Admin: http://localhost:8000/admin/

> **Примечание.** Для остановки контейнеров:
```shell
docker compose down
# или
make down
```

## 5. Автор проекта <a id=5></a>

**Павленко Дмитрий**
- Ссылка на мой профиль в GitHub [Dmitry Pavlenko](https://github.com/DPavlen)
