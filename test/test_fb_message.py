import firebase_admin
from firebase_admin import db

import bot.fb_message
from bot.util import str_to_hex

def test_message_opponent(app, mocker):
    #pylint: disable=C0301
    message = '000000000000000000000000c1912fee45d61c87cc5ea59dae31190fffff232d00000000000000000000000000000000000000000000000000000000000001c800000000000000000000000000000000000000000000000000000000000000020000000000000000000000005291fA3F70C8e3D21B58c831018E5a0D82Dc4ab900000000000000000000000055de2e479F3D0183D95f5A969bEEB3a147F60049000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000006a94d74f430000000000000000000000000000000000000000000000000000006a94d74f4300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002386f26fc10000'
    signature = '0x7f705e5b60f7d7c1360cdccafa6d2656d30fda922a63dc265fde6b387c34142d3e76759a9afdd1c65769a48b95d2126d89192b3b3f4f1515dafdf96d7b34aa6a1b'
    mocker.patch('firebase_admin.db.Reference.push')
    bot.fb_message.message_opponent(message)
    d_push = {'data': str_to_hex(message), 'signature': signature, 'queue': 'GAME_ENGINE'}
    firebase_admin.db.Reference.push.assert_called_once_with(d_push) # pylint: disable=no-member

def test_message_consumed(app, mocker):
    # Need to get a valid key for an end to end test
    mocker.patch('firebase_admin.db.Reference.delete')
    bot.fb_message.message_consumed('-LNe4HoVe29ILP0kT177')
    firebase_admin.db.Reference.delete.assert_called_once() # pylint: disable=no-member
