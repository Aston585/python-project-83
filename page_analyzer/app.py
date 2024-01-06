from .db_operations import OperatorDB
from .url_processing import normalyze_url, validate_url
from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   flash,
                   get_flashed_messages,
                   session,
                   )
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
db_operator = OperatorDB()


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html',
                               messages=messages)

    if request.method == 'POST':
        if not request.form['url']:
            flash('URL обязателен', 'error')
            return redirect(url_for('index'), code=302)

        url = normalyze_url(request.form['url'])
        if not validate_url(url):
            flash('Некорректный URL', 'error')
            return redirect(url_for('index'), code=302)

        if db_operator.check_availability(url):
            flash('Страница уже существует', 'warning')
        else:
            db_operator.add_site(url)
            flash('Страница успешно добавлена', 'success')
        site_info = db_operator.get_site_info(url)
        id_url = site_info.id
        created_at = site_info.created_at.strftime("%Y-%m-%d")
        session[f"{id_url}"] = {'id': id_url,
                                'name': site_info.name,
                                'created_at': created_at}
        return redirect(url_for('analize_site', id_url=id_url), code=302)


@app.route("/urls/<id_url>", methods=['GET', 'POST'])
def analize_site(id_url):
    if request.method == 'GET':
        messages = get_flashed_messages(with_categories=True)
        site_info = session[id_url]
        return render_template('show_site.html',
                               messages=messages,
                               site_info=site_info,
                               )
    if request.method == 'POST':
        pass


@app.route("/urls", methods=['GET', 'POST'])
def get_sites():
    if request.method == 'GET':
        return render_template('list_sites.html',
                               responsive=None,
                               )
    if request.method == 'POST':
        pass


@app.route("/urls/<id>/checks", methods=['POST'])
def checks(id):
    pass


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404