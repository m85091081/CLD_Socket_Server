# -*- coding: utf-8 -*-
# muMDAU_app main / first page
from core import app
from flask import request, render_template, \
        url_for, redirect, session, Blueprint
from core_module.dbmongo import User
from compute import dataget, othercar_y_raw , othercar_x_raw , othercar_minus , othercar_X_map, othercar_Y_map
import subprocess, os
from subprocess import PIPE
from time import sleep
from distributed import Client
client = Client('192.168.0.19:8786')
client.upload_file('compute.py')  

main = Blueprint('main', __name__ , template_folder='../core_template/templates')
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
