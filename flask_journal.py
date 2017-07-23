from flask import Flask, render_template, redirect, url_for, make_response, \
    request, g, flash
from flask_login import LoginManager
from models import user
from forms import forms
import json

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'nstoheunoadeigc4ybihct.bp8i7euhibethuibcgroep!'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return user.User.get(user.User.id == userid)
    except user.DoesNotExist:
        return None


def get_saved_data():
    try:
        data = json.loads(request.cookies.get('Yummy Cookie'))
    except TypeError:
        data = {}
    return data


@app.before_request
def before_request():
    """Connect to DB before each request"""
    g.db = user.db
    g.db.connect()


@app.after_request
def after_request(response):
    """Close DB connection after each request"""
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay, it worked")
        user.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/')
def index():
    data = get_saved_data()
    return render_template('index.html', saves=data)


@app.route('/detail.html')
def detail():
    return ('detail.html')


@app.route('/new')
def new():
    return render_template('new.html')


@app.route('/new', methods=['POST'])
def save_new():
    response = make_response(redirect(url_for('index')))
    data = get_saved_data()
    response.set_cookie('Yummy Cookie', json.dumps(data))
    return response


if __name__ == '__main__':
    user.initialize()

    try:
        user.User.create_user(
            username='huldru',
            email='ajlongstreet@gmail.com',
            password='password'
        )
    except ValueError:
        pass

    app.run(debug=DEBUG, port=PORT)
