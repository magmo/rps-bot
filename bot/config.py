from web3 import Web3

HEX_PREFIX = '0x'

BOT_ADDRESS = '0000000000000000000000000000000000000b01'
BOT_NAME = 'Smart Bot'
WALLET_UID = '0000000000000000000000000b01'

BOT_PRIVATE_KEY = 'eb5fb93933ab60f0292b4cff5d393c025f1506f2aaec9c14f5337d90f276d06e'
BOT_PUBLIC_KEY = '6198d26155fb9011652cb27b1a1cd34f2548587683035ffe47683a1412fb32b7b2b55fbf1234e41930edaecccb7b90c369f7ebafbc1c104e9cbc7849d14b4a50'

def hex_to_str(hex_str):
    if not hex_str or len(hex_str) < len(HEX_PREFIX):
        return hex_str
    return hex_str[len(HEX_PREFIX):]

def str_to_hex(string):
    return HEX_PREFIX + string

def str_to_checksum_address(string):
    w3 = Web3()
    hex_string = str_to_hex(string)
    return w3.toChecksumAddress(hex_string)
