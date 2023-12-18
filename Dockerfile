FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE DutchNewsWeb.settings
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]