# -*- encoding: utf-8 -*-
from views.decorators import speaks_json, allowed_post_only
from flask import request
from util import db
import json
import sqlite3
from typing import List, Dict, Any


@speaks_json
@allowed_post_only
def suggest_locality() -> Dict[str, Any]:
    """s
    Vyhleda lokalitu podle zadaneho retezce
    """
    query = json.loads(request.data).get("query")
    if len(query) < 3:
        return dict(result=False, message=u"Příliš krátké zadání")

    with db.ruian_db(cursor=True) as ruian_cursor:

        # Vezmeme si jich 11 a pouzijeme 10. Pak vime, jestli mame i vic :-)

        # napred ulice
        results = get_by_street(ruian_cursor, query)

        if not results:
            results = get_by_municipality_part(ruian_cursor, query)

        data = {
            'we_have_more': len(results) == 11,  # Mame jich vice
            'results': results[:10]  # Prvnich 10
        }

    return dict(result=True, data=data)


def get_by_street(c: sqlite3.Cursor, query: str) -> List[Dict[str, Any]]:
    """
    Najde lokality podle nazvu ulice.
    :param c:
    :param query:
    :return: vyslledky :-)
    """
    c.execute("""
          SELECT 
            u.nazev as street_name, 
            u.kod as street_id,
            ob.nazev as municipality_name,
            ob.kod as municipality_code,
            ok.nazev as district_name,
            ok.kod as district_code,
            k.nazev as region_name,
            k.kod as region_id  
          FROM ulice u
          JOIN obce ob ON (UPPER(SUBSTR(u.nazev, 1, 1)) || LOWER(SUBSTR(u.nazev, 2)) LIKE ? AND ob.kod = u.obec_kod)
          JOIN okresy ok ON ok.kod = ob.okres_kod 
          JOIN vusc k ON k.kod = ok.vusc_kod
          ORDER BY k.nazev, ok.nazev, ob.nazev, u.nazev
          LIMIT 11
        """, ("{}%".format(query.capitalize()), ))

    return [dict(x) for x in c.fetchall()]


def get_by_municipality_part(c: sqlite3.Cursor, query: str) -> List[Dict[str, Any]]:
    """
    Najde lokality podle nazvu casti obce.
    :param c:
    :param query:
    :return: vyslledky :-)
    """
    c.execute("""
          SELECT 
            co.nazev as municipality_part_name, 
            co.kod as municipality_part_id,
            ob.nazev as municipality_name,
            ob.kod as municipality_code,
            ok.nazev as district_name,
            ok.kod as district_code,
            k.nazev as region_name,
            k.kod as region_id  
          FROM casti_obci co
          JOIN obce ob ON (UPPER(SUBSTR(co.nazev, 1, 1)) || LOWER(SUBSTR(co.nazev, 2)) LIKE ? AND ob.kod = co.obec_kod)
          JOIN okresy ok ON ok.kod = ob.okres_kod 
          JOIN vusc k ON k.kod = ok.vusc_kod
          ORDER BY k.nazev, ok.nazev, ob.nazev, co.nazev
          LIMIT 11
        """, ("{}%".format(query.capitalize()), ))

    return [dict(x) for x in c.fetchall()]
