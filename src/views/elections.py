# -*- encoding: utf-8 -*-
from views.decorators import speaks_json, allowed_post_only
from flask import request
from util import db
import json
from typing import Dict, Tuple, List, Any


def prepare_data(request_args: Dict[str, str], data_type: str) -> Tuple[List[Dict[str, Any]], str]:
    """
    Jelikoz vsechny 3 datove sady maji stejny format, lze se na ne dotazovat stejnou funkci a
    staci jen menit nazvy tabulek.
    """
    municipality_code = request_args.get('municipality_code')

    response_data = []
    with db.common_db() as connection:
        cursor = connection.cursor()

        # Obec
        if municipality_code:
            data = cursor.execute('''SELECT metric_id, metric, value FROM {}_obec WHERE municipality_id=?'''.format(
                data_type
            ), (municipality_code,))
        else:
            data = []

        # Pripravim data pro view
        data = list(data)
        data_sum = sum([x[2] for x in data if x[0] != 'voters'])  # Pocet volicu celkem
        data_voters = sum([x[2] for x in data if x[0] == 'voters'])  # Pocet potencialnich volicu
        label = 'Volby do Poslanecké sněmovny 2013 (Účast {:.2f} % ({}/{}))'.format(
            (data_sum / data_voters) * 100,
            '{:,}'.format(int(data_sum)).replace(',', ' '),
            '{:,}'.format(int(data_voters)).replace(',', ' ')
        )
        for item in data:
            percent = (item[2] / data_sum) * 100
            response_data.append({
                'key': '{} {:.2f} %'.format(item[1], percent),
                'value': item[2],
            })

    return response_data, label


@speaks_json
@allowed_post_only
def elections() -> Dict[str, Any]:
    """
    Vrati data pro volby do Poslanecke snemovny 2013 za obce.
    """
    response_data, label = prepare_data(json.loads(request.data), 'elections')
    pack = {'data': response_data, 'title': label}

    return dict(result=True if response_data else False, data=pack)
