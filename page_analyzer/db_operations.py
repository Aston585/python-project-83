import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import NamedTupleCursor


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# URLS = [f"https://ru.hexlet{i}.io" for i in range(1000)]


class PageAbalyzerDB:
    def __init__(self):
        self.connection = psycopg2.connect(DATABASE_URL)
        self.cursor = self.connection.cursor(cursor_factory=NamedTupleCursor)
        self.connection.autocommit = True

    def deco_connection_close(method):
        def inner(self, *args):
            result_method = method(self, *args)
            return result_method
        return inner

    @deco_connection_close
    def get_list_sites(self):
        self.cursor.execute("SELECT * FROM urls ORDER BY id DESC")
        return self.cursor.fetchall()

    @deco_connection_close
    def add_site(self, url):
        self.cursor.execute("""
            INSERT INTO urls (name)
            VALUES (%s);""",
            (url,))
        self.cursor.close()
        self.connection.close()

    @deco_connection_close
    def check_availability(self, url):
        self.cursor.execute("""
            SELECT urls.name FROM urls
            WHERE name = %s""",
            (url,))
        return True if self.cursor.fetchone() else False

    @deco_connection_close
    def get_site_info(self, url):
        self.cursor.execute("""
            SELECT * FROM urls
            WHERE name = %s""",
            (url,))
        return self.cursor.fetchone()

    def check_conn_db(self):
        if self.connection.closed == 0:
            print("Соединение с базой данных установлено")
        else:
            print("Соединение с базой данных разорвано")

        # Проверка состояния соединения после закрытия
        if self.connection.closed == 0:
            print("Соединение с базой данных установлено")
        else:
            print("Соединение с базой данных разорвано")


db_operator = PageAbalyzerDB()
#db_oper.add_sites(URLS, date.today())
#print(db_oper.get_list_sites())
# print(db_oper.check_availability('https://www.psycopg.org'))
# print(db_oper.check_availability('https://ru.hexlet0.io'))
# print(db_oper.get_site('https://ru.hexlet1.io'))




# connection = psycopg2.connect(DATABASE_URL)
# connection.autocommit = True
# cursor = connection.cursor()
# cursor.execute('SELECT * FROM urls')
# # cursor.execute("""
# #     INSERT INTO urls (id, name, created_at)
# #     VALUES (%s, %s, %s);""",
# #     (_id, url, date.today()))

# print(cursor.fetchall())



# try:
#     conn = psycopg2.connect(DATABASE_URL)
# except:
#     print("[INFO] Can`t establish connection to database")

# cursor = conn.cursor()
########################################################################

# try:
#     connection = psycopg2.connect(DATABASE_URL)
#     connection.autocommit = True
    
#     with connection.cursor() as cursor:
        
    
# except Exception as _ex:
#     print("[INFO] Error while working with PostgreSQL", _ex)
# finally:
#     if connection:
#         connection.close()
#         print("[INFO] PostgreSQL connection closed")

#db_operations
