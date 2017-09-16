#!/usr/bin/env python
# coding=utf-8
import json

from flask import request
from util import db
from views.decorators import speaks_json, allowed_post_only

__all__ = ('unemployed',)

TYPE_ALL = "NEZ0004"

COLOR_ALL = "#0F0"

LIMIT = 10


@speaks_json
@allowed_post_only
def unemployed():
    """
    Vraci nezamestnanost pro obec
    """
    municipality_code = json.loads(request.data).get("municipality_code")

    response = {
        "result": False,
        "data": {
            "title": "Nezaměstnanost",
            "data": None
        }
    }

    # chybi nam id okresku
    if not municipality_code:
        response['error'] = "'municipality_code' is missing"
        return response

    all = get_data_from_query(municipality_code, TYPE_ALL, COLOR_ALL)

    combined = []
    for i in reversed(range(LIMIT)):
        combined.append(all[i])

    response['data']['data'] = combined
    response['result'] = True
    return response


def get_data_from_query(municipality_code, type_, color):
    # type: (str, str) -> list(dict)
    """
    Vytazeni poslednich 10ti zaznamu z tabulky nezamestnanosti

    :param municipality_code: ...
    :param type_: ...
    :return: ...
    """
    with db.common_db(cursor=True) as cur:
        query = """
            SELECT
                value_ AS y,
                year_ || "-" || month_ AS x,
                ? AS color
            FROM unemployed
            WHERE
                municipality_id = ? AND
                type_ = ?
            ORDER BY year_ DESC, month_ DESC
            LIMIT ?
        """
        cur.execute(query, (color, municipality_code, type_, LIMIT))
        return [dict(x) for x in cur.fetchall()]
