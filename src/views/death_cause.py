# -*- encoding: utf-8 -*-
from views.decorators import speaks_json, allowed_post_only
from flask import request
from util import db


@speaks_json
@allowed_post_only
def get_death_causes():
    """
    """

    municipality_code = request.form.get('municipality_code')
    district_code = request.form.get('district_code')
    region_code = request.form.get('region_id')

    response_data = []
    with db.common_db() as connection:
        cursor = connection.cursor()

    return response_data
