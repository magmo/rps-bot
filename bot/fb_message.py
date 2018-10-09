from firebase_admin import db
from bot import coder
from bot.config import BOT_ADDRESS
from bot.util import str_to_hex
from bot.wallet import sign_message

K_MESSAGES = 'messages'

def _get_addr_ref(addr):
    return db.reference().child(K_MESSAGES).child(str_to_hex(addr))

def message_consumed(key):
    _get_addr_ref(BOT_ADDRESS).child(key).delete()

def message_opponent(message):
    hex_message = str_to_hex(message)
    signature = str_to_hex(sign_message(hex_message))
    queue = 'GAME_ENGINE'

    d_message = {
        'data': hex_message,
        'signature': signature,
        'queue': queue
    }

    players = coder.get_channel_players(message)
    opponents = list(filter(lambda player: player != BOT_ADDRESS, players))
    opponent_address = opponents[0]
    ref = _get_addr_ref(opponent_address)
    ref.push(d_message)
