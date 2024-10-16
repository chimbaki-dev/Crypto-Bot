from telegram import Update
from telegram.ext import CallbackContext
from utils.coingecko import get_coin_data

def price(update: Update, context: CallbackContext) -> None:
    if not context.args:
        update.message.reply_text("Please provide a cryptocurrency name. Example: /price bitcoin")
        return

    coin = context.args[0].lower()
    try:
        data = get_coin_data(coin)
        message = (
            f"💰 {data['name']} ({data['symbol'].upper()})\n\n"
            f"Price: ${data['current_price']:,.2f}\n"
            f"24h Change: {data['price_change_percentage_24h']:.2f}%\n"
            f"Market Cap: ${data['market_cap']:,.0f}\n"
            f"Total Supply: {data['total_supply']:,.0f}"
        )
        update.message.reply_text(message)
    except Exception as e:
        update.message.reply_text(f"Error fetching data for {coin}. Please check the coin name and try again.")