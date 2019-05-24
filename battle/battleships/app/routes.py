from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm  #i didn't steal this bit
from flask_login import current_user, login_user
from flask_login import logout_user
from app.models import Player

from app import login #this is the batteships app

users = {'robin':Player('robin', 'nobby')}
games = {}


@login.user_loader
def load_user(id):
    print('loading user.... '+str(id))
    return users[id]



@app.route('/')
@app.route('/index')
def index():
    user = current_user
    return render_template('index.html', title='Home', user=user, games=games)

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
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))