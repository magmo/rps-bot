import firebase_admin
import pytest

import bot.fb_message
from bot.config import ADDRESSES
from bot.util import str_to_hex

@pytest.mark.usefixtures("test_app")
def test_message_opponent(mocker):
    #pylint: disable=C0301
    message = '000000000000000000000000c1912fee45d61c87cc5ea59dae31190fffff232d00000000000000000000000000000000000000000000000000000000000001c800000000000000000000000000000000000000000000000000000000000000020000000000000000000000005291fA3F70C8e3D21B58c831018E5a0D82Dc4ab900000000000000000000000055de2e479F3D0183D95f5A969bEEB3a147F60049000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000006a94d74f430000000000000000000000000000000000000000000000000000006a94d74f4300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002386f26fc10000'
    signature = '0x708b8791d6054bda70f260a1f47a71ea47942f96bee5a2dfe232fa1d2c4ce3fc3806c6a87d8ecb889d019169b2710d3e833dabba8d6aa872fc49de420bb3a27d1c'
    mocker.patch('firebase_admin.db.Reference.push')
    bot.fb_message.message_opponent(message, ADDRESSES[0])
    d_push = {'data': str_to_hex(message), 'signature': signature, 'queue': 'GAME_ENGINE'}
    firebase_admin.db.Reference.push.assert_called_once_with(d_push) # pylint: disable=no-member

@pytest.mark.usefixtures("test_app")
def test_message_consumed(mocker):
    # Need to get a valid key for an end to end test
    mocker.patch('firebase_admin.db.Reference.delete')
    bot.fb_message.message_consumed('-LNe4HoVe29ILP0kT177', ADDRESSES[0])
    firebase_admin.db.Reference.delete.assert_called_once() # pylint: disable=no-member
