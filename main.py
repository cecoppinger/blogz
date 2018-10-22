from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'aoweifjsladkfjawoiefr123j12klj'

class Blog(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(120))
  body = db.Column(db.Text)
  pub_date = db.Column(db.DateTime)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __init__(self, title, body, user, pub_date=None):
    self.title = title
    self.body = body
    if pub_date == None:
      pub_date = datetime.utcnow()
    self.pub_date = pub_date
    self.user = user

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(120), nullable=False)
  password = db.Column(db.String(120), nullable=False)
  posts = db.relationship('Blog', backref='user', lazy=True)

  def __init__(self, username, password):
    self.username = username
    self.password = password

def get_blog():
  return Blog.query.order_by(Blog.pub_date.desc())

def get_users():
  return User.query.all()

def is_in_session():
  if 'user' in session:
    return True
  else:
    return False

@app.before_request
def require_login():
  allowed_routes = ['login', 'register', 'blog', 'index']
  if 'user' not in session and request.endpoint not in allowed_routes:
    flash("Must be logged in to do that", 'error')
    return redirect('/login')

@app.route('/')
def index():
  users = User.query.all()
  return render_template('index.html', users=users, logged_in=is_in_session())

@app.route('/blog')
def blog():
  blog = get_blog()
  id = request.args.get('id')
  username = request.args.get('username')

  if id:
    post = Blog.query.get(id)
    return render_template('post.html', post=post)
  elif username:
    user = User.query.filter_by(username=username).first()
    posts = Blog.query.filter_by(user_id=user.id).order_by(Blog.pub_date.desc()).all()
    return render_template('blog.html', blog=posts, users=get_users(), logged_in=is_in_session())

  return render_template('blog.html', blog=blog, users=get_users(), logged_in=is_in_session())

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
  if request.method == 'POST':
    post_title = request.form['title']
    post_body = request.form['body']

    if not post_title or not post_body:
      flash("All fields must be filled out")
      return render_template('newpost.html', title=post_title, body=post_body)

    username = session['user']
    user = User.query.filter_by(username=username).first()
    
    new_post = Blog(post_title, post_body, user)
    db.session.add(new_post)
    db.session.commit()

    return render_template('post.html', post=new_post, logged_in=is_in_session())

  return render_template('newpost.html', logged_in=is_in_session())

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
      session['user'] = username
      return redirect('/newpost')
    elif not username or not password:
      flash("All fields must be filled out", 'error')
      return render_template('login.html')
    elif username and not user:
      flash("That username does not exist", 'error')
      return render_template('login.html')
    else:
      flash("Incorrect password", 'error')
      return render_template('login.html')

  return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():  
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify-pw']
    existing_user = User.query.filter_by(username=username).first()

    if not username or not password or not verify:
      flash('All fields must be filled out', 'error')
      return render_template('register.html', username=username)
    elif existing_user:
      flash('That username is taken', 'error')
      return render_template('register.html')
    elif password != verify:
      flash("Those passwords don't match", 'error')
      return render_template('register.html', username=username)
    elif len(username) < 3 or len(password) < 3:
      flash("Username and password must be at least 3 characters")
      return render_template('register.html')
    elif not existing_user and password == verify:
      user = User(username, password)
      db.session.add(user)
      db.session.commit()
      flash("Successfully registered")
      session['user'] = username
      return redirect('/newpost')
    else:
      flash("Seems I haven't handled this yet!")
      return render_template('register.html')

  return render_template('register.html')

@app.route('/logout')
def logout():
  del session['user']
  return redirect('/blog')

if __name__ == '__main__':
  app.run()
