from firebase_admin import db
from eth_account import Account
from eth_account.messages import defunct_hash_message
from web3 import Web3

from bot.config import get_bot, get_bot_addr
from bot.config import K_ADDRESS, K_PK, K_STAKE, K_WALLET_UID, STAKES_IN_FUNDING
from bot.util import int_to_hex_str, str_to_hex, str_to_checksum_address, set_response_message

from bot import coder

K_WALLETS = 'wallets'
K_CHANNELS = 'channels'
K_RECEIVED = 'received'
K_SENT = 'sent'
K_UID = 'uid'
K_MESSAGE = 'message'
K_NONCE = 'nonce'

def _get_new_wallet(bot_index=0):
    bot = get_bot(bot_index)
    return {
        'address': bot[K_ADDRESS],
        K_CHANNELS: None,
        'privateKey': bot[K_PK],
        K_UID: str_to_hex(bot[K_WALLET_UID]),
        K_NONCE: -1
    }

def _get_account(bot_index=0):
    key = get_bot(bot_index)[K_PK]
    return Account.privateKeyToAccount(str_to_hex(key)) #pylint: disable=E1120

def get_wallets_ref():
    return db.reference().child(K_WALLETS)

def get_wallet_ref(wallet_key):
    return get_wallets_ref().child(wallet_key)

def create_wallet(bot_index=0):
    get_wallets_ref().push(_get_new_wallet(bot_index))

def get_wallet(bot_index=0):
    uid = get_bot(bot_index)[K_WALLET_UID]
    hex_uid = str_to_hex(uid)
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
    message_hash = Web3.sha3(hexstr=message)
    defunct_hash = defunct_hash_message(message_hash)
    acct = _get_account()
    signed_hash = acct.signHash(defunct_hash)
    return int_to_hex_str(signed_hash['r']) + int_to_hex_str(signed_hash['s']) \
        + int_to_hex_str(signed_hash['v'], 2)

def fund_adjudicator(contract_addr, bot_index=0):
    infura_endpoint = 'https://ropsten.infura.io/v3/2972b45cf9444a6d8f8695f6bdbc672f'
    from_addr = str_to_checksum_address(get_bot_addr(bot_index))
    to_addr = str_to_checksum_address(contract_addr)

    provider = Web3.HTTPProvider(infura_endpoint)
    o_w3 = Web3(provider)
    eth_nonce = o_w3.eth.getTransactionCount(from_addr) #pylint: disable=E1101

    def increment_nonce(wallet_nonce):
        if wallet_nonce is None:
            return eth_nonce
        new_nonce = wallet_nonce + 1 if wallet_nonce >= eth_nonce else eth_nonce
        return new_nonce

    _, wallet_key = get_wallet()
    nonce = get_wallet_ref(wallet_key).child(K_NONCE).transaction(increment_nonce)

    stake = get_bot(bot_index)[K_STAKE]
    transaction = {
        'nonce': nonce,
        'from': from_addr,
        'to': to_addr,
        'value': stake * STAKES_IN_FUNDING,
        'gas': 100000,
        'gasPrice': o_w3.eth.gasPrice #pylint: disable=E1101
    }
    private_k = get_bot(bot_index)[K_PK]
    signed = o_w3.eth.account.signTransaction(transaction, private_k) #pylint: disable=E1101
    _sent_tx = o_w3.eth.sendRawTransaction(signed.rawTransaction) #pylint: disable=E1101
    return set_response_message('Funding success with transaction hash of ' + signed.hash.hex())
