from flask import Blueprint, request
from flask.logging import logging

import bot.coder as coder

PREFIX = '0x'
BOT_ID = '0000000000000000000000000000000000000b01'
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

class PlayerError(Exception):
    pass

class PlayerAError(PlayerError):
    def __str__(self):
        return 'The bot only plays as player B'

BP = Blueprint('channel_message', __name__)

def prefund_setup(hex_message):

    state_count = coder.get_state_count(hex_message)
    actions = []
    if state_count:
        raise PlayerAError()
    else:
        actions = [coder.increment_state_turn_num, coder.increment_channel_state]

    response_message = hex_message
    for action in actions:
        response_message = action(response_message)

    return response_message

def postfund_setup(hex_message):
    state_count = coder.get_state_count(hex_message)
    if state_count:
        pass #postfundsetupB
    else:
        raise PlayerAError()

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

def ingest_message(hex_message):
    hex_message = hex_message[len(PREFIX):]
    coder.assert_channel_num_players(hex_message)
    response = ''

    players = coder.get_channel_players(hex_message)
    if BOT_ID not in players:
        logging.warning('The message players do not include a bot')
        return response

    hex_state = int(coder.get_channel_state(hex_message))
    return PREFIX + CHANNEL_STATES[hex_state](hex_message)

@BP.route('/channel_message', methods=['POST'])
def channel_message():
    hex_message = request.form['hex_message']
    return ingest_message(hex_message)
    