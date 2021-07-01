from flask import render_template, redirect, request, url_for, flash, current_app, session
from wtforms.validators import Email
from . import auth
from .forms import LoginForm
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(email = form.email.data).first()
        conn = pymysql.connect(host='192.168.111.133', port=3306, user=current_app.config['DB_USER'], passwd=current_app.config['DB_PASSWD'], database='flasky')
        cur = conn.cursor()
        cur.execute('select id, password_hash from user where email = "%s"' %(form.email.data))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user is not None and check_password_hash(user[1], form.password.data):
            session['id'] = user[0]
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html', form = form)


@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))