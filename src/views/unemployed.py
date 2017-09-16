#!/usr/bin/env python
# coding=utf-8


from views.decorators import speaks_json
from flask import request
from util import db


__all__ = ('unemployed',)

TYPE_ALL = "NEZ0001"
TYPE_WOMEN = "NEZ0003"

COLOR_WOMEN = "#F00"
COLOR_MEN = "#FFF"
COLOR_ALL = "#00F"

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
        "data": None
    }

    # chybi nam id okresku
    if not municipality_code:
        response['error'] = "'municipality_code' is missing"
        return response

    all = get_q(municipality_code, TYPE_ALL, COLOR_ALL)
    women = get_q(municipality_code, TYPE_WOMEN, COLOR_WOMEN)

    # muzi jsou rozdil mezi vsichni a zeny
    men = [{
        "y": all[i].get("y") - women[i].get("y"),
        "x": all[i].get("x"),
        "color": all[i].get("color")
    } for i in range(LIMIT)]

    all.extend(women)
    all.extend(men)
    response['data'] = all
    return response


def get_q(municipality_code, type_, color):
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
            ORDER BY x DESC
            LIMIT ?
        """
        cur.execute(query, (color, municipality_code, type_, LIMIT))
        return [dict(x) for x in cur.fetchall()]
