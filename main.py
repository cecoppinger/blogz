from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(120))
  body = db.Column(db.Text)
  pub_date = db.Column(db.DateTime)

  def __init__(self, title, body, pub_date=None):
    self.title = title
    self.body = body
    if pub_date == None:
      pub_date = datetime.utcnow()
    self.pub_date = pub_date

def get_blog():
  return Blog.query.order_by(Blog.pub_date.desc())

@app.route('/')
def index():
  return redirect('/blog')

@app.route('/blog')
def blog():
  blog = get_blog()
  id = request.args.get('id')

  if id:
    post = Blog.query.get(id)
    return render_template('post.html', post=post)

  return render_template('blog.html', blog=blog)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
  if request.method == 'POST':
    post_title = request.form['title']
    post_body = request.form['body']

    if not post_title or not post_body:
      error_msg = 'Must not be empty'
      return render_template('newpost.html', error=error_msg, title=post_title, body=post_body)
    
    new_post = Blog(post_title, post_body)
    db.session.add(new_post)
    db.session.commit()

    return render_template('post.html', post=new_post)

  return render_template('newpost.html')

if __name__ == '__main__':
  app.run()
