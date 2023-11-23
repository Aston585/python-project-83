from flask import (Flask,
                   render_template,
                   request,
                   make_response,
                   redirect,
                   url_for,
                   flash,
                   get_flashed_messages,
                   session,
                   )
import os
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
