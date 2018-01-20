# -*- conding: utf-8 -*-
import sqlite3
from contextlib import closing
import config

with closing(sqlite3.connect(config.DB_NAME)) as conn:
	c = conn.cursor()

	create_table = '''CREATE TABLE GET_EXP (date DATE, exp INTEGER)'''

	c.execute(create_table)