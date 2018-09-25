from time import time
from flask import g
from bot.config import BOT_ADDRESS, BOT_NAME, str_to_hex

NOW = int(time()*1000)
NEW_CHALLENGE = {
    'address': str_to_hex(BOT_ADDRESS),
    'name': BOT_NAME,
    'isPublic': True,
    'stake': '1000000000000000',
    'createdAt': NOW,
    'updatedAt': NOW
}

def create_new_challenge():
    g.db.child('challenges').child(str_to_hex(BOT_ADDRESS)).set(NEW_CHALLENGE)
