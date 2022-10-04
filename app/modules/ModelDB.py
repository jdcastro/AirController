import bcrypt
from sqlalchemy.sql import func
from .. import db
# Models

class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('Users', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column("id", db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True)
    docid = db.Column(db.Integer, unique=True, nullable=False)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    user_pass = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # repr method represents how one object of this datatable
    def __repr__(self):
        return '<Users %r>' % self.docid
        # return f"Name : {self.first_name}, LastName: {self.last_name}"

    def verify_password(self, password):
        pwhash = bcrypt.hashpw(password, self.password)
        return self.password == pwhash

