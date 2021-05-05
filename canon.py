from enum import Enum


class TimeUnits:
    DAY_IN_SEC = 24 * 60 * 60
    MONTH_IN_SEC = 31 * 24 * 60 * 60
    WEEK_IN_SEC = 14 * 24 * 60 * 60


class Config:
    DUE_THRESHOLD = TimeUnits.DAY_IN_SEC * 5
    NOTIFICATION_INTERVAL = TimeUnits.DAY_IN_SEC * 3


EMAIL_BODY = 'The book "{title}" you loaned from Yirmiyahu Library Gemach is due on <b>{due_date}</b>.\n' \
             'Please make sure it is returned by the due date during library hours.\n' \
             'For every day the book is late, a fee of 1 shekel per day is incurred.\n\n' \
             '' \
             'If you wish to renew your book, you may call on the days that the library is open.\n' \
             'Books may be renewed once for an additional month.\n\n' \
             '' \
             'Phone numbers: 054-675-1195 or 054-587-0906\n\n' \
             '' \
             'Hours:Monday: 10am-12pm\n' \
             'Wednesday: 7pm-9pm\n\n' \
             'Address: Rechov Yirmiyahu 24b/14 (-1)\n\n' \
             '' \
             'Please do not leave any books outside the door.\n\n' \
             '' \
             'Thank you!\n\n' \
             '' \
             'גמ״ח ספריית ירמיהו' \
             '\n' \
             'לע״נ הרב זאב שמשון בן יעקב טוביה הלוי ז״ל' \
             '\n' \
             'ושרה בת דוד זלמן ז״ל'

UPCOMING_EMAIL_BODY_HTML = 'Dear {subscriber}' \
                           '<br>The book "{title}" you loaned from Yirmiyahu Library Gemach is due on <b>{due_date}</b>.' \
                           '<br>Please make sure it is returned by the due date during library hours.' \
                           '<br>For every day the book is late, a fee of 1 shekel per day is incurred.' \
                           '' \
                           '<p>If you wish to renew your book, please email us or call on the days that the library is open.' \
                           '<br>Books may be renewed once for an additional month (except for new books).' \
                           '<p>Please note: For every day the book is late, a fee of 1 shekel per day is incurred.'\
                           '' \
                           '<p>Thank you,' \
                           '<br>Yirmiyahu Library Gemach' \
                           '' \
                           '<p><b>Hours:</b><br>' \
                           'Monday: 10am-12pm<br>' \
                           'Wednesday: 7pm-9pm' \
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
                          'Monday: 10am-12pm<br>' \
                          'Wednesday: 7pm-9pm' \
                          '' \
                          '<p><b>Address:</b> Rechov Yirmiyahu 24b/14 (-1)' \
                          '' \
                          '<p>Please do not leave any books outside the door.' \
                          '' \
                          '<p>Thank you!' \
                          '' \
                          '<p>גמ"ח ספריית ירמיהו<br>לע"נ הרב זאב שמשון בן יעקב טוביה הלוי ז"ל<br>ושרה בת דוד זלמן ז"ל '
