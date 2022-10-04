# -*- coding: utf-8 -*-
from sqlalchemy.exc import IntegrityError

from .decorators import sqlexception_handler
import bcrypt
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from flask import (
    Flask, redirect, render_template, request, url_for, make_response
)

app = Flask(__name__)
app.config.from_pyfile('../config.py')
app.config.from_object('config.Config')  # Using configuration
 # instantiating SQLAlchemy
db = SQLAlchemy(app)
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
        cc = request.form.get("cc")
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        email = request.form.get("email")
        password = request.form.get("password")
        new_user = Users()
        new_user().add_user(cc, nombre, apellido, email, password)
        return "hola" #redirect(url_for('dashboard'))

# Users.query.filter_by(id=123).delete()
# Users.query.filter(User.id == 123).delete()
# users = Users.query.all()

@app.route('/recuperarclave')
def forgot():
    return render_template('dashboard/forgot.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard/dashboard.html')


@sqlexception_handler
@app.route('/db_init')
def check_db_status():
    start_db()
    nr = Roles()
    nr.init_roles()
    return "Todo correcto "


@app.route('/testrule')
def testrule():
    response = make_response("Hola")
    response.set_cookie('answer', '42')
    return response


class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('Users', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

    def init_roles(self):
        admin_role = Roles(id=1, name='Admin')
        pilote_role = Roles(id=2, name='Pilot')
        user_role = Roles(id=3, name='User')
        db.session.add(admin_role)
        db.session.add(pilote_role)
        db.session.add(user_role)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column("id", db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True)
    docid = db.Column(db.Integer, unique=True, nullable=False)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    user_verification = db.Column(db.String(100))
    user_active = db.Column(db.String(2))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # repr method represents how one object of this datatable
    def __repr__(self):
        return '<Users %r>' % self.docid
        # return f"Name : {self.first_name}, LastName: {self.last_name}"

    def verify_password(self, password):
        pwhash = bcrypt.hashpw(password, self.password)
        return self.password == pwhash

    def add_user(self, cc, nombre, apellido, email, password):
        # password = str(Users().verify_password(password.encode('utf-8')))
        new_user = Users(docid=cc, first_name=nombre, last_name=apellido, email=email, password=password,
                         role_id=3)
        print(cc, nombre, apellido, email, password)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def start_db():
    db.create_all()



if __name__ == '__main__':
    app.run()
