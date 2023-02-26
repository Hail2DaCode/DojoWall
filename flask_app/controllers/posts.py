from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, post, comment

@app.route('/')
def show_login_reg():
    return render_template("login_reg.html")

@app.route("/login/user", methods = ["POST"])
def check_login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = user.User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")
@app.route("/dashboard")
def show_dashboard():
    if 'user_id' not in session:
        flash("Must login or register")
        return redirect('/login_reg')
    data = {
        "id": session['user_id']
    }
    print(session['user_id'])
    return render_template("wall.html", user = user.User.get_one(data), posts=post.Post.get_all_posts_with_creator_and_comments())
@app.route("/create/post", methods=['POST'])
def create_post():
    if len(request.form['post']) < 2:
        flash("Content cannot be blank")
        return redirect('/dashboard')
    data = {"content": request.form['post'],
            "user_id": session['user_id'],
    }
    post_id = post.Post.save(data)
    return redirect('/dashboard')
@app.route('/create/comment', methods = ['POST'])
def create_comment():
    if len(request.form['comment'].strip()) < 2:
        flash("Comment cannot be blank")
        return redirect('/dashboard')
    data = {"comment": request.form['comment'],
            "user_id": session['user_id'],
            "post_id": request.form['post_id']
    }
    comment.Comment.save_comment(data)
    return redirect('/dashboard')
@app.route("/delete/post/<int:post_id>")
def delete_post(post_id):
    data = {"id": post_id}
    return redirect('/dashboard', post.Post.delete(data))

@app.route('/clear')
def clear_session():
    session.clear()
    return redirect('/')



