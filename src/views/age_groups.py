#!/usr/bin/env python
# coding=utf-8
from views.decorators import speaks_json
from flask import request, current_app
from util.db import common_db as db
from typing import Dict, Union, List
import sqlite3


return_dict_type = Dict[str, Union[str, List[Dict[str, Union[str, int]]]]]


class AgeGroup:
    def __init__(self, district, gender='a'):
        self.district = str(district)
        self.gender: str = gender
        self._db_data: List[sqlite3.Row] = None
        self.return_data: return_dict_type = {'title': 'Věk obyvatelstva v okrsku', 'data': []}
        self._get_db_data()
        self._format_data()

    def _get_db_data(self) -> None:
        if self._db_data:
            return
        with db(cursor=True) as cur:
            cur.execute('SELECT count, gender, age_start FROM age_groups WHERE district = ?', (self.district,))
            self._db_data = cur.fetchall()
        self._db_data = sorted([row for row in self._db_data if row['gender'] == self.gender],
                               key=lambda x: (x['age_start'] is None, x['age_start']))

    def _format_data(self) -> None:
        for row in self._db_data:
            if row['age_start'] is None:
                entry = {'label': 'Celkem', 'value': int(row['count'])}
            elif row['age_start'] == 95:
                entry = {'label': f"{int(row['age_start'])}+", 'value': int(row['count'])}
            else:
                entry = {'label': f"{int(row['age_start'])}-{int(row['age_start'])+5}", 'value': int(row['count'])}
            self.return_data['data'].append(entry)


@speaks_json
def age_groups_all() -> return_dict_type:
    """Vekove skupiny"""
    wanted_district = request.args.get('district_code')
    current_app.logger.debug('wanted district: %s', wanted_district)
    return AgeGroup(wanted_district).return_data
