import sqlite3
import os
from flask import Flask, render_template, request, g, flash, abort, url_for, session, redirect
from FDataBase import FDataBase

DATABSE = 'bd.db'
DEBUG = True 
SECRET_KEY = "dasdsadsa"

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'bd.db')))

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
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f"Профиль пользователя: {username}"

@app.route("/login", methods=["POST", "GET"])
def login():
    db = get_db()
    dbase = FDataBase(db)
    menu = dbase.getMenu()
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and  request.form['username'] == "selfedu" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    
    return render_template('login.html', title="Авторизация", menu=menu)

##Создание новой 
@app.route("/about", methods=["POST", "GET"])
def zayvka_kvartira():
    print(url_for('zayvka_kvartira'))
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if ( (len(request.form['zhelaemyi_adres']) >= 4) and (len(request.form['zhelaemyi_cena']) >= 4) and  (len(request.form['kol_vo_rooms']) >0)):
            res = dbase.newZayavka(
                request.form['zhelaemyi_adres'],
                request.form['zhelaemyi_cena'],
                request.form['kol_vo_rooms'],
            )   
            if not res:
                flash('Ошибка добавления заявки', category='error')
            else:
                flash('Заявка успешно добавлена', category='success')
        else:
            flash('Ошибка добавления заявки', category='error')
    
    return render_template('zayvka.html', menu=dbase.getMenu(), title="Заявки")

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
if __name__ == "__main__":
    app.run(debug=True, port=5001)
