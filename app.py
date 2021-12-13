import os, time
from enum import unique
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_login.mixins import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import redirect
from werkzeug.security import check_password_hash, generate_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SECRET_KEY'] = 'the random string' 
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.secret_key = 'testString'

login_manager = LoginManager(app)



from models import Post, User

from ads.ads import ads
app.register_blueprint(ads, url_prefix='/ads')



@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


    



# Admin Panel #
class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.login == "Ksut":
            return True
        else:
            return False
    

admin = Admin(app, name='Админка', template_mode='bootstrap3')
admin.add_view(MyModelView(Post, db.session))
admin.add_view(MyModelView(User, db.session))
# Admin Panel #


@app.route("/")
@app.route("/index")
def index():    
    return render_template("index.html")


@app.route('/profile/')
@login_required
def profile():      
    return render_template("profile.html")

#Обработчик, если пользователь незалогинен
@login_manager.unauthorized_handler     
def unauthorized_callback():            
       return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
	    return redirect(url_for('profile'))
        
    if request.method == 'POST':   
        login = request.form.get('login')
        password = request.form.get('password')

        if login and password:
            user = User.query.filter_by(login=login).first()

            if user and check_password_hash(user.password, password):
                is_checked = request.form.get('remember-me')
                if is_checked:
                    login_user(user,remember=True)
                else:
                    login_user(user)
                #next_page = request.args.get('next')
                return render_template ('profile.html')
            else:
                flash('Wrong l/p')
        else:
            flash("Введите логин и пароль")
    return render_template('login.html')


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():    
    logout_user()
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():    
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')       
    if request.method == 'POST':
        if not (login or password):
            flash("Введите все поля ввода")
        elif password != password2:
            flash("Пароли не совпадают")
        else:
            hash_password = generate_password_hash(password)
            new_user = User(login=login, password = hash_password)
            db.session.add(new_user)
            db.session.commit()
            flash("А теперь войдите в свой профиль")
            return render_template('login.html')
            
    return render_template('register.html')

#Перенаправление на логин, со страниц, где нужна авторизация для показа контента
@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect()

    return response



    

 
    
    


if __name__ == "__main__":
    app.run(debug = True)

