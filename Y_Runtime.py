#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 0muMDAU Server
from core import app , socketio 
import os, logging
from conf import setting
from core.index import main
from core.user import auth
from core import events
# muMDAU_app setting
from flask_socketio import SocketIO
app.secret_key = setting.yourkey
app.register_blueprint(main)
app.register_blueprint(auth, url_prefix="/login")
# Main function of MDAUServer
if __name__ == '__main__':
    # log writeing
    print('Yakumo is run on ' + str(setting.host) + ':' + str(setting.port))
    # check debug
    if setting.debug == 1:
        debugB = True
        socketio.run(app, debug=debugB, host=str(setting.host), port=setting.port)
    else:
        debugB = True
        logging.basicConfig(filename=setting.s_log, level=logging.WARNING)
        logdebug = open(setting.s_log, 'w')
        print('!!!Important : Now is in debug mode.')
        socketio.run(app, debug=debugB, log=logdebug, host=str(setting.host), port=setting.port)
