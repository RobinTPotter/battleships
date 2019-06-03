from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from config import Config

import uuid

from app.logconfig import logger
from app import socketio


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

class GamePlayer():
    def __init__(self,id):
        self.player = id
        self.my_board = ([['water'] * 10] * 10)
        self.their_board = ([['water'] * 10] * 10)
        self.ready = False


class Game():
    stages = ['setup','playing','ended']
    
    def __init__(self):
        self.players = {}
        self.player_limit = 2
        self.players_turn = None
        self.first_joined = None
        self.stage_number = 0
        self.id = str(uuid.uuid4())
        logger.info('created game {0}'.format(self.id))

    def stage(self):
        return stages[self.stage_number]        

    def opponent(self,id):
        opp = [p for p in self.players.keys() if p is not id]
        if len(opp) == 0:
            return "no player yet"
        else:
            return opp[0]

    def list_players(self):
        return list(self.players.keys())

    def show_board(self,id):
        return self.players[id].my_board

    def show_opponent_view_board(self,id):
        return self.players[id].their_board

    def current_number_players(self):
        return len(self.players)

    def can_join(self):
        #return False
        return not self.player_limit == len(self.players)

    def join(self,player_id):
        ok = None
        if player_id not in self.players:
            if len(self.players.keys())==self.player_limit:
                ok=False
            else:
                self.players[player_id] = GamePlayer(player_id)
                ok=True
                if self.first_joined is None: self.first_joined = player_id
            
            if len(self.players.keys())==self.player_limit:
                self.players_turn = self.first_joined
        else:
            ok = False
         
        if ok:
            logger.info('going to emit now')
            socketio.emit('joined', {'id':player_id})
        return ok
    
    def is_player(self,username):
        return username in self.players

    def move(self,data):
        pass

    @socketio.on('ping')
    def ding(self):
        logger.info('DIINGNNGG!!')
        
