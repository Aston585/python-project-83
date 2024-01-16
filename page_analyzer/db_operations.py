import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import NamedTupleCursor


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


class OperatorDB:
    def deco_manage_connection(method):
        def inner(self, *args):
            self.connection = psycopg2.connect(DATABASE_URL)
            self.connection.autocommit = True
            self.cursor = self.connection.cursor(
                cursor_factory=NamedTupleCursor)
            result_method = method(self, *args)
            self.cursor.close()
            self.connection.close()
            return result_method
        return inner

    @deco_manage_connection
    def get_list_sites(self):
        self.cursor.execute("SELECT * FROM urls ORDER BY id DESC")
        return self.cursor.fetchall()

    @deco_manage_connection
    def add_site(self, url):
        self.cursor.execute("""
            INSERT INTO urls (name)
            VALUES (%s)""", (url,))

    @deco_manage_connection
    def check_availability(self, url):
        self.cursor.execute("""
            SELECT urls.name FROM urls
            WHERE name = %s""", (url,))
        return True if self.cursor.fetchone() else False

    @deco_manage_connection
    def get_site_info(self, url):
        self.cursor.execute("""
            SELECT * FROM urls
            WHERE name = %s""", (url,))
        return self.cursor.fetchone()

    @deco_manage_connection
    def write_result_parsing(self, parsing_res):
        self.cursor.execute("""
            INSERT INTO url_checks (url_id,
                                    status_code,
                                    h1,
                                    title,
                                    description)
            VALUES (%s, %s, %s, %s, %s)""", (parsing_res.get('url_id'),
                                             parsing_res.get('status_code'),
                                             parsing_res.get('h1'),
                                             parsing_res.get('title'),
                                             parsing_res.get('description')))

    @deco_manage_connection
    def get_results_site_checks(self, url_id):
        self.cursor.execute("""
            SELECT
            id, status_code, h1, title, description, created_at
            FROM url_checks
            WHERE url_id = %s
            ORDER BY id DESC
            """, (url_id,))
        return self.cursor.fetchall()

    @deco_manage_connection
    def get_sites_info(self):
        self.cursor.execute("""
            SELECT
                urls.id,
                urls.name,
                MAX(url_checks.created_at),
                url_checks.status_code
            FROM urls
            RIGHT JOIN url_checks ON urls.id = url_checks.url_id
            GROUP BY urls.id, url_checks.status_code
            ORDER BY urls.id DESC
            """)
        return self.cursor.fetchall()
