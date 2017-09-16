# -*- encoding: utf-8 -*-
from views.decorators import speaks_json, allowed_post_only
from flask import request, json
from util import db


#COLORS = ["#AD343E", "#474747", "#F2AF29", "#000000", "#E0E0CE"]
COLORS = ["#1F77B4", "#AEC7E8", "#FF7F0E", "#FFBB78", "#2CA02C", "#98DF8A", "#D62728", "#FF9896", "#9467BD", "#C5B0D5"]


@speaks_json
@allowed_post_only
def get_death_causes():
    """
    Vrati nejcastejsi umrti.
    """
    args = json.loads(request.data)
    district_code = int(args['district_code'])

    with db.common_db(cursor=True) as cursor:
        query = """
            select 
              dc.year as year, 
              dc.cause_id as cause_id,
              sum(dc.value) as val,
              d.name as disease_name
            FROM death_cause dc, disease d
            where district_id=? and dc.value > 0 and d.code=dc.cause_id 
            GROUP BY dc.year, dc.cause_id, d.name 
            ORDER BY val DESC 
            LIMIT 8
        """
        cursor.execute(query, (district_code,))
        data = [{'x': item['disease_name'],
                'y': item['val'], 'color': color} for item, color in zip(cursor.fetchall(), COLORS) if item]

        return dict(result=True, data={'data': data, 'title': "Nejčastější úmrtí v okrese jsou na..."})

