# -*- coding utf-8 -*-

import os
import csv
from src.util import db

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


def run():
    with db.ruian_db() as ruian:
        ruian.cursor()
        """
        CREATE TABLE unemployed IF NOT EXISTS (
            municipality_id INT,
            year INT,
            month INT,
            type VARCHAR
        )
        """

    for fname in os.listdir(DATA_DIR):
        if fname not in (".", ".."):
            print(fname)
            parse(DATA_DIR + fname)


def parse(path):
    with db.ruian_db() as ruian:
        cur = ruian.cursor()
        query_prefix = """INSERT INTO unemployed VALUES """
        values = []
        with open(path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader)
            for row in reader:
                values.append((
                    row[1]
                ))


