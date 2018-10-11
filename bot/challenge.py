from time import time
from firebase_admin import db
from bot.config import get_bot, get_bot_addr, K_ADDRESS, K_NAME, K_STAKE
from bot.util import str_to_hex

def get_now_ms():
    return int(time()*1000)

NOW = get_now_ms()

def _get_new_challenge(bot_index):
    bot = get_bot(index=bot_index)
    return {
        'address': str_to_hex(bot[K_ADDRESS]),
        'name': bot[K_NAME],
        'isPublic': True,
        'stake': bot[K_STAKE],
        'createdAt': NOW
    }

def get_challenge_ref(bot_index=0):
    addr = get_bot_addr(bot_index)
    return db.reference().child('challenges').child(str_to_hex(addr))

def create_new_challenge(bot_index=0):
    get_challenge_ref().set(_get_new_challenge(bot_index))
