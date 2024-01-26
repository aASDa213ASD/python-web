import enum
from datetime import datetime
from app import db


class EnumPriority(enum.Enum):
    Low    = 1
    Medium = 2
    High   = 3


class Post(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200))
    text        = db.Column(db.Text)
    image_file  = db.Column(db.String(200), nullable=False, default='default_post.png')
    created     = db.Column(db.TIMESTAMP, default=datetime.now().replace(microsecond=0))
    type        = db.Column(db.Enum(EnumPriority), default=EnumPriority.Low)
    enabled     = db.Column(db.Boolean, default=False)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user        = db.relationship("User")
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f"Post(id={self.id}, title='{self.title}', type='{self.type}')"


class Category(db.Model):
    id    = db.Column(db.Integer,    primary_key=True)
    name  = db.Column(db.String(50), nullable=False)
    posts = db.relationship('Post', backref='category', lazy=True)


post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id',  db.Integer, db.ForeignKey('tag.id'),  primary_key=True)
)


class Tag(db.Model):
    id    = db.Column(db.Integer,    primary_key=True)
    name  = db.Column(db.String(50), nullable=False,      unique=True)
    posts = db.relationship('Post', secondary=post_tags, backref='tags')
