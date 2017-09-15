#!/usr/bin/env python
# coding=utf-8
from flask import Blueprint
from .suggest_locality import suggest_locality
from views.age_groups import age_groups_all

bp_api = Blueprint('api', __name__, url_prefix='/api/')


# Naseptavac lokalit
bp_api.add_url_rule('suggest-locality', 'suggest_locality', view_func=suggest_locality)
bp_api.add_url_rule('age-groups', 'age_groups', view_func=age_groups_all)
