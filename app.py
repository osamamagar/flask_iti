from flask import Flask, render_template, request, redirect, url_for ,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    body = db.Column(db.Text)
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


# Define the Post model here

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)


@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        name = request.form.get('name')
        body = request.form.get('body')
        image = request.form.get('image')

        new_post = Post(name=name, body=body, image=image)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('posts/create_post.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get(id)

    if request.method == 'POST':
        post.name = request.form.get('name')
        post.body = request.form.get('body')
        post.image = request.form.get('image')
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('posts/edit_post.html', post=post)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_post(id):
    post = Post.query.get(id)

    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('posts/delete_post.html', post=post)

@app.route('/posts', methods=['GET'])
def get_all_posts():
    posts = Post.query.all()
    post_list = []
    for post in posts:
        post_data = {
            'id': post.id,
            'name': post.name,
            'body': post.body,
            'image': post.image
        }
        post_list.append(post_data)

    return jsonify({'posts': post_list})


@app.route('/details/<int:id>')
def post_details(id):
    post = Post.query.get(id)
    if post:
        return render_template('posts/details.html', post=post)
    else:
        return 'Post not found', 404

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.route('/about')
    def about():
        return render_template('about.html')




if __name__ == '__main__':
    app.run(debug=True)
