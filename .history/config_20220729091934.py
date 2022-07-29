import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://admin:pass_admin@localhost:5432/fyyur_db'



DATABASE_NAME = "school_db"
DATABASE_USER = "admin"
DATABASE_USER_PASSWORD = "admin"

CONNECTION_STRING = "dbname={} user={} password={}".format(
  DATABASE_NAME , DATABASE_USER  ,DATABASE_USER_PASSWORD
)