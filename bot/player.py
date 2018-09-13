from flask import Blueprint, request
from flask.logging import logging
import bot.coder as coder

PREFIX = '0x'
BOT_ADDRESS = '0000000000000000000000000000000000000b01'
BP = Blueprint('channel_message', __name__)

# Error definitions
class PlayerError(Exception):
    pass

class PlayerAError(PlayerError):
    def __str__(self):
        return 'The bot only plays as player B'

class PlayerGamePositionNotImplementedError(PlayerError):
    def __init__(self, game_position):
        super().__init__()
        self.game_position = game_position

    def __str__(self):
        return f'The {self.game_position} is not implemented'

class PlayerChannelStateNotImplementedError(PlayerError):
    def __init__(self, channel_state):
        super().__init__()
        self.channel_state = channel_state

    def __str__(self):
        return f'The {self.channel_state} is not implemented'

def undefined_game_position(game_position):
    raise PlayerGamePositionNotImplementedError(game_position)


# Game position transitions
def playera_pays_playerb(hex_message):
    stake = coder.get_game_stake(hex_message)
    hex_message = coder.increment_state_balance(hex_message, 0, -1 * stake)
    return coder.increment_state_balance(hex_message, 1, stake)

def play_move(hex_message):
    # Always play rock for now
    return coder.update_move(hex_message, 0)

def from_game_propose(hex_message):
    return [playera_pays_playerb, play_move, coder.increment_game_position]

def from_game_reveal(hex_message):
    return [coder.new_game]

GAME_STATES = (
    lambda x: undefined_game_position('FromGameResting'),
    from_game_propose,
    lambda x: undefined_game_position('FromGameAccept'),
    from_game_reveal
)


# Channel state transitions
def prefund_setup(hex_message):
    state_count = coder.get_state_count(hex_message)
    transformations = []
    if state_count:
        raise PlayerAError()
    else:
        transformations = [coder.increment_state_count]

    return transformations

def postfund_setup(hex_message):
    return prefund_setup(hex_message)

def game(hex_message):
    game_position = coder.get_game_position(hex_message)
    return GAME_STATES[game_position](hex_message)

def conclude(hex_message):
    raise PlayerChannelStateNotImplementedError('conclude')

CHANNEL_STATES = [
    prefund_setup,
    postfund_setup,
    game,
    conclude
]


# State machine
def ingest_message(hex_message):
    hex_message = hex_message[len(PREFIX):]
    coder.assert_channel_num_players(hex_message)
    response = ''

    players = coder.get_channel_players(hex_message)
    if BOT_ADDRESS not in players:
        logging.warning('The message players do not include a bot')
        return response

    channel_state = coder.get_channel_state(hex_message)
    message_transformations = CHANNEL_STATES[channel_state](hex_message)

    response_message = hex_message
    message_transformations += [coder.increment_state_turn_num]
    for transformation in message_transformations:
        response_message = transformation(response_message)

    return PREFIX + response_message

@BP.route('/channel_message', methods=['POST'])
def channel_message():
    hex_message = request.form['hex_message']
    return ingest_message(hex_message)
    