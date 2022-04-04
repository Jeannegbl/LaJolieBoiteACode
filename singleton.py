import mysql.connector
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv('.env')


class Singleton:

    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)


@Singleton
class DBSingleton:
    def __init__(self):
        self.conn = mysql.connector.connect(user=os.environ.get('pseudo'), password=os.environ.get('password'),
                                            host='localhost', database=os.environ.get('database'))
        pass

    def query(self, sql, params=()):
        cursor = self.conn.cursor()
        # This attaches the tracer but ca marche pas on mysql
        # self.conn.set_trace_callback(print)
        cursor.execute(sql, params)
        try:
            self.result = cursor.fetchall()
        except mysql.connector.errors.InterfaceError:
            self.conn.commit()
            cursor.close()
            self.result = False
            return self.result
        else:
            self.conn.commit()

            cursor.close()
            return self.result

    def __str__(self):
        return 'Database connection object'

    def query_simple(self, sql):
        mycursor = self.conn.cursor()
        mycursor.execute(sql)
        return mycursor

    def fetchall_simple(self, sql):
        mycursor = self.query_simple(sql)
        results = mycursor.fetchall()
        mycursor.close()
        return results

    def query_arguments(self, sql, args: tuple = ()):
        mycursor = self.conn.cursor(buffered=True)
        mycursor.execute(sql, args)
        return mycursor

    def commit(self, sql, args):
        self.query_arguments(sql, args)
        self.conn.commit()


def Select(table, col, colonne_rech, id):
    db = DBSingleton.Instance()
    sql = "SELECT " + col + " from " + table + " WHERE " + colonne_rech + "=%s;"
    params: tuple = (id,)
    db.query(sql, params)
    return db.result[0]


def update(table, col, params: tuple, colonne_rech, id):
    db = DBSingleton.Instance()
    col_list = col.split(',')
    edits = ""
    compteur = 0
    for i in col_list:
        edits = edits + str(i) + "= %s,"
        compteur = compteur + 1
    edits = edits[:-1]
    sql = "UPDATE " + table + " SET " + edits + " WHERE " + colonne_rech + " = %s ;"
    params: tuple = params + (id,)
    db.query(sql, params)


def Insert(table, col, params: tuple):
    db = DBSingleton.Instance()
    insertion_pourcent_s = ""
    col_list = col.split(',')
    for _ in col_list:
        insertion_pourcent_s = insertion_pourcent_s + "%s,"
    insertion_pourcent_s = insertion_pourcent_s[:-1]
    sql = "INSERT INTO " + table + "(" + col + ")VALUES (" + insertion_pourcent_s + ")"
    db.query(sql, params)
