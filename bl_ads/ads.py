import os
from flask import Blueprint, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from models import Post,db
from flask_login import login_required, current_user
import random, string
app_ads = Blueprint('ads', __name__, template_folder='templates', static_folder='static') # Создание принта

UPLOAD_FOLDER = 'C:/Users/Ksutelash/Desktop/pyProject/static/loaded' # Папка хранения изображений
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} # Допустимые форматы изображений



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_random_string(filename):     
    letters = string.ascii_lowercase
    ext = filename.rsplit('.',1)[1]
    filename = ''.join(random.choice(letters) for i in range(10)) # Генит 10 рандомных букофк в название
    filename = filename + '.' + ext 
    return filename

@app_ads.route('/', methods=["GET"])
def index():      
    return render_template("index.html")

@app_ads.route('add', methods=["POST","GET"])
@login_required
def add():    
    if request.method == "POST":           
        tip = request.form['tip']
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        img_file = request.files['file']
        filename = secure_filename(img_file.filename)
        postcreator_login = current_user.login
        postcreator_id = current_user.id
        univ_name = current_user.univ_name
        af = allowed_file(filename)

        # Блок проверок
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

        postDB = Post(
            post_type = tip, 
            post_name = name, 
            post_description = description, 
            post_price = price, 
            post_filename = filename,
            post_univ_name = univ_name,
            post_creator_name = postcreator_login,
            post_creator_id = postcreator_id)     
        
        db.session.add(postDB) # Добавл
        db.session.flush() 
        db.session.commit() # Сохраняет
        return redirect('/ads/all')
    else:    
        return render_template("add.html")
        

@app_ads.route('all', methods=["POST","GET"])
@login_required
def all():
    u = Post.query.filter_by(post_univ_name = current_user.univ_name)

    #Пагинация    
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1    
    pages = u.paginate(page = page, per_page = 5)    
    return render_template("all.html", u = u, u_name = current_user.univ_name, pages = pages)

@app_ads.route('all/<int:id>', methods=["POST","GET"])
@login_required
def all_detail(id):

    u_id = Post.query.get(id)
    user_name =  current_user.login
    if request.method == 'POST': 
        # Обработка кнопки удалить обьявление, что проверяет владельца внутри хтмл
        if request.form.get('delete_add') == 'Удалить':    
            obj = Post.query.get(id)
            folder_path_location = "static/loaded/" # Папка хранения картинок
            file_to_delete_path = ''.join((folder_path_location,obj.post_filename)) # Обьединение целого пути с файлнеймом 
            os.remove(file_to_delete_path) 
            db.session.delete(obj) # Удаляем пост
            db.session.commit()
            return redirect('/ads/all')
            
        #Написать сообщению пользователю-обладателю объявления
        if request.form.get('send_messange') == 'Написать пользователю':
            send_to_id = id
            return redirect('/message/' + str(send_to_id))

    return render_template("cv.html", u_id = u_id, user_name = user_name)

