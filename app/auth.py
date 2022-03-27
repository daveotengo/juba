from datetime import timedelta
from functools import wraps
from time import strftime, gmtime

from flask import url_for, flash, session, render_template, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app.forms import RegistrationForm, LoginForm, RecoverPwForm, ResetPwForm
from app import login, app, db
from app.models import User
from app.utils import send_email


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))  #if this changes to a string, remove int


### custom wrap to determine access level ###
def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated: #the user is not logged in
                return redirect(url_for('login'))

            #user = User.query.filter_by(id=current_user.id).first()

            if not current_user.allowed(access_level):
                flash('You do not have access to this resource.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator





# registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,register_date=strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',  pageTitle='Register | My Flask App', form=form)

# user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash('You are now logged in', 'success')
        return redirect(next_page)
    return render_template('login.html',  pageTitle='Login | My Flask App', form=form)


#logout
@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('index'))


@app.route('/recoverpw', methods=['GET', 'POST'])
def recoverpw():
    form = RecoverPwForm()
    if request.method == "GET":
        return render_template('recoverpw.html',form=form)

    if request.method == "POST":
        email = request.form.get('email')
        user = User.verify_email(email)

        if user:
            send_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('recoverpw'))


@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_verified(token):
    user = User.verify_reset_token(token)
    print("printing token")
    print(token)
    print("printing user")
    print(user)
    if not user:
        flash('User not found or token has expired', 'warning')
        return redirect(url_for('recoverpw'))
    form = ResetPwForm()

    password = form.password.data #request.form.get('password')
    print("printing password")
    print(password)
    # if len(password or ()) < 8:
    #   flash('Your password needs to be at least 8 characters', 'error')
    if password:
        #hashed_password = generate_password_hash(password, method='sha256')
        user.set_password(password)

        print("printing hashed password")
        #print(hashed_password)
        #user.password = hashed_password
        #db.session.add(user)

        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_pwd.html',form=form)