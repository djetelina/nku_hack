#!/usr/bin/env python
# coding=utf-8

import pandas
import sqlite3


def find_distr_id(district):
    with ruian as r_conn:
        r_cur = r_conn.cursor()
        r_cur.execute('SELECT kod FROM okresy WHERE ? = nazev', (district,))
        return r_cur.fetchone()[0]


ruian = sqlite3.connect('../../db/ruian.sqlite')
intermediate_db = sqlite3.connect('processed.sqlite')

all_data: pandas.DataFrame = pandas.read_csv('source.csv')
wanted_columns: pandas.DataFrame = all_data.filter(items=['hodnota', 'vuzemi_cis', 'casref_do', 'pohlavi_txt', 'vek_txt', 'vuzemi_txt'])
this_year: pandas.Series = wanted_columns[wanted_columns['casref_do'].str.contains("2016")]
district: pandas.Series = this_year[this_year.vuzemi_cis == 101]
out_data: pandas.Series = district.filter(items=['hodnota', 'pohlavi_txt', 'vek_txt', 'vuzemi_txt'])
out_data.rename(columns={'hodnota': 'count', 'pohlavi_txt': 'gender', 'vek_txt': 'age_start', 'vuzemi_txt': 'district'}, inplace=True)
out_data['age_start'].replace({r'O*d* *([0-9]{1,2}).*': r'\1'}, regex=True, inplace=True)
out_data['gender'].replace({'muž': 'm', 'žena': 'f', None: 'a'}, inplace=True)
out_data.to_sql('age_groups', intermediate_db, if_exists='replace')


with intermediate_db as conn:
    cur = conn.cursor()
    all = cur.execute('SELECT DISTINCT district FROM age_groups').fetchall()
    for row in all:
        distr = row[0]
        ruian_id = find_distr_id(distr)
        print(distr, ruian_id)
        cur.execute('UPDATE age_groups SET district=? WHERE district=?', (ruian_id, distr))
