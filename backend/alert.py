import json
import time
import crypto
import telebot
from threading import Thread
from datetime import datetime


with open('backend/config.json', encoding='utf-8') as f:
    data = json.load(f)
    BOT_KEY = data['bot-key']
    USER_ID = data['user-id']


bot = telebot.TeleBot(BOT_KEY)


# Функция проверки балансов и отправки уведомлений
def deploy_alert():

    db = 'backend/database.json'

    with open(db, encoding='utf-8') as f:
        data = json.load(f)

    for users in data:
        user = users['login']
        
        old_btc = users['crypto']['bitcoin']['balance']
        old_trc20 = users['crypto']['trc20']['balance']
        old_erc20 = users['crypto']['erc20']['balance']

        btc = crypto.get_btc_balance(user)
        trc20 = crypto.get_trc_balance(user)
        erc20 = crypto.get_trc_balance(user)

        if float(btc) > float(old_btc):
            value = btc - old_btc

            users['crypto']['bitcoin']['balance'] = btc
            users['crypto']['bitcoin']['deploy'] = float(users['crypto']['bitcoin']['deploy']) + btc

            users['transaction'].append({
                                    'status': "Исполнен",
                                    'type': "Пополнение",
                                    'from': "Внешний BTC адрес", 
                                    'to': "Основной BTC",
                                    'sum': value,
                                    'currency': "BTC", 
                                    'description': "Успешная транзакция",
                                    'date': datetime.now().strftime("%d.%m.%Y")  
            })

            with open('backend/database.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            text = f"Пополнение BTC\n{user}\n{value} BTC"
            
            bot.send_message(USER_ID, text)

        if float(trc20) > float(old_trc20):
            value = trc20 - old_trc20

            users['crypto']['trc20']['balance'] = trc20
            users['crypto']['trc20']['deploy'] = float(users['crypto']['trc20']['deploy']) + trc20

            users['transaction'].append({
                                    'status': "Исполнен",
                                    'type': "Пополнение",
                                    'from': "Внешний TRC20 адрес", 
                                    'to': "Основной USDTTRC20",
                                    'sum': value,
                                    'currency': "USDTTRC20", 
                                    'description': "Успешная транзакция",
                                    'date': datetime.now().strftime("%d.%m.%Y")  
            })

            with open('backend/database.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            text = f"Пополнение TRC20\n{user}\n{value} USDT"
            
            bot.send_message(USER_ID, text)

        if float(erc20) > float(old_erc20):
            value = erc20 - old_erc20

            users['crypto']['erc20']['balance'] = erc20
            users['crypto']['erc20']['deploy'] = float(users['crypto']['erc20']['deploy']) + erc20

            users['transaction'].append({
                                    'status': "Исполнен",
                                    'type': "Пополнение",
                                    'from': "Внешний ERC20 адрес", 
                                    'to': "Основной USDTERC20",
                                    'sum': value,
                                    'currency': "USDTERC20", 
                                    'description': "Успешная транзакция",
                                    'date': datetime.now().strftime("%d.%m.%Y")  
            })

            with open('backend/database.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            text = f"Пополнение ERC20\n{user}\n{value} USDT"
            
            bot.send_message(USER_ID, text)


# Функция бесконечной проверки балансов
def alert():
    while True:
        deploy_alert()
        time.sleep(180)


# Функция запуска потока проверки балансов и отправки уведомлений
def alert_thread():
    thread = Thread(target=alert)
    thread.daemon = True
    thread.start()


alert_thread()