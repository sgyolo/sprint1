
# FSTR Api

Данный репозиторий представляет реализацию API сервиса Федерации Спортивного Туризма России (конкретнее - сервиса перевалов) на базе FastAPI + TortoiseORM.

API поддерживает следующие методы:

(GET) submitData/{id} - получить перевал по его id

(POST) submitData - создать перевал. В тело запроса необходимо передать корректный json (подробнее в документации)

(PATCH) submitData/{id} - обновить перевал. В тело запроса необходимо передать корректный json (подробнее в документации)

## Переменные окружения

Для запуска проекта вам нужно добавить следующие переменные окружения:

`FSTR_DB_HOST` - хост базы данных

`FSTR_DB_PORT` (по умолчанию: 5432) - порт базы данных

`FSTR_DB_LOGIN` - логин базы данных

`FSTR_DB_PASS` - пароль базы данных

## Локальный запуск

Скопируйте проект

```bash
  git clone https://github.com/sgyolo/sprint1
```

Перейдите в директорию проекта

```bash
  cd sprint1
```

Установите зависимости

```bash
  pip install requirements.txt
```

Запустите файл

```bash
  python3 main.py
```

По умолчанию API запустится по адресу 127.0.0.1:8000

Чтобы это изменить, поменяйте значения переменных HOST и PORT в файле main.py


## Документация

[\*клик\*](http://51.250.108.177:8001/docs#/)


## Протестировать API

Протестировать API можно используя IP-адрес 51.250.108.177:8001

