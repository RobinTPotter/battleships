from app.models import Player, Game
from app.logconfig import logger
users = []
users.append(Player('robin', 'nobby'))
users.append(Player('nobby', 'robin'))
games = [Game(),Game()]
logger.info('ceated default users and 2 games')
