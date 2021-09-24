import time
from atom_config import db

class User(db.Model):
    user_id         = db.Column(db.Integer, primary_key=True)
    email           = db.Column(db.String(120), unique=True, nullable=False)
    username        = db.Column(db.String(120), unique=False, nullable=False)
    psw_hash        = db.Column(db.String(36), unique=False, nullable=False)
    active          = db.Column(db.Integer, unique=False, nullable=False)
    role            = db.Column(db.String, unique=False, nullable=False)
    ts_created      = db.Column(db.Integer, unique=False, nullable=False,
                                default=lambda:int(time.time()))
    ts_updated      = db.Column(db.Integer, unique=False, nullable=False,
                                default=lambda:int(time.time()), onupdate=lambda:int(time.time()))
    @property
    def serialize(self):
        return {
            'user_id'  :self.user_id,
            'email'    :self.email,
            'username' :self.username,
            'role'     :self.role,
            'active'   :self.active
       }
    def __repr__(self):
        return '<User %r - %r>' % (self.username, self.email)