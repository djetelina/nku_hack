# -*- encoding: utf-8 -*-
from views.decorators import speaks_json
from flask import request
from util import db


@speaks_json
def suggest_locality():
    """
    Vyhleda lokalitu podle zadaneho retezce
    """
    query = request.args.get("query")

    with db.ruian_db() as ruian:
        c = ruian.cursor()
        c.execute("""
          SELECT u.nazev, u.kod as ulice_kod  
          FROM ulice u 
          WHERE u.nazev LIKE ?
        """, (query, ))
        all_ = c.fetchall()
        print(all_)

    return dict(result=True, data={'query': query})
