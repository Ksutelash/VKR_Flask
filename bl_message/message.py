from flask import render_template, request, Blueprint
from werkzeug.utils import redirect
from flask_login import current_user
from models import Post, Message, db

app_message = Blueprint('message', __name__, template_folder='templates', static_folder='static') # имя принта, имя модуля(где будут искаться каталоги и под, пути)

@app_message.route("/inbox", methods=['GET', 'POST'])
def message_inbox():
    get_info = Message.query.filter_by(user_to = current_user.login).all()    
    
    return render_template('message_inbox.html',get_info = get_info)

@app_message.route("/<int:id>", methods=['GET', 'POST'])
def message(id):
    info = Post.query.get(id)
    

    if request.method == "POST":
        message_theme = request.form.get('theme')
        message_text = request.form.get('send_text')
        message_from = current_user.login
        message_to = info.post_creator_name

        new_message = Message(user_from = message_from, user_to = message_to, mes_theme = message_theme, mes_text = message_text)
        db.session.add(new_message)
        db.session.commit()
        return render_template('message_inbox.html')
        

    return render_template('message.html',info = info)
