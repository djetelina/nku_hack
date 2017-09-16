# -*- coding utf-8 -*-

import os
import csv
from util import db
from typing import Dict, Tuple, List, Any

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


def run():
    with db.common_db() as con:
        cur = con.cursor()
        drop_table = "DROP TABLE unemployed"
        try:
            cur.execute(drop_table)
        except:
            pass

        create_table = """
        CREATE TABLE unemployed (
            municipality_id INT,
            year_ INT,
            month_ INT,
            type_ VARCHAR,
            value_ FLOAT,
            PRIMARY KEY (municipality_id, year_, month_, type_, value_)
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


def parse(path: str):
    with db.common_db() as con:
        cur = con.cursor()
        insert_query = "INSERT INTO unemployed VALUES (?, ?, ?, ?, ?)"

        values = []
        i = 0
        with open(path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader)
            for row in reader:
                i += 1
                values.append((
                    row[8],  # municipality_id
                    row[5],  # year_
                    row[6],  # month_
                    row[2],  # type_
                    row[1].replace(",", "."),  # value_
                ))
                if i > 10000:
                    cur.executemany(insert_query, values)
                    con.commit()
                    i = 0
                    values = []

            cur.executemany(insert_query, values)
            con.commit()
