import telebot
import requests


API_TOKEN = 'XXXXXXXXXXXXXXXXXXXXX'


EXCHANGE_API_KEY = '107612e59d1e29166f29cfd1'

bot = telebot.TeleBot(API_TOKEN)

def get_exchange_rate(base_currency, target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        rates = data["conversion_rates"]
        return rates.get(target_currency)
    else:
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне сумму и пару валют в формате '10 USD RUB', и я скажу тебе эквивалент суммы в другой валюте.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
    
        parts = message.text.split()

        if len(parts) == 3: 
            amount = float(parts[0]) 
            base_currency = parts[1].upper() 
            target_currency = parts[2].upper() 
        
            rate = get_exchange_rate(base_currency, target_currency)

            if rate:
                converted_amount = amount * rate
                bot.reply_to(message, f'{amount} {base_currency} = {converted_amount:.2f} {target_currency}')
            else:
                bot.reply_to(message, 'Не удалось получить курс валют. Проверь правильность введенных данных.')

        elif len(parts) == 2:  
            base_currency = parts[0].upper()
            target_currency = parts[1].upper()

            # Получаем курс валют
            rate = get_exchange_rate(base_currency, target_currency)

            if rate:
                bot.reply_to(message, f'Курс {base_currency} к {target_currency} равен {rate}')
            else:
                bot.reply_to(message, 'Не удалось получить курс валют. Проверь правильность введенных данных.')

        else:
            bot.reply_to(message, 'Пожалуйста, введи сумму и две валюты через пробел, например: 10 USD RUB или просто USD RUB')

    except ValueError:
        bot.reply_to(message, 'Ошибка: Убедитесь, что вы ввели корректные данные, например: 10 USD RUB')



@bot.message_handler(commands=['buy'])
def buy(message):
    prices = [telebot.types.LabeledPrice(label='Подписка на месяц', amount=50000)]  
    bot.send_invoice(
        message.chat.id, 
        title='Подписка на курсы валют', 
        description='Ежедневные обновления курса валют на месяц', 
        provider_token='/approve 6d557c11ac9d5944ac09d5b30173dc3690046d0a:CODE', 
        currency='RUB', 
        prices=prices, 
        start_parameter='currency-subscription', 
        invoice_payload='HAPPY_USER'
    )





bot.polling()
