#!/usr/bin/env python
# coding=utf-8
"""
Zpracuje datovou sadu CSU - dojíždění do zaměstnání mezi okresy

Spousti se v tomto adresari, je potreba mit sadu zkopirovanou do teto slozky a pojmenovanou source.csv

Vyslednou databazi processed.sqlite je potreba manualne dumpnout, pridat create, begin transaction a commit, zagzipovat
a vlozit do slozky dump

Pri uprave pozor, viz if uzemi == 3018
"""

import pandas
import sqlite3
import sys

sys.path.insert(0, '..')

from csu101 import CSU_101_TO_RUIAN

# Vytvorime si pripojeni na vyslednou databazi
intermediate_db = sqlite3.connect('processed.sqlite')

# Nahrajeme si datovou sadu z csv
all_data: pandas.DataFrame = pandas.read_csv('source.csv')
# Vyfiltrujeme si sloupce ktere nas zajimaji
wanted_columns: pandas.DataFrame = all_data.filter(items=['hodnota', 'uzemiz_kod', 'uzemido_kod'])
to_convert = ('uzemiz_kod', 'uzemido_kod')
# Pro oba sloupce od a z udelame stejnou upravu - prevedeme na ruian id z csu id
for item in to_convert:
    # Projdeme vsechny radky
    for index, uzemi in wanted_columns[item].iteritems():
        # Zkusime podle konvertoru csu101.py prevest na ruian id
        try:
            wanted_columns.set_value(index, item, CSU_101_TO_RUIAN[uzemi])
        except KeyError:
            # Narazili jsme na prahu, takze manualne, protoze CSU proste Prahu ja okrsek nikdy nevyexportuje
            if uzemi == 3018:
                wanted_columns.set_value(index, item, 3100)
            # Uzemi neni okrsek, nezajima nas
            else:
                wanted_columns.drop(index, inplace=True)

# Hezky prejmenujeme sloupce
wanted_columns.rename(columns={'hodnota': 'count', 'uzemiz_kod': 'from', 'uzemido_kod': 'to'}, inplace=True)
# Vytvotrime vyslednou tabulku
wanted_columns.to_sql('commuting', intermediate_db, if_exists='replace')
