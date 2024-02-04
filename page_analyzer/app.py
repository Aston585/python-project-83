from .db_operations import OperatorDB
from .parsing import Parser
from .url_processing import normalyze_url, validate_url
from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   flash,
                   session,
                   )
import os
from dotenv import load_dotenv
import requests
from copy import deepcopy


load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
db_operator = OperatorDB()


@app.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@app.route("/urls/<id_url>", methods=['GET'])
def analyze_site(id_url):
    if request.method == 'GET':
        site_info = session.get(id_url,
                                db_operator.get_site_info_on_id(id_url),
                                )
        site_checks = db_operator.get_results_site_checks(id_url)
        return render_template('show_site.html',
                               site_info=site_info,
                               site_checks=site_checks,
                               )


@app.route("/urls", methods=['GET', 'POST'])
def get_sites():
    if request.method == 'GET':
        urls_info = db_operator.get_urls()
        checks_info = db_operator.get_checks()

        check_sites_info = [url._asdict() for url in deepcopy(urls_info)]
        for url in check_sites_info:
            for check in checks_info:
                if url.get('id') == check.url_id:
                    url.update(
                        created_at=check.created_at,
                        status_code=check.status_code,
                    )

        return render_template('list_sites.html',
                               check_sites_info=check_sites_info,
                               )

    if request.method == 'POST':
        url = request.form['url']
        if not url:
            flash('URL обязателен', 'error')
            return render_template('index.html'), 422

        url = normalyze_url(url)
        if not validate_url(url):
            flash('Некорректный URL', 'error')
            return render_template('index.html', url=url), 422

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


@app.route("/urls/<id>/checks", methods=['POST'])
def checks(id):
    if request.method == 'POST':
        if session.get(id):
            url = session.get(id).get('name')
        else:
            url = db_operator.get_site_info_on_id(id).name

        try:
            parser = Parser(url)
            parser.response.raise_for_status()
        except requests.RequestException:
            flash('Произошла ошибка при проверке', 'error')
            return redirect(url_for('analyze_site', id_url=id), code=302)

        parsing_results = {
            'url_id': id,
            'status_code': parser.get_site_status(),
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
