# -*- encoding: UTF-8 -*-
from functools import wraps
from flask import jsonify


def speaks_json(f):
    """
    Dekorator ktery z dict vystupu fce delat normalizovanou json odpoved
    Ocekava klice result:bool, data: cokoliv, message: str - chyba nebo nic.
    :param f: dekorovana fce
    :return: fci ktera vraci json.
    """

    @wraps(f)
    def inner(*args, **kwargs):

        result_dict = {}
        res = f(*args, **kwargs)
        result_dict['result'] = res['result'] if 'result' in res else True
        result_dict['data'] = res.get('data')
        result_dict['title'] = res.get('title')
        result_dict['message'] = res.get('error', 'OK' if result_dict['result'] else 'UNKNOWN ERROR')
        return jsonify(result_dict)

    return inner


def allowed_methods(*methods):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwds):
            return func(*args, **kwds)
        wrapper.methods = methods
        return wrapper
    return decorator


allowed_post_only = allowed_methods('POST')
allowed_get_and_post = allowed_methods('GET', 'POST')
