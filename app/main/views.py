from flask import render_template, abort, session, redirect, url_for, flash, current_app
from . import main
from .forms import NameForm, EditProfileForm
from ..email import send_email
import pymysql

@main.route('/', methods=['GET', 'POST'])
def index():
    # form = NameForm()
    # if form.validate_on_submit():
    #     conn = pymysql.connect(host='192.168.111.133', port=3306, user=current_app.config['DB_USER'] , passwd=current_app.config['DB_PASSWD'], database='flasky', charset='utf8')
    #     cur = conn.cursor()
    #     cur.execute('select username from user where username="%s"' %(form.name.data))
    #     user = cur.fetchone()
    #     if user is None:
    #         cur.execute('insert into user(username) value("%s")' %(form.name.data))
    #         conn.commit()
    #         session['known'] = False
    #     else:
    #         session['known'] = True
    #     session['name'] = form.name.data
    #     form.name.data = ''
    #     cur.close()
    #     conn.close()
    #     return redirect(url_for('.index'))
    return render_template('index.html')

@main.route('/user/<username>')
def user(username):
    conn = pymysql.connect(host='192.168.111.133', port=3306, user=current_app.config['DB_USER'], passwd=current_app.config['DB_PASSWD'], database='flasky')
    cur = conn.cursor()
    cur.execute("select * from user where username = '%s'" %(username))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        abort(404)
    return render_template('user.html', user = user)


@main.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if not 'name' in session and not 'id' in session:
        flash('로그인이 되어있지 않습니다. 로그인을 해주세요.')
        return redirect(url_for('auth.login'))

    form = EditProfileForm()
    conn = pymysql.connect(host='192.168.111.133', port=3306, user=current_app.config['DB_USER'], passwd=current_app.config['DB_PASSWD'], database='flasky')
    cur = conn.cursor()
    if form.validate_on_submit():
        cur.execute('update user set name = "%s", location = "%s", about_me = "%s" where id = "%s"' %(form.name.data, form.location.data, form.about_me.data, session.get('id')))
        conn.commit()
        cur.close()
        conn.close()
        flash('Your Profile has been updated.')
        return redirect(url_for('main.user', username = session.get('name')))
    cur.execute("select name, location, about_me from user where id = '%s'" %(session.get('id')))
    user_info = cur.fetchone()
    cur.close()
    conn.close()
    form.name.data = user_info[0]
    form.location.data = user_info[1]
    form.about_me.data = user_info[2]
    return render_template('edit_profile.html', form = form)