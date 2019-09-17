from app import socketio
from app.database import users, games, get_game_from_id, get_user_from_id
from app.logconfig import logger
from flask_login import current_user
from flask import jsonify
from flask_socketio import join_room, leave_room

print (dir(socketio))

@socketio.on('ready')
def ready(data):
    logger.info(current_user)
    logger.info(data)
    id = current_user.id
    name = current_user.name
    game = data['game']
    actual_game = get_game_from_id(game)
    if actual_game is not None:
        actual_game.players[id].ready = True
        socketio.emit('player_ready', {'name':name})
        say_game_ready(actual_game)

def say_game_ready(actual_game):
    actual_game.set_next_player()
    areready = [p for p in actual_game.list_players() if actual_game.players[p].ready==True]
    logger.info('are ready {0}'.format(areready))
    if len(areready)==2:
        logger.info('both ready, playing')
        socketio.emit('game_on', {'name':actual_game.players_turn})

@socketio.on('joined')
def on_join(game_id):
    join_room(current_user.id+'_'+game_id)
    logger.info('joining room {0}_{1}'.format(current_user.id,game_id))
    actual_game = get_game_from_id(game_id)
    say_game_ready(actual_game)

@socketio.on('ping')
def ding(data):
    logger.info('ding')
    logger.info(current_user)
    logger.info(data)
    
@socketio.on('log')
def page_logging(data):
    logger.info(data)


@socketio.on('boat_moved')
def boat_moved(boat_game_user):
    logger.info('boat_moved')
    logger.info(current_user)
    logger.info(boat_game_user)
    updated_boat = boat_game_user['boat']
    user_id = boat_game_user['user']
    user = get_user_from_id(user_id)
    boat_name = updated_boat['name']
    game_id = boat_game_user['game']
    actual_game = get_game_from_id(game_id)
    boat_object = None
    boats = actual_game.get_boats(current_user.id)
    board = actual_game.get_board(current_user.id)
    logger.info(boats)
    logger.info(updated_boat)
    logger.info(user)
    boat_object = [b for b in boats if b.name==boat_name][0]
    logger.info(boat_object)
    new_placing = False
    illegal = False
    if boat_object.c==-1: new_placing = True
    # check for overlaps
    for bc in boats:
        if updated_boat['name']!=bc.name:
            for tr in range(updated_boat['r'],updated_boat['r']+updated_boat['height']):
                for tc in range(updated_boat['c'],updated_boat['c']+updated_boat['width']):
                    #logger.info('checking updated boat c{0}r{1}'.format(tc,tr))
                    for bctr in range(bc.r,bc.r+bc.height):
                        for bctc in range(bc.c,bc.c+bc.width):
                            #logger.info('checking test boat c{0}r{1}'.format(bctc,bctr))
                            if (bctc==tc and bctr==tr) or tr<0 or tc<0 or tr>=actual_game.rows or tc>=actual_game.columns:
                                illegal = True
                                logger.debug('checking updated boat c{0}r{1} and c{2}r{3} '.format(tc,tr,bctc,bctr))
                                break

    if not illegal:
        updated_boat['illegal']=0
        for k in vars(boat_object).keys():
            logger.info('{0} with {1}'.format(k,updated_boat[k]))
            if k in updated_boat: setattr(boat_object,k,updated_boat[k])
    else:
        logger.info('setting boat bck to illegal for definite')
        setattr(boat_object,'illegal', 1)
        
    logger.info(boat_object)
    socketio.emit('update_boat', str(boat_object), room='{0}_{1}'.format(current_user.id,game_id))
    