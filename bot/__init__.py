from threading import Thread
from time import sleep

from flask import Flask, g, request
from flask.logging import logging
import firebase_admin
from firebase_admin import db


from bot import challenge


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config:
        app.config.update(test_config)

    app.logger.setLevel(logging.INFO)
    @app.before_request
    def _log_request_info():
        app.logger.debug(f'Headers: {request.headers}')
        app.logger.debug(f'Body: {request.get_data()}')

    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(options={
            'databaseURL': 'https://rock-paper-scissors-dev.firebaseio.com',
            'projectId': 'rock-paper-scissors-dev'
        })


    @app.before_first_request
    def _start_challenge_update():
        def run_challenge_update():
            while True:
                challenge.update_challenge_timestamp(db.reference())
                sleep(4)

        if not app.config.get('TESTING'):
            thread = Thread(target=run_challenge_update)
            thread.start()

    def set_db():
        g.db = db.reference()
    app.before_request(set_db)

    from bot import player
    app.register_blueprint(player.BP)
    return app
