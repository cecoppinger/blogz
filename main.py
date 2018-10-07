from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:num1811418@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
  id = db.Column(db.Interger, primary_key=True)
  title = db.Column(db.String(120))
  body = db.Column(db.Text)

  def __init__(self, title, body):
    self.title = title
    self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def blog():
  return render_template('blog.html')
