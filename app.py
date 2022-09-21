from flask import (
    Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for
)
# import jinja_partials

app = Flask(__name__)

# jinja_partials.register_extensions(app)

@app.after_request
def add_header(r):
    """
    Add headers to force rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def index():
    return render_template('front/portada.html')

@app.route('/vuelos')
def vuelos():
    return render_template('dashboard/default.html')

@app.route('/ayuda')
def ayuda():
    return render_template('dashboard/default.html')

@app.route('/contacto')
def contacto():
    return render_template('dashboard/default.html')

@app.route('/politicas-privacidad')
def politicas_privacidad():
    return render_template('dashboard/default.html')

@app.route('/acceso')
def acceso():
    return render_template('dashboard/default.html')

@app.route('/acceso/registro')
def registro():
    return render_template('dashboard/default.html')

@app.route('/acceso/recuperar-clave')
def recuperar_clave():
    return render_template('dashboard/default.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard/default.html')