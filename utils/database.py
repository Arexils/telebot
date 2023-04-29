import sqlite3


class DatabaseManager:

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def create_tables(self):
        self.query('CREATE TABLE IF NOT EXISTS products (idx text, title text, body text, photo blob, price int, tag text)')
        self.query('CREATE TABLE IF NOT EXISTS orders (cid int, usr_name text, usr_address text, products text)')
        self.query('CREATE TABLE IF NOT EXISTS cart (cid int, idx text, quantity int)')
        self.query('CREATE TABLE IF NOT EXISTS categories (idx text, title text)')
        self.query('CREATE TABLE IF NOT EXISTS wallet (cid int, balance real)')
        self.query('CREATE TABLE IF NOT EXISTS questions (cid int, question text)')

        self.query('CREATE TABLE IF NOT EXISTS polling(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, vote INTEGER check (vote in (0,1)), data TEXT)')
        self.query('CREATE TABLE IF NOT EXISTS user(user_id INT PRIMARY KEY, chat_id INT, username TEXT)')
        self.query('CREATE TABLE IF NOT EXISTS chat_message(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT, chat_id INT, message TEXT)')
        self.query('CREATE TABLE IF NOT EXISTS history_cats(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, timestamp INTEGER, url TEXT)')
        self.query('CREATE TABLE IF NOT EXISTS block_list(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, timestamp INTEGER, reason TEXT)')

    def query(self, arg, values=None):
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        self.conn.commit()

    def fetchone(self, arg, values=None):
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        return self.cur.fetchone()

    def fetchall(self, arg, values=None):
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        return self.cur.fetchall()
