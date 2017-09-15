# -*- coding: utf-8 -*-

import csv

YEAR = '2011'


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
    with open('data_sources/csu_obyvatelstvo/seznam_uzemi.CSV', 'r', encoding='cp1250') as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')

        header = next(reader)

        data = {
            'kraj': {},
            'okres': {},
            'obec': {}
        }

        # Aby jsem mohl sestavit promennou data, potrebuju jeste mit tabulku pro zarazeni okresu do kraju a
        # obci do okresu a kraju.
        data_connection = {

        }

        # Smicka pocita s tim, ze v souboru jsou nejdriv kraje, pak okresy a pak obce
        for item in reader:
            if item[1] == '100':
                # kraje
                data['kraj'][]
            elif item[1] == '101':
                # okresy
                pass
            elif item[1] == '43':
                # obce
                pass


def nationality():
    with open('data_sources/csu_obyvatelstvo/SLDB_OBYVATELSTVO.CSV', 'r', encoding='cp1250') as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')

        header = next(reader)

        types = [
            ('czech_male', header.index('vse4122')),
            ('czech_female', header.index('vse4123')),
            ('moravia_male', header.index('vse4132')),
            ('moravia_female', header.index('vse4133')),
            ('slez_male', header.index('vse4142')),
            ('slez_female', header.index('vse4143')),
            ('slovakia_male', header.index('vse4152')),
            ('slovakia_female', header.index('vse4153')),
            ('germany_male', header.index('vse4162')),
            ('germany_female', header.index('vse4163')),
            ('poland_male', header.index('vse4172')),
            ('poland_female', header.index('vse4173')),
            ('gipsy_male', header.index('vse4182')),
            ('gipsy_female', header.index('vse4183')),
            ('ukraine_male', header.index('vse4192')),
            ('ukraine_female', header.index('vse4193')),
            ('vietnam_male', header.index('vse41102')),
            ('vietnam_female', header.index('vse41103')),
            ('unknown_male', header.index('vse41112')),
            ('unwknown_female', header.index('vse41113')),
        ]

        for line in reader:
            if line[2] in ('43', '100', '101'):
                # Chceme pouze obec, okres a kraj
                print('{},{},{},{},{},{},{},{},{},{},{},{}'.format(
                    line[2],
                    line[3],
                    *[int(float(line[index])) for _, index in types]
                ))


def marital_status():
    with open('data_sources/csu_obyvatelstvo/SLDB_OBYVATELSTVO.CSV', 'r', encoding='cp1250') as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')

        header = next(reader)

        types = [
            ('single_male', header.index('vse1122')),
            ('single_female', header.index('vse1123')),

            ('maried_male', header.index('vse1132')),
            ('maried_female', header.index('vse1132')),

            ('divorced_male', header.index('vse4122')),
            ('divorced_female', header.index('vse4123')),

            ('widowed_male', header.index('vse4122')),
            ('widowed_female', header.index('vse4123')),
        ]

        for line in reader:
            if line[2] in ('43', '100', '101'):
                # Chceme pouze obec, okres a kraj
                print('{},{},{},{},{},{},{},{},{},{},{},{}'.format(
                    line[2],
                    line[3],
                    *[int(float(line[index])) for _, index in types]
                ))


def education():
    with open('data_sources/csu_obyvatelstvo/SLDB_OBYVATELSTVO.CSV', 'r', encoding='cp1250') as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')

        header = next(reader)

        types = [
            ('czech_male', header.index('vse4122')),
            ('czech_female', header.index('vse4123')),
            ('moravia_male', header.index('vse4132')),
            ('moravia_female', header.index('vse4133')),
            ('slez_male', header.index('vse4142')),
            ('slez_female', header.index('vse4143')),
            ('slovakia_male', header.index('vse4152')),
            ('slovakia_female', header.index('vse4153')),
            ('germany_male', header.index('vse4162')),
            ('germany_female', header.index('vse4163')),
            ('poland_male', header.index('vse4172')),
            ('poland_female', header.index('vse4173')),
            ('gipsy_male', header.index('vse4182')),
            ('gipsy_female', header.index('vse4183')),
            ('ukraine_male', header.index('vse4192')),
            ('ukraine_female', header.index('vse4193')),
            ('vietnam_male', header.index('vse41102')),
            ('vietnam_female', header.index('vse41103')),
            ('unknown_male', header.index('vse41112')),
            ('unwknown_female', header.index('vse41113')),
        ]

        for line in reader:
            if line[2] in ('43', '100', '101'):
                # Chceme pouze obec, okres a kraj
                print('{},{},{},{},{},{},{},{},{},{},{},{}'.format(
                    line[2],
                    line[3],
                    *[int(float(line[index])) for _, index in types]
                ))

