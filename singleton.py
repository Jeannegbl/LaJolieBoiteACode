import mysql.connector
from dotenv import load_dotenv


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
        self.conn = mysql.connector.connect(user='root', password='', host='localhost', database='lajolieboiteacode')
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


def Select(col, table,id):
    db = DBSingleton.Instance()
    liste = col.split(",")
    stringInsert = ""
    for colonne in liste:
        stringInsert = stringInsert + colonne+","
    stringInsert = stringInsert[:-1]
    sql = "SELECT " + stringInsert + " from " + table + " WHERE id=%s"
    params: tuple = (id,)
    db.query(sql, params)
    return db.result[0]


