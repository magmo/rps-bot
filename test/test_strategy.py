from bot.strategy import next_move, _decode_move
from bot.config import ADDRESSES

def test_strategy1():
    move = next_move(0, 0, ADDRESSES[0])
    assert move == 0

    move = next_move(0, 0, ADDRESSES[0])
    assert move == 0

def test_strategy2():
    move = next_move(None, 0, ADDRESSES[1])
    assert move == 0

    move = next_move(move, 0, ADDRESSES[1])
    assert move == 1

    move = next_move(move, 0, ADDRESSES[1])
    assert move == 2

def test_strategy3():
    move1 = next_move(0, None, ADDRESSES[2])
    move2 = next_move(0, move1, ADDRESSES[2])
    assert move2 == (move1 + 1) % 3

    move3 = next_move(0, move2, ADDRESSES[2])
    assert move3 == (move2 + 1) % 3

'''def test_decode_move():
    #pylint: disable=C0301
    game_precommit = 'ada5013122d395ba3c54772283fb069b10426056ef8ca54750cb9bb552a59e7d'
    move = _decode_move(game_precommit)
    assert move == 0
'''