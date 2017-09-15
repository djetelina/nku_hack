# -*- coding: utf-8 -*-

import csv
import sqlite3

YEAR = '2011'


def save_to_db(table_name, data, types, ruain_data):
    """
    Ulozi data do mezidatabaze, ze ktere si pak vytvorim dump a ten ulozim do repozitare.
    """
    connection = sqlite3.connect('{}.sqlite'.format(table_name))

    # Kraj
    connection.execute('''
      CREATE TABLE {}_kraj (ID region_id, ID metric_id, TEXT metric, INT year DEFAULT 2011, REAL value)
    '''.format(table_name))

    # Okres
    connection.execute('''
          CREATE TABLE {}_okres (ID region_id, ID district_id, TEXT metric_id, TEXT metric, INT year DEFAULT 2011, REAL value)
        '''.format(table_name))

    # Kraj
    connection.execute('''
          CREATE TABLE {}_obec (ID region_id, ID district_id, ID city_id, TEXT metric_id, TEXT metric, INT year DEFAULT 2011, REAL value)
        '''.format(table_name))


def load_ruian_data():
    """
    Nacte data z nasi lokalni RUIAN databaze aby jsme mohli nazvy prevest na idcka.
    """
    pass


def load_list_location():
    """
    Nacte obsah souboru seznam_uzemi.CSV pro pouziti.

    Jelikoz soubor obsahuje udaje pro vsechny uzemni celky, vytahnu si data pouze pro svoji potrebu:

    {
        kraj: {
            kod: text,
        },
        okres: {
            kod: [<kraj_nazev>, text]
        },
        obec: {
            kod: [<kraj_nazev>, <okres_nazev>, text]
        }
    }
    """
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

        data = {
            'kraj': {},
            'okres': {},
            'obec': {}
        }

        for item in reader:
            if item[1] == '100':
                # kraje
                region = data_connection['kraj'][item[2]]
                data['kraj'][region['id']] = region['nazev']
            elif item[1] == '101':
                # okresy
                district = data_connection['okres'][item[2]]
                region = data_connection['kraj'][district['kraj']]
                data['okres'][district['id']] = [region['id'], district['nazev']]
            elif item[1] == '43':
                # obce
                city = data_connection['obec'][item[2]]
                district = data_connection['okres'][city['okres']]
                region = data_connection['kraj'][district['kraj']]
                data['obec'][city['id']] = [region['id'], district['id'], city['nazev']]

        return data


def create_data(reader, types, list_locations):
    data = {
        'kraj': {},
        'okres': {},
        'obec': {}
    }

    for line in reader:
        # Chceme pouze obec, okres a kraj
        if line[2] in ('43', '100', '101'):
            # Ziskame si ze radku vsechna uzitecna data
            line_data = [int(float(line[index])) for _, index in types]
            if line[2] == '100':
                # kraje
                location = list_locations['kraj'][line[3]]
                data['kraj'][line[3]] = {
                    'nazev': location,
                    'data': line_data
                }
            elif line[1] == '101':
                # okresy
                location = list_locations['okres'][line[3]]
                data['okres'][line[3]] = {
                    'kraj': location[0],
                    'nazev': location[1],
                    'data': line_data
                }
            elif line[1] == '43':
                # obce
                location = list_locations['obec'][line[3]]
                data['okres'][line[3]] = {
                    'kraj': location[0],
                    'okres': location[1],
                    'nazev': location[2],
                    'data': line_data
                }

    return data


def nationality(list_locations):
    with open('data_sources/csu_obyvatelstvo/SLDB_OBYVATELSTVO.CSV', 'r', encoding='cp1250') as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')

        header = next(reader)

        types = [
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

        data = create_data(reader, types, list_locations)

        return data


def marital_status(list_locations):
    with open('data_sources/csu_obyvatelstvo/SLDB_OBYVATELSTVO.CSV', 'r', encoding='cp1250') as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')

        header = next(reader)

        types = [
            ('single', header.index('vse1121'), 'Svobodní'),
            ('maried', header.index('vse1131'), 'Ženatí'),
            ('divorced', header.index('vse4121'), 'Rozvedení'),
            ('widowed', header.index('vse4121'), 'Ovdovělí'),
        ]

        data = create_data(reader, types, list_locations)
        return data


def education(list_locations):
    with open('data_sources/csu_obyvatelstvo/SLDB_OBYVATELSTVO.CSV', 'r', encoding='cp1250') as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')

        header = next(reader)

        types = [
            ('base', header.index('vse2131'), 'Základní'),
            ('apprenticeship', header.index('vse2141'), 'Vyučení'),
            ('high', header.index('vse2151'), 'Středoškolské'),
            ('extension', header.index('vse2161'), 'Nástavbové'),
            ('higherprofessional', header.index('vse2171'), 'Vyšší odborné'),
            ('university', header.index('vse2181'), 'Vysokoškolské'),
        ]

        data = create_data(reader, types, list_locations)

        return data


if __name__ == '__main__':
    locations_list = load_list_location()
    nationality_data = nationality(locations_list)
