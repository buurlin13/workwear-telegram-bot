
# Workwear Telegram Bot

Telegram-бот для заказа рабочей одежды.  
Подключается к сайту по ссылке с параметром товара.

## Установка

1. Установите зависимости:
```
pip install -r requirements.txt
```

2. Запустите бота:
```
BOT_TOKEN=your_token_here python bot.py
```

## Деплой на Render

- Подключите репозиторий на [Render.com](https://render.com)
- Укажите переменную окружения `BOT_TOKEN`
- Деплой произойдет автоматически по `render.yaml`

## Пример ссылки с сайта

```
https://t.me/your_bot_username?start=jacket
```
