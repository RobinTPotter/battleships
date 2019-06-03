from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, RegistrationForm  #i didn't steal this bit
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from app.models import Player, Game
from werkzeug.urls import url_parse

from app import login #this is the batteships app intance of flask_logined thing
from app.database import users, games
from app.logconfig import logger

logger.debug('hello from routes')

@login.user_loader
def load_user(id):
    logger.debug('loading user.... '+str(id))
    got_user = [u for u in users if u.id==id]
    if len(got_user)==0: return None
    else: return got_user[0]


@app.route('/')
@app.route('/index')
def index():
    user = current_user
    logger.info(user)
    return render_template('index.html', title='Home', games=games)


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        ##flash('login requested fir user {0}, remember me={1}'.format(form.username.data, form.remember_me.data))
        user = None
        if form.username.data in [u.id for u in users]:
            user = [u for u in users if u.id==form.username.data][0]
            logger.info('found user {0}'.format(user))
        if user is None or not user.check_password(form.password.data):
            logger.info('found user {0} and {1} ({2})'.format(user, user.check_password(form.password.data), form.password.data))
            flash('invalid user name or password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        logger.debug('next page {0}'.format(next_page))
        if not next_page or url_parse(next_page).netloc != '':
            #checks to see if the next is tampered with to got outside
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/game/<string:id>')
@login_required
def game(id):
    games_ids = [g.id for g in games]
    logger.info('games {0} testing {1} is {2}'.format(games_ids,id,id in games_ids))
    if id in games_ids:
        index = games_ids.index(id)
        game = games[index]
        if not game.is_player(current_user.id) and game.can_join():
            if game.join(current_user.id):
                logger.info('player {0} has joined {1}'.format(current_user.id,id))
        page_out = render_template('game.html', game=game, player=current_user)
        #logger.info(page_out)
        return page_out
    else:
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Player(form.username.data, form.password.data)
        users.append(user)
        flash('registration complete')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

