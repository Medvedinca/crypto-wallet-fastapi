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

# Функция проверки транзакций и отправки сообщений в ТГ
def aprove_trans():   
    with open('backend/unconfirmed.json', encoding='utf-8') as f:
        data = json.load(f)

    for trans in data:
        if trans['cheked'] == "False":

            currency = trans['currency']
            user = trans['user']
            value = trans['amount']

            # Создаем кнопки 
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Подтвердить', callback_data=f'confirm:{trans["id"]}'))  
            markup.add(telebot.types.InlineKeyboardButton(text='Отклонить', callback_data=f'decline:{trans["id"]}'))

            bot.send_message(
                USER_ID, 
                f"Вывод {currency}\n{user}\n{value} {currency}",
                reply_markup=markup
            )   

            trans['cheked'] = "True"

    with open('backend/unconfirmed.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# Функция бесконечной проверки транзакций и отправки сообщений в ТГ
def aprove():
    while True:
        aprove_trans()
        time.sleep(5)


# Функция потока проверки и отправки сообщений
def aprove_thread():
    thread = Thread(target=aprove)
    thread.daemon = True
    thread.start()


# Функция удаления транзакции при отклонении
def decline_transaction(transaction_id):
    with open('backend/unconfirmed.json', encoding='utf-8') as f:
        data = json.load(f)

    with open('backend/database.json', encoding='utf-8') as f:
        users = json.load(f)

    for transaction in data:
        if transaction["id"] == transaction_id:
            u = transaction['user']

            for user in users:
                if user['login'] == u:

                    user['transaction'].append({
                                    'status': "Отменён",
                                    'type': "Вывод",
                                    'from': f"Основной {transaction['currency']}", 
                                    'to': transaction['to_address'],
                                    'sum': transaction['amount'],
                                    'currency': transaction['currency'], 
                                    'description': "Ошибка проведения транзакции",
                                    'date': datetime.now().strftime("%d.%m.%Y")  
                    })
                    break

            data.remove(transaction)
            break

    with open('backend/unconfirmed.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    with open('backend/database.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


# Функция подтверждения транзакции
def confirm_transaction(transaction_id):
    with open('backend/unconfirmed.json', encoding='utf-8') as f:
        data = json.load(f)

    with open('backend/database.json', encoding='utf-8') as f:
        users = json.load(f)

    description = None
    status = None

    for transaction in data:
        if transaction["id"] == transaction_id:
            u = transaction['user']
            for user in users:
                if user['login'] == u:
                    if transaction['currency'] == "BTC":
                        try:
                            crypto.send_btc(u, transaction['to_address'], float(transaction['amount']))
                            description = 'Успешная транзакция.'
                            status = 'Исполнен'
                            text = f"Успешная транзакция c адреса {transaction['from_address']}\nСумма {transaction['amount']} {transaction['currency']}"          
                            bot.send_message(USER_ID, text)
                        except Exception as e:
                            description = 'Непредвиденная ошибка транзакции, попробуйте позже.'
                            status = 'Отменён'
                            text = f"Ошибка транзакции c адреса {transaction['from_address']}\nСумма {transaction['amount']} {transaction['currency']}\nОшибка {e}"          
                            bot.send_message(USER_ID, text)

                    if transaction['currency'] == "USDTTRC20":
                        try:
                            crypto.send_trc20(transaction['from_private'], transaction['to_address'], float(transaction['amount']))
                            description = 'Успешная транзакция.'
                            status = 'Исполнен'
                            text = f"Успешная транзакция c адреса {transaction['from_address']}\nСумма {transaction['amount']} {transaction['currency']}"          
                            bot.send_message(USER_ID, text)
                        except Exception as e:
                            description = 'Непредвиденная ошибка транзакции, попробуйте позже.'
                            status = 'Отменён'
                            text = f"Ошибка транзакции c адреса {transaction['from_address']}\nСумма {transaction['amount']} {transaction['currency']}\nОшибка {e}"          
                            bot.send_message(USER_ID, text)

                    if transaction['currency'] == "USDTERC20":
                        try:
                            crypto.send_erc20(transaction['from_address'], transaction['to_address'], float(transaction['amount']), transaction['from_private'])
                            description = 'Успешная транзакция.'
                            status = 'Исполнен'
                            text = f"Успешная транзакция c адреса {transaction['from_address']}\nСумма {transaction['amount']} {transaction['currency']}"          
                            bot.send_message(USER_ID, text)
                        except Exception as e:
                            description = 'Непредвиденная ошибка транзакции, попробуйте позже.'
                            status = 'Отменён'
                            text = f"Ошибка транзакции c адреса {transaction['from_address']}\nСумма {transaction['amount']} {transaction['currency']}\nОшибка {e}"          
                            bot.send_message(USER_ID, text)

                    user['transaction'].append({
                                    'status': status,
                                    'type': "Вывод",
                                    'from': f"Основной {transaction['currency']}", 
                                    'to': transaction['to_address'],
                                    'sum': transaction['amount'],
                                    'currency': transaction['currency'], 
                                    'description': description,
                                    'date': datetime.now().strftime("%d.%m.%Y")  
                    })
                    break
            data.remove(transaction)
            break
    
    with open('backend/unconfirmed.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    with open('backend/database.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)
                        

# Обработка нажатий кнопок
@bot.callback_query_handler(func=lambda call: True)  
def callback_query(call):
    if call.data.startswith("confirm"):
        trans_id = call.data.split(":")[1]

        confirm_transaction(trans_id)

        new_markup = telebot.types.InlineKeyboardMarkup() 
        new_markup.add(telebot.types.InlineKeyboardButton(text="Транзакция одобрена✅", callback_data="done"))

        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id,
            reply_markup=new_markup
        )
        
    if call.data.startswith("decline"):
        trans_id = call.data.split(":")[1]

        decline_transaction(trans_id)
         
        new_markup = telebot.types.InlineKeyboardMarkup() 
        new_markup.add(telebot.types.InlineKeyboardButton(text="Транзакция отклонена❌", callback_data="done"))

        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id,
            reply_markup=new_markup
        )


def bot_start():
    bot.polling()


aprove_thread()
bot_start()