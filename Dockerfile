FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends cron \
    && rm -rf /var/lib/apt/lists/*
RUN echo '0 19 * * * python /app/manage.py load_data' | crontab -

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN python manage.py collectstatic --noinput
