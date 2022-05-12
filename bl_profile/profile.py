import os
from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import Post, Role, User, Univ, db
from werkzeug.security import check_password_hash, generate_password_hash
app_profile = Blueprint('profile', __name__, template_folder='templates', static_folder='static') # имя принта, имя модуля(где будут искаться каталоги и под, пути)

login_manager = LoginManager(app_profile)

UPLOAD_FOLDER = 'C:/Users/Ksutelash/Desktop/pyProject/static/loaded' # Папка хранения изображений
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} # Допустимые форматы изображений

@app_profile.route('/user/', methods=['GET', 'POST'])
@login_required
def profile():      
    user_role = Role.query.get(current_user.role_id)
    user_role_is = user_role.name
    # Загрузка аватарки в профиль (переделай потом в ООП!)
    if request.method == 'POST':       
        uploaded_avatar = request.files['file']
        if not uploaded_avatar:
            flash("Аватарка не загружена")

        from bl_ads.ads import allowed_file, get_random_string
        filename = secure_filename(uploaded_avatar.filename)        
        if allowed_file(filename) == True:    
                filename = get_random_string(filename)       
                uploaded_avatar.save(os.path.join(UPLOAD_FOLDER, filename))
                update_my_avatar = User.query.filter_by(id = current_user.id).first()
                update_my_avatar.user_avatar = filename
                db.session.commit()
        
    ###########################################################################
    posts = Post.query.filter_by(post_creator_name = current_user.login)      
    return render_template("profile.html",posts=posts,user_role_is=user_role_is)
    

#Обработчик, если пользователь незалогинен
@login_manager.unauthorized_handler     
def unauthorized_callback():            
       return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app_profile.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
	    return redirect('/profile/user')
        
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


@app_profile.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():    
    logout_user()
    return render_template('index.html')


@app_profile.route("/register", methods=['GET', 'POST'])
def register(): 
    el = Univ.query.all()   
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
            univ_name = request.form.get('tip')
            new_user = User(login=login, password = hash_password, univ_name = univ_name,role_id = "2")
            db.session.add(new_user)
            db.session.commit()
            flash("А теперь войдите в свой профиль")
            return render_template('index.html')
            
    return render_template('register.html',el=el)

#Перенаправление на логин, со страниц, где нужна авторизация для показа контента
@app_profile.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect()

    return response