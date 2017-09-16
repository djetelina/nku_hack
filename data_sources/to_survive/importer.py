# -*- coding utf-8 -*-

import os
import csv
from util import db

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


def run():
    with db.common_db() as con:
        cur = con.cursor()
        drop_table = "DROP TABLE to_survive"
        try:
            cur.execute(drop_table)
        except:
            pass

        create_table = """
        CREATE TABLE to_survive (
            region_id INT,
            district_id INT,
            year_code VARCHAR,
            sex INT,
            value_ FLOAT,
            PRIMARY KEY (region_id, district_id, year_code, sex, value_)
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
    """
    Naliti dat z

    :param path:
    :return:
    """
    region_district_query = "SELECT vusc_kod, kod FROM okresy WHERE nazev = ?"
    insert_query = "INSERT INTO to_survive VALUES (?, ?, ?, ?, ?)"

    with db.ruian_db(True) as ruian_cur:
        with db.common_db() as con:
            cur = con.cursor()

            values = []
            i = 0
            with open(path, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                next(reader)
                for row in reader:
                    i += 1
                    if int(row[7]) == 101:
                        # hnusny hack :-)
                        if row[14] == "Praha":
                            row[14] = "Hlavní město Praha"

                        ruian_cur.execute(region_district_query, (row[14],))
                        ruian_response = [dict(item) for item in ruian_cur.fetchall()]
                        ruian_row = ruian_response[0]

                        values.append((
                            ruian_row['vusc_kod'],  # region_id
                            ruian_row['kod'],  # district_id
                            row[6],  # year_code
                            row[4],  # sex
                            row[1].replace(",", "."),  # value_
                        ))
                        if i > 10000:
                            cur.executemany(insert_query, values)
                            con.commit()
                            i = 0
                            values = []

                cur.executemany(insert_query, values)
                con.commit()
