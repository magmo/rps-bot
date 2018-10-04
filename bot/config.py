from web3 import Web3

HEX_PREFIX = '0x'

BOT_ADDRESS = '55de2e479F3D0183D95f5A969bEEB3a147F60049'
BOT_NAME = 'Smart Bot'
BOT_STAKE = int(1e15)
WALLET_UID = '0000000000000000000000000b01'

BOT_PRIVATE_KEY = '854564512a7cfce09334f076b3d6922ed4e1be4f8368c1202ccc5df066a8f550'

def hex_to_str(hex_str):
    if not hex_str or len(hex_str) < len(HEX_PREFIX):
        return hex_str
    return hex_str[len(HEX_PREFIX):]

def str_to_hex(string):
    return HEX_PREFIX + string

def str_to_checksum_address(string):
    w3_instance = Web3()
    hex_string = str_to_hex(string)
    return w3_instance.toChecksumAddress(hex_string)
