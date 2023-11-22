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

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
