from time import time
from firebase_admin import db
from bot.config import BOT_ADDRESS, BOT_NAME, BOT_STAKE
from bot.util import str_to_hex

def get_now_ms():
    return int(time()*1000)

NOW = get_now_ms()
NEW_CHALLENGE = {
    'address': str_to_hex(BOT_ADDRESS),
    'name': BOT_NAME,
    'isPublic': True,
    'stake': BOT_STAKE,
    'createdAt': NOW
}

def get_challenge_ref():
    return db.reference().child('challenges').child(str_to_hex(BOT_ADDRESS))

def create_new_challenge():
    get_challenge_ref().set(NEW_CHALLENGE)
