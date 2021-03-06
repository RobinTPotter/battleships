from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from config import Config
import json


import uuid

from app.logconfig import logger
from app import socketio

class Player(UserMixin):
    def __init__(self, username, password):
        self.id = str(uuid.uuid4())
        self.name = username
        self.set_password(password)
        self.games = []
    def set_password(self, password):
        self.password = generate_password_hash(password)
        logger.info('password reset')
    def check_password(self, password):
        ok = check_password_hash(self.password, password)
        logger.info('password check {0}'.format(ok))
        return ok or Config.NOPASSWORD_CHECK

class Boat():
    lengths = [5,4,3,3,2]
    names = ['carrier','battleship','submarine','cruiser','destroyer']
    def __init__(self,length=5, name=''):
        self.length = length
        self.c = -1
        self.r = -1
        self.left = 30
        self.top = 150
        self.horizontal = 1
        self.width = length
        self.height = 1
        self.name = name
        self.placed = 0
        self.illegal = 0
        
    def __repr__(self):
        return json.dumps({ 'length': self.length, 'name': self.name, 
                    'r': self.r, 'c': self.c,
                    'left': self.left,
                    'top': self.top,
                    'horizontal': self.horizontal,
                    'width': self.width,
                    'height': self.height,  
                    'placed': self.placed,  
                    'illegal': self.illegal                
                    })

class GamePlayer():
    def __init__(self,player):
        self.user = player
        self.player = player.id
        self.my_board = None
        self.their_board = None
        self.ready = False
        self.boats = [Boat(Boat.lengths[r], Boat.names[r]) for r in range(len(Boat.lengths))]
        i = 0
        for b in self.boats:
            b.top += 25*i
            i += 1
        
    def get_boats(self):
        return str([b for b in self.boats])

    def get_board(self):
        return str(self.my_board)


class Game():
    stages = ['setup','playing','ended']
    SETUP = 0
    PLAYING = 1
    ENDED = 2
    
    def __init__(self):
        self.players = {}
        self.player_limit = 2
        self.players_turn = None
        self.first_joined = None
        self.rows = 10
        self.columns = 10
        self.stage_number = Game.SETUP
        self.id = str(uuid.uuid4())
        self.border_spacing = 2
        self.cell_size = 25
        logger.info('created game {0}'.format(self.id))
    
    def generate_blank_board(self, who='you'):
        board = []
        for rr in range(self.rows):
            for cc in range(self.columns):
                board.append({ 'name': '{me}_c{cc}r{rr}'.format(me=who,cc=cc,rr=rr), 'c':cc, 'r':rr, 'type': 'water' })
        return board

    def stage(self):
        if len([p for p in self.players.keys() if self.players[p].ready==True])==self.player_limit:
            self.stage_number = Game.PLAYING
        return Game.stages[self.stage_number]        

    def opponent(self,id):
        opp = [p for p in self.players.keys() if p is not id]
        if len(opp) == 0:
            return "no player yet"
        else:
            from app.database import get_user_from_id
            o_id = opp[0]
            opp = get_user_from_id(o_id)
            logger.info('got opponent id {0} and object {1}'.format(o_id,opp))
            return opp.name
            
    
    def get_game_player(self,id):
        out = None
        if id in self.players:
            out = self.players[id]
        return out
        
    def get_user_player(self,id):
        out = None
        if id in self.players:
            from app.database import get_user_from_id
            out = get_user_from_id(self.players[id].id)
        return out

    def list_players(self):
        return list(self.players.keys())

    def get_board(self,id):
        return self.players[id].my_board

    def get_boats(self,id):
        return self.players[id].boats

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
                from app.database import get_user_from_id

                self.players[player_id] = GamePlayer(get_user_from_id(player_id))
                self.players[player_id].my_board = self.generate_blank_board('you')
                self.players[player_id].their_board = self.generate_blank_board('them')
                ok=True
                if self.first_joined is None: self.first_joined = self.players[player_id].user.name
            
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


