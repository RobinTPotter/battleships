from app import socketio
from app.database import users, games, get_game_from_id, get_user_from_id
from app.logconfig import logger

@socketio.on('ready')
def ready(data):
    logger.info(data)
    id = data['player']
    game = data['game']
    actual_game = get_game_from_id(game)
    if actual_game is not None:
        actual_game.players[id].ready = True
        socketio.emit('player_ready', {'id':id})
        areready = [p for p in actual_game.list_players() if actual_game.players[p].ready==True]
        logger.info('are ready {0}'.format(areready))
        if len(areready)==2:
            logger.info('both ready, playing')
            socketio.emit('game_on', {'id':actual_game.players_turn})



@socketio.on('ping')
def ding(self):
    logger.info('DIINGNNGG!!')
    logger.info(self)
    