import os
import sqlite3

import pandas as pd
from loguru import logger

BASE_PATH = os.curdir


class SQLInterface:
    def __init__(self, db_str=os.path.join(BASE_PATH, "db", "linq_db.db")) -> None:
        try:
            self.conn = sqlite3.connect(db_str)
            self.cur = self.conn.cursor()
            logger.success("SQL connection established")
        except:
            logger.error("SQL Connection failed")

    def new_table(self):
        self.conn.execute("CREATE TABLE test_table(tgID int, tbUsername varchar(255));")

    def insert_entry(self):
        self.conn.execute(
            "INSERT INTO test_table (tgID, tbUsername) VALUES (234, 'NathanBrowne');"
        )
        self.conn.commit()

    def available_tables(self):
        self.cur.execute('SELECT name from sqlite_master where type= "table"')
        return [x[0] for x in self.cur.fetchall()]

    def get_result(self, table):
        return pd.read_sql_query("SELECT * FROM {};".format(table), self.conn)

    def df_to_table(self, df, name, **kwargs):
        if name in self.available_tables():
            print("here")
            self.conn.execute("DROP TABLE {};".format(name))

        df.to_sql(name=name, con=self.conn, index=False, **kwargs)
