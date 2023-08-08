from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from secrets import token_hex

db = SQLAlchemy()
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), nullable=False)
)
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    posts = db.relationship("Post", backref='author', lazy=True)
    token = db.Column(db.String, unique=True)
    # liked_posts = db.relationship("Post", secondary='like')
    liked_posts2 = db.relationship("Post", secondary='like2', lazy = 'dynamic')
    followed = db.relationship("User",
        secondary='followers',
        lazy='dynamic',
        backref=db.backref('followers', lazy='dynamic'),
        primaryjoin = (followers.c.follower_id == id),
        secondaryjoin = (followers.c.followed_id == id)
        )
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.token = token_hex(16)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'date_created': self.date_created,
            'token': self.token,
            'follower_count': len(self.followers.all()),
            'following_count': len(self.followed.all()),
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String, nullable=False)
    caption = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # likers = db.relationship('User', secondary='like')
    likers2 = db.relationship('User', secondary='like2')

    def __init__(self, title, caption, img_url, user_id):
        self.title = title
        self.caption = caption
        self.img_url = img_url
        self.user_id = user_id

    def like_count(self):
        return len(self.likers2)
    
    def to_dict(self, user=None):
        return {
            'id': self.id,
            'title': self.title,
            'caption': self.caption,
            'img_url': self.img_url,
            'date_created': self.date_created,
            'user_id': self.user_id,
            'author': self.author.username,
            'like_count': self.like_count(),
            'liked': user in self.likers2
        }

like2 = db.Table('like2',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), nullable=False)
)

# class Like(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

#     def __init__(self, user_id, post_id):
#         self.user_id = user_id
#         self.post_id = post_id

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String, nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Numeric(10,2))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, product_name, description, img_url, price):
        self.product_name = product_name
        self.description = description
        self.img_url = img_url
        self.price = price
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'description': self.description,
            'img_url': self.img_url,
            'price': self.price,
            'date_created': self.date_created,
        }
    
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id