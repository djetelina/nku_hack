# -*- coding: utf-8 -*-

import csv
import os
import gzip
from util import db
import re

YEAR = '2011'
SOURCE_FILE = 'data_sources/population/SLDB_OBYVATELSTVO.CSV'
DUMP_NAME = 'csu_population'

# Aby jsem mohl naparovat data, musim provest i rucni upravy.
FIXES = {
    'obec': {'dolany': 'dolany nad vltavou'}
}


def load_ruian():
    """
    Nacte data z RUIAN pro potreby doplneni dat.

    Vraci data ve formatu:

        {
            'kraj': {
                <kraj_nazev>: <kod>
            },
            'okres': {
                <okres_nazev>,<kraj_nazev>: [<okres_kod>, <kraj_kod>]
            },
            'obec': {
                <obec_nazev>,<okres_nazev>,<kraj_nazev>: [<obec_kod>, <okres_kod>, <kraj_kod>]
            }
        }
    """
    with db.ruian_db() as connection:
        cursor = connection.cursor()

        data = cursor.execute('''
SELECT
  obce.kod, obce.nazev, okresy.kod, okresy.nazev, vusc.kod, vusc.nazev
FROM
  obce
JOIN
  okresy ON okresy.kod=obce.okres_kod
JOIN
  vusc ON vusc.kod=okresy.vusc_kod;
''')

        ruian_data = {
            'kraj': {},
            'okres': {},
            'obec': {}
        }

        for item in data:
            ruian_data['kraj'][item[5].lower()] = item[4]
            ruian_data['okres']['{},{}'.format(item[3], item[5]).lower()] = [item[2], item[4]]
            ruian_data['obec']['{},{},{}'.format(item[1], item[3], item[5]).lower()] = [item[0], item[2], item[4]]

    return ruian_data


def save_to_dump(table_name, data, metrics):
    """
    Ulozi data do dumpu.
    """
    print('Ukládám do DB.')
    gzf = gzip.GzipFile(os.path.join('dump', '{}.sql.gz'.format(table_name)), "w", compresslevel=9)

    gzf.write(bytes('PRAGMA foreign_keys = OFF;\n', 'utf-8'))
    gzf.write(bytes('BEGIN TRANSACTION;\n', 'utf-8'))

    # Kraj
    gzf.write(bytes('''CREATE TABLE {}_kraj (region_id INT, metric_id INT, metric TEXT, year INT DEFAULT 2011, value REAL);\n'''.format(table_name), 'utf-8'))

    for region_id, values in data['kraj'].items():
        for index, item in enumerate(values['data']):
            metric = metrics[index]
            gzf.write(bytes('''INSERT INTO {}_kraj (region_id, metric_id, metric, value) VALUES ('{}', '{}', '{}', '{}');\n'''.format(
                table_name, region_id, metric[0], metric[2], item
            ), 'utf-8'))

    # Okres
    gzf.write(bytes('''CREATE TABLE {}_okres (region_id INT, district_id INT, metric_id TEXT, metric TEXT, year INT DEFAULT 2011, value REAL);\n'''.format(table_name), 'utf-8'))

    for district_id, values in data['okres'].items():
        for index, item in enumerate(values['data']):
            metric = metrics[index]
            gzf.write(bytes('''INSERT INTO {}_okres (region_id, district_id, metric_id, metric, value) VALUES ('{}', '{}', '{}', '{}', '{}');\n'''.format(
                table_name, values['kraj'], district_id, metric[0], metric[2], item
            ), 'utf-8'))

    # Obec
    gzf.write(bytes('''CREATE TABLE {}_obec (region_id INT, district_id INT, city_id INT, metric_id TEXT, metric TEXT, year INT DEFAULT 2011, value REAL);\n'''.format(table_name), 'utf-8'))

    for city_id, values in data['obec'].items():
        for index, item in enumerate(values['data']):
            metric = metrics[index]
            gzf.write(bytes('''INSERT INTO {}_obec (region_id, district_id, city_id, metric_id, metric, value) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');\n'''.format(
                table_name, values['kraj'], values['okres'], city_id, metric[0], metric[2], item
            ), 'utf-8'))

    gzf.write(bytes('COMMIT;\n', 'utf-8'))


def load_list_location():
    """
    Nacte obsah souboru seznam_uzemi.CSV pro pouziti.

    Jelikoz soubor obsahuje udaje pro vsechny uzemni celky, vytahnu si data pouze pro svoji potrebu:

    {
        kraj: {
            kod: text,
        },
        okres: {
            kod: [<kraj_kod>, text]
        },
        obec: {
            kod: [<kraj_kod>, <okres_kod>, text]
        }
    }
    """
    print('Načítám seznamy území.')
    with open('data_sources/population/seznam_uzemi.CSV', 'r', encoding='cp1250') as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')

        header = next(reader)

        # Aby jsem mohl sestavit promennou data, potrebuju jeste mit tabulku pro zarazeni okresu do kraju a
        # obci do okresu a kraju.
        data_connection = {
            'kraj': {},
            'okres': {},
            'obec': {}
        }

        # Smycka pocita s tim, ze v souboru jsou nejdriv kraje, pak okresy a pak obce
        for item in reader:
            if item[1] == '100':
                # kraje
                data_connection['kraj'][item[0]] = {
                    'id': item[2],
                    'nazev': item[4]
                }
            elif item[1] == '101':
                # okresy
                data_connection['okres'][item[0]] = {
                    'id': item[2],
                    'nazev': item[4],
                    'kraj': item[8]
                }
            elif item[1] == '43':
                # obce
                data_connection['obec'][item[0]] = {
                    'id': item[2],
                    'nazev': item[4],
                    'okres': item[7]
                }

    with open('data_sources/population/seznam_uzemi.CSV', 'r', encoding='cp1250') as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')

        header = next(reader)

        data = {
            'kraj': {},
            'okres': {},
            'obec': {}
        }

        for item in reader:
            if item[1] == '100':
                # kraje
                region = data_connection['kraj'][item[0]]
                data['kraj'][region['id']] = region['nazev'].lower()
            elif item[1] == '101':
                # okresy
                district = data_connection['okres'][item[0]]
                region = data_connection['kraj'][district['kraj']]
                data['okres'][district['id']] = [region['id'], region['nazev'].lower(), district['nazev'].lower()]
            elif item[1] == '43':
                # obce
                city = data_connection['obec'][item[0]]
                district = data_connection['okres'][city['okres']]
                region = data_connection['kraj'][district['kraj']]
                if '(dříve okres' in city['nazev']:
                    # Chci odstranit text (drive okres ...)
                    city['nazev'] = re.sub(r'\s+\(.+\)$', '', city['nazev'], flags=re.DOTALL)
                data['obec'][city['id']] = [region['id'], district['id'], region['nazev'].lower(), district['nazev'].lower(), city['nazev'].lower()]
        return data


def create_data(reader, metrics, list_locations, ruian_data):
    """
    Vytvori data pro ulozeni do dumpu. IDcka lokalit se zde upravuji z CSU na RUIAN aby jsme v datech mohli hledat.
    :param reader:
    :param metrics:
    :param list_locations:
    :param ruian_data:
    :return:
    """
    print('vytvářím data pro uložení do DB.')
    data = {
        'kraj': {},
        'okres': {},
        'obec': {}
    }

    for line in reader:
        # Chceme pouze obec, okres a kraj
        if line[2] in ('43', '100', '101'):
            # Ziskame si ze radku vsechna uzitecna data
            line_data = [int(float(line[index])) for _ignore1, index, _ignore2 in metrics]
            if line[2] == '100':
                # Kraj
                kraj_id = ruian_data['kraj'][list_locations['kraj'][line[3]].lower()]
                data['kraj'][kraj_id] = {
                    'data': line_data
                }
            elif line[2] == '101':
                # Okres
                location = list_locations['okres'][line[3]]
                okres_id, kraj_id = ruian_data['okres']['{},{}'.format(location[2], location[1]).lower()]
                data['okres'][okres_id] = {
                    'kraj': kraj_id,
                    'data': line_data
                }
            elif line[2] == '43':
                # obce
                location = list_locations['obec'][line[3]]
                try:
                    obec_id, okres_id, kraj_id = ruian_data['obec']['{},{},{}'.format(location[4], location[3], location[2]).lower()]
                except KeyError:
                    try:
                        obec_id, okres_id, kraj_id = ruian_data['obec']['{},{},{}'.format(FIXES['obec'][location[4]], location[3], location[2]).lower()]
                    except KeyError:
                        print('Nenalezeno: {}'.format('{},{},{}'.format(location[4], location[3], location[2]).lower()))
                        continue
                data['obec'][obec_id] = {
                    'kraj': kraj_id,
                    'okres': okres_id,
                    'data': line_data
                }

    return data


def nationality(list_locations, ruian_data):
    print('Zpracovávám národnost.')
    with open(SOURCE_FILE, 'r', encoding='cp1250') as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')

        header = next(reader)

        metrics = [
            ('czech', header.index('vse4121'), 'Česká'),
            ('moravia', header.index('vse4131'), 'Moravská'),
            ('slez', header.index('vse4141'), 'Slezská'),
            ('slovakia', header.index('vse4151'), 'Slovenská'),
            ('germany', header.index('vse4161'), 'Německá'),
            ('poland', header.index('vse4171'), 'Polská'),
            ('gipsy', header.index('vse4181'), 'Romská'),
            ('ukraine', header.index('vse4191'), 'Ukrajinská'),
            ('vietnam', header.index('vse41101'), 'Vietnamská'),
            ('unknown', header.index('vse41111'), 'Neuvedená'),
        ]

        data = create_data(reader, metrics, list_locations, ruian_data)
        save_to_dump('nationality', data, metrics)


def marital_status(list_locations, ruian_data):
    print('Zpracovávám rodinný stav')
    with open(SOURCE_FILE, 'r', encoding='cp1250') as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')

        header = next(reader)

        metrics = [
            ('single', header.index('vse1121'), 'Svobodné/í'),
            ('maried', header.index('vse1131'), 'Ženatí/Vdané'),
            ('divorced', header.index('vse4121'), 'Rozvedené/í'),
            ('widowed', header.index('vse4121'), 'Ovdovělé/í'),
        ]

        data = create_data(reader, metrics, list_locations, ruian_data)
        save_to_dump('marital_status', data, metrics)


def education(list_locations, ruian_data):
    print('Zpracovávám vzdělání')
    with open(SOURCE_FILE, 'r', encoding='cp1250') as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')

        header = next(reader)

        metrics = [
            ('base', header.index('vse2131'), 'Základní'),
            ('apprenticeship', header.index('vse2141'), 'Vyučení'),
            ('high', header.index('vse2151'), 'Středoškolské'),
            ('extension', header.index('vse2161'), 'Nástavbové'),
            ('higherprofessional', header.index('vse2171'), 'Vyšší odborné'),
            ('university', header.index('vse2181'), 'Vysokoškolské'),
        ]

        data = create_data(reader, metrics, list_locations, ruian_data)
        save_to_dump('education', data, metrics)


def main():
    locations_list = load_list_location()
    ruian_data = load_ruian()
    nationality(locations_list, ruian_data)
    marital_status(locations_list, ruian_data)
    education(locations_list, ruian_data)


if __name__ == '__main__':
    main()
