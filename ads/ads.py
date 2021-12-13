import os
from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.utils import secure_filename
from sqlalchemy import exc
import random, string #File random gen name
from models import Post
ads = Blueprint('ads', __name__, template_folder='templates', static_folder='static') # имя принта, имя модуля(где будут искаться каталоги и под, пути)
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

UPLOAD_FOLDER = 'C:/Users/Ksutelash/Desktop/pyProject/static/loaded' # Папка хранения изображений
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} # Допустимые форматы изображений
Post.app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_random_string(filename):
    
    letters = string.ascii_lowercase
    ext = filename.rsplit('.',1)[1]
    filename = ''.join(random.choice(letters) for i in range(10)) # Генит 10 рандомных букофк в название
    filename = filename + '.' + ext 
    return filename
####################################################################################################################


@ads.route('/', methods=["POST","GET"])
def index():    
    return render_template("index.html")


@ads.route('add', methods=["POST","GET"])
@login_required
def add():    
    if request.method == "POST":           
        tip = request.form['tip']
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        img_file = request.files['file']
        filename = secure_filename(img_file.filename)
        postcreator = current_user.login
        af = allowed_file(filename)

        if not tip:
            flash("Тип не выбран")
            return redirect('/ads/add')
        if not name:
            flash("Имя пустое")
            return redirect('/ads/add')
        if not description:
            flash("Заполните описание")
            return redirect('/ads/add')
        if not price:
            flash("Цена не указана")
            return redirect('/ads/add')
        if not img_file:
            flash("Файл не выбран")
            return redirect('/ads/add')    

        if af == True:    
            filename = get_random_string(filename)       
            img_file.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            flash("Неверный формат файла, попробуйте еще раз")
            return redirect('/ads/add')

        postDB = Post(tip = tip, name = name, description = description, price = price, filename = filename, post_creator = postcreator)     
        
            
        
        Post.db.session.add(postDB) # Добавл
        Post.db.session.flush() 
        Post.db.session.commit() # Сохраняет
        return redirect('/') # Возврат на ' 
              
        #try:                                         
        #   Post.db.session.add(postDB) # Добавляет
        #   Post.db.session.flush() 
        #   Post.db.session.commit() # Сохраняет               
        #   return redirect('/') # Возврат на '
        #except exc.IntegrityError:
        #   Post.db.session.rollback()        
        #   return tip+' '+name+' '+ description + ' '+ filename + ' ' + price
        
            
    
    else:    
        return render_template("add.html")
        

@ads.route('all', methods=["POST","GET"])
@login_required
def all():
    u = Post.query.all()
    return render_template("all.html", u=u)

@ads.route('all/<int:id>', methods=["POST","GET"])
@login_required
def all_detail(id):
    u_id = Post.query.get(id)
    return render_template("cv.html", u_id=u_id)
