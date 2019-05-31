from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from config import Config

import uuid

from app.logconfig import logger


class Player(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.set_password(password)
        self.games = []
    def set_password(self, password):
        self.password = generate_password_hash(password)
        logger.info('password reset')
    def check_password(self, password):
        ok = check_password_hash(self.password, password)
        logger.info('password check {0}'.format(ok))
        return ok
    def join_game(self, game):
        if game not in games:
            games.append(game)
            return True
        return False


class Game():
    def __init__(self):
        self.players = []
        self.player_limit = 2
        self.player_in_turn = None
        self.id = str(uuid.uuid4())
        self.board = [[None] * 10] * 10
        logger.info('created game {0} {1}'.format(self.id, self.board))

    def current_number_players(self):
        return len(self.players)

    def can_join(self):
        #return False
        return not self.player_limit == len(self.players)

    def join(self,player):
        ok = None
        if player not in self.players:
            if len(self.players)==self.player_limit:
                ok=False
            else:
                self.players.append(player)
                ok=True
            
            if len(self.players)==self.player_limit:
                self.player_in_turn = 0
        else:
            ok = False
            
        return ok
    
    def is_player(self,username):
        return username in [p for p in self.players]

    def move(self,data):
        pass
        
