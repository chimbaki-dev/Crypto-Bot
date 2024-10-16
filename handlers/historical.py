from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from utils.coingecko import get_coin_id, get_historical_data
from datetime import datetime, timedelta
from prettytable import PrettyTable

def historical(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text("Usage: /historical <coin>\nExample: /historical Bitcoin")
        return
    
    coin_name = context.args[0].lower()
    days = 7  # Fixed to show data for 7 days

    coin_id = get_coin_id(coin_name)
    if not coin_id:
        update.message.reply_text(f"Could not find coin with name {coin_name}. Please check the name and try again.")
        return

    data = get_historical_data(coin_id, days)

    if "error" in data:
        update.message.reply_text(f"Error fetching data: {data['message']}")
    else:
        # Prepare the formatted message
        date_price_map = {}

        prices = data.get('prices', [])

        for entry in prices:
            timestamp = entry[0] // 1000
            price = entry[1]
            date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
            date_price_map[date] = price

        # Generate the pretty table with 7 days data
        table = PrettyTable()
        table.field_names = ["Date", "Price (USD)"]
        
        # Get the dates for the last 7 days in descending order
        for i in range(days - 1, -1, -1):
            date = (datetime.utcnow() - timedelta(days=i)).strftime('%Y-%m-%d')
            price = date_price_map.get(date, 'N/A')
            price_str = f"${price:,.2f}" if price != 'N/A' else 'N/A'
            table.add_row([date, price_str])
        
        # Prepare the reply message with coin name
        reply_message = f"Historical Data of {coin_name.capitalize()} for last {days} days:\n\n"
        reply_message += f"```\n{table}\n```"

        update.message.reply_text(reply_message, parse_mode=ParseMode.MARKDOWN_V2)
