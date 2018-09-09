from flask import Flask
from bot.message import state_message

def create_app(test_config=None):
    app = Flask(__name__)
    app.register_blueprint(state_message.bp)
    return app