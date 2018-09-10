PREFIX = '0x'
CHARS_PER_BYTE = 2
N_PLAYERS = 2
F_WIDTH = 32
ADDRESS_WIDTH = 20

CHANNEL_BYTES = F_WIDTH + F_WIDTH + F_WIDTH + F_WIDTH * N_PLAYERS #type, nonce, nPlayers, [players]
STATE_BYTES = F_WIDTH + F_WIDTH + F_WIDTH + F_WIDTH * N_PLAYERS #stateType, turnNum, stateCount, [balances]
GAME_ATTRIBUTE_OFFSET = CHANNEL_BYTES + STATE_BYTES

class CoderError(Exception):
    pass

class NumPlayersError(CoderError):
    def __init__(self, num_players):
       self.num_players = num_players

    def __str__(self):
        return f'Rock-paper-scissors requires exactly {N_PLAYERS} players. {self.num_players} provided.'

def extract_bytes(h_string, byte_offset = 0, num_bytes = F_WIDTH):
    char_offset = len(PREFIX) + byte_offset * CHARS_PER_BYTE
    return h_string[char_offset:char_offset + num_bytes * CHARS_PER_BYTE]

def extract_int(h_string, byte_offset = 0, num_bytes = 32):
    return int(extract_bytes(h_string, byte_offset, num_bytes), 16)

''' Channel attribute getters'''
def get_address_from_field(field):
    return field[CHARS_PER_BYTE * (F_WIDTH - ADDRESS_WIDTH):]

def get_channel_byte_attribute(h_message, attr_index):
    return extract_bytes(h_message, F_WIDTH * attr_index)

def get_channel_int_attribute(h_message, attr_index):
    return extract_int(h_message, F_WIDTH * attr_index)

def get_channel_type(h_message):
    type = get_channel_byte_attribute(h_message, 0)
    return get_address_from_field(type)

def get_channel_nonce(h_message):
    return get_channel_int_attribute(h_message, 1)

def get_channel_num_players(h_message):
    num_players = get_channel_int_attribute(h_message, 2)
    if num_players != N_PLAYERS:
        raise NumPlayersError(num_players)

def get_channel_players(h_message):
    player_a = get_channel_byte_attribute(h_message, 3)
    player_b = get_channel_byte_attribute(h_message, 4)
    return [get_address_from_field(player_a), get_address_from_field(player_b)]


''' State attribute getters '''
def get_state_int_attribute(h_message, attr_index):
    return extract_int(h_message, CHANNEL_BYTES + F_WIDTH * attr_index)

def get_channel_state(h_message):
    return get_state_int_attribute(h_message, 0)

def get_state_turn_num(h_message):
    return get_state_int_attribute(h_message, 1)

def get_state_count(h_message):
    return get_state_int_attribute(h_message, 2)
