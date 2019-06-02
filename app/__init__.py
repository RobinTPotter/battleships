from flask import Flask
from config import Config
from flask_login import LoginManager


from app.logconfig import logger, ch

app = Flask(__name__, static_url_path='/static')
app.logger.addHandler(ch)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login' # internally used with url_for



from app import routes
