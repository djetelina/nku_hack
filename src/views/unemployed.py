#!/usr/bin/env python
# coding=utf-8


from views.decorators import speaks_json
from flask import request
from util import db


__all__ = ('unemployed',)

TYPE_ALL = "NEZ0004"
TYPE_WOMEN = "NEZ0006"

COLOR_WOMEN = "#F00"
COLOR_MEN = "#F0F"
COLOR_ALL = "#0FF"

LIMIT = 10


@speaks_json
def unemployed():
    """
    Vraci nezamestnanost pro obec

    :return:
    """
    municipality_code = request.args.get("municipality_code")
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

    all = get_q(municipality_code, TYPE_ALL, COLOR_ALL, "v")
    women = get_q(municipality_code, TYPE_WOMEN, COLOR_WOMEN, "z")

    # muzi jsou rozdil mezi vsichni a zeny
    men = [{
        "y": all[i].get("y") - women[i].get("y"),
        "x": all[i].get("x")[:-1] + "m",
        "color": COLOR_MEN
    } for i in range(LIMIT)]

    combined = []
    for i in range(LIMIT):
        combined.append(women[i])
        combined.append(men[i])
        combined.append(all[i])

    response['data']['data'] = combined
    response['result'] = True
    return response


def get_q(municipality_code, type_, color, key):
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
                year_ || "-" || month_ || ? AS x,
                ? AS color
            FROM unemployed
            WHERE
                municipality_id = ? AND
                type_ = ?
            ORDER BY x ASC
            LIMIT ?
        """
        cur.execute(query, (key, color, municipality_code, type_, LIMIT))
        return [dict(x) for x in cur.fetchall()]
