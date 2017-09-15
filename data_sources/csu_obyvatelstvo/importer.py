# -*- coding: utf-8 -*-

import csv
from util import db

YEAR = '2011'
SOURCE_FILE = 'data_sources/csu_obyvatelstvo/SLDB_OBYVATELSTVO.CSV'


def save_to_db(table_name, data, metrics):
    """
    Ulozi data do mezidatabaze, ze ktere si pak vytvorim dump a ten ulozim do repozitare.
    """
    print('Ukládám do DB.')
    with db.common_db() as connection:
        cursor = connection.cursor()

        # Kraj
        cursor.execute('''DROP TABLE IF EXISTS {}_kraj'''.format(table_name))
        cursor.execute('''
          CREATE TABLE {}_kraj (region_id INT, metric_id INT, metric TEXT, year INT DEFAULT 2011, value REAL)
        '''.format(table_name))

        query_values = []
        for region_id, values in data['kraj'].items():
            for index, item in enumerate(values['data']):
                metric = metrics[index]
                query_values.append((region_id, metric[0], metric[2], item))
        cursor.executemany(
            '''INSERT INTO {}_kraj (region_id, metric_id, metric, value) VALUES (?, ?, ?, ?)'''.format(table_name),
            query_values
        )

        # Okres
        cursor.execute('''DROP TABLE IF EXISTS {}_okres'''.format(table_name))
        cursor.execute('''
              CREATE TABLE {}_okres (region_id INT, district_id INT, metric_id TEXT, metric TEXT, year INT DEFAULT 2011, value REAL)
            '''.format(table_name))

        query_values = []
        for district_id, values in data['okres'].items():
            for index, item in enumerate(values['data']):
                metric = metrics[index]
                query_values.append((values['kraj'], district_id, metric[0], metric[2], item))
        cursor.executemany(
            '''INSERT INTO {}_okres (region_id, district_id, metric_id, metric, value) VALUES (?, ?, ?, ?, ?)'''.format(table_name),
            query_values
        )

        # Obec
        cursor.execute('''DROP TABLE IF EXISTS {}_obec'''.format(table_name))
        cursor.execute('''
              CREATE TABLE {}_obec (region_id INT, district_id INT, city_id INT, metric_id TEXT, metric TEXT, year INT DEFAULT 2011, value REAL)
            '''.format(table_name))

        query_values = []
        for city_id, values in data['obec'].items():
            for index, item in enumerate(values['data']):
                metric = metrics[index]
                query_values.append((values['kraj'], values['okres'], city_id, metric[0], metric[2], item))
        cursor.executemany(
            '''INSERT INTO {}_obec (region_id, district_id, city_id, metric_id, metric, value) VALUES (?, ?, ?, ?, ?, ?)'''.format(table_name),
            query_values
        )

        connection.commit()

    # Vycistim data. Nelze delat v ramci transakce.
    with db.common_db() as connection:
        cursor = connection.cursor()
        cursor.execute("VACUUM")


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
    with open('data_sources/csu_obyvatelstvo/seznam_uzemi.CSV', 'r', encoding='cp1250') as f:
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

    with open('data_sources/csu_obyvatelstvo/seznam_uzemi.CSV', 'r', encoding='cp1250') as f:
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
                data['kraj'][region['id']] = region['nazev']
            elif item[1] == '101':
                # okresy
                district = data_connection['okres'][item[0]]
                region = data_connection['kraj'][district['kraj']]
                data['okres'][district['id']] = [region['id'], district['nazev']]
            elif item[1] == '43':
                # obce
                city = data_connection['obec'][item[0]]
                district = data_connection['okres'][city['okres']]
                region = data_connection['kraj'][district['kraj']]
                data['obec'][city['id']] = [region['id'], district['id'], city['nazev']]
        return data


def create_data(reader, metrics, list_locations):
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
                # kraje
                data['kraj'][line[3]] = {
                    'data': line_data
                }
            elif line[2] == '101':
                # okresy
                location = list_locations['okres'][line[3]]
                data['okres'][line[3]] = {
                    'kraj': location[0],
                    'data': line_data
                }
            elif line[2] == '43':
                # obce
                location = list_locations['obec'][line[3]]
                data['obec'][line[3]] = {
                    'kraj': location[0],
                    'okres': location[1],
                    'data': line_data
                }

    return data


def nationality(list_locations):
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

        data = create_data(reader, metrics, list_locations)
        save_to_db('nationality', data, metrics)


def marital_status(list_locations):
    print('Zpracovávám rodinný stav')
    with open(SOURCE_FILE, 'r', encoding='cp1250') as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')

        header = next(reader)

        metrics = [
            ('single', header.index('vse1121'), 'Svobodní'),
            ('maried', header.index('vse1131'), 'Ženatí'),
            ('divorced', header.index('vse4121'), 'Rozvedení'),
            ('widowed', header.index('vse4121'), 'Ovdovělí'),
        ]

        data = create_data(reader, metrics, list_locations)
        save_to_db('marital_status', data, metrics)


def education(list_locations):
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

        data = create_data(reader, metrics, list_locations)
        save_to_db('education', data, metrics)


def main():
    locations_list = load_list_location()
    nationality(locations_list)
    marital_status(locations_list)
    education(locations_list)


if __name__ == '__main__':
    main()
