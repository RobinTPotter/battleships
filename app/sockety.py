from app import socketio
from app.database import users, games, get_game_from_id, get_user_from_id
from app.logconfig import logger
from flask_login import current_user

@socketio.on('ready')
def ready(data):
    logger.info(current_user)
    logger.info(data)
    id = current_user
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
def ding(data):
    logger.info('ding')
    logger.info(current_user)
    logger.info(data)
    
@socketio.on('boat_moved')
def boat_moved(boat_game):
    logger.info('boat_moved')
    logger.info(current_user)
    logger.info(boat_game)
    boat = boat_game['boat']
    boat_name = boat['name']
    game_id = boat_game['game']
    actual_game = get_game_from_id(game_id)
    boat_object = None
    boats = actual_game.get_boats(current_user.id)
    board = actual_game.get_board(current_user.id)
    logger.info(boats)
    logger.info(boat)
    boat_object = [b for b in boats if b.name==boat_name][0]
    logger.info(boat_object)
    socketio.emit('update_boat', {'hail':'plop'})
    