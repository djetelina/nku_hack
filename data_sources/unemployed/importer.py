# -*- coding utf-8 -*-

import os
import csv
from util import db

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


def run():
    with db.common_db() as con:
        cur = con.cursor()
        vacuum = "DROP TABLE unemployed"
        try:
            cur.execute(vacuum)
        except:
            pass

        create_table = """
        CREATE TABLE unemployed (
            municipality_id INT,
            year_ INT,
            month_ INT,
            type_ VARCHAR,
            value_ FLOAT,
            type_name VARCHAR,
            municipality_text VARCHAR
        );
        """
        cur.execute(create_table)
        con.commit()

    for fname in os.listdir(DATA_DIR):
        if fname not in (".", ".."):
            parse(DATA_DIR + fname)

    with db.common_db() as con:
        cur = con.cursor()
        cur.execute("VACUUM")


def parse(path):
    with db.common_db() as con:
        cur = con.cursor()
        query_prefix = "INSERT INTO unemployed VALUES (?, ?, ?, ?, ?, ?, ?)"

        values = []
        i = 0
        with open(path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader)
            for row in reader:
                i += 1
                values.append((
                    row[8],
                    row[5],
                    row[6],
                    row[2],
                    row[1],
                    row[3],
                    row[9]
                ))
                if i > 10000:
                    cur.executemany(query_prefix, values)
                    con.commit()
                    i = 0
                    values = []

            cur.executemany(query_prefix, values)
            con.commit()
