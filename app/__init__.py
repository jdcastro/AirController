# -*- coding: utf-8 -*-
from .decorators import sqlexception_handler
from datetime import datetime
from flask import (
    Flask, redirect, render_template, request, url_for, make_response
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config.from_pyfile('../config.py')
app.config.from_object('config.Config')  # Using configuration
db = SQLAlchemy(app)  # instantiating SQLAlchemy

"""
Durante el estado de desarrollo.
Cabecera adicional para forzar la recarga de la cache.
"""
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def index():
    return render_template('front/portada.html')


@app.route(r'/acceso')
def login():
    return render_template('dashboard/login.html')


@app.route('/registrarse', methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        return render_template('dashboard/signup.html')
    elif request.method == 'POST':

        return redirect(url_for('dashboard'))


@app.route('/recuperarclave')
def forgot():
    return render_template('dashboard/forgot.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard/dashboard.html')


@sqlexception_handler
@app.route('/db_init')
def check_db_status():
    db.create_all()
    return "Todo correcto "


@app.route('/testrule')
def testrule():
    response = make_response("Hola")
    response.set_cookie('answer', '42')
    return response

if __name__ == '__main__':
    app.run()
