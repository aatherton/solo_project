# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 19:48:07 2018

@author: Neph
"""

"""### import dependancies ###"""

from flask import Flask, render_template, jsonify, redirect

import mysql.connector, json

"""### define functions ###"""

def ez_queer_e(db, do):
    cursor = db.cursor()
    cursor.execute(do)
    result = cursor.fetchall()
    cursor.close()
    return(result)

"""### declare constants ###"""

DATABASE = mysql.connector.connect(
        host = "localhost",
        user = "root",
        db = "rplace"
        )

APP = Flask(__name__)

WIP = "<p>wip<br/>rip</p>"

"""### routes go here ###"""

@APP.route("/")
def index():
    return(WIP)
    
@APP.route("/API/actions/<int:x>/<int:y>")
def get_actions(x, y):
    base_query = """select actions.ts, x_coordinate, y_coordinate, colorswap.hex
    from actions
        join colorswap on actions.color = colorswap.color"""
    try:
        y
    except NameError:
        result = ez_queer_e(DATABASE, f"""{base_query}
        where ts <= {x};""")
    else:
        result = ez_queer_e(DATABASE, f"""{base_query}
        where ts between {x} and {y};""")
    return jsonify(result)
    
"""### start ###"""

if __name__ == "__main__":
    APP.run(debug = True)