from email.policy import default
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app import db, app
from flask_login import LoginManager, UserMixin, login_user
from datetime import datetime
from werkzeug.security import generate_password_hash

class Post(db.Model):     
    post_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    post_type = db.Column(db.String(100), nullable = False)
    post_name = db.Column(db.String(200), nullable = False)
    post_description = db.Column(db.Text(300), nullable = False)    
    post_price = db.Column(db.Text, nullable = False)    
    post_filename = db.Column(db.Text, unique = False, nullable = False)
    post_univ_name = db.Column(db.String(200), nullable = False)
    post_date = db.Column(db.DateTime, default = datetime.utcnow)  
    post_creator_name = db.Column(db.String(100))
    post_creator_id = db.Column(db.Integer)
     
    def __repr__(self):
        return '<Post %r>' % self.id


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)

    login = db.Column(db.String(100), unique = True)   
    password = db.Column(db.String(100), nullable = False)
    user_avatar = db.Column(db.Text, unique = False, default = "default.jpg")
    univ_name = db.Column(db.String(200), default = "Не указан")    
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))

class Role(db.Model):
    #__tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='role',lazy='select')



class Univ(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_from = db.Column(db.String(50))
    user_to = db.Column(db.String(50))
    mes_theme = db.Column(db.String(50), default = "Без темы")
    mes_text = db.Column(db.Text)

#Создаем БД
db.create_all()

if not User.query.filter(User.login == 'Ksut').first():
        u = User(login = 'Ksut', password = generate_password_hash("123"))
        db.session.add(u)        
        admin_role = Role(name='Администратор') 
        admin_role.users.append(u)
        db.session.commit()

          
#Создание ролей

#db.session.add(admin_role)



