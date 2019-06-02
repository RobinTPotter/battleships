from flask import Flask
from config import Config
from flask_login import LoginManager

from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

async_mode = None ## TODO whats this
from app.logconfig import logger, ch

app = Flask(__name__, static_url_path='/static')
app.logger.addHandler(ch)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login' # internally used with url_for


socketio = SocketIO(app, async_mode=async_mode)



from app import routes
