from enum import Enum


class TimeUnits:
    DAY_IN_SEC = 24 * 60 * 60
    MONTH_IN_SEC = 31 * 24 * 60 * 60
    WEEK_IN_SEC = 14 * 24 * 60 * 60


class Config:
    DUE_THRESHOLD = TimeUnits.DAY_IN_SEC * 5
    NOTIFICATION_INTERVAL = TimeUnits.DAY_IN_SEC * 3


class Auth:
    CLIENT_ID = '980879137585-hh6hgmp8o1bmg45gv6oqb75ugqpmtr11.apps.googleusercontent.com'


EMAIL_BODY = 'The book "{title}" you loaned from Yirmiyahu Library Gemach is due on <b>{due_date}</b>.\n' \
             'If you wish to renew your book, please email us or call on the days that the library is open.\n' \
             'Books may be renewed for an additional month (except for new books).\n\n' \
             '' \
             'Please note: For every week the book is late, a fee of 5nis is incurred.\n\n' \
             '' \
             'Thank you!\n' \
             'Yirmiyahu Library Gemach\n\n' \
             '' \
             'Phone numbers:\n ' \
             'Shoshi 054-675-1195 or Tova Rina 054-587-0906\n\n' \
             '' \
             'Hours:\n' \
             'Monday: 10am-11.30am\n' \
             'Wednesday: 7.30pm-8.30pm\n\n' \
             'Address: Rechov Yirmiyahu 24b/14 (-1)\n\n' \
             '' \
             'Please do not leave any books outside the door.\n\n' \
             '' \
             'Thank you!\n' \
             'גמ״ח ספריית ירמיהו' \
             '\n' \
             'לע״נ הרב זאב שמשון בן יעקב טוביה הלוי ז״ל' \
             '\n' \
             'שרה בת דוד זלמן ז״ל'\
             '\n' \
             'מרת חיה פעשא בת בצלאל הלוי ע״ה'

UPCOMING_EMAIL_BODY_HTML = 'Dear Subscriber' \
                           '<br>The book "{title}" you loaned from Yirmiyahu Library Gemach is due on <b>{due_date}</b>.' \
                           '' \
                           '<p>If you wish to renew your book, please email us or call on the days that the library is open.' \
                           '<br>Books may be renewed once for an additional month (except for new books).' \
                           '<p>Please note: For every day the book is late, a fee of 1 shekel per day is incurred.'\
                           '' \
                           '<p>Thank you,' \
                           '<br>Yirmiyahu Library Gemach' \
                           '' \
                           '<p><b>Hours:</b><br>' \
                           'Monday: 10am-11.30am<br>' \
                           'Wednesday: 7.30pm-8.30pm' \
                           '<p><b>Address:</b> Rechov Yirmiyahu 24b/14 (-1)' \
                           '' \
                           '<p><b>Phone numbers:</b>' \
                           '<br>Shoshi 054-675-1195 or Tova Rine 054-587-0906' \
                           '' \
                           '<p>Please do not leave any books outside the door.' \
                           '' \
                           '<p>Thank you!' \
                           '' \
                           '<p>גמ"ח ספריית ירמיהו' \
                           '<br>לע"נ הרב זאב שמשון בן יעקב טוביה הלוי ז"ל' \
                           '<br>מרת שרה בת דוד זלמן ע״ה' \
                           '<br>מרת חיה פעשא בת בצלאל הלוי ע"ה'

OVERDUE_EMAIL_BODY_HTML = 'The book "{title}" you loaned from Yirmiyahu Library Gemach was due on <b>{due_date}</b>.' \
                          '<br>Please make sure it is returned as soon as possible during library hours.' \
                          '<br>For every day the book is late, a fee of 1 shekel per day is incurred.' \
                          '' \
                          '<p><b>Phone numbers:</b>' \
                          ' <br>054-675-1195 or 054-587-0906' \
                          '' \
                          '<p><b>Hours:</b><br>' \
                          'Monday: 10am-11.30am<br>' \
                          'Wednesday: 7.30pm-8.30pm' \
                          '' \
                          '<p><b>Address:</b> Rechov Yirmiyahu 24b/14 (-1)' \
                          '' \
                          '<p>Please do not leave any books outside the door.' \
                          '' \
                          '<p>Thank you!' \
                          '' \
                          '<p>גמ"ח ספריית ירמיהו<br>לע"נ הרב זאב שמשון בן יעקב טוביה הלוי ז"ל<br>ושרה בת דוד זלמן ז"ל '
