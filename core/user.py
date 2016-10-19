# -*- coding: utf-8 -*-

from core import app
from flask import session, redirect, url_for, request, Blueprint
import hashlib
from core_module.dbmongo import User

auth = Blueprint('auth', __name__ , template_folder='../core_template/templates')
@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['buser']
        passd = request.form['bpass']
        password = User.login(user)
        passd = hashlib.sha256(passd.replace('\n', '').encode()).hexdigest()
        
        if not password:
            return '帳號錯誤'
        else:
            if password == passd:
                session['username'] = user
                session['name'] = user
                return redirect(url_for('main.index'))
            else:
                return '密碼錯誤'

    else:
        return redirect(url_for('main.index'))

@auth.route('/api', methods=['GET', 'POST'])
def loginapi():
    if request.method == 'POST':
        user = request.form['buser']
        passd = request.form['bpass']
        password = User.login(user)
        passd = hashlib.sha256(passd.replace('\n', '').encode()).hexdigest()
        
        if not password:
            return 'no account'
        else:
            if password == passd:
                session['username'] = user
                session['name'] = user
                return 'login'
            else:
                return 'password err'



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main.index'))

