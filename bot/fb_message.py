from bot import coder
from bot.config import BOT_ADDRESS, str_to_hex

K_MESSAGES = 'messages'

def _get_opponent_ref(addr, fb):
    return fb.child(K_MESSAGES).child(str_to_hex(addr))

def message_opponent(message, fb):
    hex_message = str_to_hex(message)
    signature = ''
    # Are there other queues?
    queue = 'GAME_ENGINE'

    d_message = {
        'data': hex_message,
        'signature': signature,
        'queue': queue
    }

    players = coder.get_channel_players(message)
    opponents = list(filter(lambda player: player != BOT_ADDRESS, players))
    opponent_address = opponents[0]
    ref = _get_opponent_ref(opponent_address, fb)
    ref.push(d_message)
