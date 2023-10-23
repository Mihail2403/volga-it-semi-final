FROM python:3.11-alpine

WORKDIR /backend

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY . .

RUN pip install --no-cache-dir -r requirements.txt