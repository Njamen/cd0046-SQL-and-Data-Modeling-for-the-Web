import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = '<Put your local database url>'
'postgresql://admin:admin@localhost:5432/school_db'

// admin 
// pass_admin   
// fyyur_db 