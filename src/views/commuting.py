#!/usr/bin/env python
# coding=utf-8

from views.decorators import speaks_json, allowed_post_only
from flask import request, current_app
from util.db import common_db as db
import json


class Commuting:
    def __init__(self, district):
        self.district = district
        self.return_data = {
            'title': 'Dojíždění za prací', 'data': [
                {'key': 'Přijíždějících', 'value': self.incoming},
                {'key': 'Odjíždějících', 'value': self.outgoing}
            ]
        }

    @property
    def incoming(self):
        with db(cursor=True) as cur:
            cur.execute('SELECT count FROM commuting WHERE `to` = ?', (self.district,))
            return cur.fetchone()

    @property
    def outgoing(self):
        with db(cursor=True) as cur:
            cur.execute('SELECT count FROM commuting WHERE `from` = ?', (self.district,))
            return cur.fetchone()


@speaks_json
@allowed_post_only
def commuting():
    """Vekove skupiny"""
    print(request.data)
    wanted_district = json.loads(request.data).get('district_code')
    current_app.logger.debug('wanted district: %s', wanted_district)
    return dict(data=Commuting(wanted_district).return_data)
