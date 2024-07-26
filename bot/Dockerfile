FROM python:3.9

WORKDIR /bot

COPY requirements.txt /bot/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r /bot/requirements.txt

COPY . .