from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='css')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:num1811418@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(120))
  body = db.Column(db.Text)

  def __init__(self, title, body):
    self.title = title
    self.body = body

def get_blog():
  return Blog.query.all()

@app.route('/')
def index():
  return redirect('/blog')

@app.route('/blog')
def blog():
  blog = get_blog()
  return render_template('blog.html', blog=blog)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
  #error_msg = ''

  if request.method == 'POST':
    post_title = request.form['title']
    post_body = request.form['body']

    if not post_title or not post_body:
      error_msg = 'Must not be empty'
      return render_template('newpost.html', error=error_msg)
    
    new_post = Blog(post_title, post_body)
    db.session.add(new_post)
    db.session.commit()

    return redirect('/blog')

  return render_template('newpost.html')

if __name__ == '__main__':
  app.run()
