"""
battleships main app
"""

from flask import Flask
from config import Config

#load app and set config
app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

#add login manager and set redirect for pages needing authentication
from flask_login import LoginManager
login = LoginManager(app)
login.login_view = 'login' # internally used with url_for

#connect socketio for two way comms
from flask_socketio import SocketIO, emit, disconnect
async_mode = None ## TODO whats this
socketio = SocketIO(app, async_mode=async_mode)

#attach log hangler to main app
from app.logconfig import logger, handler
app.logger.addHandler(handler)

from app import routes

from app import sockety
