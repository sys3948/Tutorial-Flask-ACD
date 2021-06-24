from flask import Flask, render_template, abort, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
app = Flask(__name__)
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


app.config['SECRET_KEY'] = 'hard secret key token'

@app.route('/', methods=['GET', 'POST'])
def index():
    # name = None
    form = NameForm()
    if form.validate_on_submit():
        # name = form.name.data
        session['name'] = form.name.data
        form.name.data = ''
        print("URL : " + url_for('login'))
        return redirect(url_for('login'))
    # return render_template('index.html', form = form, name = name)
    return render_template('index.html', form = form, name = session.get('name'))

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


