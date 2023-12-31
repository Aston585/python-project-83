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
            VALUES (%s);""", (url,))

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

