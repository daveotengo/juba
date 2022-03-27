from time import strftime, gmtime

from flask import render_template, make_response, request, jsonify, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from app.auth import requires_access_level
from app.constants import ACCESS
from app.forms import AccountDetailForm
from app import db,app
from app.models import User
from app.utils import gen_pass

#### Routes ####

# index

#@app.route('/<string:anyurl>')
from config import APP_NAME


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', pageTitle='Home')

# about
@app.route('/about')
def about():
    return render_template('about.html', pageTitle='About')

################ GUEST ACCESS FUNCTIONALITY OR GREATER ###################

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def account():
    user = User.query.get_or_404(current_user.id)
    form = AccountDetailForm()

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)

        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))

    form.name.data = user.name
    form.email.data = user.email

    return render_template('profile.html', form=form, pageTitle='Profile')



################ USER ACCESS FUNCTIONALITY OR GREATER ###################

# dashboard
# @app.route('/index')
# @requires_access_level(ACCESS['user'])
# def dashboard():
#     return render_template('index.html', pageTitle='My Flask App Dashboard')

################ ADMIN ACCESS FUNCTIONALITY ###################

# control panel
@app.route('/user_mgmt')
@requires_access_level(ACCESS['admin'])
def control_panel():
    if request.method == "GET":
        all_users = User.query.all()
        return render_template('user_mgmt.html', users=all_users, pageTitle='User Mgmt')

@app.route('/api/users',methods=['GET'])
@requires_access_level(ACCESS['admin'])
def api_user():
    if request.method == "GET":
        all_users = User.query.all()
        print(all_users)
        return jsonify([
            {'id': user.id, 'name':user.name,'email': user.email, 'username': user.username,'access':user.access,'register_date':user.register_date}
            for user in all_users
        ])

    if request.method == "POST":
        all_users = User.query.all()
        return all_users;

@app.route('/api/users/user/<int:user_id>', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def user_by_id(user_id):
        user = User.query.get_or_404(user_id)
        response = make_response(
            jsonify(
                {'id': user.id, 'name':user.name,'email': user.email, 'username': user.username,'access':user.access,'register_date':user.register_date}
            ),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        return response


@app.route('/api/users/user/update', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def update_user():
    print("======entered api======")
    content = request.json

    name = content['name']
    username = content['username']
    email = content['email']
    access = content['access']
    id = content['id']


    print(name)

    user = User.query.get_or_404(id)

    orig_user = user.username # get user details stored in the database - save username into a variable

    user.name = name
    user.email = email

    new_user = username

    if new_user != orig_user: # if the form data is not the same as the original username
        valid_user = User.query.filter_by(username=new_user).first() # query the database for the usernam
        if valid_user is not None:
            response = make_response(
                jsonify(
                    {"message": "That username is already taken...", "status": "01"}
                ),
                200, )
            response.headers["Content-Type"] = "application/json"
            return response

    # if the values are the same, we can move on.
    user.username = username
    user.access = access
    db.session.commit()

    response = make_response(
    jsonify(
        {"message": "The user has been updated.", "status": "00"}
    ),
    200,)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/api/users/user/delete/<int:user_id>', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def delete_user(user_id):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        response = make_response(
            jsonify(
                {"message": "User deleted Successfully", "status": "00"}
            ),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        return response


@app.route('/api/users/user', methods=['POST'])
def new_user():
    print("======entered api======")
    content = request.json
    print(content['name'])


    # data = json.loads(request.data)
    # print(data.get("name", None))

    # data = request.form
    # print(data)

    name = content['name']
    username = content['username']
    email = content['email']
    access = content['access']
    print(name)
    print(username)
    print(email)
    print(access)

    #print(content['password'])

    if request.method == 'POST':
        user = User(name=name, username=username, email=email,register_date=strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        print("printing user")
        print(user)
        generated_pwd = gen_pass()
        print("printing generated_pwd")
        print(generated_pwd)
        user.set_password(generated_pwd)
        user.access = access
        db.session.add(user)
        db.session.commit()
        response = make_response(
            jsonify(
                {"message": "User has been successfully created", "status": "00"}
            ),
            201,
        )
    response.headers["Content-Type"] = "application/json"
    return response


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.errorhandler(400)
def bad_request():
    """Bad request."""
    return make_response(
        render_template("400.html"),
        400
    )

@app.context_processor
def inject_user():
    return dict(app_name=APP_NAME)

