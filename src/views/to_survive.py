#!/usr/bin/env python
# coding=utf-8

import json

from flask import request
from util import db
from views.decorators import speaks_json, allowed_post_only

__all__ = ('to_survive',)


@speaks_json
@allowed_post_only
def to_survive():
    """
    Vrati nadeji na doziti pro okres
    """
    request_data = json.loads(request.data)
    region_id = request_data.get("region_id")
    district_code = request_data.get("district_code")

    response = {
        "result": False,
        "data": {
            "title": "Naděje na dožiti",
            "data": None
        }
    }

    # chybi nam id okresku
    if not region_id or not district_code:
        response['error'] = "'region_id' or 'district_code' are missing"
        return response

    # all = get_data_from_query(municipality_code, TYPE_ALL)
    #
    # combined = []
    # for i in reversed(range(LIMIT)):
    #     combined.append(all[i])
    #
    # response['data']['data'] = combined
    # response['result'] = True

    return response


def get_data_from_query(municipality_code, type_):
    # type: (str, str) -> list(dict)
    """
    TODO

    :param municipality_code: ...
    :param type_: ...
    :return: ...
    """
    with db.common_db(cursor=True) as cur:
        query = """
            SELECT
                value_ AS y,
                year_ || "-" || month_ AS x
            FROM unemployed
            WHERE
                municipality_id = ? AND
                type_ = ?
            ORDER BY year_ DESC, month_ DESC
            LIMIT ?
        """
        cur.execute(query, (municipality_code, type_, LIMIT))
        return [dict(x) for x in cur.fetchall()]
