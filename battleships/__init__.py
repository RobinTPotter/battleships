from config import PORT, DEFAULTNAME, LOGNAME
import logging

formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger = logging.getLogger(LOGNAME)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

logger.error('just kidding')



from flask import Flask
from flask import render_template, url_for, request, session, redirect
import json, re
import os
import random
import datetime
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

async_mode = None ## TODO whats this
from player import Player
from game import Game


whereme = os.path.dirname(os.path.realpath(__file__))
template_folder=whereme+'/templates'
static_folder=whereme+'/static'

app = Flask('battleships',static_folder=static_folder, template_folder=template_folder)
app.secret_key = 'any random string'
app.permanent_session_lifetime = datetime.timedelta(days=365)

players = {}
games = {}

new_game = Game()
games[new_game.id] = new_game

socketio = SocketIO(app, async_mode=async_mode)

'''
@app.route('/')
def index():
    ##session['username'] = request.form['username']
    print (session)
    return render_template('index.html') #.decode('utf-8')).decode('utf-8'))
'''

def create_games_object():
    thing = [{'id': games[g].id, 'in': games[g].current_number_players(), 'total': games[g].player_limit} for g in games]
    return thing

@app.route('/', methods=['GET', 'POST'])
def index(default=DEFAULTNAME):
    trying = 1
    while default in players:
        default = DEFAULTNAME + str(trying)
        trying += 1

    if 'username' in session:
        username = session['username']
        if username in players:
            player = players[username]
            g = create_games_object()
            logger.info('games {0}'.format(g))
            return render_template('index.html', player=player, game_list=g, player_list=players.keys())
        else:
            session.pop('username', None)

    return render_template('player.html', name=default)

@app.route('/join', methods=['POST'])
def join():
    logger.info(dir(request))
    logger.info(request.form)
    name = request.form.get('username')
    if name_taken(name): return redirect(url_for('index', name=name+'x'))
    else:
        session['username'] = name
        players[name] = Player(name)
        player = players[name]
        g = create_games_object()
        return render_template('index.html', player=player, game_list=g, player_list=players.keys())

@app.route('/game/<string:id>')
def game(id):
    username = session['username']
    if username in players:
        player = players[username]
        game = games[id]
        return render_template('game.html', player=player, game=game)

@socketio.on('join_request')
def check_username(message):
    logger.info('join request {0}'.format(message))
    game = games[message['game']]
    if game.join(players[message['username']]) or game.is_player(message['username']): socketio.emit('join_success', {'id': message['game'] })

@socketio.on('checkname')
def check_username(message):
    if name_taken(message['username']): socketio.emit('username_taken', {'status': 'taken'})
    else: socketio.emit('username_free', {'status': 'free'})

def name_taken(name):
    if name in players: return True
    else: return False

@socketio.on('ping')
def ping(message):
    logger.info(message)




if __name__ == "__main__":
    app.debug = True
    logger.info('created app {0}'.format(app))
    app.run(host='0.0.0.0', port=PORT, threaded=True, extra_files=[template_folder+'/index.html','config.py'])
