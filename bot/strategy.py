from random import randint
from bot.config import ADDRESSES, NUM_MOVES

ROCK = 0

# Error definitions
class StrategyError(Exception):
    pass

class InvalidStrategyError(StrategyError):
    def __str__(self):
        return 'The strategy does not exist'

def _raise_error():
    raise InvalidStrategyError()

def _pick_rock(_last_bot_move, _last_opponent_move):
    return ROCK

def _pick_increment(last_bot_move, _last_opponent_move):
    if last_bot_move is None:
        return ROCK
    return (last_bot_move + 1) % NUM_MOVES

def _pick_opponent_increment(_last_bot_move, last_opponent_move):
    if last_opponent_move is None:
        return randint(ROCK, NUM_MOVES)
    return (last_opponent_move + 1) % NUM_MOVES

def next_move(last_bot_move, last_opponent_move, addr):
    bot_index = ADDRESSES.index(addr)
    if bot_index < 0:
        _raise_error()
    return STRATEGY[bot_index](last_bot_move, last_opponent_move)

STRATEGY = [
    _pick_rock,
    _pick_increment,
    _pick_opponent_increment
]
