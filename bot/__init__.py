from os import environ
from threading import Thread
from time import sleep

import firebase_admin
from flask import Flask, g, request
from flask.logging import logging

from bot import challenge

def get_project_name():
    return environ.get('GOOGLE_CLOUD_PROJECT', 'rock-paper-scissors-dev')

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
        project_name = get_project_name()
        firebase_admin.initialize_app(options={
            'databaseURL': f'https://{project_name}.firebaseio.com',
            'projectId': project_name
        })


    from bot import player
    app.register_blueprint(player.BP)
    return app
