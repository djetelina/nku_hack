#!/usr/bin/env python
# coding=utf-8
"""View k hlavnimu behu."""
from flask import current_app, Blueprint, render_template

bp_common = Blueprint('common', __name__)


@bp_common.route('/')
def hello_world():
    return render_template('home.html')


@bp_common.before_app_request
def before_request():
    pass


@bp_common.after_app_request
def after_request(response):
    current_app.logger.debug('Response: %s', response)
    return response
