//FASTAPI
1. Правильный запуск uvicorna: uvicorn src.main:app --reload (где main - название основного файла) 

//DOCKER
# УПРАВЛЕНИЕ КОНТЕЙНЕРАМИ
## Запуск контейнера:
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

## Остановка контейнера:
docker stop <CONTAINER_ID_OR_NAME>

## Запуск остановленного контейнера:
docker start <CONTAINER_ID_OR_NAME>

## Просмотр работающих контейнеров:
docker ps

## Просмотр всех контейнеров (включая остановленные):
docker ps -a

## Удаление контейнера:
docker rm <CONTAINER_ID_OR_NAME>


# УПРАВЛЕНИЕ ОБРАЗАМИ
## Просмотр списка образов:
docker images

## Загрузка образа с Docker Hub:
docker pull <IMAGE_NAME>

## Создание образа из контейнера:
docker commit <CONTAINER_ID_OR_NAME> <NEW_IMAGE_NAME>

## Удаление образа:
docker rmi <IMAGE_ID_OR_NAME>


# УПРАВЛЕНИЕ СЕТЯМИ:
## Просмотр списка сетей:
docker network ls

## Создание сети:
docker network create <NETWORK_NAME>

## Подключение контейнера к сети:
docker network connect <NETWORK_NAME> <CONTAINER_ID_OR_NAME>

## Отключение контейнера от сети:
docker network disconnect <NETWORK_NAME> <CONTAINER_ID_OR_NAME>


# РАБОТА С ЛОГАМИ И ИНФОРМАЦИЕЙ
## Просмотр логов контейнера:
docker logs <CONTAINER_ID_OR_NAME>

## Получение информации о контейнере:
docker inspect <CONTAINER_ID_OR_NAME>

## Получение информации о образе:
docker inspect <IMAGE_ID_OR_NAME>

## Выполнение команды внутри контейнера:
docker exec -it <CONTAINER_ID_OR_NAME> <COMMAND>


# ALEMBIC
## Создание ревизии
alembic revision --autogenerate -m "prod_postgres_rev"
alembic revision --autogenerate -m "test_postgres_rev"
## Применение изменений в ревизии к базе
alembic upgrade revision_id

# CELERY и RABBIT MQ
celery -A celery_worker worker -l INFO # для линукса
celery -A celery_worker worker -l INFO --pool solo # для винды
celery -A celery_beat beat -l INFO
celery -A src.celery flower


# ГОТОВЫЕ КОМАНДЫ ДЛЯ РАЗВЕРТЫВАНИЯ КОНТЕЙНЕРОВ
sudo docker run --name postgresql -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -v pg_data:/var/lib/postgresql -p 5432:5432 -d postgres
sudo docker run --name adminer -p 8080:8080 -d adminer
# развертываем redis и rabbit перед запуском воркера
docker run --name redis -d -p 6379:6379 redis
docker run --name rabbit_mq -d -p 5672:5672 -e RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS"-rabbit consumer_timeout 36000000" rabbitmq

docker run -d --name prometheus -p 9090:9090 -v prometheus-data:/prometheus prom/prometheus
docker run -d --name grafana -p 3000:3000 -v grafana-data:/var/lib/grafana grafana/grafana
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 -v rabbitmq-data:/var/lib/rabbitmq rabbitmq:management

# ALEMBIC ENV
import sys
from os.path import abspath, dirname
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))

from src.users.models import UserModel, RefreshSessionModel
from src.database import Base
from src.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
if settings.MODE == "TEST":
    config.set_main_option("sqlalchemy.url", f"{settings.TEST_DATABASE_URL}?async_fallback=True")
else:
    config.set_main_option("sqlalchemy.url", f"{settings.DATABASE_URL}?async_fallback=True")

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata