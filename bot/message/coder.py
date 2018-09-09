PREFIX = '0x'
PREFIX_OFFSET = len(PREFIX)
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
    char_offset = PREFIX_OFFSET + byte_offset * CHARS_PER_BYTE
    return PREFIX + h_string[char_offset:char_offset + num_bytes * CHARS_PER_BYTE]

def extract_int(h_string, byte_offset = 0, num_bytes = 32):
    return int(extract_bytes(h_string, byte_offset, num_bytes), 16)

def extract_channel(h_message):
    offset_so_far = F_WIDTH - ADDRESS_WIDTH
    type = extract_bytes(h_message, offset_so_far, ADDRESS_WIDTH)    
    offset_so_far += ADDRESS_WIDTH

    nonce = extract_int(h_message, offset_so_far)
    offset_so_far +=F_WIDTH
    
    num_players = extract_int(h_message, offset_so_far)
    offset_so_far +=F_WIDTH

    if num_players != N_PLAYERS:
        raise NumPlayersError(num_players)

    offset_so_far += F_WIDTH - ADDRESS_WIDTH
    participant_a = extract_bytes(h_message, offset_so_far, ADDRESS_WIDTH)
    offset_so_far += ADDRESS_WIDTH

    offset_so_far += F_WIDTH - ADDRESS_WIDTH
    participant_b = extract_bytes(h_message, offset_so_far, ADDRESS_WIDTH)
    return {'type': type, 'nonce': nonce, 'participants': [participant_a, participant_b]}

def decode(h_message):
    pass
    #channel = extract_channel(h_message)
    #turnNum = extractTurnNum(hexMessage)
    #stateType = extractStateType(hexString)
    #balances = extractBalances(hexString)

    #return {'channel': channel}

def encode(sMessage):
    pass