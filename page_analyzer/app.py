from .db_operations import OperatorDB
from .parsing import request_site_status, Parser
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
            return redirect(url_for('get_sites'), code=302)

        url = normalyze_url(request.form['url'])
        if not validate_url(url):
            flash('Некорректный URL', 'error')
            session['invalid_url'] = url
            return redirect(url_for('get_sites'), code=302)

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
        return redirect(url_for('analyze_site', id_url=id_url), code=302)


@app.route("/urls/<id_url>", methods=['GET'])
def analyze_site(id_url):
    if request.method == 'GET':
        messages = get_flashed_messages(with_categories=True)
        site_info = session.get(id_url,
                                db_operator.get_site_info_on_id(id_url),
                                )
        site_checks = db_operator.get_results_site_checks(id_url)
        return render_template('show_site.html',
                               messages=messages,
                               site_info=site_info,
                               site_checks=site_checks,
                               )


@app.route("/urls", methods=['GET'])
def get_sites():
    if request.method == 'GET':
        messages = get_flashed_messages(with_categories=True)
        if messages:
            if messages[0][0] == 'error':
                invalid_url = session.get('invalid_url', '')
                session['invalid_url'] = ''
                return render_template('index.html',
                                       messages=messages,
                                       invalid_url=invalid_url)

        check_sites_info = db_operator.get_sites_info()
        return render_template('list_sites.html',
                               check_sites_info=check_sites_info,
                               )


@app.route("/urls/<id>/checks", methods=['POST'])
def checks(id):
    if request.method == 'POST':
        if session.get(id):
            url = session.get(id).get('name')
        else:
            url = db_operator.get_site_info_on_id(id).name
        site_status = request_site_status(url)
        if not site_status:
            flash('Произошла ошибка при проверке', 'error')
            return redirect(url_for('analyze_site', id_url=id), code=302)
        parser = Parser(url)
        parsing_results = {
            'url_id': id,
            'status_code': site_status,
            'h1': parser.get_tag_h1(),
            'title': parser.get_tag_title(),
            'description': parser.get_attr_content_from_tag_meta()
        }
        db_operator.write_result_parsing(parsing_results)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('analyze_site', id_url=id), code=302)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
