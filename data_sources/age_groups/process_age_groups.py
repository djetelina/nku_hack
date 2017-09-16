#!/usr/bin/env python
# coding=utf-8
"""
Zpracuje datovou sadu CSU - obyvatelstvo podle pětiletých věkových skupin

Spousti se v tomto adresari, je potreba mit sadu zkopirovanou do teto slozky a pojmenovanou source.csv

Vyslednou databazi processed.sqlite je potreba manualne dumpnout, pridat create, begin transaction a commit, zagzipovat
a vlozit do slozky dump

Pri uprave pozor, Praha je vedena jako obec ale plati i pro okres

TODO pouzit csu101.py - poucit se z pozdeji upravene sady commmuting
"""

import pandas
import sqlite3
from typing import Union


def find_distr_id(district: str) -> Union[int, bool]:
    """Prevede nazev okresu podle stringu CSU na ruian, pokud neni okres, vrati False"""
    with ruian as r_conn:
        r_cur = r_conn.cursor()
        r_cur.execute('SELECT kod FROM okresy WHERE ? = nazev', (district,))
        resp = r_cur.fetchone()
        return resp[0] if resp else False


# vytvorime pripojeni na ruian databazi
ruian: sqlite3.Connection = sqlite3.connect('../../db/ruian.sqlite')
# Vytvorime pripojeni na mezidatabazi
intermediate_db: sqlite3.Connection = sqlite3.connect('processed.sqlite')

# Precteme csv
all_data: pandas.DataFrame = pandas.read_csv('source.csv')
# Vyfiltrujeme si sloupce, se kterymi budeme pracovat - TODO tady mozna neco prebyva, Praha udelala trosku bordel
wanted_columns: pandas.DataFrame = all_data.filter(items=['hodnota', 'vuzemi_cis', 'casref_do', 'pohlavi_txt', 'vek_txt', 'vuzemi_txt'])
# Odfiltrujeme si jen posledni rok (v tomto pripade 2016), pokud bychom chteli historicka data v db, tento krok preskocime
this_year: pandas.DataFrame = wanted_columns[wanted_columns['casref_do'].str.contains("2016")]
# Vyfiltrujeme si sloupce ktere posleme do databaze
out_data: pandas.DataFrame = this_year.filter(items=['hodnota', 'pohlavi_txt', 'vek_txt', 'vuzemi_txt'])
# Prejmenujeme sloupce
out_data.rename(columns={'hodnota': 'count', 'pohlavi_txt': 'gender', 'vek_txt': 'age_start', 'vuzemi_txt': 'district'}, inplace=True)
# Pres regex si z textoveho vekoveho rozhrani vezmeme zacatek vekoveho rozhrani - dal by se pouzit ciselnik, priste...
out_data['age_start'].replace({r'O*d* *([0-9]{1,2}).*': r'\1'}, regex=True, inplace=True)
# Prevedeme si pohlavi na m(ale)/f(emale)/a(all) namisto ceskych nazvu a None
out_data['gender'].replace({'muž': 'm', 'žena': 'f', None: 'a'}, inplace=True)
# Posleme data do databaze
out_data.to_sql('age_groups', intermediate_db, if_exists='replace')

# Nad databazi jeste budeme pracovat
with intermediate_db as conn:
    cur = conn.cursor()
    # Vybereme si vsechny mozne okrsky
    all = cur.execute('SELECT DISTINCT district FROM age_groups').fetchall()
    for row in all:
        distr = row[0]
        # Najdeme si ruian id okrsku
        ruian_id = find_distr_id(distr)
        # Pokud je je id okrsek, vymenime string za id (ale sqlite -> zustane sloupec stringoyvy
        if ruian_id:
            cur.execute('UPDATE age_groups SET district=? WHERE district=?', (ruian_id, distr))
        # Pokud jsme id nenamatchovali na okrskove, smazeme "okrsek" ktery neni okrsek
        else:
            cur.execute('DELETE FROM age_groups WHERE district=?', (distr,))
        conn.commit()
