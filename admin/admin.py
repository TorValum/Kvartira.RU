from flask import Blueprint, render_template, request, url_for, redirect, flash, session

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

def login_admin():
    session['admin_logged'] = 1

def isLogged():
    return True if session.get('admin_logged') else False

def logout_admin():
    session.pop('admin_logged', None)

menu = [{'url': '.list_zayvka', 'title': 'Заявки'},
        {'url': '.logout', 'title': 'Выйти'}]

@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))
    return render_template('admin/index.html', menu=menu)

@admin.route('/list-zayvka', methods=["POST", "GET"])
def list_zayvka():
    if not isLogged():
        return redirect(url_for('.login'))
    from app import get_db, FDataBase
    db = get_db()
    dbase = FDataBase(db)
    zayavki = dbase.getAllZayavki()
    return render_template('admin/list-zayvka.html', menu=menu, zayavki=zayavki)

@admin.route('/zayvka-approve/<int:zayavka_id>', methods=["POST"])
def zayvka_approve(zayavka_id):
    if not isLogged():
        return redirect(url_for('.login'))
    from app import get_db, FDataBase
    db = get_db()
    dbase = FDataBase(db)
    if dbase.updateZayavkaStatus(zayavka_id, 'Одобрено'):
        flash('Заявка одобрена', 'success')
    else:
        flash('Ошибка одобрения заявки', 'error')
    return redirect(url_for('.list_zayvka'))

@admin.route('/zayvka-reject/<int:zayavka_id>', methods=["POST"])
def zayvka_reject(zayavka_id):
    if not isLogged():
        return redirect(url_for('.login'))
    from app import get_db, FDataBase
    db = get_db()
    dbase = FDataBase(db)
    if dbase.updateZayavkaStatus(zayavka_id, 'Отклонено'):
        flash('Заявка отклонена', 'error')
    else:
        flash('Ошибка отклонения заявки', 'error')
    return redirect(url_for('.list_zayvka'))

@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for('.index'))
    
    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['pws'] == "12345":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Неверная пара логин/пароль", "error")
    return render_template('admin/login.html', title ='Админ-панель')

@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))

    logout_admin()

    return redirect(url_for('.login'))
