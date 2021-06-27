from flask import Flask, render_template, abort, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import pymysql
from flask_mail import Mail
from flask_mail import Message

import sys
sys.path.append('d:/uploadGit/account_info')
import google_info as g_info
import mysql_info as m_info

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = g_info.account_h
app.config['MAIL_PASSWORD'] = g_info.password_h

mail = Mail(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


app.config['SECRET_KEY'] = 'hard secret key token'

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'


def send_email(to, subject, template, **kwargs):
    msg = Message(subject, sender = 'Flasky Admin <flasky@example.com>', recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        conn = pymysql.connect(host='192.168.111.133', port=3306, user=m_info.account_c , passwd=m_info.password_c, database='flasky', charset='utf8')
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
        return redirect(url_for('index'))
    return render_template('index.html', form = form, name = session.get('name'), known = session.get('known', False))

@app.route('/name/<test>')
def name(test):
    send_email(to = 'sys3948@naver.com', subject='New User', template='mail/new_user')
    return render_template('user.html', name=test) 

@app.route('/login')
def login():
    return '<h1>Hello login Page!</h1>'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)


