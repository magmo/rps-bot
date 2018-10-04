from flask import g
from eth_account import Account
from eth_account.messages import defunct_hash_message

from web3 import Web3

from bot.config import BOT_ADDRESS, BOT_PRIVATE_KEY, BOT_STAKE, STAKES_IN_FUNDING, WALLET_UID
from bot.util import str_to_hex, str_to_checksum_address

from bot import coder

K_WALLETS = 'wallets'
K_CHANNELS = 'channels'
K_RECEIVED = 'received'
K_SENT = 'sent'
K_UID = 'uid'
K_MESSAGE = 'message'

NEW_WALLET = dict(
    address=str_to_hex(BOT_ADDRESS),
    channels=None,
    privateKey=BOT_PRIVATE_KEY,
    uid=str_to_hex(WALLET_UID)
)

def _get_account():
    return Account.privateKeyToAccount(str_to_hex(BOT_PRIVATE_KEY)) #pylint: disable=E1120

def get_wallets_ref():
    return g.db.child(K_WALLETS)

def get_wallet_ref(wallet_key):
    return get_wallets_ref().child(wallet_key)

def create_wallet():
    get_wallets_ref().push(NEW_WALLET)

def get_wallet():
    hex_uid = str_to_hex(WALLET_UID)
    wallets_ref = get_wallets_ref()
    bot_wallet_query = wallets_ref.order_by_child(K_UID).equal_to(hex_uid).limit_to_first(1)
    wrapped_wallet = bot_wallet_query.get()
    if not wrapped_wallet:
        create_wallet()
        wrapped_wallet = bot_wallet_query.get()

    return (list(wrapped_wallet.values())[0], list(wrapped_wallet.keys())[0])

def clear_wallet_channels():
    _, wallet_key = get_wallet()
    get_wallet_ref(wallet_key).child(K_CHANNELS).delete()

def get_last_message_for_channel(hex_message):
    wallet = get_wallet()[0]
    channels = wallet.get(K_CHANNELS)
    if not channels:
        return None

    channel_id = coder.get_channel_id(hex_message)
    last_message = None
    try:
        last_message = channels[channel_id][K_RECEIVED][K_MESSAGE]
    except KeyError:
        pass

    return last_message

def record_received_message(hex_message):
    wallet, wallet_key = get_wallet()
    channel_id = coder.get_channel_id(hex_message)

    channels = wallet.get(K_CHANNELS, {})
    channel = channels.get(channel_id, {})
    received = channel.get(K_RECEIVED, {})

    received[K_MESSAGE] = str_to_hex(hex_message)
    channel[K_RECEIVED] = received
    channels[channel_id] = channel
    wallet[K_CHANNELS] = channels

    get_wallet_ref(wallet_key).update(wallet)

def sign_message(message):
    message_hash = defunct_hash_message(hexstr=message)
    acct = _get_account()
    signed_message = acct.signHash(message_hash)
    return signed_message['signature'].hex()

def fund_adjudicator(contract_addr=None):
    #hardcoded_addr = str_to_checksum_address('cdb594a32b1cc3479d8746279712c39d18a07fc0')
    infura_endpoint = 'https://ropsten.infura.io/v3/2972b45cf9444a6d8f8695f6bdbc672f'
    from_addr = str_to_checksum_address(BOT_ADDRESS)
    to_addr = str_to_checksum_address(contract_addr)

    provider = Web3.HTTPProvider(infura_endpoint)
    o_w3 = Web3(provider)
    nonce = o_w3.eth.getTransactionCount(from_addr) + 1 #pylint: disable=E1101
    transaction = {
        'nonce': nonce,
        'from': from_addr,
        'to': to_addr,
        'value': BOT_STAKE * STAKES_IN_FUNDING,
        'gas': 100000,
        'gasPrice': o_w3.eth.gasPrice #pylint: disable=E1101
    }
    signed = o_w3.eth.account.signTransaction(transaction, BOT_PRIVATE_KEY) #pylint: disable=E1101
    o_w3.eth.sendRawTransaction(signed.rawTransaction) #pylint: disable=E1101
    return {'message': 'funding success'}
