import os
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from werkzeug.security import check_password_hash, generate_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import random, string #File random gen name


UPLOAD_FOLDER = 'C:/Users/Ksutelash/Desktop/pyProject/static/loaded' # Папка хранения изображений
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} # Допустимые форматы изображений
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydb.db"
app.config['SECRET_KEY'] = 'the random string' 
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'testString'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Blueprints #
from bl_ads.ads import app_ads
app.register_blueprint(app_ads, url_prefix = '/ads')

from bl_profile.profile import app_profile
app.register_blueprint(app_profile, url_prefix = '/profile')

from bl_message.message import app_message
app.register_blueprint(app_message, url_prefix = '/message')

from models import Post, Role, User, Univ

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

# Admin Panel #
class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.login == "Ksut":
            return True
        else:
            return False
    

admin = Admin(app, name='Админка', template_mode='bootstrap3')

# Плашки #
admin.add_view(MyModelView(Post, db.session))
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Univ, db.session))
admin.add_view(MyModelView(Role, db.session))
#################################################

#################################################
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_random_string(filename):     
    letters = string.ascii_lowercase
    ext = filename.rsplit('.',1)[1]
    filename = ''.join(random.choice(letters) for i in range(10)) # Генит 10 рандомных букофк в название
    filename = filename + '.' + ext 
    return filename

@app.route("/")
@app.route("/index")
def index():    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)

