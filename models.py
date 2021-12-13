from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app import db, app
from flask_login import LoginManager, UserMixin, login_user
from datetime import datetime

class Post(db.Model): 
    
    app = app
    db = db    
       
    id = db.Column(db.Integer, primary_key = True)
    tip = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(200), nullable = False)
    description = db.Column(db.Text(300), nullable = False)    
    price = db.Column(db.Text, nullable = False)    
    filename = db.Column(db.Text, unique = False, nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)  

    post_creator = db.Column(db.String(100))

    def __repr__(self):
        return '<Post %r>' % self.id


class User(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(100), unique = True)   
    password = db.Column(db.String(100), nullable = False)

