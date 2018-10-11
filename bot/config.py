from collections import OrderedDict

FINNEY = int(1e15)
STAKES_IN_FUNDING = 50
NUM_BOTS = 3

ADDRESSES = [
    '55de2e479F3D0183D95f5A969bEEB3a147F60049',
    '55de2e479F3D0183D95f5A969bEEB3a147F60048',
    '55de2e479F3D0183D95f5A969bEEB3a147F60047']


NAMES = ['Young Bot', 'Muscle Bot', 'Fine Taste Bot']

WALLET_UID = [
    '0000000000000000000000000b00',
    '0000000000000000000000000b01',
    '0000000000000000000000000b02'
]

PKS = [
    '854564512a7cfce09334f076b3d6922ed4e1be4f8368c1202ccc5df066a8f550',
    '854564512a7cfce09334f076b3d6922ed4e1be4f8368c1202ccc5df066a8f550',
    '854564512a7cfce09334f076b3d6922ed4e1be4f8368c1202ccc5df066a8f550'
]

K_ADDRESS = 'bot_addr'
K_NAME = 'bot_name'
K_WALLET_UID = 'bot_wallet_uid'
K_PK = 'bot_pk'
K_STAKE = 'bot_stake'

_BOTS = OrderedDict()

def create_bots():
    for i_bot in range(0, NUM_BOTS):
        bot = {}
        bot[K_ADDRESS] = ADDRESSES[i_bot]
        bot[K_NAME] = NAMES[i_bot]
        bot[K_WALLET_UID] = WALLET_UID[i_bot]
        bot[K_PK] = PKS[i_bot]
        bot[K_STAKE] = FINNEY
        _BOTS[ADDRESSES[i_bot]] = bot

def get_bot(addr=None, index=0):
    if not _BOTS:
        create_bots()

    if addr:
        return _BOTS[addr]
    return list(_BOTS.values())[index]

def get_bot_addr(index=0):
    return get_bot(index=index)[K_ADDRESS]
