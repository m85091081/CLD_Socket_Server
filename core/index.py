# -*- coding: utf-8 -*-
# muMDAU_app main / first page 
from core import app, socketio
from threading import Thread
from flask import request, render_template, Blueprint, url_for, redirect, session
from core_module.dbmongo import User
from compute import dataget, othercar_y_raw , othercar_x_raw , othercar_minus , othercar_X_map, othercar_Y_map
import subprocess, os
from subprocess import PIPE
from time import sleep
from distributed import Client
client = Client('192.168.0.19:8786')
client.upload_file('compute.py')  

main = Blueprint('main', __name__ , template_folder='../core_template/templates')
thread = None
# index page main route page 
@main.route('/download',methods=['GET'])
def download():
    from os import listdir
    from os.path import isfile, join
    mypath = '/home/ubuntu/hlsvideo'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return render_template('paneldw.html', **locals())
    

@main.route('/api/compute/car_KL',methods=['GET','POST'])
def carkl():
    other_car_X = client.gather(client.map(othercar_X_map,othercar_x_raw(dataget())))
    other_car_Y = client.gather(client.map(othercar_Y_map,othercar_y_raw(dataget())))
    orign_car_X = []
    orign_car_Y = []
    for x in range(len(other_car_X)-1) :
        orign_car_X.append(other_car_X[0])
        orign_car_Y.append(other_car_Y[0])
    del other_car_X[0]
    del other_car_Y[0]
    X = client.gather(client.map(othercar_minus,other_car_X,orign_car_X))   
    Y = client.gather(client.map(othercar_minus,other_car_Y,orign_car_Y))   
    return str([X,Y])

@main.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return render_template('panel.html', **locals())
    else:
        return render_template('login.html')

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

# test of adduser route page 
@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        user = request.form['buser']
        if LoginSQL.getPass(user) is None:
            import hashlib
            import random
            ans = random.uniform(1, 10)
            hashpass1 = hashlib.sha1(str(ans).encode())
            passd1 = hashpass1.hexdigest()
            hashpass0 = hashlib.sha256(passd1.replace('\n', '').encode())
            ManageSQL.addUser(user, hashpass0.hexdigest(), '0', '1')
            return passd1
        else:
            return '使用者已經他媽的存在了喔！'
