import pytest
import web3

from bot.config import ADDRESSES
import bot.wallet
from util import get_wallets_fn

#pylint: disable=C0301
MESSSAGE = '000000000000000000000000c1912fee45d61c87cc5ea59dae31190fffff232d00000000000000000000000000000000000000000000000000000000000001c800000000000000000000000000000000000000000000000000000000000000020000000000000000000000005291fA3F70C8e3D21B58c831018E5a0D82Dc4ab900000000000000000000000055de2e479F3D0183D95f5A969bEEB3a147F60049000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000006a94d74f430000000000000000000000000000000000000000000000000000006a94d74f4300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002386f26fc10000'

def test_sign_message():
    signature = bot.wallet.sign_message(MESSSAGE, ADDRESSES[0])
    assert signature == '708b8791d6054bda70f260a1f47a71ea47942f96bee5a2dfe232fa1d2c4ce3fc3806c6a87d8ecb889d019169b2710d3e833dabba8d6aa872fc49de420bb3a27d1c'

@pytest.mark.usefixtures("test_app")
def test_fund_adjudicator(mocker):
    #pylint: disable=C0301
    tx_hash = '0x8bac5e6025bfed10b752741d40bb165c70e1d3cd0edcf089c4fba8c63b5e6836'
    mocker.patch('firebase_admin.db.Query.get', new=get_wallets_fn('wallets'))
    mocker.patch('firebase_admin.db.Reference.transaction', lambda _1, _2: 10)
    mocker.patch('web3.eth.Eth.gasPrice', 2000000000)
    mocker.patch('web3.eth.Eth.sendRawTransaction', autospec=True)
    response = bot.wallet.fund_adjudicator('cdb594a32b1cc3479d8746279712c39d18a07fc0', ADDRESSES[0])

    web3.eth.Eth.sendRawTransaction.assert_called_once() # pylint: disable=no-member
    assert response['message'] == f'Funding success with transaction hash of {tx_hash}'

def test_record_received_message():
    # This test uses the test Firebase realtime database
    bot.wallet.record_received_message(MESSSAGE, ADDRESSES[0])
