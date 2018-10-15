from bot.config import ADDRESSES

# Error definitions
class StrategyError(Exception):
    pass

class InvalidStrategyError(StrategyError):
    def __str__(self):
        return 'The strategy does not exist'

def _raise_error():
    raise InvalidStrategyError()

def _pick_rock():
    return 0

def next_move(addr):
    bot_index = ADDRESSES.index(addr)
    if bot_index < 0:
        _raise_error()
    return STRATEGY[bot_index]()

STRATEGY = [
    _pick_rock,
    _raise_error,
    _raise_error
]
