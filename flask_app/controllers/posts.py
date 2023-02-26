from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, post, comment


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



