from flask import Flask, render_template, abort, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import pymysql

app = Flask(__name__)
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


app.config['SECRET_KEY'] = 'hard secret key token'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        conn = pymysql.connect(host='192.168.111.133', port=3306, user='user_name', passwd='password', database='schema name')
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


