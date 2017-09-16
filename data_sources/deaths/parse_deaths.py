# -*- encoding: utf-8 -*-
import csv
import os
import pickle
import gzip
from typing import Dict, Tuple, List, Any

from data_sources.csu101 import CSU_101_TO_RUIAN


SOURCE_FILE = "raw_data/zemreli.csv"
TMP_FILE = "raw_data/zemreli.pickle"
YEARS = ['2015']

DEST_FILE = "dump/deaths.sql.gz"

TABLE_SQL = """
    BEGIN;
    CREATE TABLE death_cause 
    (
      sex boolean,
      year int,
      district_id int,
      cause_id varchar(3),
      value int
    );
    CREATE INDEX death_cause_compound_idx ON death_cause(district_id, year, sex);
"""


def read_data(path: str) -> Tuple[List, List]:
    """
    precte data ze souboru a udela z toho list dictu.
    :param path:
    :return:
    """
    records = []
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        headers = None
        for row in reader:

            # preskocime jiny nez vybrany rok, kumulovana pohlavi, nebo bez priciny
            if headers and (row[9] not in YEARS or row[4] == '' or row[5] == '' or row[7] != '101'):
                continue

            # Ulozim hlavicku
            if not headers:
                headers = row
                continue

            records.append(row)

    return headers, records


def temp_or_calculate(fname: str, function):
    """
    vrati data z picklu, nebo je spocita, kdyz nejsou
    :param fname:
    :param function:
    :return:
    """
    if os.path.isfile(fname):
        return pickle.load(open(fname, "rb"))
    else:
        dta = function()
        pickle.dump(dta, open(fname, 'wb'))
        return dta


def parse_file(path: str) -> None:
    """
    zpracuje soubor.
    :param path: cesta k souboru.
    :return:
    """

    records = read_data(path)

    headers, data = records
    gzf = gzip.GzipFile(DEST_FILE, "w", compresslevel=9)
    gzf.write(bytes(TABLE_SQL, 'utf-8'))

    for i in data:
        int_district = int(i[8])
        ruian_district = CSU_101_TO_RUIAN[int_district]
        sex = 1 if i[4] == '1' else 0  # Predelame cisselnik pohlavi na spravne hodnoty :-)
        year = int(i[9])
        code = i[6]
        value = int(i[1])
        gzf.write(bytes("INSERT INTO death_cause VALUES ({}, {}, {}, '{}', {});\n".format(
            sex, year, ruian_district, code, value
        ), 'utf-8'))
    gzf.write(b"COMMIT;\n")
    gzf.flush()
    gzf.close()


if __name__ == '__main__':
    parse_file(SOURCE_FILE)

