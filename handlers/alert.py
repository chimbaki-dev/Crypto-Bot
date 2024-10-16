from telegram import Update
from telegram.ext import CallbackContext
from utils.coingecko import get_coin_price

alerts = {}

def set_alert(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 3:
        update.message.reply_text("Please provide a coin, price, and type (above/below). Example: /alert bitcoin 50000 above")
        return

    coin, price, alert_type = context.args[0].lower(), float(context.args[1]), context.args[2].lower()
    if alert_type not in ['above', 'below']:
        update.message.reply_text("Alert type must be 'above' or 'below'.")
        return

    user_id = update.effective_user.id

    if user_id not in alerts:
        alerts[user_id] = {}
    
    alerts[user_id][coin] = {'price': price, 'type': alert_type}
    update.message.reply_text(f"Alert set for {coin} when price goes {alert_type} ${price:,.2f}")

def check_alerts(context: CallbackContext):
    alerts_copy = alerts.copy()
    for user_id, user_alerts in alerts_copy.items():
        user_alerts_copy = user_alerts.copy()
        for coin, target_price in user_alerts_copy.items():
            current_price = get_coin_price(coin)
            if current_price is not None:
                if (target_price['type'] == 'above' and current_price > target_price['price']) or \
                   (target_price['type'] == 'below' and current_price < target_price['price']):
                    message = f"Alert: {coin.upper()} price is now ${current_price:.2f}, which is {target_price['type']} your target of ${target_price['price']:.2f}"
                    context.bot.send_message(chat_id=user_id, text=message)
                    del alerts[user_id][coin]
                    if not alerts[user_id]:
                        del alerts[user_id]
