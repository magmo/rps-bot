import requests

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

def test_decode_move():
    #pylint: disable=C0301
    hex_message = '000000000000000000000000A1796Db2b57144a2C21A92AE647B86B9641A47ac00000000000000000000000000000000000000000000000000000000000001c8000000000000000000000000000000000000000000000000000000000000000200000000000000000000000035a2119712091a77B40FaB61ecabc8fBE950eb1600000000000000000000000055de2e479F3D0183D95f5A969bEEB3a147F6004900000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000b1a2bc2ec5000000000000000000000000000000000000000000000000000000b1a2bc2ec50000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000038d7ea4c680002f29e990b57b3c5621748e5dfb3cf7c098f0a3db21c5aa444bb8685f7042a29c'
    move = _decode_move(hex_message)
    assert move == 1

def test_strategy4(mocker):
    #pylint: disable=C0301
    hex_message1 = '000000000000000000000000A1796Db2b57144a2C21A92AE647B86B9641A47ac00000000000000000000000000000000000000000000000000000000000001c8000000000000000000000000000000000000000000000000000000000000000200000000000000000000000035a2119712091a77B40FaB61ecabc8fBE950eb1600000000000000000000000055de2e479F3D0183D95f5A969bEEB3a147F6004900000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000b1a2bc2ec5000000000000000000000000000000000000000000000000000000b1a2bc2ec50000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000038d7ea4c680002f29e990b57b3c5621748e5dfb3cf7c098f0a3db21c5aa444bb8685f7042a29c'
    move = next_move(None, None, ADDRESSES[3], hex_message=hex_message1)
    assert move == 2

    mocker.patch('requests.post')
    hex_message2 = '000000000000000000000000A1796Db2b57144a2C21A92AE647B86B9641A47ac00000000000000000000000000000000000000000000000000000000000001c8000000000000000000000000000000000000000000000000000000000000000200000000000000000000000035a2119712091a77B40FaB61ecabc8fBE950eb1600000000000000000000000055de2e479F3D0183D95f5A969bEEB3a147F6004900000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000b1a2bc2ec5000000000000000000000000000000000000000000000000000000b1a2bc2ec50000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000038d7ea4c680002f29e990b57b3c5621748e5dfb3cf7c098f0a3db21c5aa444bb8685f7042a29d'
    move = next_move(None, None, ADDRESSES[3], hex_message=hex_message2)
    assert move == 0
