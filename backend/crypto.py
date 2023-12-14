import json
import bitcoinlib
from web3 import Web3
from tronpy import Tron
from tronpy.keys import PrivateKey
from bitcoinlib.wallets import Wallet
from tronpy.providers import HTTPProvider


with open('backend/config.json', encoding='utf-8') as f:
    data = json.load(f)
    TRON_API = data['api-tron']
    ERC20_NODE = data['erc20-node']
    USDT = data['usdt-contract']


# Функция получения BTC
def get_btc_balance(username: str):
    wallet = Wallet(username)
    wallet.scan()
    balance = wallet.balance()

    return balance


# Функция получения USDT TRC20
def get_trc_balance(username: str):
    client = Tron(HTTPProvider(api_key=TRON_API))

    db = 'backend/database.json'

    with open(db, encoding='utf-8') as f:
        data = json.load(f)

    wallet_address = None    

    for user in data:
        if user['login'] == username:
            wallet_address = user['crypto']['trc20']['address']
            break
    
    contract_address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

    contract = client.get_contract(contract_address)
    balance = contract.functions.balanceOf(wallet_address)
    balance = balance/1000000

    return balance


# Функция получения USDT ERC20
def get_erc_balance(username: str):
    db = 'backend/database.json'

    USDT_DECIMALS = 6

    with open(db, encoding='utf-8') as f:
        data = json.load(f)

    wallet_address = None    

    for user in data:
        if user['login'] == username:
            wallet_address = user['crypto']['erc20']['address']
            break

    web3 = Web3(Web3.HTTPProvider(ERC20_NODE))

    abi = json.loads('[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}]')

    contract_address = USDT # Контракт USDT

    contract = web3.eth.contract(address=contract_address, abi=abi)
    balance = contract.functions.balanceOf(wallet_address).call()

    balance = web3.from_wei(balance, 'wei') / 10**USDT_DECIMALS

    return balance


# Функция отправки BTC
def send_btc(username, to, amount):
    wallet = bitcoinlib.wallets.wallet_create_or_open(username, witness_type='segwit', network='bitcoin')
    wallet.scan()
    satoshi_amount = int(amount * 100_000_000)
    trans = wallet.send_to(to, satoshi_amount, fee=None)
    trans.send()


# Функция отправки USDT TRC20
def send_trc20(private_key, to, amount):
    
    tron = Tron(HTTPProvider(api_key=TRON_API))
    private_key = PrivateKey(bytes.fromhex(private_key))
    
    public_key = private_key.public_key

    trc20_contract = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t" 

    token_contract = tron.get_contract(trc20_contract)
    
    tx = token_contract.functions.transfer(
        to, 
        int(amount * 10**6)) \
        .with_owner(public_key.to_base58check_address()) \
        .build() \
        .sign(private_key) \
        .broadcast() \
        .wait()

    if tx:
        print(f"Успешно отправлено {amount} USDT по адресу {to}")
    else:
        print("Ошибка транзакции")


# Функция отправки USDT ERC20
def send_erc20(sender, receiver, amount, priv_key):
    ERC20_ABI = json.loads('''[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"decimals_","type":"uint8"}],"name":"setupDecimals","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]''')

    web3 = Web3(Web3.HTTPProvider(ERC20_NODE))

    # USDT токен
    usdt_contract_address = USDT

    usdt_contract = web3.eth.contract(usdt_contract_address, abi=ERC20_ABI)

    dict_transaction = {
        'chainId': web3.eth.chain_id,
        'from': sender,
        'gas': 210000,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(sender),
    }

    usdt_decimals = usdt_contract.functions.decimals().call()

    value = int(amount * 10 ** usdt_decimals)

    transaction = usdt_contract.functions.transfer(
    receiver, value
    ).build_transaction(dict_transaction)

    signed_txn = web3.eth.account.sign_transaction(transaction, priv_key)

    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)