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

        return redirect(url_for('show_post', post_path=post_path))

    return render_template('form.html')


@app.route('/<post_path>')
def show_post(post_path):
    post = db_session.query(Post).filter(Post.path == post_path).first()

    if post is None:
        abort(404)

    return render_template('post.html', post=post)


if __name__ == "__main__":
    app.run()
