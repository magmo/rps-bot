from flask import g

WALLET_UID = '0x0000000000000000000000000000000000000b01'
def get_last_message_for_channel(hex_message):
    wallets_ref = g.db.child('wallets')
    bot_wallet_query = wallets_ref.order_by_child('uid').equal_to(WALLET_UID).limit_to_first(1)
    wallet = bot_wallet_query.get()
    return wallet
