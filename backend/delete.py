import bitcoinlib

# Удаление всех кошельков из bitcoinlib

wallets = bitcoinlib.wallets.wallets_list()

for wallet in wallets:
    user = wallet['name']
    print(user)
    bitcoinlib.wallets.wallet_delete(user)