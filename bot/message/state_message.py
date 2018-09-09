from flask import Blueprint, request
from flask.logging import logging

import bot.message.coder as coder

BOT_ID = '0x0000000000000000000000000000000000000B01'
bp = Blueprint('state_message', __name__, url_prefix='/message')

@bp.route('/state_message', methods=['POST'])
def state_message():
    hex_message = request.form['hex_message']
    d_channel = coder.extract_channel(hex_message)
    if BOT_ID not in d_channel['participants']:
        logging.warning('The message participants do not include a bot')

    return "That's it for now"