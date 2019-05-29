from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm  #i didn't steal this bit
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from app.models import Player, Game

from app import login #this is the batteships app

users = {'robin':Player('robin', 'nobby')}
new_game = Game()
games = { new_game.id: new_game }


@login.user_loader
def load_user(id):
    print('loading user.... '+str(id))
    return users[id]


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = current_user
    print(user)
    return render_template('index.html', title='Home', games=games)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        flash('login requested fir user {0}, remember me={1}'.format(form.username.data, form.remember_me.data))
        user = None
        if form.username.data in users:
            user = users[form.username.data]
            
        if user is None or not user.check_password(form.password.data):
            flash('invalid user name or password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '': #checks to see if the next is tampered with to got outside
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



