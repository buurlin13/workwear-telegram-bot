import os
import logging
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

WEBHOOK_PATH = f"/{TOKEN}"
PORT = int(os.environ.get("PORT", "8443"))  # Render обычно даёт порт в $PORT

catalog = {
    "jacket": "Рабочая куртка утеплённая",
    "overalls": "Комбинезон защитный",
    "boots": "Ботинки рабочие",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query_params = update.message.text.split(" ")
    if len(query_params) > 1:
        product_key = query_params[1]
        await show_product(update, context, product_key)
    else:
        await show_catalog(update, context)

async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"product_{key}")]
        for key, name in catalog.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите рабочую одежду:", reply_markup=reply_markup)

async def show_product(update: Update, context: ContextTypes.DEFAULT_TYPE, product_key: str):
    product_name = catalog.get(product_key, "Неизвестный товар")
    keyboard = [
        [InlineKeyboardButton("Заказать", callback_data=f"order_{product_key}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Вы выбрали: {product_name}", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("product_"):
        product_key = data.split("_")[1]
        await query.message.delete()
        await show_product(query, context, product_key)

    elif data.startswith("order_"):
        product_key = data.split("_")[1]
        product_name = catalog.get(product_key, "Неизвестный товар")
        await query.message.reply_text(f"Ваш заказ на {product_name} принят! Менеджер свяжется с вами.")

async def handle_update(request: web.Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return web.Response(text="ok")

async def main():
    global application
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Установка webhook
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"
    await application.bot.set_webhook(webhook_url)
    logger.info(f"Webhook set to {webhook_url}")

    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_update)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(f"Webhook server started on port {PORT}")

    # Чтобы приложение не завершилось
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
