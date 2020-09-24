from app import db, login, ma
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {} {}>'.format(self.username,self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
            if not self.is_following(user):
                self.followed.append(user)

    def unfollow(self, user):
            if self.is_following(user):
                self.followed.remove(user)

    def is_following(self, user):
            return self.followed.filter(
                followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

#Phonebook Class/Model
class Phonebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    address =db.Column(db.String(140))
    city = db.Column(db.String(20))
    phonenumber =db.Column(db.Integer)

    def __repr__(self):
        return '<Phonebook {}>'.format(self.name)
    def to_dict(self):
        data = {
            'id' : self.id,
            'name' : self.name,
            'address' : self.address,
            'city' : self.city,
            'phonenumber' : self.phonenumber
        }
        return data

    def __init__(self, name, phonenumber, address, city): #Class constructor
        self.name = name
        self.phonenumber = phonenumber
        self.address = address
        self.city = city

class PhonebookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name','phonenumber', 'address', 'city')

phonebook_schema =  PhonebookSchema()
phonebooks_schema =  PhonebookSchema(many=True)