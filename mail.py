from time import time
from typing import Tuple

from flask_mail import Mail, Message
from apscheduler.schedulers.blocking import BlockingScheduler
from collections import namedtuple
from datetime import datetime

from canon import Config, UPCOMING_EMAIL_BODY_HTML, OVERDUE_EMAIL_BODY_HTML
from model_wrappers import loans_wrapper, email_trackers
from models import app

Subs = namedtuple('Subs', ['loan_id', 'email'])

mail_schedule = BlockingScheduler()

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'yirmiyahu.library@gmail.com',
    "MAIL_PASSWORD": 'Tzal1Fr1edm@n'
}

app.config.update(mail_settings)

mail = Mail(app)


def email_reminder(loans: Tuple, overdue: bool):
    if not loans:
        print('no relevant loans found')
    for loan_id, due_date, email, title in loans:
        if not email:
            continue
        notif = email_trackers.get_by_loan_id(loan_id)
        if notif:
            if time() - notif['last_trigger'] < Config.NOTIFICATION_INTERVAL:
                continue
            if not notif['is_overdue']:
                continue
        msg = Message(sender=('Yirmiyahu Library', app.config.get("MAIL_USERNAME")),
                      recipients=[email])
        if overdue:
            msg.html = OVERDUE_EMAIL_BODY_HTML.format(title=title,
                                                      due_date=datetime.fromtimestamp(due_date).strftime("%d %B %Y"))
            msg.subject = f'The book "{title}" is overdue'
        else:
            msg.html = UPCOMING_EMAIL_BODY_HTML.format(title=title,
                                                       due_date=datetime.fromtimestamp(due_date).strftime("%d %B %Y"))
            msg.subject = f'The book "{title}" is due in 5 days'

        try:
            print('sending mail')
            mail.send(msg)
            print('Mail sent')
            email_trackers.add({'loan_id': loan_id, 'is_overdue': overdue})
        except Exception as exp:
            print(f'something went wrong: {exp}')


def handle_emails():
    with app.app_context():
        print('About to handle emails')
        over_due_loans = loans_wrapper.get_overdue_loans()
        email_reminder(over_due_loans, overdue=True)
        upcoming_due_loans = loans_wrapper.get_upcoming_due_loans(Config.DUE_THRESHOLD)
        email_reminder(upcoming_due_loans, overdue=False)


@mail_schedule.scheduled_job('interval', hours=1)
def timed_job():
    handle_emails()


# print('starting mail scheduler')
# mail_schedule.start()
handle_emails()
