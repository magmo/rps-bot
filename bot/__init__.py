from flask import Flask
from flask import g
import firebase_admin
from firebase_admin import db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(test_config)

    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(options={
            'databaseURL': 'https://rock-paper-scissors-dev.firebaseio.com',
            'projectId': 'rock-paper-scissors-dev'
        })

    def set_db():
        g.db = db.reference()

    app.before_request(set_db)

    from bot import player
    app.register_blueprint(player.BP)
    return app
