
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

catalog = {
    "jacket": "Рабочая куртка утеплённая",
    "overalls": "Комбинезон защитный",
    "boots": "Ботинки рабочие"
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

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()

if __name__ == "__main__":
    main()
