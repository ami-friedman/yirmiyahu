from abc import abstractmethod
from datetime import datetime
from time import time
from typing import List, Tuple, Optional
import sqlalchemy
from typing import Dict

from dateutil.relativedelta import relativedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

from canon import TimeUnits
from models import Book, db, Subscriber, Loan, Author, Subscription, EmailTracker, Category


class ModelWrapperBase:

    def __init__(self, db: SQLAlchemy, model):
        self._db = db
        self._model = model
        self._valid_keys: Tuple[str] = None

    @property
    def _now(self) -> datetime:
        return datetime.now()

    def get_all(self) -> List[Dict]:
        items = self._model.query.all()
        return [item.to_dict() for item in items]

    def get_by_id(self, id: str) -> Dict:
        item = self._model.query.get(id)
        return item.to_dict()

    def search(self, **kwargs):
        items = self._model.query.filter_by(**kwargs).all()
        return [item.to_dict() for item in items]

    @abstractmethod
    def add(self, new_item: Dict):
        pass

    def valid(self, item: Dict) -> bool:
        return all(k in item for k in self._valid_keys)


class Books(ModelWrapperBase):
    def __init__(self, db: SQLAlchemy, model):
        super().__init__(db, model)
        self._valid_keys = ['title', 'author', 'category']

    def add(self, new_item: Dict) -> Dict:
        author = authors_wrapper.add(new_item['author'])
        category = Category.query.get(new_item['category']['id'])
        book = Book(title=new_item['title'].title(), author_id=author['id'], category=category)
        db.session.add(book)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as _:
            db.session.rollback()
            print('Book exists! no need to add new one')
        except Exception as exc:
            print(f'Something went wrong: {exc}')
        finally:
            return Book.query.filter_by(title=new_item['title'].title()).first().to_dict()

    def update(self, id: str, updated_item: Dict):
        book = self._model.query.get(id)
        book.title = updated_item['title']
        book.category_id = updated_item['category']['id']

        db.session.add(book)

        try:
            db.session.commit()
        except Exception as exc:
            print(f'Something went wrong: {exc}')

    def delete(self, id):
        book_query = self._model.query.filter_by(id=id)

        try:
            book_query.delete()
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            print('Book linked to a loan! cannot delete')
        except Exception as exc:
            print(f'Something went wrong: {exc}')


class Subscribers(ModelWrapperBase):
    def __init__(self, db: SQLAlchemy, model):
        super().__init__(db, model)
        self._valid_keys = ['first_name', 'last_name', 'subscription_id']

    def add(self, new_item: Dict) -> Dict:
        subscription = subscriptions_wrapper.get_by_id(new_item['subscription_id'])
        subscriber = Subscriber(first_name=new_item['first_name'].title(),
                                last_name=new_item['last_name'].title(),
                                email=new_item.get('email'),
                                phone=new_item.get('phone'),
                                subscription_id=new_item['subscription_id'],
                                paid=new_item.get('paid'),
                                exp_date=int((self._now + relativedelta(months=+subscription['months'])).timestamp()))
        db.session.add(subscriber)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as _:
            db.session.rollback()
            print('subscriber exists! no need to add new one')
        except Exception as exc:
            print(f'Something went wrong: {exc}')

    def update(self, id: str, updated_item: Dict):
        sub = Subscriber.query.get(id)
        sub.first_name = updated_item['first_name']
        sub.last_name = updated_item['last_name']
        sub.email = updated_item.get('email')
        sub.phone = updated_item.get('phone')
        sub.paid = updated_item.get('paid')

        db.session.add(sub)

        try:
            db.session.commit()
        except Exception as exc:
            print(f'Something went wrong: {exc}')

    def get_by_id(self, id: str) -> Dict:
        sub = super().get_by_id(id)
        loans = self._db.session\
            .query(Subscriber,
                   Subscription.months,
                   Loan,
                   Book)\
            .join(Subscription)\
            .join(Loan, Loan.sub_id == Subscriber.id)\
            .join(Book, Loan.book_id == Book.id)\
            .filter(Subscriber.id == id)\
            .all()
        if loans:
            sub['loans'] = [{'loan_id': loan.Loan.id,
                             'title': loan.Book.title,
                             'loan_date': datetime.fromtimestamp(loan.Loan.loan_date).strftime('%b %d %Y') if loan.Loan.loan_date else loan.Loan.loan_date,
                             'due_date': datetime.fromtimestamp(loan.Loan.due_date).strftime('%b %d %Y') if loan.Loan.due_date else loan.Loan.due_date,
                             'return_date': datetime.fromtimestamp(loan.Loan.return_date).strftime('%b %d %Y') if loan.Loan.return_date else loan.Loan.return_date,
                             'original_due_date': datetime.fromtimestamp(loan.Loan.original_due_date).strftime('%b %d %Y') if loan.Loan.original_due_date else loan.Loan.original_due_date,
                             } for loan in loans]

        return sub

    def set_expired_subscribers(self):
        num_subscribers = db.session.query(Subscriber).filter(Subscriber.exp_date < time()).update({'expired': True,
                                                                                                    'paid': False})
        print(f'About to update to expired {num_subscribers} subscribers')
        try:
            db.session.commit()
        except Exception as exc:
            print(f'Something went wrong: {exc}')

        print(f'Updated {num_subscribers} subscribers to be EXPIRED!')

    def extend(self, id: str, subscription: Dict):
        sub: Subscriber = Subscriber.query.get(id)
        subscription_from_db = subscriptions_wrapper.get_by_id(subscription.get('id'))

        sub.subscription_id = subscription_from_db['id']
        current_exp_dt = datetime.fromtimestamp(sub.exp_date)
        new_exp_dt = current_exp_dt + relativedelta(months=+subscription_from_db['months'])
        sub.exp_date = int(new_exp_dt.timestamp())
        sub.expired = False

        db.session.add(sub)

        try:
            db.session.commit()
        except Exception as exc:
            print(f'Something went wrong: {exc}')


class Loans(ModelWrapperBase):
    def __init__(self, db: SQLAlchemy, model):
        super().__init__(db, model)
        self._valid_keys = ['books', 'subscriber_id']

    def add(self, new_item: Dict) -> List[Dict]:
        for book_to_loan in new_item['books']:
            book = Book.query.get(book_to_loan['id'])
            now = int(time())
            due_date = now + 1 * TimeUnits.MONTH_IN_SEC
            loan = Loan(book_id=book.id,
                        sub_id=new_item['sub_id'],
                        loan_date=now,
                        due_date=due_date)
            db.session.add(loan)
            db.session.flush()
            book.loan_id = loan.id
            db.session.add(book)
        try:
            db.session.commit()
        except Exception as exc:
            print(f'Something went wrong: {exc}')
            db.session.rollback()
        finally:
            loans = Loan.query.filter_by(sub_id=new_item['sub_id']).all()
            loans = [loan.to_dict() for loan in loans]
            return loans

    def delete(self, id):
        loan = self._model.query.get(id)
        book = Book.query.get(loan.book_id)
        book.loan_id = sqlalchemy.null()
        loan.return_date = int(time())
        db.session.add(book)
        db.session.add(loan)
        try:
            db.session.commit()
        except Exception as exc:
            print(f'Something went wrong: {exc}')
            db.session.rollback()

    def update(self, id):
        """
        Currently only extends the due date
        """
        loan = self._model.query.get(id)
        loan.original_due_date = loan.due_date
        loan.due_date = loan.due_date + 1 * TimeUnits.MONTH_IN_SEC

        db.session.add(loan)

        try:
            db.session.commit()
        except Exception as exc:
            print(f'Something went wrong: {exc}')
            db.session.rollback()

    def get_overdue_loans(self) -> List[Dict]:
        loans = db.session.query(Loan.id, Loan.due_date, Subscriber.email, Book.title)\
            .join(Subscriber)\
            .join(Book, Loan.book_id == Book.id)\
            .filter(and_(Loan.due_date < time(), Loan.return_date == None)).all()
        return loans

    def get_upcoming_due_loans(self, threshold: int) -> List[Dict]:
        loans = db.session.query(Loan.id, Loan.due_date, Subscriber.email, Book.title)\
            .join(Subscriber)\
            .join(Book, Loan.book_id == Book.id)\
            .filter(and_(Loan.due_date > time(),
                         Loan.due_date < (time() + threshold),
                         Loan.return_date == None)).all()
        return loans


class Authors(ModelWrapperBase):
    def __init__(self, db: SQLAlchemy, model):
        super().__init__(db, model)
        self._valid_keys = ['first_name', 'last_name']

    def search(self, search_query: str):
        pass

    def add(self, new_item: Dict) -> Dict:
        author = self._model(first_name=new_item['first_name'].title(), last_name=new_item['last_name'].title())
        try:
            self._db.session.add(author)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as _:
            print('Author exists! no need to add new one')
            db.session.rollback()
        return self._model.query.filter_by(first_name=new_item['first_name'].title(),
                                           last_name=new_item['last_name'].title()).first().to_dict()


class Subscriptions(ModelWrapperBase):
    def __init__(self, db: SQLAlchemy, model):
        super().__init__(db, model)
        self._valid_keys = ['months']

    def search(self, search_query: str):
        pass

    def add(self, new_item: Dict) -> Dict:
        sub = self._model(months=new_item['months'])
        try:
            self._db.session.add(sub)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as _:
            print('Subscription exists! no need to add new one')
            db.session.rollback()
        return self._model.query.filter_by(months=new_item['months']).first().to_dict()


class EmailTrackers(ModelWrapperBase):
    def add(self, new_item: Dict):
        email_tracker = self._model.query.filter_by(loan_id=new_item['loan_id']).first()
        if not email_tracker:
            email_tracker = self._model(loan_id=new_item['loan_id'],
                                        last_trigger=time(),
                                        is_overdue=new_item['is_overdue'])
        else:
            email_tracker.last_trigger = time()
            email_tracker.is_overdue = new_item['is_overdue']
        try:
            self._db.session.add(email_tracker)
            db.session.commit()
        except Exception as exc:
            print(f'Something went wrong: {exc}')
            db.session.rollback()

    def get_by_loan_id(self, loan_id: int) -> Optional[Dict]:
        notif = self._model.query.filter_by(loan_id=loan_id).first()
        return notif.to_dict() if notif else notif


class Categories(ModelWrapperBase):
    def __init__(self, db: SQLAlchemy, model):
        super().__init__(db, model)
        self._valid_keys = ['name']

    def add(self, new_item: Dict):
        category = self._model(name=new_item['name'])
        try:
            self._db.session.add(category)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as _:
            print('Category exists! no need to add new one')
            db.session.rollback()
        return self._model.query.filter_by(name=new_item['name']).first().to_dict()

    def update(self, id: str, updated_item: Dict):
        sub = self._model.query.get(id)
        sub.name = updated_item['name']

        db.session.add(sub)

        try:
            db.session.commit()
        except Exception as exc:
            print(f'Something went wrong: {exc}')
            raise

    def delete(self, id):
        category_query = self._model.query.filter_by(id=id)

        try:
            category_query.delete()
            db.session.commit()
        except Exception as exc:
            print(f'Something went wrong: {exc}')
            raise


books_wrapper = Books(db, Book)
subs_wrapper = Subscribers(db, Subscriber)
loans_wrapper = Loans(db, Loan)
authors_wrapper = Authors(db, Author)
subscriptions_wrapper = Subscriptions(db, Subscription)
email_trackers = EmailTrackers(db, EmailTracker)
categories_wrapper = Categories(db, Category)

