from flask import g
from bot.config import BOT_ADDRESS, BOT_PRIVATE_KEY, WALLET_UID
from bot.config import hex_to_str, str_to_hex

from bot import coder

K_WALLETS = 'wallets'
K_CHANNELS = 'channels'
K_RECEIVED = 'received'
K_SENT = 'sent'
K_UID = 'uid'
K_MESSAGE = 'message'

NEW_WALLET = dict(
    address=str_to_hex(BOT_ADDRESS),
    channels=None,
    privateKey=BOT_PRIVATE_KEY,
    uid=str_to_hex(WALLET_UID)
)

def get_wallets_ref():
    return g.db.child(K_WALLETS)

def get_wallet_ref(wallet_key):
    return get_wallets_ref().child(wallet_key)

def create_wallet():
    get_wallets_ref().push(NEW_WALLET)

def get_wallet():
    hex_uid = str_to_hex(WALLET_UID)
    wallets_ref = get_wallets_ref()
    bot_wallet_query = wallets_ref.order_by_child(K_UID).equal_to(hex_uid).limit_to_first(1)
    wrapped_wallet = bot_wallet_query.get()
    if not wrapped_wallet:
        create_wallet()
        wrapped_wallet = bot_wallet_query.get()

    return (list(wrapped_wallet.values())[0], list(wrapped_wallet.keys())[0])

def clear_wallet_channels():
    _, wallet_key = get_wallet()
    get_wallet_ref(wallet_key).child(K_CHANNELS).delete()

def get_last_message_for_channel(hex_message):
    wallet = get_wallet()[0]
    channels = wallet.get(K_CHANNELS)
    if not channels:
        return None

    channel_id = coder.get_channel_id(hex_message)
    last_message = None
    try:
        last_message = channels[channel_id][K_RECEIVED][K_MESSAGE]
    except KeyError:
        pass

    return last_message

def record_received_message(hex_message):
    wallet, wallet_key = get_wallet()
    channel_id = coder.get_channel_id(hex_message)

    channels = wallet.get(K_CHANNELS, {})
    channel = channels.get(channel_id, {})
    received = channel.get(K_RECEIVED, {})

    received[K_MESSAGE] = str_to_hex(hex_message)
    channel[K_RECEIVED] = received
    channels[channel_id] = channel
    wallet[K_CHANNELS] = channels

    get_wallet_ref(wallet_key).update(wallet)
