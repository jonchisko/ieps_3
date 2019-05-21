import sqlite3

class Database:

    def __init__(self, dbName):
        self.dbName = dbName

    def setup(self):
        with sqlite3.connect(self.dbName) as conn:
            conn.executescript("""CREATE TABLE IndexWord (
                                  word TEXT PRIMARY KEY
                             );"""
                         )

            conn.commit()

            conn.executescript("""CREATE TABLE Posting (
                                  word TEXT NOT NULL,
                                  documentName TEXT NOT NULL,
                                  frequency INTEGER NOT NULL,
                                  indexes TEXT NOT NULL,
                                  PRIMARY KEY(word, documentName),
                                  FOREIGN KEY (word) REFERENCES IndexWord(word)
                             );""")

            conn.commit()

    def get(self, table, columns='*', conditions = ""):
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()

        query = "SELECT {} FROM {} ".format(columns, table) + conditions + ";"
        cursor.execute(query)

        table = cursor.fetchall()

        return table

    # content of form {key1: [val10, val11, ..., val1N], key2: [val20, val21, ... val2N], ...}
    def insert(self, table, content:dict):
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()

        keys = list(content.keys())
        base = "INSERT INTO {} {} VALUES ".format(table, "(" + ",".join([key for key in keys]) + ")")

        vals = []
        for i in range(len(content[keys[0]])):
            values = str(tuple([content[key][i] if isinstance(content[key][i], str) else content[key][i] for key in keys]))
            if values[-2] == ',':
                values = values[:-2] + ')'

            vals.append(values)
            if i%5000 == 0:
                query = base + ','.join(vals)

                try:
                    cursor.execute(query)
                    conn.commit()
                except:
                    print(query)

                vals = []


        query = base + ','.join(vals)
        try:
            cursor.execute(query)
            conn.commit()
        except:
            print(query)

        cursor.close()
        conn.close()

