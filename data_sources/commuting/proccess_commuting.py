#!/usr/bin/env python
# coding=utf-8

import pandas
import sqlite3
import sys

sys.path.insert(0, '..')

from csu101 import CSU_101_TO_RUIAN

intermediate_db = sqlite3.connect('processed.sqlite')

all_data: pandas.DataFrame = pandas.read_csv('source.csv')
wanted_columns: pandas.DataFrame = all_data.filter(items=['hodnota', 'uzemiz_kod', 'uzemido_kod'])
for index, uzemi in wanted_columns['uzemiz_kod'].iteritems():
    try:
        wanted_columns.set_value(index, 'uzemiz_kod', CSU_101_TO_RUIAN[uzemi])
    except KeyError:
        wanted_columns.drop(index, inplace=True)
for index, uzemi in wanted_columns['uzemido_kod'].iteritems():
    try:
        wanted_columns.set_value(index, 'uzemido_kod', CSU_101_TO_RUIAN[uzemi])
    except KeyError:
        wanted_columns.drop(index, inplace=True)

wanted_columns.rename(columns={'hodnota': 'count', 'uzemiz_kod': 'from', 'uzemido_kod': 'to'}, inplace=True)
wanted_columns.to_sql('commuting', intermediate_db, if_exists='replace')
