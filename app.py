import sqlite3
import os
import time
from flask import Flask, render_template, request, g, flash, abort, url_for, session, redirect, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from FDataBase import FDataBase
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from admin.admin import admin 

DATABSE = 'bd.db'
DEBUG = True 
MAX_CONTENT_LENGHT = 1024*1024
 
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = "dasdsajfdsfkjdsfkjbdhfbdsi32139721387198739fuidhuh178dsa"

app.register_blueprint(admin, url_prefix='/admin')

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'bd.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db(): #from app import create_db -> create_db()
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
    return []

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

dbase = None
@app.before_request
def before_request():
    """установка соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)

@app.route("/") ##если есть / d url
def index ():
    print(url_for('index'))
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu = dbase.getMenu())

@app.route("/contact", methods=["POST", "GET"]) 
@login_required
def contact ():
    print(url_for('contact'))
    if request.method == 'POST':
        print(request.form['username'])
        if len(request.form['username']) >2 and len(request.form['email']) >2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
    db = get_db()
    dbase = FDataBase(db)
    return render_template('feedback.html')

@app.route("/kvartiry")
@login_required
def show_kvartiry():
    print(url_for('show_kvartiry'))
    db = get_db()
    dbase = FDataBase(db)
    kvartiry = dbase.getKvartiras()
    return render_template('Kvartira.html', kvartiry=kvartiry)

@app.route("/udm")
def kvartira_udm():
    print(url_for('kvartira_udm'))
    kv =dbase.getKvartiraByUrl('/udm')
    if not kv: abort(404)
    return render_template('KvartiraUdm.html', kv=kv)

@app.route("/mol")
def kvartira_mol():
    print(url_for('kvartira_mol'))
    kv =dbase.getKvartiraByUrl('/mol')
    if not kv: abort(404)
    return render_template('KvartiraMol.html', kv=kv)

@app.route("/sov")
def kvartira_sov():
    print(url_for('kvartira_sov'))
    kv =dbase.getKvartiraByUrl('/sov')
    if not kv: abort(404)
    return render_template('KvartiraSov.html', kv=kv)

@app.errorhandler(404)
def error(e):
    db = get_db()
    dbase = FDataBase(db)
    menu = dbase.getMenu() 
    return render_template('error.html', menu = menu)

@app.route("/profile/<username>")
@login_required
def profile(username):
    if current_user.name != username:
        abort(401)
    return f"Профиль пользователя: {username}"

#-------------------------------------login.html старый, чисто templates-------------------------------------------
#@app.route("/login")
#def login():
#    return render_template("login.html", menu = dbase.getMenu())
#-----------------------------------------------------------------------------------------------------------------


@app.route("/register", methods=["POST", "GET"])
def register():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if request.form['psw'] != request.form['psw2']:
            flash('Пароли не совпадают', category='error')
        elif dbase.addUser(request.form['name'], request.form['email'], generate_password_hash(request.form['psw'])):
            flash('Вы успешно зарегистрированы', category='success')
            return redirect(url_for('login'))
        else:
            flash('Ошибка регистрации', category='error')
    return render_template("register.html", menu = dbase.getMenu()) 

@app.route("/login", methods=["POST", "GET"])
def login():
    db = get_db()
    dbase = FDataBase(db)
    menu = dbase.getMenu()
    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect(url_for('index'))

        flash("Неверная пара логин/пароль", "error")

    return render_template('login.html', title="Авторизация", menu=menu)


#---------------------------------------------------------------------------------КУКИ ---------------------------------------------------------------------------
##@app.route("/login")
##def login():
##    log=""
##    if request.cookies.get('logged'):
##        log = request.cookies.get('logged')
##    res = make_response(f"<h1>Форма автторизации</h1><p>loogged: {log}")
##    res.set_cookie("logged", "yes", 30*24*3600)
##    return res

##@app.route("/logout")
##def logout():
##    res = make_response("<p>Вы больше не авторизованы!</p>")
##    res.set_cookie("logged", "", 0)
##    return res
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------


##Создание новой 
@app.route("/about", methods=["POST", "GET"])
@login_required
def zayvka_kvartira():
    print(url_for('zayvka_kvartira'))
    db = get_db()
    dbase = FDataBase(db)
    user_id = current_user.get_id()
    my_zayavki = dbase.getZayavkiByUser(user_id)
    if request.method == "POST":
        if ( (len(request.form['zhelaemyi_adres']) >= 4) and (len(request.form['zhelaemyi_cena']) >= 4) and  (len(request.form['kol_vo_rooms']) >0)):
            tm = int(time.time())
            res = dbase.newZayavka(
                request.form['zhelaemyi_adres'],
                request.form['zhelaemyi_cena'],
                request.form['kol_vo_rooms'],
                user_id,
                'На рассмотрении',
                tm
            )   
            if not res:
                flash('Ошибка добавления заявки', category='error')
            else:
                flash('Заявка успешно добавлена', category='success')
        else:
            flash('Ошибка добавления заявки', category='error')
    
    return render_template('zayvka.html', menu=dbase.getMenu(), title="Заявки", my_zayavki=my_zayavki)

'''
##хз!!!!!!!!!!!!!!!!!!
def showSite(alias): 
    StationId, StationName, url = dbase.getStations(alias)
    if request.method == "POST":
        res = dbase.objectsInCertificates(request.form['name'], request.form['number'], alias)
        if not res:
            flash('Ошибка добавления Объекта', category='error')
        else:
            flash('Объект успешно добавлен в Сертификат', category='success')

    return render_template('station.html', menu=dbase.getMenu(), certificates=dbase.getCertificateAnonce(), propertyObjects=dbase.getObjectAnonce(), 
                           objectsInCertificate=dbase.getObjectInCertificatesAnonce(), StationId=StationId, StationName=StationName, title=StationName)

'''
@app.route("/logout")
@login_required
def logout():
    logout_user()  # Эта функция удаляет данные пользователя из сессии Flask
    flash("Вы успешно вышли из аккаунта", category='success')
    return redirect(url_for('login'))

def migrate_db():
    """Добавляет недостающие колонки в таблицу Zayavka2 для уже существующей БД"""
    db = connect_db()
    cur = db.cursor()
    try:
        cur.execute("ALTER TABLE Zayavka2 ADD COLUMN status varchar DEFAULT 'На рассмотрении'")
    except sqlite3.OperationalError:
        pass  # колонка уже существует
    try:
        cur.execute("ALTER TABLE Zayavka2 ADD COLUMN user_id integer")
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute("ALTER TABLE Zayavka2 ADD COLUMN time integer")
    except sqlite3.OperationalError:
        pass
    db.commit()
    db.close()

if __name__ == "__main__":
    migrate_db()
    app.run(debug=True, port=5008)

