#!/usr/bin/env python
# coding=utf-8
"""View k hlavnimu behu."""
from flask import current_app, Blueprint, render_template

from views.decorators import speaks_json

bp_common = Blueprint('common', __name__)


@bp_common.route('/trest')
@speaks_json
def hello_json():
    return dict(ressult=True, data=["Dlata"], message="kuk")


@bp_common.before_app_request
def before_request():
    pass


@bp_common.after_app_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    current_app.logger.debug('Response: %s', response)
    return response
