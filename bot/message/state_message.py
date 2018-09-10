from flask import Blueprint, request
from flask.logging import logging

import bot.message.coder as coder

BOT_ID = '0x0000000000000000000000000000000000000B01'
CHANNEL_STATES = (
    'PreFundSetup',
    'PostFundSetup'
    'Game'
    'Conclude'
)

PREFUND_STATE = (
    'PreFundSetupA',
    'PreFundSetupB',
)

POSTFUND_STATES = (
    'PostFundSetupA',
    'PostFundSetupB'
)

GAME_STATES = (
    'GameResting',
    'GamePropose',
    'GameAccept',
    'GameReveal'
)

bp = Blueprint('state_message', __name__)

def prefund_setup(hex_message):
    pass

def postfund_setup(hex_message):
    pass

def game(hex_message):
    pass

def conclude(hex_message):
    pass

CHANNEL_STATES = [
    prefund_setup,
    postfund_setup,
    game,
    conclude
]

@bp.route('/state_message', methods=['POST'])
def state_message():
    hex_message = request.form['hex_message']

    num_players = coder.get_channel_num_players(hex_message)

    players = coder.get_channel_players(hex_message)
    if BOT_ID not in players:
        logging.warning('The message players do not include a bot')
        #return "The message players do not include a bot"

    hex_state = int(coder.get_channel_state(hex_message))
    CHANNEL_STATES[hex_state](hex_message)

    return "That's it for now"