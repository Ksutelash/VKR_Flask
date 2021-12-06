from enum import unique
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.utils import redirect

UPLOAD_FOLDER = "/loaded"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

#Проверка допустимого расширения
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS