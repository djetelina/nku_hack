#!/usr/bin/env python
# coding=utf-8
from views.decorators import speaks_json, allowed_post_only
from flask import request, current_app
from util.db import common_db as db
from typing import Dict, Union, List
import sqlite3
import json


return_dict_type = Dict[str, Union[str, List[Dict[str, Union[str, int]]]]]


class AgeGroup:
    def __init__(self, district, gender='a'):
        self.district = str(district)
        self.gender: str = gender
        self._db_data: List[sqlite3.Row] = None
        self.return_data: return_dict_type = {
            'title': 'Věk obyvatelstva v okrsku', 'data': [], 'axisLabels': {'x': 'Věk', 'y': 'Počet'}
        }
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
                continue
            #    entry = {'x': 'Celkem', 'y': int(row['count'])}
            elif row['age_start'] == 95:
                entry = {'x': f"{int(row['age_start'])}+", 'y': int(row['count'])}
            else:
                entry = {'x': f"{int(row['age_start'])}-{int(row['age_start'])+4}", 'y': int(row['count'])}
            self.return_data['data'].append(entry)


@speaks_json
@allowed_post_only
def age_groups_all() -> Dict[str, return_dict_type]:
    """Vekove skupiny"""
    print(request.data)
    wanted_district = json.loads(request.data).get('district_code')
    current_app.logger.debug('wanted district: %s', wanted_district)
    return dict(data=AgeGroup(wanted_district).return_data)
