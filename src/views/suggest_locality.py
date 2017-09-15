# -*- encoding: utf-8 -*-
from views.decorators import speaks_json
from flask import request


@speaks_json
def suggest_locality():
    """
    Vyhleda lokalitu podle zadaneho retezce
    """
    query = request.args.get("query")

    return dict(result=True, data={'query': query})
