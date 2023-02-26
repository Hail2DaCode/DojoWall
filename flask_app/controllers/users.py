from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, post, comment
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/register/user', methods = ['POST'])
def create_user():
    print(request.form)
    users = user.User.get_all()
    if not user.User.validate_user(request.form, users):
        return redirect ('/') 
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "fname": request.form['first_name'],
        "lname": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = user.User.save(data)
    session['user_id'] = user_id
    session['first_name'] = data['fname']
    print(session['user_id'])
    return redirect("/dashboard")