CHARS_PER_BYTE = 2
N_PLAYERS = 2
F_WIDTH = 32
ADDRESS_WIDTH = 20

# type, nonce, nPlayers, [players]
CHANNEL_BYTES = F_WIDTH + F_WIDTH + F_WIDTH + F_WIDTH * N_PLAYERS
# stateType, turnNum, stateCount, [balances]
STATE_BYTES = F_WIDTH + F_WIDTH + F_WIDTH + F_WIDTH * N_PLAYERS
''' RockPaperScissors Game Fields
    (relative to game offset)
    ==============================
    [  0 -  31] enum positionType
    [ 32 -  63] uint256 stake
    [ 64 -  95] bytes32 preCommit
    [ 96 - 127] enum bPlay
    [128 - 159] enum aPlay
    [160 - 191] bytes32 salt
    [192 - 223] uint256 roundNum
'''
GAME_OFFSET = CHANNEL_BYTES + STATE_BYTES


class CoderError(Exception):
    pass

class NumPlayersError(CoderError):
    def __init__(self, num_players):
        super().__init__()
        self.num_players = num_players

    def __str__(self):
        return f'Rock-paper-scissors requires exactly ' + \
            '{N_PLAYERS} players. {self.num_players} provided.'

def int_to_field(num):
    h_num = format(num, 'x')
    return '{:0>64}'.format(h_num)

def extract_bytes(h_string, byte_offset=0, num_bytes=F_WIDTH):
    char_offset = byte_offset * CHARS_PER_BYTE
    return h_string[char_offset:char_offset + num_bytes * CHARS_PER_BYTE]

def extract_int(h_string, byte_offset=0, num_bytes=32):
    return int(extract_bytes(h_string, byte_offset, num_bytes), 16)

def get_address_from_field(field):
    return field[CHARS_PER_BYTE * (F_WIDTH - ADDRESS_WIDTH):]

def get_byte_attribute_at_offset(h_message, offset, attr_index):
    return extract_bytes(h_message, offset + F_WIDTH * attr_index)

def get_int_attribute_at_offset(h_message, offset, attr_index):
    return extract_int(h_message, offset + F_WIDTH * attr_index)

def update_field(h_message, offset, attr_index, new_field):
    field_offset = (offset + F_WIDTH * attr_index) * CHARS_PER_BYTE
    prefix = h_message[:field_offset]
    suffix = h_message[field_offset + F_WIDTH * CHARS_PER_BYTE:]
    return prefix + new_field + suffix

# Channel attribute getters
def get_channel_byte_attribute(h_message, attr_index):
    return get_byte_attribute_at_offset(h_message, 0, attr_index)

def get_channel_int_attribute(h_message, attr_index):
    return get_int_attribute_at_offset(h_message, 0, attr_index)

def get_channel_type(h_message):
    channel_type = get_channel_byte_attribute(h_message, 0)
    return get_address_from_field(channel_type)

def get_channel_nonce(h_message):
    return get_channel_int_attribute(h_message, 1)

def get_channel_num_players(h_message):
    num_players = get_channel_int_attribute(h_message, 2)
    if num_players != N_PLAYERS:
        raise NumPlayersError(num_players)
    return num_players

def assert_channel_num_players(h_message):
    get_channel_num_players(h_message)

def get_channel_players(h_message):
    player_a = get_channel_byte_attribute(h_message, 3)
    player_b = get_channel_byte_attribute(h_message, 4)
    return [get_address_from_field(player_a), get_address_from_field(player_b)]


# State attribute getters
def get_state_int_attribute(h_message, attr_index):
    return get_int_attribute_at_offset(h_message, CHANNEL_BYTES, attr_index)

def get_channel_state(h_message):
    return get_state_int_attribute(h_message, 0)

def get_state_turn_num(h_message):
    return get_state_int_attribute(h_message, 1)

def get_state_count(h_message):
    return get_state_int_attribute(h_message, 2)

def increment_state_turn_num(h_message):
    turn_num = get_state_turn_num(h_message)
    turn_num += 1
    return update_field(h_message, CHANNEL_BYTES, 1, int_to_field(turn_num))

def increment_channel_state(h_message):
    state = get_channel_state(h_message)
    state += 1
    return update_field(h_message, CHANNEL_BYTES, 2, int_to_field(state))

# Game attribute getters
def get_game_byte_attribute(h_message, attr_index):
    return get_byte_attribute_at_offset(h_message, GAME_OFFSET, attr_index)

def get_game_int_attribute(h_message, attr_index):
    return get_int_attribute_at_offset(h_message, GAME_OFFSET, attr_index)

def get_game_position_type(h_message):
    return get_game_int_attribute(h_message, 0)

def get_game_stake(h_message):
    return get_game_int_attribute(h_message, 1)

def get_game_precommit(h_message):
    return get_game_byte_attribute(h_message, 2)

def get_game_bplay(h_message):
    return get_game_int_attribute(h_message, 3)

def get_game_aplay(h_message):
    return get_game_int_attribute(h_message, 4)

def get_game_salt(h_message):
    return get_game_byte_attribute(h_message, 5)
