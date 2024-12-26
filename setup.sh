#!/bin/bash

# Создание виртуального окружения
python3.10 -m venv venv

# Активировать виртуальное окружение
source venv/bin/activate

# Установка Poetry
pip install poetry

# Лочим зависимости с Poetry
poetry lock

# Обновляем зависимости
poetry update