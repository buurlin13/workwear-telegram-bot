import os
from aiohttp import web
from telegram.ext import Application, CommandHandler

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = "https://workwear-telegram-bot.onrender.com/webhook"

application = Application.builder().token(TOKEN).build()

# Пример команды
async def start(update, context):
    await update.message.reply_text("Привет! Я бот.")

application.add_handler(CommandHandler("start", start))

# Устанавливаем webhook
async def on_startup(app):
    await application.bot.set_webhook(url=WEBHOOK_URL)

# aiohttp сервер
async def webhook_handler(request):
    data = await request.text()
    await application.update_queue.put(data)
    return web.Response()

app = web.Application()
app.router.add_post("/webhook", webhook_handler)
app.on_startup.append(on_startup)

if __name__ == "__main__":
    web.run_app(app, port=int(os.getenv("PORT", 8443)))
