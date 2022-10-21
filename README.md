![Foodgram](https://github.com/Drvmnekta/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# Проект Foodgram

## Адрес

51.250.22.124

## Авторы

Наталья Камышева - backend

## Описание

Foodgram - социальная сеть, где вы можете демонстрировать свои знания кулинарии, публикуя рецепты. Добавляйте в избранное понравившиейся рецепты, подписывайтесь на искусных авторов и добавляйте приглянувшееся в список покупок - вы легко сможете скачать суммарный список, когда соберетесь в магазин!


## Ресурсы API Foodgram

- Ресурс auth: аутентификация.
- Ресурс users: пользователи.
- Ресурс tags: получение данных тега или списка тегов рецепта.
- Ресурс recipes: создание/редактирование/удаление рецептов, а также получение списка рецептов или данных о рецепте.
- Ресурс shopping_cart: добавление/удаление рецептов в список покупок.
- Ресурс download_shopping_cart: cкачивание файла со списком покупок.
- Ресурс favorite: добавление/удаление рецептов в избранное пользователя.
- Ресурс subscribe: добавление/удаление пользователя в подписки.
- Ресурс subscriptions: возвращает пользователей, на которых подписан текущий пользователь. В выдачу добавляются рецепты.
- Ресурс ingredients: получение данных ингредиента или списка ингредиентов.


## Шаблон наполнения env-файла

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД
DB_HOST=db # название сервиса
DB_PORT=5432 # порт для подключения к БД 


## Стек технологий

- Django==3.2.13
- djangorestframework==3.13.1
- djangorestframework-simplejwt==4.7.2
- djoser==2.1.0
- gunicorn==20.0.4
- Jinja2==3.1.2
- MarkupSafe==2.1.1
- Pillow==9.1.0
- psycopg2-binary==2.9.3
- pycparser==2.21
- PyJWT==2.4.0
- requests==2.27.1
- requests-oauthlib==1.3.1
- social-auth-app-django==4.0.0
- social-auth-core==4.2.0
- sqlparse==0.4.2


## Примеры

Примеры запросов по API:

- [GET] /api/users/ - Получить список всех пользователей.
- [POST] /api/users/ - Регистрация пользователя.
- [GET] /api/tags/ - Получить список всех тегов.
- [POST] /api/recipes/ - Создание рецепта.
- [GET] /api/recipes/download_shopping_cart/ - Скачать файл со списком покупок.
- [POST] /api/recipes/{id}/favorite/ - Добавить рецепт в избранное.
- [DEL] /api/users/{id}/subscribe/ - Отписаться от пользователя.
- [GET] /api/ingredients/ - Список ингредиентов с возможностью поиска по имени.
