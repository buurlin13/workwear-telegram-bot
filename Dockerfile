FROM python:3.12-slim

WORKDIR /app

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8443

CMD ["python", "bot.py"]
