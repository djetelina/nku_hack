# -*- encoding: utf-8 -*-
from views.decorators import speaks_json, allowed_post_only
from flask import request
from util import db
import json


def prepare_data(request_args, data_type):
    """
    Jelikoz vsechny 3 datove sady maji stejny format, lze se na ne dotazovat stejnou funkci a
    staci jen menit nazvy tabulek.
    """
    municipality_code = request_args.get('municipality_code')
    district_code = request_args.get('district_code')
    region_code = request_args.get('region_id')

    response_data = []
    with db.common_db() as connection:
        cursor = connection.cursor()

        # Obec
        if municipality_code:
            data = cursor.execute('''SELECT metric, value FROM {}_obec WHERE city_id=?'''.format(
                data_type
            ), (municipality_code,))

        # Okres
        elif district_code:
            data = cursor.execute('''SELECT metric, value FROM {}_okres WHERE district_id=?'''.format(
                data_type
            ), (district_code,))

        # Kraj
        elif region_code:
            data = cursor.execute('''SELECT metric, value FROM {}_kraj WHERE region_id=?'''.format(
                data_type
            ), (region_code,))
        else:
            data = []

        # Pripravim data pro view
        data = list(data)
        data_sum = sum([x[1] for x in data])
        for item in data:
            percent = (item[1] / data_sum) * 100
            response_data.append({
                'key': '{} {:.2f} %'.format(item[0], percent),
                'value': item[1],
            })

    return sorted(response_data, key=lambda x: x['value'], reverse=True)


@speaks_json
@allowed_post_only
def education():
    # type: () -> Dict[str, Any]
    """
    Vrati data pro vzdelani.
    """
    response_data = prepare_data(json.loads(request.data), 'education')
    pack = {'data': response_data, 'title': 'Vzdělání'}

    return dict(result=True if response_data else False, data=pack)


@speaks_json
@allowed_post_only
def marital_status():
    # type: () -> Dict[str, Any]
    """
    Vrati data pro rodinny stav.
    """
    response_data = prepare_data(json.loads(request.data), 'marital_status')
    pack = {'data': response_data, 'title': 'Rodinný stav'}

    return dict(result=True if response_data else False, data=pack)


@speaks_json
@allowed_post_only
def nationality():
    # type: () -> Dict[str, Any]
    """
    Vrati data pro narodnost.
    """
    response_data = prepare_data(json.loads(request.data), 'nationality')
    pack = {'data': response_data, 'title': 'Národnost'}

    return dict(result=True if response_data else False, data=pack)
