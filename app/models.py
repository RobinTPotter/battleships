from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from config import Config


import uuid

from app.logconfig import logger
from app import socketio

logger.info(dir(socketio))

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

class Boat():
    lengths = [5,4,3,3,2]
    names = ['carrier','battleship','submarine','cruiser','destroyer']
    def __init__(self,length=5, name=''):
        self.length = length
        self.offset_x = None
        self.offset_y = None
        self.name = name
        self.block = 21

class GamePlayer():
    def __init__(self,id):
        self.player = id
        self.my_board = ([['water'] * 10] * 10)
        self.their_board = ([['water'] * 10] * 10)
        self.ready = False
        self.boats = [Boat(Boat.lengths[r], Boat.names[r]) for r in range(len(Boat.lengths))]
    def get_boats(self):
        return self.boats


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
        self.border_spacing = 5
        self.cell_size = 25

    def stage(self):
        return Game.stages[self.stage_number]        

    def opponent(self,id):
        opp = [p for p in self.players.keys() if p is not id]
        if len(opp) == 0:
            return "no player yet"
        else:
            return opp[0]
    
    def get_game_player(self,id):
        out = None
        if id in self.players:
            out = self.players[id]
        return out
        
    def get_user_player(self,id):
        out = None
        if id in self.players:
            out = get_user_from_id(self.players[id].id)
        return out

    def list_players(self):
        return list(self.players.keys())

    def show_board(self,id):
        return self.players[id].my_board

    def show_ready(self,id):
        return self.players[id].ready

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
    
    def set_next_player(self):
        players = [p for p in self.players if p != self.players_turn]
        if len(players)==1:
            if players[0] != self.players_turn: socketio.emit('player_turn_changed',{'id': self.players_turn})
            self.players_turn = players[0]

    def is_player(self,username):
        return username in self.players


