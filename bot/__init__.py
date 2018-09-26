from flask import Flask, g
import firebase_admin
from firebase_admin import db
from threading import Thread
from time import sleep

from bot import challenge


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config:
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


    @app.before_first_request
    def start_challenge_update():
        def run_challenge_update():
            while True:
                challenge.update_challenge_timestamp(db.reference())
                sleep(4)

        if not app.config.get('TESTING'):
            thread = Thread(target=run_challenge_update)
            thread.start()

    from bot import player
    app.register_blueprint(player.BP)
    return app
