# notes
'''
This file is for creating a Flask server to be used for the dash app.
'''
# package imports
import os
from flask import Flask

server = Flask(__name__)
server.config.update(
    SESSION_COOKIE_SAMESITE="None",  # Change this to "Strict" or "None" as needed
    SESSION_COOKIE_SECURE=True,  # Recommended if using "None" for SAMESITE
    SECRET_KEY=os.getenv('SECRET_KEY')
)