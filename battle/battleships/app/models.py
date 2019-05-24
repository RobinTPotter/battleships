from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import login #this is the batteships app

class Player(UserMixin):
    games = []
    def __init__(self, username, password):
        self.id = username
        self.set_password(password)
    def set_password(self, password):
        self.password = generate_password_hash(password)
		
    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(id):
    print('loading user.... '+str(id))
    return User.query.get(int(id))