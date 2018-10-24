import datetime

from flask import Flask, render_template, request, redirect, url_for, session
from flask import abort

from utils import get_post_path
from db import db_session, Post
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY


def get_unique_post_path(post_header):
    post_path = get_post_path(post_header)

    count_same_post_paths = len(
        db_session.query(Post.path).filter(
            Post.path.like('{}%'.format(post_path)),
        ).all(),
    )
    return '{}-{}'.format(
        post_path,
        count_same_post_paths,
    ) if count_same_post_paths > 0 else post_path


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        post_path = get_unique_post_path(post_header=request.form['header'])

        db_session.add(
            Post(
                header=request.form['header'],
                signature=request.form['signature'],
                body=request.form['body'],
                published=datetime.date.today(),
                path=post_path,
            ),
        )
        db_session.commit()

        session[post_path] = post_path
        session.permanent = True

        return redirect(url_for('show_post', post_path=post_path))

    return render_template('form.html')


@app.route('/<post_path>')
def show_post(post_path):
    post = db_session.query(Post).filter(Post.path == post_path).first()

    if post is None:
        abort(404)

    return render_template('post.html', post=post)


@app.route('/<post_path>/edit', methods=['GET', 'POST'])
def edit_post(post_path):
    if post_path not in session or session[post_path] != post_path:
        abort(403)

    post = db_session.query(Post).filter(Post.path == post_path).first()

    if post is None:
        abort(404)

    if request.method == 'POST':
        post.header = request.form['header']
        post.signature = request.form['signature']
        post.body = request.form['body']
        post.published = datetime.date.today()

        db_session.commit()

        return redirect(url_for('show_post', post_path=post_path))

    return render_template(
        'form.html',
        header=post.header,
        signature=post.signature,
        body=post.body,
    )


@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run()
