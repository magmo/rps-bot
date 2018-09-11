from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(test_config)

    from bot import player
    app.register_blueprint(player.BP)
    return app
