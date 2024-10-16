from telegram import Update
from telegram.ext import CallbackContext
from utils.chart_utils import generate_price_chart

def chart(update: Update, context: CallbackContext) -> None:
    if not context.args:
        update.message.reply_text("Please provide a cryptocurrency name. Example: /chart bitcoin")
        return

    coin = context.args[0].lower()
    try:
        chart_buffer = generate_price_chart(coin)
        update.message.reply_photo(photo=chart_buffer, caption=f"7-day price chart for {coin.capitalize()}")
    except Exception as e:
        update.message.reply_text(f"Error generating chart for {coin}. Please check the coin name and try again.")