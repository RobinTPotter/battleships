
from app.models import Player, Game

from app.logconfig import logger

users = []
users.append(Player('robin', 'nobby'))
users.append(Player('nobby', 'robin'))

games = [Game(),Game()]
logger.info('ceated default users and 2 games')

def get_game_from_id(game_id):
    game_out = None
    
    if game_id in [g.id for g in games]:
        game_out = [g for g in games if g.id == game_id][0]
        
    return game_out    
    
def get_user_from_id(user_id):
    user = None
    
    if user_id in [u.id for u in users]:
        user = [u for u in users if u.id == user_id][0]
        
    return user    
     
def get_user_from_name(name):
    user = None
    
    if name in [u.name for u in users]:
        user = [u for u in users if u.name == name][0]
        
    return user    
    