#!/usr/bin/env python
# coding=utf-8


import os


DEBUG = True
SECRET_KEY = 'nkuhacksznway'
DATA_PATH = os.path.dirname(os.path.realpath(__file__)) + "/../db/"

RUIAN_PATH = DATA_PATH + "ruian.sqlite"
DB_PATH = DATA_PATH + "db.sqlite"
