from flask import render_template, redirect, request, url_for, flash, current_app, session
from wtforms.validators import Email
from . import auth
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetForm, PasswordResetRequestForm, ChangeEmailForm
from ..email import send_email
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash # 비밀번호 해쉬를 위한 모듈.
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import date, datetime

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
    cur.execute('select id, confirmed, email from user where id = "%s"' %(data.get('confirm')))
    user = cur.fetchone()

    if user[1]:
        return redirect(url_for('main.index'))
    elif user[0] == data.get('confirm'):
        cur.execute('update user set confirmed=true where id="%s"' %(user[0]))
        if user[2] == current_app.config['FLASKY_ADMIN']:
            cur.execute("update user set role_id = (select id from role where name='Administrator') where id = '%s'" %(user[0]))
        else:
            cur.execute("update user set role_id = (select id from role where default_value = 1) where id = '%s'" %(user[0]))
        conn.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')

    cur.close()
    conn.close()
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request(): # request hooks - before_request : 각 리퀘스트 전에 실행하는 함수를 등록하는 후크이다. before_request 와 같은 후크로 blueprint를 적용할 시 before_request 후크는 before_app_request로 변경된다.
    # print('request hooks!!')
    # print('request End Point! : ' + request.endpoint) # 현재 URL에 해당하는 뷰함수의 포인트를 출력 ex) main/views.py의 index 뷰함수면 main.index
    # print('request Blueprint! : ' + request.blueprint) # 현재 URL에 해당하는 blueprint의 명칭을 출력.
    if 'id' in session and 'name' in session: # 로그인 확인 조건문을 통해 로그인 여부를 체크한다. 조건문이 True라면 최신 접속일은 update한다.
        conn = pymysql.connect(host='192.168.111.133', port=3306, user=current_app.config['DB_USER'], passwd=current_app.config['DB_PASSWD'], database='flasky')
        cur = conn.cursor()
        cur.execute('select confirmed, username from user where id = "%s"' %(session.get('id')))
        user = cur.fetchone()
        # request hooks를 이용하여 최근 로그인 시간은 update하는 기능인데 이 부분을 login과 logout을 시도할 때 update하는것이 더 낫지 않을까..?
        cur.execute("update user set last_seen = '%s' where id = '%s'" %(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), session.get('id')))
        conn.commit()
        if not user[0] and request.blueprint != 'auth': # user 인증 확인과 auth blueprint를 제외(로그인, 회원가입, 재인증, 인증 등에 엮이지 않도록 하기 위한 조건문 내용)하는 조건문으로 인증이 되지 않으면 재인증 페이지로 이동
            cur.close()
            conn.close()
            return redirect(url_for('auth.unconfirmed'))
        cur.close()
        conn.close()


@auth.route('/unconfirmed')
def unconfirmed():
    if 'id' in session and 'name' in session:
        conn = pymysql.connect(host='192.168.111.133', port=3306, user=current_app.config['DB_USER'], passwd=current_app.config['DB_PASSWD'], database='flasky')
        cur = conn.cursor()
        cur.execute('select confirmed, username from user where id = "%s"' %(session.get('id')))
        confirm = cur.fetchone()
        cur.close()
        conn.close()
        if confirm[0]:
            return redirect(url_for('main.index'))
        return render_template('auth/unconfirmed.html', username = confirm[1])


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


@auth.route('/change-password', methods=['GET','POST'])
def change_password():
    if not 'name' in session and not 'id' in session:
        flash('로그인을 해주세요.')
        return redirect(url_for('auth.login'))
    form = ChangePasswordForm()
    if form.validate_on_submit(): # submit 버튼을 클릭 했을 때 해당 조건문은 True가 된다.
        conn = pymysql.connect(host='192.168.111.133', port=3306, user=current_app.config['DB_USER'], passwd=current_app.config['DB_PASSWD'], database='flasky')
        cur = conn.cursor()
        cur.execute('select password_hash from user where id = "%s"' %(session.get('id')))
        user = cur.fetchone()
        if user and check_password_hash(user[0], form.old_password.data): # 위에서 조회한 페스워드 해쉬 값과 사용자가 입력한 현재 비밀벊호가 맞는지 확인하고 서브밋한 사용자 계정의 존재 유무를 확인하는 조건문이다.
            cur.execute("update user set password_hash = '%s' where id = '%s'" %(generate_password_hash(form.password.data), session.get('id'))) # 조건문이 True이면 사용자가 변경한 비밀번호 값을 werkzeug.security 모듈의 generate_password_hash 함수로 해싱을 하여 DB에 Update한다.
            conn.commit()
            flash('Your password has been updated')
            cur.close()
            conn.close()
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password')
        cur.close()
        conn.close()
    return render_template('auth/change_password.html', form = form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_required():
    # password를 잊었을 때 찾기 위한 뷰함수로 로그인이 되어있지 않는 상태여야한다.
    if 'name' in session and 'id' in session:
        flash('잘 못 접근하셨습니다.')
        return redirect('main.index')
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        # reset password 요청 폼이 submit되었을 때 해당 이메일로 토큰을 전송해야한다.
        # 토큰 전송할 값은 id 컬럼 값이다.
        conn = pymysql.connect(host='192.168.111.133', port=3306, user=current_app.config['DB_USER'], passwd=current_app.config['DB_PASSWD'], database='flasky')
        cur = conn.cursor()
        cur.execute('select id, username from user where email = "%s"' %(form.email.data))
        token_id = cur.fetchone()
        cur.close()
        conn.close()
        if not token_id:
            flash('해당 이메일이 존재하지 않습니다.')
            return redirect(url_for('auth.password_reset_required'))
        s = Serializer(current_app.config['SECRET_KEY'], 3600)
        token = s.dumps({'reset' : token_id[0]})
        send_email(form.email.data, 'Reset Your Password', 'auth/email/reset_password',username = token_id[1], token = token)
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if 'name' in session and 'id' in session:
        flash('잘 못 된 접근 입니다.')
        return redirect(url_for('main.index'))

    form = PasswordResetForm()

    if form.validate_on_submit():
        s = Serializer(current_app.config['SECRET_KEY'], 3600)
        conn = pymysql.connect(host='192.168.111.133', port=3306, user=current_app.config['DB_USER'], passwd=current_app.config['DB_PASSWD'], database='flasky')
        cur = conn.cursor()
        try:
            data = s.loads(token)
            print(data)
            cur.execute("select id from user where id = '%s'" %(data.get('reset')))
            user_info = cur.fetchone()
            if not user_info:
                cur.close()
                conn.close()
                flash('잘 못 된 정보입니다.')
                return redirect(url_for('main.index'))
            cur.execute("update user set password_hash = '%s' where id = '%s'" %(generate_password_hash(form.password.data), user_info[0]))
            conn.commit()
            cur.close()
            conn.close()
            flash('Your password has been update.')
            return redirect(url_for('auth.login'))
        except Exception as e:
            cur.close()
            conn.close()
            print('에러 발생! 에러 내용 : ' + str(e))
            flash('에러가 발생했습니다.')
            return redirect(url_for('main.index'))

    return render_template('auth/reset_password.html', form = form)


@auth.route('/change_email', methods=['GET', 'POST'])
def change_email():
    if not 'id' in session and not 'name' in session:
        flash('로그인을 해주세요.')
        return redirect(url_for('auth.login'))
    form = ChangeEmailForm()
    if form.validate_on_submit():
        conn = pymysql.connect(host='192.168.111.133', port=3306, user=current_app.config['DB_USER'], passwd=current_app.config['DB_PASSWD'], database='flasky')
        cur = conn.cursor()
        if cur.execute("select email from user where email = '%s'" %(form.email.data)):
            cur.close()
            conn.close()
            flash('가입된 이메일입니다.')
            return redirect(url_for('auth.change_email'))
        cur.execute("select username, password_hash from user where id = '%s'" %(session.get('id')))
        token_id = cur.fetchone()
        cur.close()
        conn.close()

        if check_password_hash(token_id[1], form.password.data):
            s = Serializer(current_app.config['SECRET_KEY'], 3600)
            token = s.dumps({'id' : session.get('id'), 'email' : form.email.data})
            send_email(form.email.data, 'Change Your Email', 'auth/email/change_email', username = token_id[0], token = token)
            flash('이메일 인증 절차를 진행합니다. 인증 메일 ' + form.email.data + '에 메일을 전송했습니다. 확인해주세요.')
            return redirect(url_for('main.index'))
        else:
            flash('비밀번호가 옳바르지 않습니다.')
            return redirect(url_for('auth.change_email'))

    return render_template('auth/change_email.html', form = form)


@auth.route('/email_confirm/<token>')
def change_email_token(token):
    print('test email token')
    if not 'id' in session and not 'name' in session:
        flash('로그인을 해주세요.')
        return redirect(url_for('auth.login'))

    s = Serializer(current_app.config['SECRET_KEY'], 3600)
    data = s.loads(token)
    conn = pymysql.connect(host='192.168.111.133', port=3306, user=current_app.config['DB_USER'], passwd=current_app.config['DB_PASSWD'], database='flasky')
    cur = conn.cursor()
    if not cur.execute('select * from user where id = "%s"' %(data.get('id'))):
        cur.close()
        conn.close()
        flash('잘 못 된 토큰 정보입니다.')
        return redirect(url_for('auth.change_email'))

    cur.execute("update user set email = '%s' where id = '%s'" %(data.get('email'), data.get('id')))
    conn.commit()
    cur.close()
    conn.close()

    session.clear()

    flash('이메일 수정되었습니다. 다시 로그인을 해주세요.')
    return redirect(url_for('auth.login'))