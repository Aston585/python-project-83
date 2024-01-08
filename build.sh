#!/usr/bin/env bash

export DATABASE_URL=postgresql://admin@localhost:5432/page_analyzer_db

make install && poetry install --extras "postgresql"
if [ $? -eq 0 ]; then
    echo "Все зависимости успешно установлены"
    # Создать роль 'admin' с правом создания БД;
    createuser -U postgres --superuser --no-password admin
    if [ $? -eq 0 ]; then
        echo "Роль 'admin' успешно создана"

        # Создать базу данных 'page_analayzer_db' с владельцем 'admin';
        createdb -U admin --host=localhost --port=5432 page_analyzer_db
        if [ $? -eq 0 ]; then
            echo "База данных создана"

            # Подключиться к новой БД и выполнить команды SQL из файла;
            psql -U admin -a --dbname=$DATABASE_URL --file=database.sql
            if [ $? -eq 0 ]; then
                echo "Подключение к базе данных выполнено успешно"
            else
                echo "Ошибка в подключени к базе данных"
                exit 1
            fi
        else
            echo "Ошибка в создании базы данных"
            exit 1
        fi
    else
        echo "Ошибка при создании роли 'admin'"
        exit 1
    fi
else
    echo "Ошибка при установки зависимостей"
    exit 1
fi
