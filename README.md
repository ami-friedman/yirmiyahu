New Laptop:
 - Install postgres:
   - brew services restart postgresql
   - Open new terminal and run: createdb yirmiyahu
 - Update env variable DATABASE_URL:
   - For Prod: Get this info from Heroku
   - For Dev: postgres://localhost:5432/yirmiyahu
 - From Pycharm run:
   - Add to the bottom of "models.py" a call to db.create_all()
   - Run it from pycharm (don't forget to add the DATABASE_URL env var)
   - In the terminal run:
     - flask db stamp head 
     - flask db migrate
 