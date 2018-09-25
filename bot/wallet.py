from flask import g
from bot.config import BOT_ADDRESS, BOT_PRIVATE_KEY, WALLET_UID
from bot.config import hex_to_str, str_to_hex

from bot import coder

NEW_WALLET = dict(
    address=str_to_hex(BOT_ADDRESS),
    channels=None,
    privateKey=BOT_PRIVATE_KEY,
    uid=str_to_hex(WALLET_UID)
)

def get_wallet_ref():
    return g.db.child('wallets')

def create_wallet():
    get_wallet_ref().push(NEW_WALLET)

def get_last_message_for_channel(hex_message):
    hex_uid = str_to_hex(WALLET_UID)
    wallets_ref = get_wallet_ref()
    bot_wallet_query = wallets_ref.order_by_child('uid').equal_to(hex_uid).limit_to_first(1)
    wrapped_wallet = bot_wallet_query.get()
    if not wrapped_wallet:
        create_wallet()
        wrapped_wallet = bot_wallet_query.get()

    wallet = list(wrapped_wallet.values())[0]
    channels = wallet.get('channels')
    if not channels:
        return None

    return ''
