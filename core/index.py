# -*- coding: utf-8 -*-
# muMDAU_app main / first page
from core import app
from flask import request, render_template, \
        url_for, redirect, session, Blueprint
from core_module.dbmongo import User

main = Blueprint(
        'main',
        __name__,
        template_folder='../core_template/templates'
        )


# index page main route page
@main.route('/', methods=['GET', 'POST'])
def index():
    Pos1Y = 120.536654
    Pos1X = 23.695556
    Pos2Y = 120.536738
    Pos2X = 23.694996
    Pos3Y = 120.537346
    Pos3X = 23.695508
    Pos4Y = 120.535441
    Pos4X = 23.695428
    if 'username' in session:
        return render_template('panel.html', **locals())
    else:
        return render_template('panel.html', **locals())
        #return render_template('login.html')


# init route to first time use
@app.route('/init', methods=['GET', 'POST'])
def init():
    if request.method == 'POST':
        user = request.form['buser']
        passd = request.form['bpass']
        import hashlib
        hashsha = hashlib.sha256(passd.replace('\n', '').encode())
        # ManageSQL.addUser(user, hashsha.hexdigest(), '1', '0')
        User.add(user, hashsha.hexdigest(), '1')

        return redirect(url_for('main.index'))
    else:
        return render_template('first.html')
