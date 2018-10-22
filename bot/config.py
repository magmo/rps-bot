from collections import OrderedDict

ROPSTEN = 'ropsten'
KOVAN = 'kovan'
TESTNET = ROPSTEN

FINNEY = int(1e15)
STAKES_IN_FUNDING = 50
NUM_BOTS = 4

NUM_MOVES = 3

ADDRESSES = [
    '55de2e479f3d0183d95f5a969beeb3a147f60049',
    '7892ea3a79ffb40388d6769ef58642b3e4412fbb',
    '9f2495062cd959c42e5bb2867138a125c63fb17a',
    'b7dcd4ff30040c58eda8ba3bca6736fdad467660']


NAMES = ['Young Bot', 'Muscle Bot', 'Fine Taste Bot', 'Psychic Bot']

WALLET_UID = [
    '0000000000000000000000000b00',
    '0000000000000000000000000b01',
    '0000000000000000000000000b02',
    '0000000000000000000000000b03',
]

PKS = [
    '854564512a7cfce09334f076b3d6922ed4e1be4f8368c1202ccc5df066a8f550',
    'A39E13320C7752AEA43CE032CF40EF6B10BDC7753AA8B98A07F9477F30C8AC8F',
    '0000000000000000000000000000000000000000000000000000000000000b02',
    '0000000000000000000000000000000000000000000000000000000000000b03'
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
