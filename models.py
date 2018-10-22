from app import db
from hashutils import make_pw_hash
from datetime import datetime

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
  pw_hash = db.Column(db.String(120), nullable=False)
  posts = db.relationship('Blog', backref='user', lazy=True)

  def __init__(self, username, password):
    self.username = username
    self.pw_hash = make_pw_hash(password)
