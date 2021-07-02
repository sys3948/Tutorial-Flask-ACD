from flask import render_template, abort, session, redirect, url_for, flash, current_app
from . import main
from .forms import NameForm
from ..email import send_email
import pymysql

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        conn = pymysql.connect(host='192.168.111.133', port=3306, user=current_app.config['DB_USER'] , passwd=current_app.config['DB_PASSWD'], database='flasky', charset='utf8')
        cur = conn.cursor()
        cur.execute('select username from user where username="%s"' %(form.name.data))
        user = cur.fetchone()
        if user is None:
            cur.execute('insert into user(username) value("%s")' %(form.name.data))
            conn.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        cur.close()
        conn.close()
        return redirect(url_for('.index'))
    return render_template('index.html')

@main.route('/name/<test>')
def name(test):
    send_email(to = 'sys3948@naver.com', subject='New User', template='mail/new_user')
    return render_template('user.html', name=test) 