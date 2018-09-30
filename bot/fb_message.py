from bot import coder
from bot.config import BOT_ADDRESS, str_to_hex
from bot.wallet import sign_message

K_MESSAGES = 'messages'

def _get_addr_ref(addr, fb_ref):
    return fb_ref.child(K_MESSAGES).child(str_to_hex(addr))

def message_consumed(key, fb_ref):
    _get_addr_ref(BOT_ADDRESS, fb_ref).child(key).delete()

def message_opponent(message, fb_ref):
    hex_message = str_to_hex(message)
    signature = sign_message(hex_message)
    queue = 'GAME_ENGINE'

    d_message = {
        'data': hex_message,
        'signature': signature,
        'queue': queue
    }

    players = coder.get_channel_players(message)
    opponents = list(filter(lambda player: player != BOT_ADDRESS, players))
    opponent_address = opponents[0]
    ref = _get_addr_ref(opponent_address, fb_ref)
    ref.push(d_message)
