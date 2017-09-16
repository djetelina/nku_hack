# -*- encoding: utf-8 -*-

# Data CSU pro volby. Cislenik politickych stran.

import csv

with open('CIS_1071.csv', 'r') as f:
    reader = csv.reader(f, delimiter=';', quotechar='\"')

    header = next(reader)

    data = {}
    for item in reader:
        print('\'{}\': \'{}\','.format(item[2], item[3]))
