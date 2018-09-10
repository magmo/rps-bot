from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(test_config)

    from bot.message import state_message
    app.register_blueprint(state_message.bp)
    return app