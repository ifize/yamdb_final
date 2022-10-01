# YaMDb Final
![YaMDb workflow](https://github.com/ifize/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
## О проекте:

RestAPI для сервиса Yamdb
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles).
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Список категорий (Category) может быть расширен администратором.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка.
Произведению может быть присвоен жанр (Genre) из списка предустановленны.
Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и
ставят произведению оценку в диапазоне от одного до десяти (целое число);
из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число).
На одно произведение пользователь может оставить только один отзыв.
## Начало работы

Для запуска проекта на локальной машине в целях разработки и тестирования. See deployment for notes on how to deploy the project on a live system.

### Предварительная подготовка

#### Установка Docker
Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop) 
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). Установите [Docker Compose](https://docs.docker.com/compose/install/)

### Установка проекта (на примере Linux)

- Создайте папку для проекта YaMDb `mkdir yamdb` и перейдите в нее `cd yamdb`
- Склонируйте этот репозиторий в текущую папку `git clone https://github.com/ifize/yamdb_final .`.
- Создайте файл `.env` командой `touch .env` и добавьте в него переменные окружения для работы с базой данных:
```sh
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнер в котором будет развернута БД)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY=... # секретный ключ
DEBUG = True # данную опцию следует добавить для отладки
```
- Запустите docker-compose `sudo docker-compose up -d` 
- Примените миграции `sudo docker-compose exec web python manage.py migrate`
- Соберите статику `sudo docker-compose exec web python manage.py collectstatic --no-input`
- Создайте суперпользователя Django `sudo docker-compose exec web python manage.py createsuperuser --email 'admin@yamdb.com'`
## Примеры эндпоинтов
- Создать пользователя        /api/v1/auth/signup/
```
{ "email": "string", "username": "string" }
```
- Получить Jwt Token      /api/v1/auth/token/
```
{ "username": "string", "confirmation_code": "string" }
```
- Категории      /api/v1/categories/
- Жанры         /api/v1/genres/
- Произведения         /api/v1/titles/
- Отзывы        /api/v1/titles/1/reviews/
- Комментарии       /api/v1/titles/1/reviews/1/comments/
- Пользователи          /api/v1/users/


![](https://img.shields.io/pypi/pyversions/p5?logo=python&logoColor=yellow&style=for-the-badge)
![](https://img.shields.io/badge/Django-2.2.16-blue)
![](https://img.shields.io/badge/DRF-3.12.4-lightblue)