#!/usr/bin/env python
# coding=utf-8
"""Zachovat ciste :)"""

from flask import Flask, logging

from views.common import bp_common
from views.api import bp_api

app = Flask(__name__)
# sorry kluci,ale me se ty cirkularni import proste nelibi, takze blueprinty :)
app.register_blueprint(bp_common)
app.register_blueprint(bp_api)
app.config.from_pyfile('config.py')

# ohack pro log co tolik nespammuje, posledni stable (0.12) to ma jeste osklive...
# http://flask.pocoo.org/docs/dev/logging/ - the dream!
setattr(logging, 'DEBUG_LOG_FORMAT', '[%(asctime)s] %(levelname)s in %(module)s: %(message)s')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
