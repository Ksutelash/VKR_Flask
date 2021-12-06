import os
from enum import unique
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.utils import redirect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


#UPLOAD_FOLDER = 'C:/Users/Ksutelash/Desktop/pyProject/loaded' # Папка хранения изображений
#ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} # Допустимые форматы изображений


app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'the random string' 
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

########################БД###############################
class Post(db.Model):
    app = app    
    db = db
    id = db.Column(db.Integer, primary_key = True)
    tip = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(200), nullable = False)
    description = db.Column(db.Text(300), nullable = False)    
    price = db.Column(db.Text, nullable = False)
    post_creator = db.Column(db.Integer, )
    filename = db.Column(db.Text, unique = False, nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)    
#######################################################################

    def __repr__(self):
        return '<Post %r>' % self.id

class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tip = db.Column(db.String(100), nullable = True)

    def __repr__(self):
        return '<Test %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100),nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(100), nullable = False)
##########################################################



admin = Admin(app, name='Админка', template_mode='bootstrap3')
admin.add_view(ModelView(Post, db.session))
# Add administrative views here

#db = SQLAlchemy(app)
##########################################################

# Blueprints #
from ads.ads import ads
app.register_blueprint(ads, url_prefix='/ads')






@app.route("/")
@app.route("/index")
def index():    
    return render_template("index.html")




if __name__ == "__main__":
    app.run(debug = True)

