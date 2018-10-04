from flask import Blueprint, current_app, g, jsonify, request

from bot import challenge, coder, fb_message, wallet
from bot.config import BOT_ADDRESS
from bot.util import hex_to_str, set_response_message

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

def from_game_propose(_hex_message):
    return [playera_pays_playerb, play_move, coder.increment_game_position]

def from_game_reveal(_hex_message):
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

def conclude(_hex_message):
    raise PlayerChannelStateNotImplementedError('conclude')

CHANNEL_STATES = [
    prefund_setup,
    postfund_setup,
    game,
    conclude
]


# State machine
def transition_from_state(hex_message):
    channel_state = coder.get_channel_state(hex_message)
    message_transformations = CHANNEL_STATES[channel_state](hex_message)

    response_message = hex_message
    message_transformations += [coder.increment_state_turn_num]
    for transformation in message_transformations:
        response_message = transformation(response_message)

    return response_message


def game_engine_message(message):
    d_response = {}

    hex_last_message = wallet.get_last_message_for_channel(message)
    last_message = hex_to_str(hex_last_message)
    if last_message == message:
        warning = f'Duplicate message received {hex_last_message}'
        current_app.logger.warning(warning)
        return set_response_message(warning, d_response)
    wallet.record_received_message(message)

    coder.assert_channel_num_players(message)
    players = coder.get_channel_players(message)
    if BOT_ADDRESS not in players:
        warning = 'The message players do not include a bot'
        current_app.logger.warning(warning)
        return set_response_message(warning, d_response)

    new_state = transition_from_state(message)

    current_app.logger.info(f'Sending opponent: {new_state}')
    fb_message.message_opponent(new_state, g.db)
    return set_response_message(new_state, d_response)

@BP.route('/channel_message', methods=['POST'])
def channel_message():
    request_json = request.get_json()
    current_app.logger.info(f'Request_json: {request_json}')

    message = hex_to_str(request_json['data'])
    queue = request_json['queue']
    fb_message_key = request_json.get('message_key')
    d_response = set_response_message()

    if queue == 'GAME_ENGINE':
        d_response = game_engine_message(message)
    elif queue == 'WALLET':
        d_response = wallet.fund_adjudicator(message)
        current_app.logger.info(d_response.get('message'))

    fb_message.message_consumed(fb_message_key, g.db)
    return jsonify(d_response)

@BP.route('/clear_wallet_channels')
def clear_wallet():
    wallet.clear_wallet_channels()
    return jsonify({})

@BP.route('/create_challenge')
def create_challenge():
    challenge.create_new_challenge()
    return jsonify({})

@BP.route('/update_challenge_timestamp')
def update_challenge_timestamp():
    challenge.update_challenge_timestamp()
    return jsonify({})
