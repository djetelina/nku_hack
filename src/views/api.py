#!/usr/bin/env python
# coding=utf-8

from flask import Blueprint
from .suggest_locality import suggest_locality
from views.age_groups import age_groups_all
from .unemployed import unemployed
from .csu_population import education, marital_status, nationality

bp_api = Blueprint('api', __name__, url_prefix='/api/')


# Naseptavac lokalit
bp_api.add_url_rule('suggest-locality', 'suggest_locality', view_func=suggest_locality)

# Tahani nezamestnanosti
bp_api.add_url_rule('unemployed', 'unemployed', view_func=unemployed)

bp_api.add_url_rule('age-groups', 'age_groups', view_func=age_groups_all)

# Data z CSU - obyvatelstvo
bp_api.add_url_rule('education', 'education', view_func=education)
bp_api.add_url_rule('marital-status', 'marital_status', view_func=marital_status)
bp_api.add_url_rule('nationality', 'nationality', view_func=nationality)

