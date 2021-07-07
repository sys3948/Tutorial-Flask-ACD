from flask import render_template, redirect, request, url_for, flash, current_app, session
from wtforms.validators import Email
from . import auth
from .forms import LoginForm, RegistrationForm
from ..email import send_email
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(email = form.email.data).first()
        conn = pymysql.connect(host='192.168.111.133', port=3306, user=current_app.config['DB_USER'], passwd=current_app.config['DB_PASSWD'], database='flasky')
        cur = conn.cursor()
        cur.execute('select id, password_hash, username from user where email = "%s"' %(form.email.data))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user is not None and check_password_hash(user[1], form.password.data):
            session['id'] = user[0]
            session['name'] = user[2]
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html', form = form)


@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        conn = pymysql.connect(host='192.168.111.133', port=3306, user=current_app.config['DB_USER'], passwd=current_app.config['DB_PASSWD'], database='flasky')
        cur = conn.cursor()
        cur.execute('insert into user(email, username, password_hash) values("%s", "%s", "%s")' %(form.email.data, form.username.data, generate_password_hash(form.password.data)))
        conn.commit()
        cur.execute('select id from user where email = "%s"' %form.email.data)
        confirm = cur.fetchone()
        cur.close()
        conn.close()
        s = Serializer(current_app.config['SECRET_KEY'], 3600)
        token = s.dumps({'confirm' : confirm[0]})
        send_email(form.email.data, 'Confirm Your Account', 'auth/email/confirm', username=form.username.data, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form = form)


@auth.route('/confirm/<token>')
def confirm(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except Exception as e:
        flash('token error! ' + str(e))
        return redirect(url_for('auth.login'))
    conn = pymysql.connect(host='192.168.111.133', port=3306, user=current_app.config['DB_USER'], passwd=current_app.config['DB_PASSWD'], database='flasky')
    cur = conn.cursor()
    cur.execute('select id, confirmed from user where id = "%s"' %(data.get('confirm')))
    user = cur.fetchone()

    if user[1]:
        return redirect(url_for('main.index'))
    if user[0] == data.get('confirm'):
        cur.execute('update user set confirmed=true where id="%s"' %(user[0]))
        conn.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')

    cur.close()
    conn.close()
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request(): # request hooks - before_request : 각 리퀘스트 전에 실행하는 함수를 등록하는 후크이다. before_request 와 같은 후크로 blueprint를 적용할 시 before_request 후크는 before_app_request로 변경된다.
    print('request hooks!!')
    print('request End Point! : ' + request.endpoint) # 현재 URL에 해당하는 뷰함수의 포인트를 출력 ex) main/views.py의 index 뷰함수면 main.index
    print('request Blueprint! : ' + request.blueprint) # 현재 URL에 해당하는 blueprint의 명칭을 출력.
    if 'id' in session and 'name' in session and request.blueprint != 'auth': # user 인증 확인 조건문으로 auth blueprint를 제외(로그인, 회원가입, 재인증, 인증 등에 엮이지 않도록 하기 위한 조건문 내용)
        conn = pymysql.connect(host='192.168.111.133', port=3306, user=current_app.config['DB_USER'], passwd=current_app.config['DB_PASSWD'], database='flasky')
        cur = conn.cursor()
        cur.execute('select confirmed, username from user where id = "%s"' %(session.get('id')))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if not user[0]:
            return render_template('auth/unconfirmed.html', username = user[1])


@auth.route('/confirm')
def resend_confirmation():
    if not 'id' in session and not 'name' in session:
        return redirect(url_for('auth.login'))
    s = Serializer(current_app.config['SECRET_KEY'], 3600)
    token = s.dumps({'confirm' : session.get('id')})
    conn = pymysql.connect(host='192.168.111.133', port=3306, user=current_app.config['DB_USER'], passwd=current_app.config['DB_PASSWD'], database='flasky')
    cur = conn.cursor()
    cur.execute('select username, email from user where id = "%s"' %(session.get('id')))
    user = cur.fetchone()
    cur.close()
    conn.close()
    send_email(user[1], 'Confirm Your Account', 'auth/email/confirm', username=user[0], token=token)
    print('send Email!!')
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))