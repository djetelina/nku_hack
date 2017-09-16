#!/usr/bin/env python
# coding=utf-8

import json

from flask import request
from util import db
from views.decorators import speaks_json, allowed_post_only

__all__ = ('to_survive',)


CHILD_YEAR_CODE = '400000600001000'


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
            "title": "Střední délka života",
            "data": None
        }
    }

    # chybi nam id okresku
    if not region_id or not district_code:
        response['error'] = "'region_id' or 'district_code' are missing"
        return response

    result = get_data_from_query(region_id, district_code)
    for row in result:
        row['key'] = "{} ({} let)".format(
            "Muži" if int(row['sex']) == 1 else "Ženy",
            round(row['value'], 2)
        )

    response['data']['data'] = result

    return response


def get_data_from_query(region_id, district_code):
    # type: (str, str) -> list(dict)
    """
    Vraci stredni delka zivota a prumer nad celym statem.
    Metoda radi dle pohlavi (muzi/zeny)
    """
    with db.common_db(cursor=True) as cur:
        query = """
            SELECT
                value_ AS value,
                sex
            FROM to_survive
            WHERE
                region_id = ? AND
                district_id = ? AND
                year_code = ?
            GROUP BY sex
            ORDER BY sex ASC
        """
        cur.execute(query, (region_id, district_code, CHILD_YEAR_CODE))
        return [dict(x) for x in cur.fetchall()]
