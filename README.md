# nearest-cities

HTTP API для получения ближайших городов.
Used stack: *FastAPI*, *PostgreSQL*, *DaDataAPI*.

## Установка

Установить `nearest-cities` из источника:

    git clone https://github.com/omka0708/nearest-cities
    cd nearest-cities

Вы должны иметь файл `.env` в папке */nearest-cities*.

Файл `.env` должен содержать:

    DB_USER=<ваш db username>
    DB_PASS=<ваш db pass>
    DB_HOST=nearest-cities-db
    DB_PORT=5432
    DB_NAME=<ваш db name>
    
    PGADMIN_EMAIL=<ваш pgadmin email>
    PGADMIN_PASSWORD=<ваш pgadmin password>

## Запуск

Запустите эту команду в рабочей директории */nearest-cities*:

    docker compose up -d --build

## Документация

Вы можете перейти на OpenAPI документацию с помощью:

    GET localhost:8000

Этот запрос сделает редирект на документацию (*/docs*).

### /api/city/create

#### POST

##### Summary:

Добавить город в хранилище

##### Parameters

| Name    | Required |
|---------|----------|
| title   | Yes      |

##### Responses

| Code | Description                        |
|------|------------------------------------|
| 201  | Город добавлен                     |
| 409  | Город уже был добавлен в хранилище |
| 404  | Города не существует               |

### /api/city/get/all

#### GET

##### Summary:

Получить все города

##### Responses

| Code | Description              |
|------|--------------------------|
| 200  | Все города были получены |

### /api/city/get

#### GET

##### Summary:

Получить город (по ID или названию)

##### Parameters

| Name    | Located in | Required |
|---------|------------|----------|
| city_id | query      | No       | 
| title   | query      | No       |

##### Responses

| Code | Description                           |
|------|---------------------------------------|
| 200  | Город получен                         |
| 422  | Необходимо передать city_id или title |
| 404  | Города нет в хранилище                |

### /api/city/delete

#### DELETE

##### Summary:

Удалить город из хранилища

##### Parameters (query)

| Name    | Required |
|---------|----------|
| city_id | No       |
| title   | No       | 

##### Responses

| Code | Description                           |
|------|---------------------------------------|
| 204  | Город удалён                          |
| 422  | Необходимо передать city_id или title |
| 404  | Города нет в хранилище                |

### /api/city/get/nearest

#### GET

##### Summary:

Получить ближайшие города

##### Parameters

| Name   | Located in | Description                          | Required |
|--------|------------|--------------------------------------|----------|
| lat    | query      | Широта                               | Yes      | 
| lon    | query      | Долгота                              | Yes      | 
| amount | query      | Количество городов, по умолчанию = 2 | No       |

##### Responses

| Code | Description               |
|------|---------------------------|
| 200  | Ближайшие города получены |
