import uuid
import tronpy
import crypto
import uvicorn
import requests
import subprocess
import bitcoinlib.wallets
from datetime import datetime
from eth_account import Account
from json_io import read, write
from fastapi import FastAPI, Request
from bitcoinlib.mnemonic import Mnemonic
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


DB = 'backend/database.json'
UNCONFIRMED = 'backend/unconfirmed.json'


app = FastAPI(debug=True)


app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
templates = Jinja2Templates(directory="frontend/templates")


# Функция проверки логина пароля пользователя
def check_user(login :str, password: str):
    
    data = read(DB)

    user = None

    for u in data:
        if u['login'] == login and u['password'] == password:
            user = u
            break
    
    if not user:
        return False
    
    return True


# Функция генерации мнемонической фразы для пользователя
def gen_mnemo(username :str):
    passphrase = Mnemonic().generate(strength=256)

    data = read(DB)

    for user in data:
        if user['login'] == username:
            user['seed'] = passphrase
            break

    write(DB, data)


# Функция создания адресов из мнемонической фразы для пользователя
def create_address(username: str):
    
    data = read(DB)

    for user in data:
        if user['login'] == username:
            seed = user['seed']
            break


    tron = tronpy.Tron()
    trc20 = tron.generate_address_from_mnemonic(seed)

    trc20_address = trc20['base58check_address']
    trc20_private = trc20['private_key']

    wallet = bitcoinlib.wallets.wallet_create_or_open(username, witness_type='segwit', network='bitcoin', keys=seed)

    address = wallet.get_key().address
    private = wallet.get_key().wif

    bitcoin_private = private
    bitcoin_address = address

    erc20 = Account.enable_unaudited_hdwallet_features()
    erc20 = Account.from_mnemonic(seed)

    erc20_private = erc20._private_key.hex()
    erc20_address = erc20.address

    for user in data:
        if user['login'] == username:
            user['crypto']['bitcoin']['address'] = bitcoin_address
            user['crypto']['bitcoin']['private'] = bitcoin_private

            user['crypto']['trc20']['address'] = trc20_address
            user['crypto']['trc20']['private'] = trc20_private

            user['crypto']['erc20']['address'] = erc20_address
            user['crypto']['erc20']['private'] = erc20_private

            break

    write(DB, data)


# Функция проверки пустых полей адресов в базе пользователя
def empty_address(username: str):
    
    data = read(DB)

    for user in data:
        if user['login'] == username:
            empty_btc = not user['crypto']['bitcoin']['address'] or not user['crypto']['bitcoin']['private']
            empty_trc20 = not user['crypto']['trc20']['address'] or not user['crypto']['trc20']['private'] 
            empty_erc20 = not user['crypto']['erc20']['address'] or not user['crypto']['erc20']['private']

            return empty_btc or empty_trc20 or empty_erc20
    return False    


# Функция поиска кошельков пользователя в базе
def find_wallets(username :str):
    
    data = read(DB)

    for user in data:
        if user['login'] == username:
            return user['wallets']
        

# Функция проверки есть ли мнемоническая фраза у пользователя
def check_mnemo(username :str):
    
    data = read(DB)

    for user in data:
        if user['login'] == username:
            if user['seed'] == "":
                return True
        return False
        

# Функция поиска транзакций пользователя
def find_transaction(username :str):
    
    data = read(DB)

    for user in data:
        if user['login'] == username:
            return user['transaction']
        

# Функция получения курса BTC
def get_btc():
    BTC = 'https://blockchain.info/ru/ticker'

    response = requests.get(BTC).json()

    btc = float(response["RUB"]["last"])

    return btc


# Функция получения курса USD
def get_usd():
    USD = 'https://www.cbr-xml-daily.ru/daily_json.js'

    response = requests.get(USD).json()

    usd = response["Valute"]["USD"]["Value"]

    return usd


# Функция считающая общий баланс пользователя
def get_sum(username :str):
    
    data = read(DB)

    for user in data:
        if user['login'] == username:
            btc_course = get_btc()
            usd_course = get_usd()
            rub = user['wallets'][0]['amount']
            usd = user['wallets'][1]['amount'] * usd_course
            btc = user['wallets'][2]['amount'] * btc_course
            usdt = user['wallets'][2]['amount'] * usd_course
            amount = round(rub + usd + btc + usdt, 2)
            return amount
        

# Функция получения крипто адресов
def get_crypto(username :str):
    
    data = read(DB)

    for user in data:
        if user['login'] == username:
            return user['crypto']


# Функция инициализации балансов
def init_balance(username: str):
    
    data = read(DB)

    for user in data:
        if user['login'] == username:
            if user['crypto']['bitcoin']['balance'] == "":
                user['crypto']['bitcoin']['balance'] = crypto.get_btc_balance(username)

            if user['crypto']['trc20']['balance'] == "":
                user['crypto']['trc20']['balance'] = crypto.get_trc_balance(username)

            if user['crypto']['erc20']['balance'] == "":
                user['crypto']['erc20']['balance'] = crypto.get_erc_balance(username)    
        break

    write(DB, data)        


# Рут корневой страницы
@app.get("/")
def index(request: Request):
    context = {"request": request}

    user = request.cookies.get("user")

    if user:
        return RedirectResponse("/balance")
    else:
        return templates.TemplateResponse("index.html", context=context)


# Рут страницы баланса
@app.get("/balance") 
async def balance(request: Request):
    context = {"request": request}

    user = request.cookies.get("user")

    if user:
        context['user'] = user

        wallets = find_wallets(user)
        context['wallets'] = wallets

        transaction = find_transaction(user)
        context['transaction'] = transaction

        usd = float(get_usd())
        context['usd'] = usd

        btc = float(get_btc())
        context['btc'] = btc

        amount = get_sum(user)
        context['amount'] = amount


        if check_mnemo(user):
            gen_mnemo(user)


        if empty_address(user):
            create_address(user)

        init_balance(user)

        crypto = get_crypto(user)
        context['btcadr'] = crypto['bitcoin']['address']
        context['trcadr'] = crypto['trc20']['address']
        context['ercadr'] = crypto['erc20']['address']

        context['btcmax'] = float(crypto['bitcoin']['deploy']) *2
        context['trcmax'] = float(crypto['trc20']['deploy']) * 2
        context['ercmax'] = float(crypto['erc20']['deploy']) * 2

        context['btcpriv'] = crypto['bitcoin']['private']
        context['trcpriv'] = crypto['trc20']['private']
        context['ercpriv'] = crypto['erc20']['private']
        

    if not user:
        return RedirectResponse("/")
    else:
        return templates.TemplateResponse("balance.html", context=context)
    

# Рут обработки обмена
@app.post("/exchange")
async def exchange(request: Request):
    data = await request.json()

    user_cookie = request.cookies.get("user")

    # получаем данные из запроса
    from_amount = float(data['fromAmount']) 
    from_currency = data['fromCurrency']
    to_amount = float(data['toAmount'])
    to_currency = data['toCurrency'].upper()
    
    from_trans = 'Основной' + ' ' + from_currency
    to_trans = 'Основной' + ' ' + to_currency
    sum_trans = from_amount
    status_trans = 'Исполнен'
    type_trans = 'Обмен'
    desc_trans = 'Успешная транзакция.'
    currency_trans = from_currency
    date_trans = datetime.now().strftime("%d.%m.%Y")

    data = read(DB)

    user = None
    for u in data:
        if u['login'] == user_cookie: 
            user = u
            break

    user['transaction'].append({
                                'status': str(status_trans),
                                'type': str(type_trans),
                                'from': str(from_trans), 
                                'to': str(to_trans),
                                'sum': sum_trans,
                                'currency': currency_trans, 
                                'description': str(desc_trans),
                                'date': str(date_trans)  
    })

    for wallet in user['wallets']:
        if wallet['currency'] == from_currency:
            wallet['amount'] -= from_amount
            if wallet['currency'] == 'BTC':
                wallet['amount'] = round(wallet['amount'], 8)
            else:
                wallet['amount'] = round(wallet['amount'], 2)
        
        if wallet['currency'] == to_currency:  
            wallet['amount'] += to_amount
            if wallet['currency'] == 'BTC':
                wallet['amount'] = round(wallet['amount'], 8)
            else:
                wallet['amount'] = round(wallet['amount'], 2)


    write(DB, data)

    return {'status': 'ok'}


# Рут обработки пополнения
@app.post("/deploy")
async def deploy(request: Request):
    data = await request.json()

    user_cookie = request.cookies.get("user")

    # получаем данные из запроса
    status = 'Отменён'
    typedp = 'Пополнение'
    from_card = data['fromCard']
    to_main = 'Основной' + ' ' + data['fromCurrency']
    sum_main = data['sumAmount'].replace(' ', '')[:-1]
    currency = 'RUB'
    description = 'Ошибка транзакции, обратитесь в свой банк.'
    date = datetime.now().strftime("%d.%m.%Y")


    data = read(DB)

    user = None
    for u in data:
        if u['login'] == user_cookie: 
            user = u
            break

    user['transaction'].append({
                                'status': str(status),
                                'type': str(typedp),
                                'from': str(from_card), 
                                'to': str(to_main),
                                'sum': sum_main,
                                'currency': currency, 
                                'description': str(description),
                                'date': str(date)  
    })

    write(DB, data)

    return {'status': 'ok'}


# Рут обработки вывода
@app.post("/withdraw")
async def withdraw(request: Request):
    data = await request.json()

    user_cookie = request.cookies.get("user")

    # получаем данные из запроса
    status = 'Отменён'
    typedp = 'Вывод'
    to_main = data['fromCard']
    from_card = 'Основной' + ' ' + data['fromCurrency']
    sum_main = data['sumAmount'].replace(' ', '')[:-1]
    currency = 'RUB'
    description = 'Вывод возможен только на карту с которой производилось пополнение.'
    date = datetime.now().strftime("%d.%m.%Y")

    data = read(DB)

    user = None
    for u in data:
        if u['login'] == user_cookie: 
            user = u
            break

    user['transaction'].append({
                                'status': str(status),
                                'type': str(typedp),
                                'from': str(from_card), 
                                'to': str(to_main),
                                'sum': sum_main,
                                'currency': currency, 
                                'description': str(description),
                                'date': str(date)  
    })

    write(DB, data)

    return {'status': 'ok'}


# Рут авторизации
@app.post("/login")
async def login(request: Request):
  data = await request.form()

  username = data['username']
  password = data['password']

  if check_user(username, password):
    response = RedirectResponse("/balance", status_code=303) 
    response.set_cookie("user", username)
    return response
  else:
    response = RedirectResponse("/", status_code=303)
    return response


# Рут вывода крипты
@app.post("/withdrawcrypto")
async def withdrawcrypto(request: Request):
    data = await request.json()

    user_cookie = request.cookies.get("user")

    from_address = data['from_address']
    amount = float(data['sum'])
    currency = data['currency']
    to_address = data['to_address']
    trans_id = str(uuid.uuid4())

    private = get_crypto(user_cookie)

    from_private = None

    if currency == 'BTC':
        from_private = private['bitcoin']['private']

    if currency == 'USDTTRC20':
        from_private = private['trc20']['private']

    if currency == 'USDTERC20':
        from_private = private['erc20']['private']

    data = read(UNCONFIRMED)

    data.append({
                'id': trans_id,
                'user': user_cookie,
                'from_address': from_address,
                'from_private': from_private,
                'amount': amount,
                'currency': currency,
                'to_address': to_address,
                'cheked': "False"  
    })

    write(UNCONFIRMED, data)

    return {'status': 'ok'}    


# Запуск подпроцессов алёртов и апрувов при запуске сервера
@app.on_event("startup")
def startup_event():
    subprocess.Popen(["backend/.venv/Scripts/python.exe", "backend/aprove.py"])
    subprocess.Popen(["backend/.venv/Scripts/python.exe", "backend/alert.py"])


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)