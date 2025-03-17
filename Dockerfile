# Используем официальный образ Python
FROM python:3.13

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry и зависимости
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Копируем код проекта внутрь контейнера
COPY src ./src

# Переменные окружения
ENV PYTHONPATH=/app/src

# Запуск сервера
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
