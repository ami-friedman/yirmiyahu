import os
from datetime import datetime
from typing import Dict

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

app = Flask(__name__)
DATABASE_URL = os.environ['DATABASE_URL']
print('DB_URL:' + DATABASE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Author(db.Model):
    __table_args__ = (
        db.UniqueConstraint('first_name', 'last_name', name='unique_author'),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)

    def to_dict(self) -> Dict:
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'id': self.id,
        }

    def __repr__(self):
        return f'<Author {self.first_name} {self.last_name}>'


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    author = db.relationship('Author', backref=db.backref('books'), lazy=True)
    author_id = db.Column(db.Integer, ForeignKey('author.id'), nullable=False)
    loan_id = db.Column(db.Integer, ForeignKey('loan.id'))
    category_id = db.Column(db.Integer, ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('books'), lazy=True)
    book_type_id = db.Column(db.Integer, ForeignKey('book_type.id'), nullable=True)
    book_type = db.relationship('BookType', backref=db.backref('books'), lazy=True)

    def __repr__(self):
        return f'<Book {self.title}>'

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'author_id': self.author_id,
            'loan_id': self.loan_id,
            'author': self.author.to_dict(),
            'category': self.category.to_dict() if self.category else None,
            'book_type': self.book_type.to_dict() if self.book_type else None
        }


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text)
    phone = db.Column(db.Text)
    subscription_id = db.Column(db.Integer, ForeignKey('subscription.id'))
    exp_date = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Boolean, nullable=False, default=False)
    expired = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Subscriber {self.first_name} {self.last_name}>'

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'exp_date': datetime.fromtimestamp(self.exp_date).strftime('%b %d %Y'),
            'paid': self.paid,
            'subscription_id': self.subscription_id,
            'expired': self.expired,
        }


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    months = db.Column(db.Integer, nullable=False, unique=True)

    def __repr__(self):
        return f'<Subscription {self.months}>'

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'months': self.months,
        }


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    loan_date = db.Column(db.Integer, nullable=False)
    due_date = db.Column(db.Integer, nullable=False)
    original_due_date = db.Column(db.Integer, nullable=True)
    return_date = db.Column(db.Integer)
    book_id = db.Column(db.Integer, ForeignKey('book.id', use_alter=True), nullable=False)
    sub_id = db.Column(db.Integer, ForeignKey('subscriber.id'), nullable=False)

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'loan_date': datetime.fromtimestamp(self.loan_date).strftime('%b %d %Y'),
            'due_date': datetime.fromtimestamp(self.due_date).strftime('%b %d %Y'),
            'original_due_date': datetime.fromtimestamp(self.original_due_date).strftime('%b %d %Y')
            if self.original_due_date else '',
            'book_id': self.book_id,
            'return_date': datetime.fromtimestamp(self.return_date).strftime('%b %d %Y') if self.return_date else '',
            'sub_id': self.sub_id,
        }


class EmailTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    loan_id = db.Column(db.Integer, ForeignKey('loan.id'), unique=True)
    last_trigger = db.Column(db.Integer)
    is_overdue = db.Column(db.Boolean)

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'loan_id': self.loan_id,
            'last_trigger': self.last_trigger,
            'is_overdue': self.is_overdue,
        }


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
        }


class BookType(db.Model):
    __table_args__ = (
        db.UniqueConstraint('loan_duration', 'loan_duration_unit', name='unique_type'),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    loan_duration = db.Column(db.Integer, nullable=False)
    loan_duration_unit = db.Column(db.Text, nullable=False)

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'loan_duration': self.loan_duration,
            'loan_duration_unit': self.loan_duration_unit,
        }
