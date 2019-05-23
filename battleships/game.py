import uuid
from config import LOGNAME
import logging
logger = logging.getLogger(LOGNAME)

class Game():
    players = []
    player_limit = 2
    player_in_turn = None
    board = None
    id = None
    
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.board = [[None] * 10] * 10
        logger.info('created game {0} {1}'.format(self.id, self.board))

    def current_number_players(self):
        return len(self.players)

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
        return username in [p.name for p in self.players]

    def move(self,data):
        pass
        